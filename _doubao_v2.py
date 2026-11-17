# -*- coding: utf-8 -*-
"""豆包去水印 —— 稳健版：每张图开新对话 + 下载用文件名集合 diff + md5 去重校验。
坐标候选覆盖「宽对话」和「右侧编辑面板压窄」两种布局，命中即停。
用法: python _doubao_v2.py file1.jpg file2.jpg ...
"""
import os, sys, time, glob, ctypes, subprocess, hashlib
from PIL import Image, ImageDraw

DL = os.path.expanduser(r"~\Downloads")
OUT = r"C:\Users\Administrator\nj_imgs_clean"
os.makedirs(OUT, exist_ok=True)

WIN_X, WIN_Y = 0, 0
INPUT_BOX = (1087, 928)          # 最大化布局输入框中心
MENU_OFF = (67, 95)
CAND = [(739, 640), (399, 742), (739, 742), (399, 692), (739, 692),
        (560, 720), (620, 700), (399, 640), (900, 700), (399, 800)]
PROMPT = ("请帮我把这张图片上的水印文字和logo去掉，恢复被遮挡的设备表面和白色背景，"
          "其他部分保持不变。只要处理后的图片，不要其他文字。")

def sc(pt): return (WIN_X + pt[0], WIN_Y + pt[1])

def click(pt, right=False):
    x, y = sc(pt)
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.15)
    d, u = (8, 16) if right else (2, 4)
    ctypes.windll.user32.mouse_event(d, 0, 0, 0, 0); time.sleep(0.06)
    ctypes.windll.user32.mouse_event(u, 0, 0, 0, 0); time.sleep(0.4)

def wheel(n=22):
    x, y = sc((1087, 520))
    ctypes.windll.user32.SetCursorPos(x, y); time.sleep(0.2)
    for _ in range(n):
        ctypes.windll.user32.mouse_event(0x0800, 0, 0, -120, 0); time.sleep(0.10)
    time.sleep(0.8)

def ps(cmd, timeout=120):
    subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, timeout=timeout)

def activate():
    ps("Add-Type -AssemblyName System.Windows.Forms; $ws=New-Object -ComObject wscript.shell; $ws.AppActivate('豆包') | Out-Null")

def keys(k):
    ps("Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('" + k + "')")

def copy_image(path):
    ps("Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; "
       "$img=[System.Drawing.Image]::FromFile('" + path + "'); "
       "[System.Windows.Forms.Clipboard]::SetImage($img); $img.Dispose()")

def copy_text(t):
    ps("Set-Clipboard -Value '" + t.replace("'", "''") + "'")

def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()

def strip_mark(path, name):
    im = Image.open(path).convert("RGB"); w, h = im.size
    d = ImageDraw.Draw(im)
    d.rectangle((int(w * 0.80), int(h * 0.945), w, h), fill=(255, 255, 255))
    out = os.path.join(OUT, name + "_clean.png")
    im.save(out, optimize=True)
    return out

SEEN = set()
for f in glob.glob(os.path.join(OUT, "*.png")):
    try: SEEN.add(md5(f))
    except Exception: pass
print("已有 clean 图哈希:", len(SEEN))

def process(src):
    name = os.path.splitext(os.path.basename(src))[0]
    t0 = time.time()
    print("\n▶ " + name, flush=True)
    activate(); time.sleep(0.6)
    keys("^+k"); time.sleep(3.0)          # 新对话（铁律：可靠性优先）
    click(INPUT_BOX); time.sleep(0.5)
    copy_image(src); time.sleep(0.8)
    activate(); keys("^v"); time.sleep(2.5)
    copy_text(PROMPT); time.sleep(0.4)
    activate(); keys("^v"); time.sleep(1.0)
    keys("{ENTER}")
    print("   已发送，等生成…", flush=True)
    time.sleep(54)
    for cx, cy in CAND:
        before = set(os.path.basename(x) for x in glob.glob(os.path.join(DL, "*.png")))
        click((cx, cy), right=True); time.sleep(1.0)
        click((cx + MENU_OFF[0], cy + MENU_OFF[1])); time.sleep(4.5)
        now = set(os.path.basename(x) for x in glob.glob(os.path.join(DL, "*.png")))
        new = now - before
        if not new:
            print(f"   · ({cx},{cy}) 无新文件", flush=True); continue
        f = max([os.path.join(DL, n) for n in new], key=os.path.getmtime)
        h = md5(f)
        if h in SEEN:
            print(f"   · ({cx},{cy}) 下载到重复图，跳过", flush=True)
            try: os.remove(f)
            except Exception: pass
            continue
        SEEN.add(h)
        out = strip_mark(f, name)
        print(f"   ✅ ({cx},{cy}) {os.path.basename(out)} {os.path.getsize(out)//1024}KB "
              f"md5={h[:8]} {time.time()-t0:.0f}s", flush=True)
        return out
    print("   ❌ 全坐标未命中", flush=True)
    return None

if __name__ == "__main__":
    ok = 0
    for s in sys.argv[1:]:
        n = os.path.splitext(os.path.basename(s))[0]
        if os.path.exists(os.path.join(OUT, n + "_clean.png")):
            hh = md5(os.path.join(OUT, n + "_clean.png"))
            dup = list(SEEN).count(hh)
            print(f"\n⏭ 已存在 {n}（md5 {hh[:8]}）", flush=True)
        try:
            if process(s): ok += 1
        except Exception as e:
            print("   ❌", str(e)[:150], flush=True)
        time.sleep(2)
    print(f"\n完成 {ok}/{len(sys.argv)-1}", flush=True)
