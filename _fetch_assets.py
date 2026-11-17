# -*- coding: utf-8 -*-
import re, subprocess, os, html

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
IMGIN = r"C:\Users\Administrator\kingdaotech_newsite\images\products"
os.makedirs(IMGIN, exist_ok=True)

def curl(url, out=None):
    cmd = ["curl", "-s", "-m", "40", "-4", "-A", UA]
    if out:
        cmd += ["-o", out]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True)
    return r.stdout.decode("utf-8", "ignore") if not out else r.returncode

# ---------- 1. 蓝深 刮泥机 ----------
for pid in ("15", "13"):
    u = f"http://www.lanshengroup.com.cn/Products_detail/{pid}.html"
    h = curl(u)
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", "\n", t)
    lines = [html.unescape(x).strip() for x in t.split("\n") if x.strip()]
    print("=" * 70)
    print(f"Lanshen {pid}: len={len(h)}")
    KEY = re.compile(r"型号|规格|功率|池径|直径|深度|处理量|m3|m³|kW|kw|转速|材质|参数|选型")
    for x in lines:
        if KEY.search(x) and len(x) < 130:
            print("  ", x)
    # 表格
    for tb in re.findall(r"<table.*?</table>", h, re.S | re.I):
        print("  --TABLE--")
        for tr in re.findall(r"<tr.*?</tr>", tb, re.S | re.I)[:14]:
            cells = [html.unescape(re.sub(r"<[^>]+>", " ", c)).strip()
                     for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S | re.I)]
            cells = [re.sub(r"\s+", " ", c) for c in cells if c.strip()]
            if cells:
                print("    ", " | ".join(cells)[:150])

# ---------- 2. 下载蓝赛主图 ----------
LANS = {
    "grille-mech-rotary-rake.jpg": "/uFile/102435/product/2026529125556133.jpg",
    "grille-mech-coarse.jpg":      "/uFile/102435/product/2026529125535245.jpg",
    "grille-mech-grab.jpg":        "/uFile/102435/product/2026529125515345.jpg",
    "grille-mech-rotary-cleaner.jpg": "/uFile/102435/product/202022594241356.jpg",
    "grille-fine-step.jpg":        "/uFile/102435/product/2026529122947764.jpg",
    "grille-fine-drum.jpg":        "/uFile/102435/product/202022594113397.jpg",
    "grille-fine-plate-step.jpg":  "/uFile/102435/product/2026529125645914.jpg",
    "grille-fine-plate-step2.jpg": "/uFile/102435/product/20265291303472.jpg",
    "grille-fine-inflow.jpg":      "/uFile/102435/product/202652912274895.jpg",
    "screw-screen-wshaft.jpg":     "/uFile/102435/product/20202259266950.jpg",
    "screw-screen-press.jpg":      "/uFile/102435/product/202022592625455.jpg",
    "screw-screen-gp.jpg":         "/uFile/102435/product/2020228113242114.jpg",
    "screw-screen-grit.jpg":       "/uFile/102435/product/202022592527909.jpg",
}
print("=" * 70)
for fn, path in LANS.items():
    out = os.path.join(IMGIN, fn)
    rc = curl("http://www.njlshb.cn" + path, out=out)
    sz = os.path.getsize(out) if os.path.exists(out) else 0
    print(f"{fn:32} rc={rc} {sz//1024} KB")
