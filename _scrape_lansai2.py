# -*- coding: utf-8 -*-
import re, subprocess, os, json

BASE = "http://www.njlshb.cn/"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
OUT = r"C:\Users\Administrator\kingdaotech_newsite\_src_njlshb"
os.makedirs(OUT, exist_ok=True)

TARGETS = [
    (135, 158, "mech-coarse"),   # 机械粗格栅
    (136, 158, "grab"),          # 抓斗式机械格栅
    (134, 158, "rotary-rake"),   # 回转式不锈钢齿耙格栅
    (26, 158, "rotary-cleaner"),  # 回转式格栅除污机
    (25, 158, "step-fine"),      # 阶梯式细格栅
    (28, 158, "drum-fine"),      # 卧式滚筒细格栅
    (138, 158, "plate-step"),    # 孔板阶梯回转式格栅
    (139, 158, "plate-step2"),   # 回转阶梯式孔板格栅清污机
    (10, 153, "inflow-fine"),    # 转鼓式孔板膜精细格栅
    (63, 159, "screw1"), (64, 159, "screw2"), (65, 159, "screw3"),
    (66, 159, "screw4"), (122, 159, "screw5"), (123, 159, "screw6"),
]

def get(url):
    r = subprocess.run(["curl", "-s", "-m", "40", "-4", "-A", UA, url], capture_output=True)
    return r.stdout.decode("utf-8", "ignore")

KEY = re.compile(r"材质|栅隙|栅距|渠宽|渠深|角度|功率|电压|处理量|m3|m³|型号|规格|速度|孔径|网孔|厚度|长度|直径|kw|KW|安装|流量|重量|电机")

for pid, cid, tag in TARGETS:
    url = f"{BASE}product_view_{pid}_{cid}.html"
    h = get(url)
    open(os.path.join(OUT, f"raw_{pid}_{cid}.html"), "w", encoding="utf-8").write(h)
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    title = m.group(1).strip() if m else "?"
    # 主图：pro_main 内第一张非 s 前缀图
    imgs = re.findall(r'<img[^>]+src="([^"]+\.(?:jpg|jpeg|png))"', h, re.I)
    imgs = [i for i in imgs if "/s2" not in i and not os.path.basename(i).startswith("s")]
    img = imgs[0] if imgs else ""
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = t.replace("&nbsp;", " ").replace("&amp;", "&").replace("&deg;", "°").replace("&ndash;", "-").replace("&le;", "<=").replace("&ge;", ">=")
    lines = [x.strip() for x in t.split("\n") if x.strip()]
    keep = [x for x in lines if KEY.search(x) and len(x) < 120]
    seen, ded = set(), []
    for x in keep:
        if x not in seen:
            seen.add(x); ded.append(x)
    print("=" * 70)
    print(f"[{tag}] {pid}_{cid} | {title}")
    print("IMG:", img)
    for x in ded[:26]:
        print("  ", x)
