# -*- coding: utf-8 -*-
"""豆包桌面客户端批量去水印 —— 工业产品图（2026-11-13 验证可用，70-75 秒/张）

适用场景：官网/画册需要产品图，但供应商给的图中央压着「XX公司」水印，cv2 inpaint 会毁细节、
FAL 等 AI 修图 API 无余额时的兜底方案。

═══ 三条铁律（都是踩出来的）═══
1. ⛔ 不要每张图新开对话 —— 主人明确要求「可以在同一个任务里面去文字logo，不用一直新开任务」。
   同一对话连续处理省掉新开+加载，且图片位置更稳定。
2. ⛔ 右下角「豆包AI生成」水印的处理方式**取决于图片背景**：
   · 纯白背景产品图（抠图稿）→ 涂白 `(255,255,255)` 无痕
   · **实景照片（水泥地/厂房）→ 必须裁掉底部 6~7%**，涂白会留一块刺眼白方块（本次把一体化泵站图修坏过）
3. ⛔ Electron/Chromium 客户端（豆包、微信、Notion…）**不吃 PostMessage 键盘事件**。
   cua-driver 的 `hotkey` 即使传 delivery_mode="foreground" 也回落到 PostMessage → Ctrl+V 变成输入一个 "v"。
   必须走 PowerShell `[System.Windows.Forms.SendKeys]::SendWait()`（系统级输入队列）。

═══ 前置条件 ═══
- 豆包 PC 客户端已启动并**已登录**（未登录时左下角是黑色登录条；登录后左侧能看到历史对话）
- 客户端窗口位置固定，记下窗口左上角屏幕坐标 → WIN_X / WIN_Y
- 窗口内关键坐标用 cua-driver `get_window_state` 截图 + vision 读出来，一次性标定好

用法:
  python doubao_watermark_batch.py y=500 img1.png img2.jpg ...
  （y=500 是滚动到底后"最新图片中心"的窗口内 y 坐标，首次需 vision 标定）
"""
import os, sys, time, glob, ctypes, subprocess
from PIL import Image, ImageDraw

# ── 按现场修改 ──────────────────────────────────────────
DL = os.path.expanduser(r"~\Downloads")          # 豆包"下载原图"落点
OUT = r"C:\Users\Administrator\nj_imgs_clean"     # 输出去水印后
WIN_X, WIN_Y = 0, 0                          # 豆包窗口左上角屏幕坐标
INPUT_BOX = (1087, 928)                           # 输入框（窗口内坐标）
MENU_DOWNLOAD_OFFSET = (67, 95)
IMG_X = 739                  # 相对右键点 → 菜单"下载原图"

PROMPT = ("请帮我把这张图片上的水印文字和logo去掉，恢复被遮挡的设备表面和白色背景，"
          "其他部分保持不变。只要处理后的图片，不要其他文字。")
# ────────────────────────────────────────────────────────

os.makedirs(OUT, exist_ok=True)


def sc(pt):
    return (WIN_X + pt[0], WIN_Y + pt[1])


def click(pt, right=False):
    x, y = sc(pt)
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.15)
    down, up = (8, 16) if right else (2, 4)
    ctypes.windll.user32.mouse_event(down, 0, 0, 0, 0)
    time.sleep(0.06)
    ctypes.windll.user32.mouse_event(up, 0, 0, 0, 0)
    time.sleep(0.4)


def wheel(times=8):
    """滚到底：对话累积后必须滚，否则右键到的是旧图"""
    x, y = sc((1087, 520))
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.2)
    for _ in range(times):
        ctypes.windll.user32.mouse_event(0x0800, 0, 0, -120, 0)
        time.sleep(0.12)
    time.sleep(0.8)


def ps(cmd, timeout=120):
    subprocess.run(["powershell", "-NoProfile", "-Command", cmd],
                   capture_output=True, timeout=timeout)


def activate():
    ps("Add-Type -AssemblyName System.Windows.Forms; "
       "$ws=New-Object -ComObject wscript.shell; $ws.AppActivate('豆包') | Out-Null")


def keys(k):
    """SendKeys 是唯一能穿透 Chromium 的路径"""
    ps(f"Add-Type -AssemblyName System.Windows.Forms; "
       f"[System.Windows.Forms.SendKeys]::SendWait('{k}')")


