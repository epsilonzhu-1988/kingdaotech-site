import re, subprocess, json, os, sys

BASE = "http://www.njlshb.cn/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0 Safari/537.36"
OUT = r"C:\Users\Administrator\kingdaotech_newsite\_src_njlshb"
os.makedirs(OUT, exist_ok=True)

def get(url):
    r = subprocess.run(["curl", "-s", "-m", "40", "-4", "-A", UA, url],
                       capture_output=True)
    return r.stdout.decode("utf-8", "ignore")

def strip(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<[^>]+>", "\n", h)
    h = h.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    lines = [x.strip() for x in h.split("\n")]
    return "\n".join([x for x in lines if x])

cats = {158: "格栅除污机", 153: "内进流格栅", 159: "输送压榨机"}
allp = {}
for cid, cname in cats.items():
    h = get(BASE + f"product_{cid}.html")
    links = sorted(set(re.findall(r"product_view_(\d+)_%d(?:\.html)?" % cid, h)), key=int)
    names = re.findall(r'product_view_\d+_%d\.html"[^>]*>\s*(?:<[^>]+>\s*)*([^<]{2,60})' % cid, h)
    print(f"=== cid {cid} {cname}: {len(links)} 个 -> {links}")
    allp[cid] = links
    open(os.path.join(OUT, f"list_{cid}.txt"), "w", encoding="utf-8").write(h)
print()
for cid, pids in allp.items():
    for pid in pids:
        url = f"product_view_{pid}_{cid}.html"
        h = get(BASE + url)
        t = strip(h)
        # 标题
        m = re.search(r"<title>(.*?)</title>", h, re.S)
        title = m.group(1).strip() if m else "?"
        # 主图
        mi = re.search(r'\.pro_main.*?<img[^>]+src="([^"]+)"', h, re.S)
        if not mi:
            mi = re.search(r'<img[^>]+src="(/upload[^"]+)"', h)
        img = mi.group(1) if mi else ""
        open(os.path.join(OUT, f"{pid}_{cid}.txt"), "w", encoding="utf-8").write(t)
        print(f"--- {pid}_{cid} | {title[:40]} | img={img}")
        # 打印正文里的参数样例行
        lines = [x for x in t.split("\n") if re.search(r"\d", x) and len(x) < 200]
        for x in lines[:14]:
            print("   ", x)
        print()
