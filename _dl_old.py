# -*- coding: utf-8 -*-
import json, subprocess, os
p = r"C:\Users\Administrator\kingdaotech_newsite\old_site_map.json"
d = json.load(open(p, encoding='utf-8'))
OUTDIR = r"C:\Users\Administrator\kingdaotech_offline_pages\_old_site_img"
os.makedirs(OUTDIR, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/138.0.0.0 Safari/537.36"
urls = []
for pr in d['products']:
    for u in pr['imgs']:
        if '/static/upload/' in u and u not in urls:
            urls.append(u)
todo = [u for u in urls if not (os.path.exists(os.path.join(OUTDIR, u.rsplit('/', 1)[-1]))
        and os.path.getsize(os.path.join(OUTDIR, u.rsplit('/', 1)[-1])) > 1000)]
print(f"总 {len(urls)} | 待下 {len(todo)}", flush=True)
done = 0
for u in todo:
    fn = os.path.join(OUTDIR, u.rsplit('/', 1)[-1])
    subprocess.run(['curl', '-s', '-m', '50', '-A', UA, '-o', fn, u], capture_output=True)
    if os.path.exists(fn) and os.path.getsize(fn) > 1000:
        done += 1
    print(f"  {done}/{len(todo)} {os.path.basename(fn)} {os.path.getsize(fn)//1024 if os.path.exists(fn) else 0}KB", flush=True)
print("DONE", done, flush=True)
