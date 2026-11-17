# -*- coding: utf-8 -*-
"""KINGDAO 官网 A 组改造：
1) 格栅 4 页 + 刮泥机页 → 补真实选型/参数表（蓝赛 / 蓝深 素材）
2) 无素材设备 9 页下线（删文件 + 删 products/index 卡片 + 重建 sitemap）
3) 首屏设备数量按实际在线页数纠正
"""
import os, re, glob, shutil, datetime

ROOT = r"C:\Users\Administrator\kingdaotech_newsite"
os.chdir(ROOT)

def rd(p):  return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8").write(s)

def sec(eyebrow, h2, lead, tables_html):
    return (f'\n<section class="soft"><div class="wrap">\n'
            f'  <div class="sec-head"><div class="eyebrow">{eyebrow}</div>\n'
            f'    <h2>{h2}</h2>\n    <p class="lead">{lead}</p></div>\n'
            f'{tables_html}\n</div></section>\n')

def table(headers, rows, cls="spec"):
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = ""
    for r in rows:
        tds = "".join(f"<td>{c}</td>" for c in r)
        tr += f"<tr>{tds}</tr>"
    return (f'  <div class="spec-wrap"><table class="{cls}">\n'
            f'    <thead><tr>{th}</tr></thead>\n    <tbody>{tr}</tbody>\n  </table></div>')

def kv(rows, title=None):
    body = "".join(f'<div><b>{k}</b><span>{v}</span></div>' for k, v in rows)
    t = f'<h3 style="margin:26px 0 12px">{title}</h3>' if title else ""
    return f'{t}<div class="kv-row">{body}</div>'

PAGES = {}

# ── 1. 机械格栅 ────────────────────────────────────────────
PAGES["mechanical-bar-screen.html"] = [
 sec("Selection · four mechanisms",
     "Four bar-screen mechanisms — choose by channel, not by price.",
     "A bar screen is sized by the channel it sits in: width and depth decide the mechanism, "
     "the rake gap decides what reaches the next stage. Below are the four drives we build, "
     "with the range each one actually covers.",
     table(["Type", "Rake gap", "Channel width", "Channel depth", "Install angle",
            "Drive motor", "Capture"],
           [["<strong>Rotary rake</strong> — bars sit between the chains, so screenings cannot ride under the rake",
             "1–50 mm (10–50 coarse / 1–10 fine)", "500–3,000 mm", "1,000–5,000 mm", "60°–75°",
             "0.55–5.5 kW, IP55", "≥95%"],
            ["<strong>Mechanical coarse</strong> — continuous chain-rake, the workhorse for municipal inlets",
             "10 / 20 / 30 / 40 / 50 mm", "500–3,500 mm", "to civil drawing", "60°–75°",
             "0.75–5.5 kW, IP55", "rake speed 2.5–4.5 m/min"],
            ["<strong>Grab type</strong> — single grab on a travelling gantry; wide and deep channels",
             "10–50 mm", "1,000–8,000 mm", "1,500–8,000 mm", "vertical", "hoist 4–8 m/min, travel 6–12 m/min",
             "intermittent duty"],
            ["<strong>Rotary cleaner (GSHZ)</strong> — compact single-frame unit for pump stations",
             "10–50 mm", "600–2,000 mm", "2,000–5,000 mm", "75°", "0.75–2.2 kW, IP55", "continuous"]]))
 + kv([("Frame", "304 / 316L stainless, welded on a jig, trial-run before dispatch"),
       ("Bar elements", "304 stainless flat bar, straightness and gap tolerance ≤0.5 mm, no sharp leading edge"),
       ("Chain", "wide-plate stainless, safety factor ≥6, with tensioner; enclosed so screenings cannot enter the chain slot"),
       ("Protection", "overload relay plus shear pin — the pin cuts before the drive or the chain does"),
       ("Duty", "24 h continuous or intermittent, per site requirement")],
      "Shared structure — all four types")
 + kv([("Model code", "GSHZ – channel width × channel depth – rake gap"),
       ("Example", "GSHZ-1200×3500-10 = 1,200 mm wide, 3,500 mm deep, 10 mm gap")],
      "Reading the model code")],

