# -*- coding: utf-8 -*-
"""IndexNow 推送：把站点地图里的 URL 主动提交给 Bing / Yandex / Seznam。
用法: python _indexnow.py            # 提交全部
      python _indexnow.py <url> ...  # 只提交指定 URL
"""
import json, os, sys, urllib.request, re

ROOT = os.path.dirname(os.path.abspath(__file__))
KEY = open(os.path.join(ROOT, "_indexnow_key.txt"), encoding="utf-8").read().strip()
HOST = "www.kingdaotech.com"

if len(sys.argv) > 1:
    urls = sys.argv[1:]
else:
    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    urls = re.findall(r"<loc>(.*?)</loc>", sm)

payload = {
    "host": HOST,
    "key": KEY,
    "keyLocation": f"https://{HOST}/{KEY}.txt",
    "urlList": urls,
}
data = json.dumps(payload).encode()
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow", data=data,
    headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
try:
    with urllib.request.urlopen(req, timeout=45) as r:
        body = r.read().decode(errors="ignore")[:300]
        print(f"HTTP {r.status} {r.reason} | 提交 {len(urls)} 条 | {body}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code} {e.reason} | {e.read().decode(errors='ignore')[:300]}")
except Exception as e:
    print("ERR", e)
