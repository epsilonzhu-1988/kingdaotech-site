# -*- coding: utf-8 -*-
"""上线前全面体检 v2 —— 按主人 11-17 清单逐条核验（本地文件 + 线上）"""
import os, re, glob, json, subprocess

S = r"C:\Users\Administrator\kingdaotech_newsite"
os.chdir(S)
PAGES = ["index.html","products.html","projects.html","solutions.html","about.html","oem.html","contact.html"] + sorted(glob.glob("products/*.html"))
def rd(p): return open(p, encoding='utf-8', errors='ignore').read()

R = []
def add(cat, item, status, detail=""):
    R.append((cat, item, status, detail))

# ── 1. 表单 ──
forms = []
for p in PAGES:
    s = rd(p)
    for m in re.finditer(r'<form[^>]*>', s):
        forms.append((p, m.group(0)[:100]))
if not forms:
    add("表单", "存在 <form>", "❌", "全站 0 个 form 标签")
else:
    bad = [(p, f) for p, f in forms if 'action=' not in f]
    add("表单", f"form 数 {len(forms)}", "⚠" if bad else "✅", f"{len(bad)} 个无 action")
# 有 name 属性的输入框
named = 0
for p in PAGES:
    named += len(re.findall(r'<(?:input|textarea|select)[^>]*\bname=', rd(p)))
add("表单", "带 name 的字段", "❌" if named == 0 else "✅", f"共 {named} 个")

# ── 2. favicon ──
fav_local = os.path.exists("favicon.ico")
fav_ref = any("favicon" in rd(p) for p in PAGES[:7])
add("favicon", "本地文件", "✅" if fav_local else "❌", "favicon.ico" )
add("favicon", "页面引用", "✅" if fav_ref else "⚠", "有 <link rel=icon>" if fav_ref else "无引用")

# ── 3. CSS 背景图 ──
css = rd("assets/css/style.css")
bg = re.findall(r'url\(["\']?([^"\')]+\.(?:jpg|png|webp))', css)
missing_bg = []
for b in bg:
    if b.startswith("http") or b.startswith("data:"): continue
    cand = os.path.normpath(os.path.join("assets/css", b))
    if not os.path.exists(cand): missing_bg.append(b)
add("CSS 图", f"背景图 {len(bg)} 个", "❌" if missing_bg else "✅", "缺: " + ", ".join(missing_bg[:3]) if missing_bg else "全部存在")

# ── 4. 数字口径 ──
def count_phrase(pat, scope=PAGES):
    hits = []
    for p in scope:
        for m in re.finditer(pat, rd(p)):
            hits.append((p, m.group(0)[:40]))
    return hits
prod_nums = {}
for pat, label in ((r'\b(\d{1,2})\s*(?:equipment lines|product lines|EQUIPMENT LINES|PRODUCT LINES)', "设备数"),
                   (r'(\d{1,2})\s+equipment lines', "设备数")):
    for p, t in count_phrase(pat): prod_nums.setdefault(t, []).append(p)
ind = count_phrase(r'\b(\d{1,2})\s+industries')
cap = count_phrase(r'(\d{2},\d{3})\s*m.?/d')
add("口径", "设备数出现", "⚠", str({k: len(v) for k, v in prod_nums.items()}) if prod_nums else "未找到")
vals = sorted({t.split()[0] for _, t in ind})
add("口径", "行业数", "❌" if len(vals) > 1 else "✅", "出现: " + "/".join(vals) if vals else "未找到")
caps = sorted({t.split()[0].rstrip(',') for _, t in cap})
add("口径", "规模数字", "⚠" if len(caps) > 3 else "✅", "出现: " + ", ".join(caps[:8]))

# ── 5. Detail page 残留 ──
dp = [(p, s.count("Detail page")) for p in PAGES if "Detail page" in rd(p)]
dp = [(p, c) for p, c in dp]
add("占位", "Detail page 残留", "❌" if dp else "✅", f"{sum(c for _, c in dp)} 处 / {len(dp)} 页")

# ── 6. Tertiary treatment 空分类 ──
sol = rd("solutions.html")
add("内容", "Tertiary treatment 空分类", "⚠" if "Tertiary" in sol else "✅",
    "存在（需检查是否有内容）" if "Tertiary" in sol else "未出现")

