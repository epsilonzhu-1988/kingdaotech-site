# -*- coding: utf-8 -*-
"""上线前 SEO 修：① canonical 改成自指的唯一 URL（原来是全站指首页，会把 24 页并成 1 页）
② 删掉导航里的「Old site」外链  ③ 统一到生产域名"""
import re, os, glob

ROOT = r"C:\Users\Administrator\kingdaotech_newsite"
PROD = "https://www.kingdaotech.com"      # 上线后的正式域名
os.chdir(ROOT)

def url_for(path):
    p = path.replace("\\", "/")
    if p == "index.html":
        return PROD + "/"
    if p.endswith(".html"):
        return PROD + "/" + p[:-5]
    return PROD + "/" + p

changed = 0
for f in ["404.html"] + sorted(glob.glob("*.html")) + sorted(glob.glob("products/*.html")):
    if f == "404.html" and not os.path.exists(f):
        continue
    s = open(f, encoding="utf-8").read()
    orig = s
    canon = url_for(f) if f != "404.html" else PROD + "/"
    s = re.sub(r'<link rel="canonical" href="[^"]*"',
               f'<link rel="canonical" href="{canon}"', s, count=1)
    # 删导航里的 Old site 外链
    s = re.sub(r'<li>\s*<a href="https://www\.kingdaotech\.com/?">\s*Old site\s*</a>\s*</li>', "", s)
    s = re.sub(r'<li><a href="https://www\.kingdaotech\.com/?">Old site</a></li>', "", s)
    if s != orig:
        open(f, "w", encoding="utf-8").write(s)
        changed += 1

print(f"改动 {changed} 个页面")
# 校验
bad = []
for f in glob.glob("*.html") + glob.glob("products/*.html"):
    s = open(f, encoding="utf-8").read()
    m = re.search(r'<link rel="canonical" href="([^"]*)"', s)
    if not m:
        bad.append((f, "无 canonical"))
    elif m.group(1) != url_for(f):
        bad.append((f, m.group(1)))
    if "Old site" in s:
        bad.append((f, "仍有 Old site"))
print("异常:", len(bad))
for x in bad[:10]:
    print("  ", x)
