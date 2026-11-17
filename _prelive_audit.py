# -*- coding: utf-8 -*-
"""KINGDAO 官网上线前全站内容终检：文案 / 表格 / 一致性 / 红线词"""
import os, re, glob, html, collections

ROOT = r"C:\Users\Administrator\kingdaotech_newsite"
os.chdir(ROOT)
PAGES = ["index.html"] + [os.path.basename(p) for p in
        ["products.html", "projects.html", "solutions.html", "oem.html", "about.html", "contact.html"]]
PAGES += sorted(glob.glob("products/*.html"))

def txt(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s))

RED = {  # 供应商 / 竞品 / 禁用表述
 "蓝赛": "供应商名", "蓝深": "供应商名", "凯美": "供应商名", "富丽斯": "供应商名",
 "南京": "供应商地名", "南通": "供应商地名",
 "Aquaflex": "他方型号代号", "FLISTEC": "他方品牌", "Pentair": "他方品牌",
 "Grimm": "他方品牌", "Kobelco": "他方品牌", "lanshen": "供应商域名", "njlshb": "供应商域名",
 "not a trading": "否定句", "we are not": "否定句", "not here to": "否定句",
 "made in our own factory": "夸大自产", "every item is manufactured": "夸大自产",
 "Screw stack": "过时译名",
}
TYPOS = ["Environmrntal", "manfacturer", "As manfacturer", "recieve", "seperate", "occured",
         "equipement", "techonology", "effeciency", "accomodate", "compatibel", "sucessful"]

issues = collections.defaultdict(list)
tables_total = 0

for p in PAGES:
    if not os.path.exists(p):
        issues["缺文件"].append(p); continue
    s = open(p, encoding="utf-8", errors="ignore").read()
    t = txt(s)
    plain = s

    # A. 红线词
    for w, why in RED.items():
        if w.lower() in plain.lower():
            issues[f"红线·{why}"].append(f"{p}: {w}")

    # B. 拼写
    for w in TYPOS:
        if w.lower() in t.lower():
            issues["拼写"].append(f"{p}: {w}")

    # C. 中文残留（英文页不该有汉字，除 logo alt/注释）
    han = re.findall(r"[\u4e00-\u9fff]{2,}", re.sub(r"<!--.*?-->", "", plain, flags=re.S))
    if han:
        issues["中文残留"].append(f"{p}: {han[:6]}")

    # D. 结尾标点/双空格/未转义
    if re.search(r"\s{3,}\S", t):
        issues["多余空格"].append(p)
    if "&amp;amp;" in plain:
        issues["双重转义"].append(p)

    # E. 页面元信息
    title = re.search(r"<title>(.*?)</title>", plain, re.S)
    desc = re.search(r'name="description"\s+content="([^"]*)"', plain)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", plain, re.S)
    title = html.unescape(title.group(1)).strip() if title else ""
    desc = html.unescape(desc.group(1)).strip() if desc else ""
    h1 = txt(h1.group(1)).strip() if h1 else ""
    if not title: issues["缺 title"].append(p)
    if not desc: issues["缺 meta description"].append(p)
    elif len(desc) < 70 or len(desc) > 175:
        issues["meta 长度"].append(f"{p}: {len(desc)} 字")
    if not h1: issues["缺 H1"].append(p)
    if "KINGDAO" not in title: issues["title 无品牌"].append(f"{p}: {title[:50]}")

    # F. 表格体检
    for ti, tb in enumerate(re.findall(r"<table.*?</table>", plain, re.S | re.I)):
        tables_total += 1
        head = re.search(r"<thead.*?</thead>", tb, re.S | re.I)
        rows = re.findall(r"<tr.*?</tr>", tb, re.S | re.I)
        ncol = None
        for ri, r in enumerate(rows):
            cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S | re.I)
            cells = [txt(c) for c in cells]
            if not cells: continue
            if ncol is None:
                ncol = len(cells); continue
            if len(cells) != ncol:
                issues["表格列数不齐"].append(f"{p} 表{ti+1} 行{ri+1}: {len(cells)} vs {ncol}")
            for c in cells:
                if c.strip() in ("", "-", "—", "N/A", "TBD", "待补"):
                    issues["表格空单元格"].append(f"{p} 表{ti+1}: '{c}'")

    # G. 数字口径
    for kw, want in (("EQUIPMENT LINES", "17"), ("YEARS IN WATER", "20")):
        for m in re.finditer(r"<b>(\d+)</b></span>" if False else r"<b>([\d,]+)</b>", plain):
            pass

# H. 跨页一致性：设备数量
nums = collections.Counter()
for p in PAGES:
    s = open(p, encoding="utf-8", errors="ignore").read()
    for m in re.finditer(r"<b>([\d,]+)</b><span>([A-Z][^<]*)</span>", s):
        nums[(m.group(1), m.group(2).strip()[:28])] += 1
    for m in re.finditer(r"([A-Za-z-]+) equipment lines?", s):
        nums[("word:" + m.group(1), "equipment lines")] += 1

print("=" * 74)
print(f"扫描 {len(PAGES)} 个页面 | 表格 {tables_total} 个")
print("=" * 74)
for k in sorted(issues, key=lambda x: -len(issues[x])):
    v = issues[k]
    print(f"\n【{k}】{len(v)} 处")
    for x in v[:14]:
        print("   ", x)
    if len(v) > 14: print(f"    … 另 {len(v)-14} 处")

print("\n【trustbar / 数字口径】")
for (n, label), c in sorted(nums.items(), key=lambda kv: -kv[1]):
    print(f"   {n:<8} {label:<32} x{c}")
print("\n检查完毕")