# ── 2. 细格栅 ─────────────────────────────────────────────
PAGES["fine-bar-screen.html"] = [
 sec("Selection · 1–25 mm",
     "Fine screening is a different problem: it is about open area, not about gaps.",
     "Below about 10 mm the bar screen stops working — rags blind the bars and the head loss runs away. "
     "That is why fine screening uses perforated plate, wedge-wire drums or a stepped plate: the water "
     "passes through a hole, not between two bars.",
     table(["Type", "Aperture", "Channel width", "Install angle", "Capacity", "Drive", "Note"],
           [["<strong>Stepped plate, rotary</strong>",
             "1 / 3 / 5 / 6 / 10 / 15 / 25 mm", "500–3,000 mm", "65°–90° (75° typical)",
             "50–5,000 m³/h", "0.75–3.0 kW", "open area 30%+ above a flat screen of the same footprint"],
            ["<strong>Stepped plate, rotary wiper</strong>",
             "1 / 3 / 5 / 6 / 10 / 15 / 20 mm", "500–3,000 mm", "65°–90° (70°–75° typical)",
             "100–5,000 m³/h", "0.55–3.0 kW", "top brush + ≥0.4 MPa backwash, plate regeneration ≥85%, capture ≥98%"],
            ["<strong>In-flow perforated plate</strong>",
             "3 / 5 / 6 mm typical", "to civil drawing", "vertical, 90°",
             "by flow, e.g. 4 units at 20,000 m³/d each", "IP55 / class F",
             "separation ≥97%, head loss ≤300 mm at 40% blinding"],
            ["<strong>Horizontal drum</strong> — wedge-wire cylinder",
             "0.5–5 mm slot", "inline in channel", "horizontal", "by drum diameter and speed",
             "gear motor with VFD", "continuous separation, variable speed, cylinder resists blinding"],
            ["<strong>Stepped fine screen</strong> — static steps",
             "1–10 mm", "500–2,000 mm", "60°–75°", "by channel", "none (static)", "no drive, lowest maintenance"]]))
 + kv([("Plate", "304 / 316L laser-perforated, stepped arrangement"),
       ("Frame & housing", "304 / 316L, box-section, stiffened for 1.0 m water-level difference"),
       ("Submerged parts", "no bearings or drives below water — only the plate touches the flow"),
       ("Drive", "top-mounted gear motor, torque limiter, overload stop"),
       ("Sealing", "neoprene or nitrile")],
      "Structure and materials")
 + kv([("Head loss", "≤300 mm at 40% blinded (in-flow plate) / ≤350 mm (stepped plate wiper)"),
       ("Separation", "≥97% (in-flow plate) / ≥98% (stepped plate wiper)"),
       ("MTBF", "≈8,000 h, machine life designed for 15 years"),
       ("Noise", "≤70–78 dB(A)"),
       ("Power supply", "380 V / 3 ph / 50 Hz — 440 V / 60 Hz on request (Philippines)")],
      "Performance the numbers refer to")],

# ── 3. 粗格栅 / 人工格栅 ──────────────────────────────────
PAGES["coarse-manual-screen.html"] = [
 sec("Selection · coarse and hand-cleaned",
     "Coarse screening: when a machine is worth it, and when it is not.",
     "Coarse bar screens (10–50 mm) exist to protect pumps. On a small works with light screenings, "
     "a hand-cleaned screen is still the correct answer — it is a fabricated assembly, not a machine, "
     "and it never breaks down. The decision is screenings volume, not budget.",
     table(["Type", "Rake gap", "Channel width", "Mechanism", "Drive", "When it is the right choice"],
           [["<strong>Mechanical coarse</strong> — chain rake",
             "10 / 20 / 30 / 40 / 50 mm", "500–3,500 mm", "continuous chain rake, self-cleaning on the return",
             "0.75–5.5 kW, IP55", "continuous screenings, unmanned stations, pump protection"],
            ["<strong>Grab type</strong> — travelling gantry",
             "10–50 mm", "1,000–8,000 mm", "grab lifts and dumps; no submerged drive",
             "hoist 4–8 m/min, travel 6–12 m/min", "wide and deep inlet channels, stormwater, large pump stations"],
            ["<strong>Hand-cleaned bar screen</strong> — fabricated",
             "10–50 mm", "to civil drawing", "manually raked; hinged or lift-out bar rack",
             "none", "small works, light screenings, emergency or bypass channel"]]))
 + kv([("Bar rack", "304 stainless flat bar in a welded frame, set to your channel section"),
       ("Gap tolerance", "±1 mm on hand-cleaned racks, ≤0.5 mm on machined machine bars"),
       ("Inclination", "60°–75° for machine raking; 45°–60° for hand raking (easier reach)"),
       ("Finishing", "pickled and passivated; 316L for saline or high-chloride duty"),
       ("Supply", "screen only, or screen with screenings bin, conveyor and Control panel")],
      "What we need from your civil drawing")],

