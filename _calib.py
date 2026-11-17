# -*- coding: utf-8 -*-
"""标定豆包对话里\"结果图中心\"的 y 坐标：对已生成的多张结果图逐个 y 试右键下载。"""
import importlib.util, os, glob, time, sys

SK = r"E:\hermes\profiles\grace\skills\sales\website-maintenance\scripts\doubao_watermark_batch.py"
spec = importlib.util.spec_from_file_location("db", SK)
db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db)

DL = db.DL
before = set(glob.glob(os.path.join(DL, "*.png")))
print("Downloads 现有 png:", len(before))

db.activate(); time.sleep(0.6)
for y in (300, 350, 400, 450, 500, 550, 600, 250):
    db.wheel(8)
    db.click((420, y), right=True)
    time.sleep(1.4)
    # 先判断菜单是否出现：截图不做，直接点菜单项位置，再看有没有新文件
    db.click((420 + db.MENU_DOWNLOAD_OFFSET[0], y + db.MENU_DOWNLOAD_OFFSET[1]))
    time.sleep(5)
    now = set(glob.glob(os.path.join(DL, "*.png")))
    new = now - before
    print(f"y={y:>4}  新文件 {len(new)}")
    if new:
        f = max(new, key=os.path.getmtime)
        print("   ✅ 命中:", os.path.basename(f), os.path.getsize(f) // 1024, "KB")
        before = now
        open(os.path.join(os.path.dirname(__file__), "_calib_y.txt"), "w").write(str(y))
        break
else:
    print("❌ 全部 y 都未命中")