# ── 7. 中文混入英文页 ──
cn = []
for p in PAGES:
    for m in re.finditer(r'>([^<>]*[\u4e00-\u9fff][^<>]*)<', rd(p)):
        t = m.group(1).strip()
        if t and t not in ("朱  荣  涛",): cn.append((p, t[:24]))
add("内容", "英文页中文残留", "⚠" if cn else "✅", f"{len(cn)} 处: " + str(cn[:3]))

# ── 8. 表单占位 ──
ph = []
for p in PAGES:
    s = rd(p)
    for m in re.finditer(r'placeholder="([^"]*)"', s):
        ph.append((p, m.group(1)))
bad_ph = [x for x in ph if "+60" in x[1] or "m3/d" in x[1]]
add("表单", "占位符问题", "⚠" if bad_ph else "✅", str(bad_ph[:3]))

# ── 9. canonical ──
canon = {}
for p in PAGES:
    m = re.search(r'<link rel="canonical" href="([^"]+)"', rd(p))
    canon[p] = m.group(1) if m else None
no_canon = [p for p, v in canon.items() if not v]
www_canon = [p for p, v in canon.items() if v and v.startswith("https://www.kingdaotech.com")]
add("SEO", "canonical 缺失", "❌" if no_canon else "✅", f"{len(no_canon)} 页")
add("SEO", "canonical 指向 www", "⚠" if www_canon else "✅", f"{len(www_canon)} 页: {www_canon[:2]}")

# ── 10. OG 标签 ──
og = [p for p in PAGES if 'property="og:' in rd(p)]
add("SEO", "OG 标签", "✅" if len(og) == len(PAGES) else "⚠", f"{len(og)}/{len(PAGES)} 页有")

# ── 11. 首页空 alt ──
idx = rd("index.html")
imgs = re.findall(r'<img[^>]*>', idx)
empty_alt = [i for i in imgs if 'alt=""' in i or 'alt=' not in i]
add("SEO", "首页空 alt", "❌" if empty_alt else "✅", f"{len(empty_alt)}/{len(imgs)} 张")

# ── 12. 页脚纯文本链接 ──
foot = idx[idx.find("<footer"):idx.find("</footer>")]
plain = re.findall(r'<(?:div|span|li|p)[^>]*>(?:[^<>]{2,40})</(?:div|span|li|p)>', foot)
fb = "Food & Beverage" in foot
add("内链", "页脚纯文本项", "⚠", f"{len(plain)} 个非链接文本块")
add("内链", "Food & Beverage 假链接", "❌" if fb else "✅", "存在" if fb else "无")

# ── 13. 图片体积 ──
big = []
for f in glob.glob("images/**/*.jpg", recursive=True) + glob.glob("images/**/*.png", recursive=True):
    kb = os.path.getsize(f) // 1024
    if kb > 260: big.append((f, kb))
big.sort(key=lambda x: -x[1])
add("性能", f">260KB 图片", "⚠" if big else "✅", f"{len(big)} 张, 最大 {big[0][1]}KB ({big[0][0]})" if big else "无")

# ── 14. sitemap lastmod ──
try:
    sm = rd("sitemap.xml")
    lms = sorted(set(re.findall(r'<lastmod>([^<]+)</lastmod>', sm)))
    add("SEO", "sitemap lastmod", "⚠" if lms and max(lms) < "2026-11-17" else "✅", f"最新 {max(lms) if lms else '无'}, {sm.count('<loc>')} 条")
except Exception as e:
    add("SEO", "sitemap", "❌", str(e)[:40])

# ── 15. 彭州进 Solutions ──
add("内容", "彭州在 Solutions", "✅" if "Cifeng" in sol or "Pengzhou" in sol else "⚠",
    "有" if ("Cifeng" in sol or "Pengzhou" in sol) else "无")

print(f"{'类别':<6} {'检查项':<24} {'状态':<4} 详情")
print("-" * 96)
for cat, item, st, det in R:
    print(f"{cat:<6} {item:<24} {st:<4} {det[:70]}")
bad = [r for r in R if r[2] == "❌"]
print(f"\n❌ {len(bad)} 项 / ⚠ {len([r for r in R if r[2]=='⚠'])} 项 / ✅ {len([r for r in R if r[2]=='✅'])} 项")