def copy_image(path):
    ps(f"""Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing;
    $img=[System.Drawing.Image]::FromFile('{path}');
    [System.Windows.Forms.Clipboard]::SetImage($img); $img.Dispose()""")


def copy_text(t):
    """中文提示词：SendKeys 不支持中文，必须走剪贴板 + Ctrl+V"""
    ps("Set-Clipboard -Value '" + t.replace("'", "''") + "'")


def strip_bean_mark(path, name, mode="auto"):
    """去掉右下角"豆包AI生成"。
    mode: auto=白底涂白 / crop=裁底部（实景照片必须用这个）/ paint=强制涂白
    """
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if mode == "crop":
        im = im.crop((0, 0, w, int(h * 0.935)))
    else:
        # auto: 采样四角判断是否纯白背景
        import numpy as np
        a = np.array(im)
        corners = [a[2:10, 2:10], a[2:10, -10:-2], a[-10:-2, 2:10]]
        bg = np.median(np.concatenate([c.reshape(-1, 3) for c in corners]), axis=0)
        is_white = bool((bg > 245).all())
        if mode == "paint" or is_white:
            d = ImageDraw.Draw(im)
            d.rectangle((int(w * 0.80), int(h * 0.945), w, h), fill=tuple(int(v) for v in bg))
        else:
            im = im.crop((0, 0, w, int(h * 0.935)))   # 实景 → 裁
    out = os.path.join(OUT, name + "_clean.png")
    im.save(out, optimize=True)
    return out


def newest_png(since):
    fs = [f for f in glob.glob(os.path.join(DL, "*.png")) if os.path.getmtime(f) > since]
    return max(fs, key=os.path.getmtime) if fs else None


def process(src, ypos, mode="auto"):
    name = os.path.splitext(os.path.basename(src))[0]
    t0 = time.time()
    print(f"\n▶ {name}")

    activate(); time.sleep(0.5)
    click(INPUT_BOX)                 # 同一对话：不按 Ctrl+Shift+K
    copy_image(src); time.sleep(0.7)
    activate(); keys("^v"); time.sleep(2.2)

    copy_text(PROMPT); time.sleep(0.4)
    activate(); keys("^v"); time.sleep(1.0)
    keys("{ENTER}")
    print("   已发送，等生成…")

    time.sleep(52)                   # 实测 40~50s 出图，留余量
    wheel(22)                        # 对话变长后必须多滚，否则没到底
    f = None
    CANDS = [(IMG_X, ypos), (399, 742), (399, 692), (560, 700), (IMG_X, 660),
             (399, 780), (IMG_X, 700), (620, 700), (399, 640)]
    for cx, yy in CANDS:
        click((cx, yy), right=True)
        time.sleep(1.0)
        click((cx + MENU_DOWNLOAD_OFFSET[0], yy + MENU_DOWNLOAD_OFFSET[1]))
        time.sleep(4.0)
        f = newest_png(t0)
        if f:
            print(f"   命中 ({cx},{yy})")
            break
        print(f"   · ({cx},{yy}) 未命中")

    if not f:
        print("   ❌ 未检测到下载（右键位置多半偏了，重标定 y）")
        return None
    out = strip_bean_mark(f, name, mode)
    print(f"   ✅ {os.path.basename(out)} ({time.time()-t0:.0f}s)")
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    ypos, mode = 500, "auto"
    if args and args[0].startswith("y="):
        ypos = int(args[0][2:]); args = args[1:]
    if args and args[0].startswith("mode="):
        mode = args[0][5:]; args = args[1:]
    done = []
    for s in args:
        _n = os.path.splitext(os.path.basename(s))[0]
        if os.path.exists(os.path.join(OUT, _n + "_clean.png")):
            print(f"\n⏭ 跳过（已存在）{_n}")
            done.append(os.path.join(OUT, _n + "_clean.png"))
            continue
        try:
            r = process(s, ypos, mode)
            if r:
                done.append(r)
        except Exception as e:
            print("   ❌", str(e)[:120])
        time.sleep(2)
    print(f"\n完成 {len(done)}/{len(args)}")
    for d in done:
        print("  ", d)