# ── 4. 螺旋格栅 ───────────────────────────────────────────
PAGES["screw-screen.html"] = [
 sec("Selection · GP press range",
     "Screw screens and presses — the dewatering end of the screening train.",
     "Whatever the screen catches has to leave the building as a manageable solid. "
     "The GP range covers the usual 1–4 m³/h of screenings; the shaftless conveyor moves it, "
     "the press takes the water back out of it.",
     table(["Model", "Screw Ø mm", "Screw speed", "Capacity m³/h", "Inlet dry solids",
            "Outlet dry solids", "Motor kW", "L mm", "B mm"],
           [["<strong>GP-200</strong>", "200", "4–8 r/min", "1.0", "85–95%", "40–45%", "1.1", "1,500", "260"],
            ["<strong>GP-300</strong>", "300", "4–8 r/min", "2.0", "85–95%", "40–45%", "1.5", "1,500", "320"],
            ["<strong>GP-400</strong>", "400", "4–8 r/min", "4.0", "85–95%", "40–45%", "3.0", "1,800", "420"]]))
 + kv([("Shaftless screw conveyor", "no centre shaft, no hanger bearings in the trough — rags and fibres cannot wrap and stall it"),
       ("Integrated conveyor-press", "conveying and dewatering in one trough; screenings arrive at the bin already drained"),
       ("High-drainage press (GP)", "perforated trough plus inclined press zone; 85–95% inlet down to 40–45% outlet"),
       ("Grit separator", "spiral classifier for grit from grit chambers; grit settles, organics are carried back"),
       ("Wear parts", "screw flights and trough liners are the consumables — replaceable without removing the trough")],
      "Four components, one train")
 + kv([("Wetted parts", "304 / 316L stainless; UHMW-PE wear liner in the press zone"),
       ("Drive", "shaft-mounted gear motor, IP55, overload protection"),
       ("Installation", "trough set to site slope; press outlet height set to the bin"),
       ("Duty", "continuous, coordinated with the screen's rake cycle")],
      "Specification")],

# ── 5. 刮泥机（蓝深素材）────────────────────────────────────
PAGES["sludge-scraper.html"] = [
 sec("Selection · ZQ(B)GN",
     "Sludge scraping: the scraper travels a helix, not a radius.",
     "A rake arm pushed radially leaves a ring of sludge at the tank wall. The ZQ(B)GN scraper "
     "is set so the blade travels a spiral path — every pass sweeps fresh floor and pushes toward "
     "the sludge hopper, so the tank does not silt up between desludging cycles.",
     table(["Configuration", "Bridge", "Typical tank", "Drive", "What it is for"],
           [["<strong>ZQGN — full bridge</strong>", "full diameter, two supports on the wall ring",
             "large diameter tanks", "higher drive power, twin drive optional",
             "big secondary clarifiers where one arm cannot cover the floor in a reasonable time"],
            ["<strong>ZQBN — half bridge</strong>", "half diameter, one centre pivot + one wall carriage",
             "small and medium tanks", "single drive, economy",
             "rectangular-to-round conversions, small works, package plants"]]))
 + kv([("Scraping path", "helical — blade angle set so each revolution advances the sludge inward"),
       ("Sludge removal", "floor slope carries sludge to the central hopper; scraper does not have to push it uphill"),
       ("Scum removal", "surface skimmer blade + wall scum baffle, discharging to a scum box in the same revolution"),
       ("Obstruction handling", "arm lifts on obstruction, torque protection stops the drive — it recovers, it does not shear the shaft"),
       ("Main beam", "carbon steel (painted) / stainless / aluminium, by span and corrosion class"),
       ("Drive", "shaft-mounted gear motor, direct coupled — fewer failure points than chain drives"),
       ("Control", "PLC interface, run-time and interval setting, torque alarm to SCADA")],
      "How it is built")
 + kv([("Tank", "diameter, depth, wall height above floor, floor slope"),
       ("Duty", "primary or secondary clarifier, and the sludge draw-off arrangement"),
       ("Bridge", "full or half, and whether a walkway or handrail is required"),
       ("Material", "carbon steel, stainless or aluminium for beam; stainless for submerged parts"),
       ("Options", "scum skimmer, effluent weir plate, froth spray, hopper valve")],
      "What we need to select one")],

