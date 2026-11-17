# -*- coding: utf-8 -*-
import re, os, glob, html

OUT = r"C:\Users\Administrator\kingdaotech_newsite\_src_njlshb"

def tables(h):
    out = []
    for tb in re.findall(r"<table.*?</table>", h, re.S | re.I):
        rows = []
        for tr in re.findall(r"<tr.*?</tr>", tb, re.S | re.I):
            cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S | re.I)
            cells = [html.unescape(re.sub(r"<[^>]+>", " ", c)).strip() for c in cells]
            cells = [re.sub(r"\s+", " ", c) for c in cells if c]
            if cells:
                rows.append(" | ".join(cells))
        if rows:
            out.append(rows)
    return out

def main_img(h):
    m = re.search(r'class="[^"]*pro_main[^"]*"(.*?)</div>', h, re.S | re.I)
    block = m.group(1) if m else h
    imgs = re.findall(r'<img[^>]+src="([^"]+\.(?:jpg|jpeg|png))"', block, re.I)
    imgs = [i for i in imgs if "/uFile/" in i]
    return imgs[0] if imgs else (imgs)

for f in sorted(glob.glob(os.path.join(OUT, "raw_*.html"))):
    h = open(f, encoding="utf-8", errors="ignore").read()
    name = os.path.basename(f).replace("raw_", "").replace(".html", "")
    print("=" * 70)
    print(name, "| main_img:", main_img(h))
    tbs = tables(h)
    for i, rows in enumerate(tbs):
        print(f"  -- table {i} ({len(rows)} rows)")
        for r in rows[:16]:
            print("     ", r[:150])
