# -*- coding: utf-8 -*-
"""抓老站产品目录：每个分类页 → 产品链接+名称；每个详情页 → 大图 URL。结果存 old_site_map.json"""
import json, urllib.request, websocket, time, os, re

OUT = r"C:\Users\Administrator\kingdaotech_newsite\old_site_map.json"
HOME = "https://www.kingdaotech.com/"
CIDS = [7, 8, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

def new_tab():
    req = urllib.request.Request('http://127.0.0.1:9222/json/new?about:blank', method='PUT')
    return json.load(urllib.request.urlopen(req))

class CDP:
    def __init__(self):
        self.tab = new_tab()
        self.ws = websocket.create_connection(self.tab['webSocketDebuggerUrl'], timeout=45)
        self.i = 0
        self.send('Page.enable'); self.send('Runtime.enable')
    def send(self, m, p=None):
        self.i += 1
        self.ws.send(json.dumps({'id': self.i, 'method': m, 'params': p or {}}))
        while True:
            r = json.loads(self.ws.recv())
            if r.get('id') == self.i:
                return r
    def ev(self, js):
        r = self.send('Runtime.evaluate', {'expression': js, 'returnByValue': True, 'awaitPromise': True})
        return r.get('result', {}).get('result', {}).get('value')
    def goto(self, url, wait=7):
        self.send('Page.navigate', {'url': url}); time.sleep(wait)
    def close(self):
        try:
            urllib.request.urlopen(urllib.request.Request(
                'http://127.0.0.1:9222/json/close/' + self.tab['id'], method='PUT'))
        except Exception:
            pass

c = CDP()
result = {"categories": [], "products": []}
EXT_JS = """JSON.stringify({
  title: document.title,
  h1: (document.querySelector('h1')||{}).innerText || '',
  items: [...document.querySelectorAll('a[href*=".html"]')].map(a=>({
      href:a.href, name:(a.innerText||a.title||'').trim().slice(0,80),
      img:(a.querySelector('img')||{}).src||''})).filter(x=>x.name && /list_\\d+\\/\\d+\\.html/.test(x.href)),
  imgs: [...new Set([...document.images].map(i=>i.currentSrc||i.src))].filter(u=>u.includes('/static/upload/'))
})"""

for cid in CIDS:
    url = f"{HOME}?list_{cid}/"
    c.goto(url, 7)
    raw = c.ev(EXT_JS)
    try:
        d = json.loads(raw)
    except Exception:
        print("解析失败", cid); continue
    cat = {"cid": cid, "name": d.get("h1") or d.get("title", ""), "items": d.get("items", []),
           "imgs": d.get("imgs", [])}
    result["categories"].append(cat)
    print(f"[{cid}] {cat['name'][:30]} | 产品 {len(cat['items'])} | 图 {len(cat['imgs'])}", flush=True)

done = set()
for cat in result["categories"]:
    for it in cat["items"]:
        if it["href"] in done:
            continue
        done.add(it["href"])
        c.goto(it["href"], 6)
        raw = c.ev(EXT_JS)
        try:
            d = json.loads(raw)
        except Exception:
            continue
        result["products"].append({
            "cid": cat["cid"], "list_name": cat["name"],
            "href": it["href"], "name": d.get("h1") or it["name"] or d.get("title", ""),
            "imgs": d.get("imgs", [])})
        print(f"  - {it['name'][:34]} → 图 {len(d.get('imgs',[]))}", flush=True)

json.dump(result, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n完成：分类 {len(result['categories'])} / 产品 {len(result['products'])} → {OUT}", flush=True)
c.close()