# ── 插入 ───────────────────────────────────────────────────
report = []
for fn, blocks in PAGES.items():
    p = os.path.join("products", fn)
    s = rd(p)
    if "KINGDAO_A_GROUP" in s:
        report.append(f"SKIP(已改过) {fn}"); continue
    i = s.find("</section>")
    assert i > 0, fn
    j = i + len("</section>")
    flat = []
    for b in blocks:
        flat.extend(b if isinstance(b, list) else [b])
    ins = "\n<!-- KINGDAO_A_GROUP -->" + "".join(flat)
    s = s[:j] + ins + s[j:]
    wr(p, s)
    report.append(f"OK 插入参数表 {fn} ({os.path.getsize(p)//1024} KB)")

# ── 下线 9 页 ──────────────────────────────────────────────
OFFLINE = ["daf", "sand-filter", "uv", "screw-pump", "sludge-dryer",
           "screw-conveyor", "dm-dewatering", "small-integrated-stp", "mbbr"]
os.makedirs("_offline_pages", exist_ok=True)
for slug in OFFLINE:
    p = os.path.join("products", slug + ".html")
    if os.path.exists(p):
        shutil.move(p, os.path.join("_offline_pages", slug + ".html"))
        report.append(f"下线 {slug}.html → _offline_pages/")

# ── 删卡片 ────────────────────────────────────────────────
def drop_cards(path, slugs):
    s = rd(path); n0 = len(s)
    for slug in slugs:
        # 整卡：<a ... href=".../slug.html" ...> ... </a>
        pat = re.compile(r'<a\b[^>]*href="[^"]*' + re.escape(slug) + r'\.html"[^>]*>.*?</a>', re.S)
        s, k = pat.subn("", s)
        if k: report.append(f"  {os.path.basename(path)}: 删 {slug} 卡 x{k}")
    if len(s) != n0:
        wr(path, s)

drop_cards("products.html", OFFLINE)
drop_cards("index.html", OFFLINE)

# ── 重建 sitemap ──────────────────────────────────────────
BASE = "https://new.kingdaotech.com"
extras = ["index.html", "products.html", "projects.html", "solutions.html",
          "oem.html", "about.html", "contact.html"]
urls = []
for f in extras:
    u = "/" if f == "index.html" else "/" + f[:-5]
    urls.append(u)
for f in sorted(glob.glob("products/*.html")):
    urls.append("/products/" + os.path.basename(f)[:-5])
today = datetime.date.today().isoformat()
xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    xml.append(f"  <url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod></url>")
xml.append("</urlset>")
wr("sitemap.xml", "\n".join(xml) + "\n")
rb = rd("robots.txt")
rb = re.sub(r"Sitemap:.*", f"Sitemap: {BASE}/sitemap.xml", rb)
wr("robots.txt", rb)
report.append(f"重建 sitemap.xml：{len(urls)} 条（product {len(glob.glob('products/*.html'))} 页）")

# ── 纠正首屏设备数量 ─────────────────────────────────────
alive = len(glob.glob("products/*.html"))
for f in ("index.html", "products.html"):
    s = rd(f)
    n = 0
    s, k1 = re.subn(r"<b>\d+</b>(\s*)EQUIPMENT", r"<b>%d</b>\1EQUIPMENT" % alive, s); n += k1
    s, k2 = re.subn(r">\s*\d+\s*EQUIPMENT LINES? SUPPLIED", "> %d EQUIPMENT LINES SUPPLIED" % alive, s); n += k2
    s, k3 = re.subn(r"Twenty-five equipment", "%s equipment" % ("Twenty-севен" if alive == 27 else
                     ("Seventeen" if alive == 17 else str(alive))), s); n += k3
    if n:
        wr(f, s); report.append(f"  {f}: 设备数量 → {alive}（{n} 处）")

print("\n".join(report))
print(f"\n在线产品页 = {alive}")
