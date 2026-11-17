# -*- coding: utf-8 -*-
"""CDP 抓老站（www.kingdaotech.com）：枚举产品页链接 + 图片 URL。
老站有 WAF，curl 直抓是 403 假页，必须走真浏览器。"""
import json, urllib.request, websocket, time, sys, re

def new_tab(url):
    req = urllib.request.Request('http://127.0.0.1:9222/json/new?' + url, method='PUT')
    return json.load(urllib.request.urlopen(req))

class CDP:
    def __init__(self, tab):
        self.ws = websocket.create_connection(tab['webSocketDebuggerUrl'], timeout=40)
        self.i = 0
        self.tab = tab
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
    def goto(self, url, wait=8):
        self.send('Page.navigate', {'url': url}); time.sleep(wait)
    def close(self):
        try:
            urllib.request.urlopen(urllib.request.Request(
                'http://127.0.0.1:9222/json/close/' + self.tab['id'], method='PUT'))
        except Exception:
            pass

tab = new_tab("about:blank")
c = CDP(tab)
c.send('Page.enable'); c.send('Runtime.enable')

HOME = "https://www.kingdaotech.com/"
c.goto(HOME, 10)
print("标题:", c.ev("document.title"))
print("正文长度:", c.ev("document.body.innerText.length"))

js = """JSON.stringify({
  imgs: [...new Set([...document.images].map(i=>i.currentSrc||i.src))],
  links: [...new Set([...document.querySelectorAll('a[href]')].map(a=>a.href))]
})"""
raw = c.ev(js)
data = json.loads(raw) if raw else {"imgs": [], "links": []}
print(f"\n图片 {len(data['imgs'])} 个：")
for u in data["imgs"][:30]:
    print("  ", u)
print(f"\n链接 {len(data['links'])} 个（含产品页）：")
prod = [u for u in data["links"] if any(k in u for k in ("list_", "show_", "/?p", "product"))]
for u in prod[:40]:
    print("  ", u)

c.close()
