# -*- coding: utf-8 -*-
"""豆包高清放大 —— 与 _doubao_v2.py 同流程，prompt 改成高清放大/去logo。
用法: python _doubao_hd.py <图片路径> [更多...]
"""
import os, sys, time, glob, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _doubao_v2 as D   # 复用 activate/keys/click/copy_image/copy_text/md5

D.PROMPT = ("请把这张图片做高清放大处理：保持设备的外观、颜色、结构和所有细节完全不变，"
            "不要增减任何部件、不要改变角度；把分辨率提升到 2000 像素以上，让边缘和表面更清晰。"
            "同时去掉设备表面和画面上的品牌 logo 与中文/英文字样，背景保持纯白。"
            "只要处理后的图片，不要任何解释文字。")

DL = D.DL
OUTDIR = r"C:\Users\Administrator\_hd_out"
os.makedirs(OUTDIR, exist_ok=True)

def run(src):
    name = os.path.splitext(os.path.basename(src))[0]
    print("\n▶ " + name, flush=True)
    D.activate(); time.sleep(0.6)
    D.keys("^+k"); time.sleep(3.0)
    D.click(D.INPUT_BOX); time.sleep(0.5)
    D.copy_image(src); time.sleep(0.9)
    D.activate(); D.keys("^v"); time.sleep(2.5)
    D.copy_text(D.PROMPT); time.sleep(0.4)
    D.activate(); D.keys("^v"); time.sleep(1.0)
    D.keys("{ENTER}")
    print("   已发送，等生成（高清较慢，等 90s）…", flush=True)
    time.sleep(90)
    seen = {D.md5(f) for f in glob.glob(os.path.join(OUTDIR, "*.png"))}
    for cx, cy in D.CAND:
        before = set(os.path.basename(x) for x in glob.glob(os.path.join(DL, "*.png")))
        D.click((cx, cy), right=True); time.sleep(1.0)
        D.click((cx + D.MENU_OFF[0], cy + D.MENU_OFF[1])); time.sleep(5.0)
        now = set(os.path.basename(x) for x in glob.glob(os.path.join(DL, "*.png")))
        new = now - before
        if not new: continue
        f = max([os.path.join(DL, n) for n in new], key=os.path.getmtime)
        h = D.md5(f)
        if h in seen:
            try: os.remove(f)
            except Exception: pass
            continue
        from PIL import Image
        im = Image.open(f).convert("RGB")
        out = os.path.join(OUTDIR, name + "_hd.png")
        im.save(out, optimize=True)
        print(f"   ✅ ({cx},{cy}) {im.size} {os.path.getsize(out)//1024}KB", flush=True)
        return out
    print("   ❌ 未拿到图（可能仍在生成，稍后重试或用 _doubao_max.py）", flush=True)
    return None

if __name__ == "__main__":
    for s in sys.argv[1:]:
        run(s)
