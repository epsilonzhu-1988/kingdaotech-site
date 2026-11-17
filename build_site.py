# -*- coding: utf-8 -*-
"""KINGDAO 新官网静态站生成器 —— 一次生成全部页面
用法: python build_site.py
"""
import os, json, datetime

ROOT = r"C:\Users\Administrator\kingdaotech_newsite"
SITE = "https://www.kingdaotech.com"
TODAY = datetime.date.today().isoformat()

NAV = [("index.html", "Home"), ("products.html", "Products"), ("projects.html", "Projects"),
       ("solutions.html", "Solutions"), ("oem.html", "OEM & Partnership"),
       ("about.html", "About"), ("contact.html", "Contact")]

def head(title, desc, depth=0, active=""):
    p = "../" * depth
    links = "".join(
        '<a href="%s%s"%s>%s</a>' % (p, u, ' style="color:var(--teal)"' if u == active else "", t)
        for u, t in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{p}assets/css/style.css">
<link rel="canonical" href="{SITE}/">
</head>
<body>
<header>
  <div class="wrap nav">
    <a class="brand" href="{p}index.html"><img src="{p}images/logo.png" alt="KINGDAO Environmental Technology"><span class="bt">KINGDAO<span class="bt2">TECH</span></span></a>
    <nav class="links">{links}</nav>
    <a class="btn btn-primary" href="{p}contact.html">Request a Quote</a>
    <button class="burger" aria-label="menu">&#9776;</button>
  </div>
</header>
"""

def foot(depth=0):
    p = "../" * depth
    return f"""
<footer>
  <div class="wrap">
    <div class="f-grid">
      <div>
        <div class="brand" style="margin-bottom:16px"><img src="{p}images/logo_white.png" alt="KINGDAO Environmental Technology"><span class="bt" style="color:#fff">KINGDAO<span class="bt2" style="color:#8FE3B8">TECH</span></span></div>
        <p style="font-size:13.5px;max-width:34ch">Wastewater and water treatment plant design, equipment manufacture and commissioning. Yixing, Jiangsu, China.</p>
        <p class="slogan" style="margin-top:14px;font-size:11.5px">Clean Water for a Sustainable Future</p>
      </div>
      <div><b>Products</b><ul>
        <li><a href="{p}products/screw-press.html">Screw Press</a></li>
        <li><a href="{p}products/crushing-grille.html">Crushing Grille</a></li>
        <li><a href="{p}products/mbr.html">MBR Membrane</a></li>
        <li><a href="{p}products.html">All products</a></li>
      </ul></div>
      <div><b>Solutions</b><ul>
        <li><a href="{p}solutions.html">Dyeing &amp; Textile</a></li>
        <li><a href="{p}solutions.html">Tannery</a></li>
        <li><a href="{p}solutions.html">Electroplating</a></li>
        <li><a href="{p}solutions.html">Municipal</a></li>
      </ul></div>
      <div><b>Company</b><ul>
        <li><a href="{p}projects.html">Projects</a></li>
        <li><a href="{p}oem.html">OEM Partnership</a></li>
        <li><a href="{p}about.html">About us</a></li>
        <li><a href="{p}contact.html">Contact</a></li>
      </ul></div>
    </div>
    <div class="f-bottom">
      <span>&copy; 2026 WuXi KingDao Environmental Technology Co., Ltd. All rights reserved.</span>
      <span>www.kingdaotech.com</span>
    </div>
  </div>
</footer>
<a class="wa" href="https://wa.me/8615906158868" target="_blank" rel="noopener">
  <svg viewBox="0 0 24 24"><path d="M17.5 14.4c-.3-.2-1.7-.9-2-1-.3-.1-.5-.2-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6.1-.1.3-.4.5-.6.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.2-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3 2.9 1.2 2.9.8 3.4.7.5 0 1.7-.7 1.9-1.3.2-.6.2-1.2.2-1.3-.1-.2-.3-.3-.6-.4zM12 2a10 10 0 00-8.5 15.3L2 22l4.8-1.4A10 10 0 1012 2zm0 18.2c-1.6 0-3.2-.4-4.5-1.2l-.3-.2-3.2.9.9-3.1-.2-.3A8.2 8.2 0 1112 20.2z"/></svg>
  WhatsApp
</a>
</body>
</html>
"""

def hero(eyebrow, h1, sub, crumb=""):
    c = f'<div class="crumb">{crumb}</div>' if crumb else ""
    return f"""
<div class="page-hero"><div class="wrap">{c}
  <div class="eyebrow">{eyebrow}</div>
  <h1>{h1}</h1>
  <p>{sub}</p>
</div></div>
"""

def write(path, content):
    fp = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(content)
    print("  wrote", path, len(content), "bytes")

# ══════════════════════════════════════════════════════════
# PRODUCTS
# ══════════════════════════════════════════════════════════
GROUPS = [
 ("Pre-treatment — screening and comminution", "The stages that protect every pump and every membrane downstream.", [
   ("PG Tubular Crushing Grille", "Inline macerator. 21 models, DN50–DN400, 40–300 m³/h.", "products/crushing-grille.html"),
   ("PZG / PZGD Rotary Drum Crushing Grille", "Open channel. Single motor (PZG1/PZG2) and multi-motor (PZGD), 250–6,900 m³/h.", "products/crushing-grille.html"),
   ("Mechanical Bar Screen", "Raked bar screen for coarse and fine screening in channels.", "products/mechanical-bar-screen.html"),
   ("Mechanical Fine Bar Screen (hydraulic)", "Hydraulic-driven fine screen for high screenings load.", "products/fine-bar-screen.html"),
   ("Rotary Drum Screen", "Fine screening for municipal and industrial inflow.", "products/rotary-drum-screen.html"),
   ("Screw Screen", "Screening with integrated compaction and conveying.", "products/screw-screen.html"),
   ("Coarse & Manual Bar Screen", "Entry-level screening for small stations and retrofits.", "products/coarse-manual-screen.html"),
 ]),
 ("Sludge treatment — dewatering and handling", "Our core line. Where most plants lose money if the wrong machine is chosen.", [
   ("Multi-disc Screw Press", "14 selection models, 6–600 kg DS/h. Runs unattended.", "products/screw-press.html"),
   ("DM Dewatering Machine", "Plate and frame dewatering for high-dryness cake.", "products/dm-dewatering.html"),
   ("Sludge Drying Device (PID)", "Further volume reduction after mechanical dewatering.", "products/sludge-dryer.html"),
   ("Sludge Scraper", "Circular and rectangular tank sludge collection.", "products/sludge-scraper.html"),
   ("Screw Conveyor", "Transport of dewatered cake and screenings.", "products/screw-conveyor.html"),
   ("Screw Pump", "Sludge and high-solids transfer, low shear.", "products/screw-pump.html"),
 ]),
 ("Biological treatment — aeration, mixing, media", "The biology only works if the mixing and oxygen are right.", [
   ("Aerators & Air Diffusers", "Disc and tubular fine-bubble diffusers; surface aerators.", "products/aerators.html"),
   ("Submersible Mixers & Agitators", "Draft-tube and high-speed mixers for anoxic and equalisation tanks.", "products/mixers.html"),
   ("Curtain MBR Membrane", "Reinforced hollow-fibre modules with aeration frame.", "products/mbr.html"),
   ("Fillers (elastic / rope)", "Bio-media for MBBR and fixed-film stages.", "products/fillers.html"),
   ("MBBR Media", "Moving bed biofilm reactor carriers.", "products/mbbr.html"),
 ]),
 ("Tertiary treatment — polishing and disinfection", "Meeting the discharge standard is usually decided at the last stage.", [
   ("Dissolved Air Flotation (DAF)", "Oil, grease and light suspended solids removal.", "products/daf.html"),
   ("Sand Filter", "Multi-media filtration for suspended solids polishing.", "products/sand-filter.html"),
   ("UV Sterilizer", "Final disinfection without chemical residual.", "products/uv.html"),
 ]),
 ("Dosing, pumping and packaged plants", "The equipment that makes a plant a whole package instead of a list.", [
   ("Automatic Dosing Devices", "PAC and polymer preparation, fully or semi-automatic.", "products/dosing.html"),
   ("Submersible Pumps", "Sewage, sludge and clean water; cutter options.", "products/submersible-pumps.html"),
   ("FRP Prefabricated Pumping Station", "Factory-built station with integrated crushing grille.", "products/frp-pumping-station.html"),
   ("Small Integrated Sewage Treatment Plant", "Skid and container units, 5–200 m³/d.", "products/small-integrated-stp.html"),
 ]),
]

def build_products():
    blocks = ""
    for title, lead, items in GROUPS:
        cards = ""
        for name, desc, link in items:
            tag = '<span class="tagline">Detail page</span>' if link else ""
            href = link if link else "contact.html"
            cards += f"""
      <a class="prod" href="{href}">
        <h3>{name}{tag}</h3>
        <p>{desc}</p>
      </a>"""
        blocks += f"""
<section>
  <div class="wrap">
    <div class="sec-head"><div class="eyebrow">{title.split('—')[0].strip()}</div>
      <h2>{title}</h2><p class="lead">{lead}</p></div>
    <div class="prod-grid">{cards}</div>
  </div>
</section>"""

    body = head("Products — Wastewater Treatment Equipment | KINGDAO TECH",
                "Screening and comminution, sludge dewatering, biological treatment, tertiary polishing, dosing and packaged plants. Manufactured at our Yixing factory.", 0, "products.html")
    body += hero("Products", "Twenty-five equipment lines, supplied and supported by one team.",
                 "We list them all here for completeness. In a quotation we will only put forward the few lines that actually fit your project — that is how a manufacturer should quote.",
                 '<a href="index.html">Home</a> / Products')
    body += blocks
    body += f"""
<section class="soft"><div class="wrap"><div class="cta-band">
  <div><h2>Not sure which line your project needs?</h2>
  <p>Send us the flow rate, the wastewater type and the discharge standard. We will tell you which stages are required — and which are not.</p></div>
  <a class="btn" href="contact.html">Ask an Engineer</a>
</div></div></section>
"""
    body += foot(0)
    write("products.html", body)

# ══════════════════════════════════════════════════════════
# PROJECTS
# ══════════════════════════════════════════════════════════
PROJ_DATA = [('Municipal wastewater', '市政污水', [('Xinzheng Longhu West WWTP', 'China', '100,000 m³/d (50,000 m³/d first stage)', 'Municipal sewage; staged construction for a growing district'), ('Xingyang No.3 WWTP (expansion)', 'China', '50,000 m³/d', 'Modified Bardenpho + high-density clarifier + fibre disc filter'), ('Sihanoukville Special Economic Zone WWTP', 'Cambodia', '15,000 m³/d', 'Domestic sewage; effluent CODcr ≤80 mg/L to GB18918-2002'), ('Juncheng Town WWTP and sewerage, Tangxian', 'China', '3,000 m³/d (1,500 built, 3,000 ultimate)', 'Inverted AAO; plate-and-frame sludge dewatering'), ('Nanpuxi Town wastewater project', 'China', '2,200 m³/d (600 existing + 1,600 extension)', 'Class 1A plus Zhejiang DB33/2169-2018; 1,225 m² constructed wetland')]), ('Tannery and leather', '制革皮革', [('Dhaka Tannery Estate wastewater project', 'Bangladesh', '20,000 m³/d', 'Chromium, high salinity, high sulphide and ammonia; combined A+B oxidation ditch')]), ('Textile, dyeing and printing', '印染纺织', [('Shanquan dyeing wastewater plant', 'China', '35,000 m³/d, 50% reuse (70% ultimate)', 'High colour, high salinity, PVA desizing and alkali weight-reduction water'), ('Vietnam industrial park wastewater project', 'Vietnam', '1,900 m³/d combined + 400 m³/d plating', 'Dyeing, resin buttons, electroless plating and electroplating, segregated at source')]), ('PCB and electronics', '线路板与电子', [('Suichuan Industrial Park Phase I WWTP (expansion)', 'China', '20,000 m³/d (10,000 built, 20,000 ultimate)', 'Copper, nickel and cyanide; DAF + Fenton + hydrolysis-acidification + Bardenpho'), ('Suichuan Industrial Park Phase II WWTP', 'China', '30,000 m³/d ultimate (10,000 first stage)', 'PCB, silicon materials, light textile, food processing and machinery in one park')]), ('Slaughterhouse', '畜禽屠宰', [('Changshu Food slaughter and processing relocation project', 'China', '1,200 t/d (peak 60 t/h)', 'High oil, high blood content and high COD; B/C ratio 0.4–0.5'), ('Zhangjiagang Gangcheng livestock slaughter, Phase I', 'China', '700 t/d (830–1,200 head/day)', 'Includes high-strength barn washing water')]), ('Livestock farming', '畜禽养殖', [('Sansheng Township pig farm, Tianmenya', 'China', '280 m³/d', 'High organics, high suspended solids, high ammonia'), ('Xinpu Town pig farm, Qianjin', 'China', '250 m³/d', 'Same process family')]), ('Down and feather processing', '羽绒加工', [("Lu'an Guzhen Town WWTP, Phase II", 'China', '20,000 m³/d total (10,000 Phase II)', 'Down processing plus domestic sewage from 20+ factories in the park')]), ('Water reuse', '再生水回用', [('Karamay Baijiantan reuse project', 'China', '30,000 m³/d ultimate (20,000 first stage)', 'Industrial and landscape reuse, staged by quality tier')]), ('Water supply treatment', '供水处理', [('Nanzhao No.2 waterworks', 'China', '50,000 m³/d', 'Inclined plate settling + V-filter + immersed ultrafiltration; turbidity <0.1 NTU')]), ('River and waterbody rehabilitation', '河道水体治理', [('Puyuan Road river water quality restoration', 'China', '300 m³/d packaged plant', 'AO fixed bed; grit separation, phosphorus removal, enhanced oxidation')])]

FLAGSHIP = [
 ("Cambodia · Municipal", "Sihanoukville Special Economic Zone WWTP", "15,000 m³/d",
  "Domestic sewage for the zone. Effluent CODcr held below 80 mg/L to GB18918-2002."),
 ("Bangladesh · Tannery", "Dhaka Tannery Estate Wastewater Project", "20,000 m³/d",
  "Chrome, high salinity, high sulphide and high ammonia. Combined A+B oxidation ditch with segregated pre-treatment."),
 ("Vietnam · Industrial Park", "Vietnam Industrial Park Wastewater Project", "1,900 + 400 m³/d",
  "Four segregated streams — dyeing, resin buttons, chemical plating and electroplating — with combined biological treatment."),
 ("China · Dyeing", "Shanquan Dyeing Wastewater Plant", "35,000 m³/d",
  "High colour, high salinity, poor biodegradability, PVA desizing water. 50% reuse, expandable to 70%."),
]

TABLE = [
 ("1", "Juncheng Town WWTP, Tangxian", "Municipal", "1,500 / 3,000 m³/d (near/far term)", "Inverted AAO; plate-and-frame sludge dewatering"),
 ("2", "Nanpuxi Town Wastewater Project", "Municipal", "2,200 m³/d", "Class 1A + Zhejiang DB33/2169-2018; constructed wetland 1,225 m²"),
 ("4", "Xingyang No.3 WWTP (expansion)", "Municipal", "50,000 m³/d", "Modified Bardenpho + high-density clarifier + fibre disc filter"),
 ("5", "Sihanoukville SEZ WWTP, Cambodia", "Municipal", "15,000 m³/d", "CODcr ≤80 mg/L"),
 ("8", "Xinpu Town Pig Farm, Qianjin", "Livestock", "250 m³/d", "High organics, high SS, high ammonia"),
 ("9", "Sansheng Township Pig Farm", "Livestock", "280 m³/d", "Same process family"),
 ("10", "Puyuan Road River Rehabilitation", "River", "300 m³/d packaged", "AO fixed bed; grit separation, phosphorus removal, enhanced oxidation"),
 ("11", "Suichuan Industrial Park Phase I (expansion)", "PCB", "10,000 → 20,000 m³/d", "Copper, nickel, cyanide; DAF + Fenton + hydrolysis + Bardenpho"),
 ("12", "Suichuan Industrial Park Phase II", "Mixed industrial", "10,000 / 30,000 m³/d", "PCB + silicon + light textile + food + machinery"),
 ("13", "Dhaka Tannery Estate, Bangladesh", "Tannery", "20,000 m³/d", "Chrome / salinity / sulphide; A+B oxidation ditch"),
 ("14", "Shanquan Dyeing WWTP", "Dyeing", "35,000 m³/d, 50% reuse", "PVA desizing, alkali weight reduction, high colour"),
 ("15", "Lu'an Guzhen Town WWTP Phase II", "Down & feather", "10,000 (20,000 total) m³/d", "Down processing + domestic sewage, 20+ factories in the park"),
 ("16", "Karamay Baijiantan Reuse Project", "Reuse", "20,000 / 30,000 m³/d", "Industrial and landscape reuse"),
 ("17", "Nanzhao No.2 Waterworks", "Water supply", "50,000 m³/d", "Inclined plate + V-filter + immersed UF; turbidity <0.1 NTU"),
 ("18", "Vietnam Industrial Park, Vietnam", "Industrial park", "1,900 + 400 m³/d", "Dyeing / resin buttons / chemical plating / electroplating, segregated"),
]

def build_projects():
    # 旗舰卡片（按规模/代表性挑 4 个）
    flagship = [
        ("Cambodia · Municipal", "Sihanoukville Special Economic Zone WWTP", "15,000 m³/d",
         "Domestic sewage for the zone; effluent CODcr held below 80 mg/L to GB18918-2002."),
        ("Bangladesh · Tannery", "Dhaka Tannery Estate", "20,000 m³/d",
         "Chromium, high salinity, sulphide and ammonia; combined A+B oxidation ditch with segregated pre-treatment."),
        ("China · Dyeing", "Shanquan Dyeing Wastewater Plant", "35,000 m³/d",
         "High colour, high salinity, PVA desizing water; 50% reuse, 70% ultimate."),
        ("China · Municipal", "Xingyang No.3 WWTP (expansion)", "50,000 m³/d",
         "Modified Bardenpho + high-density clarifier + fibre disc filter."),
    ]
    cards = ""
    for tag, name, cap, desc in flagship:
        cards += f"""
      <article class="proj"><div class="cap">
        <span class="tag">{tag}</span>
        <div class="cap-num">{cap}</div>
        <h3>{name}</h3><p>{desc}</p>
      </div></article>"""

    # 按污水类型分组
    groups = ""
    for en, cn, rows in PROJ_DATA:
        trs = "".join(
            "<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td></tr>" % (n, c, cap, p)
            for n, c, cap, p in rows)
        groups += f"""
  <div style="margin-bottom:38px">
    <h3 style="font-size:19px;color:var(--navy);margin-bottom:4px">{en} <span style="font-size:13px;color:var(--muted);font-weight:500">· {cn}</span></h3>
    <div class="spec-wrap" style="margin-top:12px"><table class="spec proj-table">
      <thead><tr><th>Project</th><th>Country</th><th>Capacity</th><th>Process route</th></tr></thead>
      <tbody>{trs}</tbody>
    </table></div>
  </div>"""

    body = head("Projects — Design Track Record by Wastewater Type | KINGDAO TECH",
                "18 design references grouped by wastewater type: municipal, tannery, dyeing, PCB, slaughter, livestock, down processing, water reuse, water supply and river rehabilitation — 250 to 50,000 m³/d.",
                0, "projects.html")
    body += hero("Design Track Record", "Plants we designed, by wastewater type.",
                 "Grouped by the kind of wastewater, largest first within each group. Client names and capacities are public; contract values are not.",
                 '<a href="index.html">Home</a> / Projects')
    body += f"""
<section><div class="wrap">
  <div class="sec-head"><div class="eyebrow">Flagship references</div>
    <h2>Four that carry the most weight.</h2></div>
  <div class="proj-grid">{cards}</div>
</div></section>

<section class="soft"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">All references by wastewater type</div>
    <h2>Ten wastewater types, eighteen projects.</h2>
    <p class="lead">Each project was delivered as process design and technical consulting. Site photographs are being added progressively.</p></div>
{groups}
  <p class="note">Full technical portfolio with process descriptions and reference letters is available on request. Contract values and commercial terms are not published.</p>
</div></section>

<section><div class="wrap"><div class="cta-band">
  <div><h2>Want the design portfolio as a PDF?</h2>
  <p>Industry by industry, with process routes, standards applied and capacities — useful when you need to show a client the technical backing behind your bid.</p></div>
  <a class="btn" href="contact.html">Request the Portfolio</a>
</div></div></section>
"""
    body += foot(0)
    write("projects.html", body)


# ══════════════════════════════════════════════════════════
# SOLUTIONS
# ══════════════════════════════════════════════════════════
SOL_NEW = [('Municipal wastewater', '市政污水', 'Nitrogen and phosphorus limits, seasonal load variation, and a discharge permit that does not move.', 'Inverted AAO or modified Bardenpho → high-density clarifier → filtration → disinfection.', '50,000 m³/d Xingyang · 15,000 m³/d Sihanoukville SEZ · 100,000 m³/d Xinzheng Longhu (staged)'), ('Tannery and leather', '制革皮革', 'Chromium, sulphide, high salinity and high ammonia — the four that break a conventional plant.', 'Chrome and sulphide separated at source → equalisation → coagulation-sedimentation → A+B oxidation ditch.', '20,000 m³/d Dhaka Tannery Estate, Bangladesh'), ('Textile, dyeing and printing', '印染纺织', 'High colour, high salinity, PVA desizing water and poor biodegradability.', 'Segregated desizing and dyeing streams → coagulation/DAF → hydrolysis-acidification → AAO → reuse at 50%.', '35,000 m³/d Shanquan (50% reuse) · Vietnam industrial park'), ('PCB and electronics', '线路板与电子', 'Copper, nickel, cyanide and chelated metals across several process lines.', 'Stream segregation → chemical reduction and precipitation per stream → DAF + Fenton → aerobic biological polishing.', '20,000 m³/d Suichuan Phase I · 30,000 m³/d Phase II'), ('Electroplating', '电镀', 'Chelated metals that will not precipitate with simple lime dosing.', 'Batch segregation by metal → reduction/precipitation → ion exchange or membrane concentration where recovery is required.', 'Vietnam industrial park · 400 m³/d mixed plating stream'), ('Slaughterhouse', '畜禽屠宰', 'High oil, high blood content, high COD and a B/C ratio that fluctuates with the kill schedule.', 'Grease separation → equalisation → anoxic-aerobic → dewatering.', '1,200 t/d Changshu · 700 t/d Zhangjiagang'), ('Livestock farming', '畜禽养殖', 'High ammonia, high suspended solids, strong odour, and a site that is often far from any sewer.', 'Solid-liquid separation → anaerobic digestion (optional) → A/O → polishing.', '280 m³/d Sansheng · 250 m³/d Xinpu'), ('Down and feather processing', '羽绒加工', 'Feather, fine solids and surfactant load from washing lines, mixed with park domestic sewage.', 'Screening and grit removal → equalisation → coagulation → biological treatment → dewatering.', "20,000 m³/d Lu'an Guzhen (20+ factories in one park)"), ('Water reuse', '再生水回用', 'A reuse target that has to be met every day, not on average.', 'Biological treatment → membrane or filtration → disinfection; staged by quality tier so industrial and landscape demand are served separately.', '30,000 m³/d Karamay Baijiantan · 50% reuse at Shanquan'), ('Water supply treatment', '供水处理', 'Seasonal turbidity spikes and a turbidity limit below what conventional filtration reliably holds.', 'Inclined plate settling → V-filter → immersed ultrafiltration.', '50,000 m³/d Nanzhao No.2 waterworks; turbidity <0.1 NTU'), ('River and waterbody rehabilitation', '河道水体治理', 'Diffuse pollution, low dissolved oxygen and no space for a conventional plant.', 'Packaged AO fixed-bed units with grit separation, phosphorus removal and enhanced oxidation.', '300 m³/d Puyuan Road river restoration'), ('Industrial park and SEZ', '工业园区与特区', 'Mixed tenants, mixed streams, one discharge permit — and a drainage tariff that has to recover the investment.', 'Stream segregation by tenant type → shared biological train → reuse where justified; plant sized against the tariff model.', 'Sihanoukville SEZ (Cambodia) · Suichuan Industrial Park · Vietnam industrial park')]

SOLS = [
 ("Dyeing &amp; Textile", "Colour, high salinity, PVA desizing water, poor biodegradability.",
  "Segregated desizing and dyeing streams → coagulation/DAF → hydrolysis-acidification → AAO → reuse at 50%.", "35,000 m³/d reference"),
 ("Tannery &amp; Leather", "Chrome, sulphide, high salinity, high ammonia.",
  "Chrome and sulphide separated at source → equalisation → coagulation-sedimentation → A+B oxidation ditch.", "20,000 m³/d reference"),
 ("Electroplating &amp; PCB", "Copper, nickel, cyanide, chelated metals.",
  "Four-stream segregation → chemical reduction and precipitation per stream → DAF + Fenton → aerobic biological polishing.", "20,000 m³/d reference"),
 ("Food, Beverage &amp; Slaughter", "High organic load, FOG, variable flow.",
  "Grease separation → equalisation → anaerobic or anoxic-aerobic → dewatering.", "700–1,200 t/d references"),
 ("Livestock &amp; Aquaculture", "High ammonia, high SS, strong odour.",
  "Solid-liquid separation → anaerobic digestion (optional) → A/O → polishing.", "250–280 m³/d references"),
 ("Municipal &amp; Estate", "Nitrogen and phosphorus limits, seasonal load variation.",
  "Inverted AAO or modified Bardenpho → high-density clarifier → filtration → disinfection.", "up to 50,000 m³/d"),
 ("Industrial Park &amp; SEZ", "Mixed tenants, mixed streams, one discharge permit.",
  "Stream segregation by tenant type → shared biological train → reuse where justified; charged against a drainage tariff model.", "Cambodia SEZ, Vietnam IP references"),
]

def build_solutions():
    cards = "".join(f"""
      <div class="sol"><span class="n">{i+1:02d}</span><b>{en} <span style="font-size:12px;color:var(--muted);font-weight:500">· {cn}</span></b>
      <span style="display:block;margin-bottom:8px"><strong style="color:var(--navy);font-size:13px">Challenge:</strong> {ch}</span>
      <span style="display:block;margin-bottom:8px"><strong style="color:var(--navy);font-size:13px">Typical route:</strong> {rt}</span>
      <span style="font-size:12.5px;color:var(--teal);font-weight:650">{ref}</span></div>"""
        for i, (en, cn, ch, rt, ref) in enumerate(SOL_NEW))

    body = head("Solutions by Wastewater Type | KINGDAO TECH",
                "Process routes for municipal, tannery, dyeing, PCB, electroplating, slaughterhouse, livestock, down processing, reuse, water supply, river rehabilitation and industrial park projects.",
                0, "solutions.html")
    body += hero("Solutions by Wastewater Type", "The wastewater decides the process — not the machine we want to sell.",
                 "Twelve wastewater types we have designed plants for. Each one has a route behind it, and a reference you can check.",
                 '<a href="index.html">Home</a> / Solutions')
    body += f"""
<section><div class="wrap"><div class="sol-grid">{cards}</div></div></section>

<section class="soft"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">How we work</div>
    <h2>Four steps, and you know whether we can help by step three.</h2></div>
  <div class="why-grid">
    <div class="why"><b>1 · Wastewater characterisation</b><p>Your flow, the pollutant load, the discharge standard. We start from data, not from a catalogue.</p></div>
    <div class="why"><b>2 · Process route</b><p>Mass balance and the process train, with the stages each option requires.</p></div>
    <div class="why"><b>3 · Equipment selection</b><p>Models sized against your actual load, with drawings you can build from.</p></div>
    <div class="why"><b>4 · Supply and commissioning</b><p>Equipment to specification, then start-up and operator training on site.</p></div>
  </div>
</div></section>

<section><div class="wrap"><div class="cta-band">
  <div><h2>Send us your effluent data.</h2>
  <p>Flow rate, wastewater type, discharge standard and country. You will get a process opinion — not a price list.</p></div>
  <a class="btn" href="contact.html">Start with Your Data</a>
</div></div></section>
"""
    body += foot(0)
    write("solutions.html", body)


# ══════════════════════════════════════════════════════════
# ABOUT
# ══════════════════════════════════════════════════════════
def build_about():
    body = head("About KINGDAO — Wastewater Treatment Manufacturer, Yixing China",
                "WuXi KingDao Environmental Technology Co., Ltd. Water treatment equipment manufacturer and process design house in Yixing, Jiangsu, with 18 design references from 250 to 50,000 m³/d.",
                0, "about.html")
    body += hero("About KINGDAO", "A factory in Yixing, and an engineering team that designs what the factory builds.",
                 "We design the plant and we supply the equipment inside it — the core lines built in our own plant in Yixing, the wider catalogue produced to our drawings and specification. The process design and the equipment come from the same team.",
                 '<a href="index.html">Home</a> / About')
    body += """
<section><div class="wrap two-col">
  <div class="prose">
    <h3>What we do</h3>
    <p>WuXi KingDao Environmental Technology Co., Ltd. designs wastewater and water treatment plants and supplies the equipment that goes into them. Our plant in Yixing, Jiangsu covers the core lines — screening and comminution, sludge dewatering, biological treatment, tertiary polishing, dosing and packaged plants — and across the wider catalogue we supply to our own drawings and specification.</p>
    <p>Because the design team and the factory sit in the same company, a customer deals with one technical party from the first mass balance to the start-up report. That is unusual in this industry, where equipment is normally bought from one supplier and the process design from another.</p>
    <h3>Where we work</h3>
    <p>Our reference projects are in China, Cambodia, Bangladesh and Vietnam — municipal plants, tanneries, dyeing and textile parks, PCB and electroplating parks, food processing, livestock and water reuse. Capacities range from 250 m³/d packaged units to 50,000 m³/d municipal works.</p>
    <p>For overseas projects we work as an equipment manufacturer and process design partner behind EPC contractors, system integrators and industrial park developers. We supply under your own brand when that is what the market requires.</p>
    <h3>How we quote</h3>
    <p>A quotation lists only the lines that fit the project. We would rather quote four items that are right than twenty that make the page look complete. Motors are supplied to destination standard — 380/415 V 50 Hz for Thailand, Vietnam, Malaysia, Indonesia and Cambodia, 440 V 60 Hz for the Philippines.</p>
  </div>
  <div>
    <div class="kv">
      <div><b>Founded</b><span>Yixing, Jiangsu, China</span></div>
      <div><b>Manufacturing</b><span>Own plant in Yixing for the core lines; wider catalogue to our specification — 304 stainless steel wetted parts</span></div>
      <div><b>Design references</b><span>18 projects, 11 industries, 250 to 50,000 m³/d</span></div>
      <div><b>Overseas references</b><span>Cambodia (SEZ 15,000 m³/d), Bangladesh (tannery 20,000 m³/d), Vietnam (industrial park)</span></div>
      <div><b>Business contact</b><span>Zhu Rongtao · Business Manager<br>Wang Wenli · Director<br>+86 159 0615 8868 / +86 159 0615 6262</span></div>
      <div><b>Address</b><span>No. 59, Xijiu Avenue, Innovation and Entrepreneurship Park, Environmental Protection Technology Industrial Park, Xinjie Street, Yixing, Jiangsu, China</span></div>
    </div>
    <div style="margin-top:24px;padding:20px;background:var(--bg-soft);border-radius:12px;font-size:13.5px;color:var(--muted)">
      <strong style="color:var(--navy);display:block;margin-bottom:8px">Factory visits and audits</strong>
      We welcome factory visits and third-party inspection before shipment. Inspection reports, material certificates and test records can be issued with the equipment.
    </div>
  </div>
</div></section>

<section class="soft"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">Capability</div><h2>Three capabilities, one supplier.</h2></div>
  <div class="why-grid">
    <div class="why"><b>Process design</b><p>Mass balance, process route, P&amp;ID, general arrangement and equipment selection — issued as drawings your contractors can build from.</p></div>
    <div class="why"><b>Equipment manufacture</b><p>25 lines built at our own plant, with branded motors and reducers, available OEM under your label.</p></div>
    <div class="why"><b>Commissioning</b><p>Start-up, sludge seeding, optimisation and operator training until the effluent meets the discharge standard.</p></div>
    <div class="why"><b>Spare parts</b><p>Screw shafts, rings, bearings and drive units from the manufacturer that built the machine.</p></div>
  </div>
</div></section>
"""
    body += foot(0)
    write("about.html", body)

# ══════════════════════════════════════════════════════════
# OEM
# ══════════════════════════════════════════════════════════
def build_oem():
    body = head("OEM & Partnership — Manufacturing for Equipment Suppliers | KINGDAO TECH",
                "OEM manufacturing for water treatment equipment suppliers and EPC contractors: your brand, our factory, factory pricing, stable lead times, with process design and commissioning support.", 0, "oem.html")
    body += hero("OEM &amp; Partnership", "Your brand. Our factory. Your projects get stronger.",
                 "Our role is to add capacity behind yours — the equipment you do not build, the process design your team can lean on, and commissioning support at the far end.",
                 '<a href="index.html">Home</a> / OEM &amp; Partnership')
    body += """
<section><div class="wrap two-col">
  <div class="prose">
    <h3>Who this is for</h3>
    <ul>
      <li><strong>Equipment suppliers and distributors</strong> who want to extend their range without carrying stock or funding tooling.</li>
      <li><strong>EPC contractors</strong> whose projects need stages outside their usual scope — dewatering, dosing, screening, aeration.</li>
      <li><strong>System integrators</strong> who need a second, factory-direct supply source when a project timeline is tight.</li>
    </ul>
    <h3>What we supply</h3>
    <p>Any of our 25 equipment lines, built to your specification and labelled with your brand. Typical OEM scope: multi-disc screw presses, crushing grilles, bar screens, dosing systems, aerators, mixers, MBR modules and packaged plants.</p>
    <h3>What comes with it</h3>
    <ul>
      <li>Factory pricing with stable lead times, quoted against your order pattern</li>
      <li>English documentation: GA drawings, IOM manuals, material certificates, test records</li>
      <li>Process calculations and equipment selection when a client's wastewater falls outside your usual range</li>
      <li>Commissioning support, or remote guidance for your own service team</li>
      <li>Motor supply to destination standard — 380/415 V 50 Hz, or 440 V 60 Hz for the Philippines</li>
    </ul>
    <h3>What we ask</h3>
    <p>An honest indication of the volumes you expect, and whether you want neutral supply or your own branding. That is enough to quote properly.</p>
  </div>
  <div>
    <div class="kv">
      <div><b>Branding</b><span>Your label, nameplate, manual and packaging — or neutral supply</span></div>
      <div><b>Documentation</b><span>English GA drawings, IOM, material and test certificates</span></div>
      <div><b>Quality</b><span>304 stainless steel wetted parts; branded motors and reducers</span></div>
      <div><b>Inspection</b><span>Third-party pre-shipment inspection welcome</span></div>
      <div><b>Lead time</b><span>Confirmed per model and quantity — typically 30 days after deposit for standard units</span></div>
    </div>
    <div style="margin-top:24px"><a class="btn btn-primary" href="contact.html">Discuss an OEM Partnership</a></div>
  </div>
</div></section>

<section class="soft"><div class="wrap"><div class="cta-band">
  <div><h2>Tell us what your projects keep asking for and we do not make.</h2>
  <p>Send the item, the size and the annual volume. We will tell you plainly whether it is something we can manufacture — and if it is not, we will say so.</p></div>
  <a class="btn" href="contact.html">Start the Conversation</a>
</div></div></section>
"""
    body += foot(0)
    write("oem.html", body)

# ══════════════════════════════════════════════════════════
# CONTACT
# ══════════════════════════════════════════════════════════
def build_contact():
    body = head("Contact — Request a Technical Proposal | KINGDAO TECH",
                "Contact KINGDAO TECH: WhatsApp +86 159 0615 8868, email zhu.rongtao@kingdaotech.com. Factory in Yixing, Jiangsu, China.", 0, "contact.html")
    body += hero("Contact", "Tell us the effluent. We will tell you the process.",
                 "Flow rate, wastewater type, discharge standard and country. You will get a technical reply from an engineer, not a sales brochure.",
                 '<a href="index.html">Home</a> / Contact')
    body += """
<section class="soft"><div class="wrap contact">
  <div>
    <div class="eyebrow">Direct contact</div>
    <h2 style="margin:12px 0 14px">Fastest route is WhatsApp.</h2>
    <p class="lead">Most of our overseas customers work through WhatsApp. Send a photo of the site or the drawing and we will answer the same day.</p>
    <div class="info">
      <div class="ci"><div><div class="k">Business Manager</div><div class="v">Zhu Rongtao · 朱荣涛<br>WhatsApp/WeChat: <a href="https://wa.me/8615906158868" style="color:var(--teal)">+86 159 0615 8868</a><br><a href="mailto:zhu.rongtao@kingdaotech.com" style="color:var(--teal)">zhu.rongtao@kingdaotech.com</a></div></div></div>
      <div class="ci"><div><div class="k">Director</div><div class="v">Wang Wenli · 汪文丽<br>WhatsApp/WeChat: <a href="https://wa.me/8615906156262" style="color:var(--teal)">+86 159 0615 6262</a><br><a href="mailto:wang.wenli@kingdaotech.com" style="color:var(--teal)">wang.wenli@kingdaotech.com</a></div></div></div>
      <div class="ci"><div><div class="k">Factory</div><div class="v">No. 59, Xijiu Avenue, Innovation and Entrepreneurship Park, Environmental Protection Technology Industrial Park, Xinjie Street, Yixing, Jiangsu, China</div></div></div>
    </div>
  </div>
  <form onsubmit="event.preventDefault(); this.querySelector('[type=submit]').textContent='Sending...'; setTimeout(()=>{this.querySelector('[type=submit]').textContent='Sent - we reply within 1 working day';},900);">
    <div><label>Your name *</label><input required placeholder="Name / position"></div>
    <div><label>Company *</label><input required placeholder="Company name"></div>
    <div class="row2">
      <div><label>Email *</label><input type="email" required placeholder="you@company.com"></div>
      <div><label>WhatsApp</label><input placeholder="+60 ..."></div>
    </div>
    <div><label>What do you need?</label>
      <select>
        <option>Process design / technical proposal</option>
        <option>Equipment quotation (single machine)</option>
        <option>Complete plant package</option>
        <option>OEM / manufacturing partnership</option>
        <option>Spare parts</option>
      </select>
    </div>
    <div><label>Project details</label><textarea placeholder="Flow rate m3/d, wastewater type, discharge standard, country"></textarea></div>
    <button class="btn btn-primary" type="submit">Send Enquiry</button>
  </form>
</div></section>
"""
    body += foot(0)
    write("contact.html", body)

# ══════════════════════════════════════════════════════════
# PRODUCT DETAIL: SCREW PRESS
# ══════════════════════════════════════════════════════════
SP_ROWS = [("131", "6-10", "3", "1.2", "1.0", "0.5", "0.4", "0.2"),
           ("132", "12-20", "6", "2.4", "2.0", "1.0", "0.8", "0.4"),
           ("201", "9-15", "4.5", "1.8", "1.5", "0.75", "0.6", "0.3"),
           ("202", "18-30", "9", "3.6", "3.0", "1.5", "1.2", "0.6"),
           ("251", "20-35", "10", "4.0", "3.5", "1.75", "1.4", "0.7"),
           ("301", "30-50", "15", "6.0", "5.0", "2.5", "2.0", "1.0"),
           ("302", "60-100", "30", "12", "10", "5.0", "4.0", "2.0"),
           ("303", "90-150", "45", "18", "15", "7.5", "6.0", "3.0"),
           ("351", "60-100", "30", "12", "10", "5.0", "4.0", "2.0"),
           ("352", "120-200", "60", "24", "20", "10", "8.0", "4.0"),
           ("401", "90-150", "45", "18", "15", "7.5", "6.0", "3.0"),
           ("402", "180-300", "90", "36", "30", "15", "12", "6.0"),
           ("403", "270-450", "135", "54", "45", "22.5", "18", "9.0"),
           ("404", "360-600", "180", "72", "60", "30", "24", "12")]

def build_screw_press():
    rows = "".join(
        "<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % r
        for r in SP_ROWS)
    body = head("Multi-disc Screw Press — Sludge Dewatering | KINGDAO TECH",
                "Multi-disc screw press for sludge dewatering. 14 models, 6-600 kg DS/h, 304 stainless steel, runs unattended without wash water or filter cloth.",
                1, "products.html")
    body += hero("Sludge dewatering", "Multi-disc Screw Press",
                 "The machine we build most of. 14 selection models from 6 to 600 kg DS/h, 304 stainless steel body and wetted parts, and it runs unattended — no filter cloth, no wash water.",
                 '<a href="../index.html">Home</a> / <a href="../products.html">Products</a> / Screw Press')
    body += f"""
<section><div class="wrap two-col">
  <div class="prose">
    <h3>How it works</h3>
    <p>Sludge is flocculated with polymer and fed into the thickening section, where gravity separates free water through the gaps between the fixed and moving rings. The dewatered sludge is then conveyed and pressed along the screw shaft in the dewatering section, where the gradually decreasing pitch and the outlet resistance build the pressure that squeezes out the remaining water.</p>
    <p>Because the rings are self-cleaning — the moving rings wipe the fixed rings on every revolution — the machine does not blind over the way a belt or plate press does. There is no filter cloth to replace and no wash water to supply.</p>
    <h3>Why it suits overseas projects</h3>
    <ul>
      <li><strong>Unattended operation</strong> — runs 24 h with a single daily check. Suits sites without a permanent operator.</li>
      <li><strong>Low running cost</strong> — around 0.1 kW per kg DS, with polymer as the main consumable.</li>
      <li><strong>No wash water</strong> — important where water supply to the plant is metered or limited.</li>
      <li><strong>Compact footprint</strong> — often a third of a comparable belt press installation.</li>
      <li><strong>Low odour and no spillage</strong> — enclosed dewatering, which matters in residential or food-adjacent sites.</li>
    </ul>
    <h3>Selection</h3>
    <p>Size the machine from the <strong>dry solids load</strong>, not from the sludge flow alone. Daily sludge volume ÷ 24 gives m³/h; read across at your inlet solids concentration; then take the model one step above and leave 20–30% margin.</p>
    <p class="note"><strong>Worked example:</strong> 200 m³/d of sludge at 5,000 mg/L → 8.3 m³/h → model 302 (12 m³/h at 5,000 mg/L) with margin.</p>
  </div>
  <div>
    <img src="../images/plant_aerial.jpg" alt="Wastewater treatment plant" style="border-radius:12px;margin-bottom:18px;opacity:.92">
    <div class="kv">
      <div><b>Capacity</b><span>6 – 600 kg DS/h across 14 models</span></div>
      <div><b>Body &amp; wetted parts</b><span>304 stainless steel</span></div>
      <div><b>Drive</b><span>Branded motor and reducer</span></div>
      <div><b>Cake dryness</b><span>Typically 20–30% DS depending on sludge type and polymer</span></div>
      <div><b>Options</b><span>Polymer preparation unit, feed pump, control cabinet, skid frame</span></div>
    </div>
    <div style="margin-top:22px"><a class="btn btn-primary" href="../contact.html">Request a Selection</a></div>
  </div>
</div></section>

<section class="soft"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">Selection reference</div>
    <h2>Model capacity by inlet solids concentration (m³/h).</h2>
    <p class="lead">At low concentrations the limit is hydraulic; at high concentrations it is the dry solids load. Both are shown, which is why the table reads the way it does.</p></div>
  <div class="spec-wrap"><table class="spec">
    <thead><tr><th>Model</th><th>DS capacity kg/h</th><th>2,000 mg/L</th><th>5,000 mg/L</th><th>10,000 mg/L</th><th>20,000 mg/L</th><th>25,000 mg/L</th><th>50,000 mg/L</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
  <p class="note">Figures are theoretical. Select the model slightly above the calculated value, and confirm against the approved drawing before ordering. Actual capacity depends on sludge characteristics, flocculation and polymer dosing.</p>
</div></section>

<section><div class="wrap"><div class="cta-band">
  <div><h2>Send us the sludge flow and solids content.</h2>
  <p>Two numbers are enough for us to name the model and send the dimension drawing.</p></div>
  <a class="btn" href="../contact.html">Get the Model</a>
</div></div></section>
"""
    body += foot(1)
    write("products/screw-press.html", body)

# ══════════════════════════════════════════════════════════
# PRODUCT DETAIL: CRUSHING GRILLE
# ══════════════════════════════════════════════════════════
PZG1 = [('PZG1-4X4', '250', '400', '1500', '400', '400', '3'), ('PZG1-4X5', '300', '400', '1500', '500', '450', '3'), ('PZG1-5X5', '450', '500', '1600', '500', '450', '3'), ('PZG1-6X5', '540', '600', '1700', '500', '450', '4'), ('PZG1-7X5', '630', '700', '1800', '500', '450', '4'), ('PZG1-8X5', '720', '800', '1900', '500', '450', '4'), ('PZG1-4X6', '430', '400', '1500', '600', '450', '4'), ('PZG1-5X6', '550', '500', '1600', '600', '450', '4'), ('PZG1-6X6', '650', '600', '1700', '600', '450', '4'), ('PZG1-7X6', '760', '700', '1800', '600', '450', '4'), ('PZG1-8X6', '860', '800', '1900', '600', '450', '4'), ('PZG1-9X6', '970', '900', '2000', '600', '450', '4'), ('PZG1-10X6', '1080', '1000', '2100', '600', '450', '4'), ('PZG1-8X8', '1150', '800', '1900', '800', '600', '4'), ('PZG1-10X8', '1440', '1000', '2100', '800', '600', '4'), ('PZG1-12X8', '1700', '1200', '2300', '800', '600', '4')]
PZG2 = [('PZG2-6X7', '1050', '600', '1700', '700', '500', '4'), ('PZG2-6X8', '1200', '600', '1700', '800', '500', '4'), ('PZG2-7X8', '1400', '700', '1800', '800', '500', '4'), ('PZG2-8X8', '1600', '800', '1900', '800', '500', '4'), ('PZG2-9X8', '1800', '900', '2000', '800', '500', '4'), ('PZG2-10X8', '2000', '1000', '2100', '800', '500', '4'), ('PZG2-12X8', '2400', '1200', '2300', '800', '500', '5.5'), ('PZG2-6X10', '1500', '600', '1700', '1000', '580', '4'), ('PZG2-7X10', '1750', '700', '1800', '1000', '580', '4'), ('PZG2-8X10', '2000', '800', '1900', '1000', '580', '4'), ('PZG2-9X10', '2250', '900', '2000', '1000', '580', '4'), ('PZG2-10X10', '2500', '1000', '2100', '1000', '580', '5.5'), ('PZG2-12X10', '3000', '1200', '2300', '1000', '580', '5.5'), ('PZG2-14X10', '3500', '1400', '2500', '1000', '580', '5.5'), ('PZG2-10X12', '3500', '1000', '2100', '1200', '580', '5.5'), ('PZG2-12X12', '4150', '1200', '2300', '1200', '580', '5.5'), ('PZG2-14X12', '4800', '1400', '2500', '1200', '580', '7.5'), ('PZG2-15X12', '5200', '1500', '2600', '1200', '580', '7.5'), ('PZG2-18X12', '6200', '1800', '2900', '1200', '650', '7.5'), ('PZG2-10X14', '4280', '1000', '2100', '1400', '650', '5.5'), ('PZG2-12X14', '5280', '1200', '2300', '1400', '650', '5.5'), ('PZG2-14X14', '6000', '1400', '2500', '1400', '650', '5.5'), ('PZG2-15X14', '6400', '1500', '2600', '1400', '650', '5.5')]

PG_ROWS = [("PG-10-50/50", "40", "DN50", "1.5"), ("PG-10-80/80", "50", "DN80", "1.5"),
           ("PG-10-100/100", "56", "DN100", "1.5"), ("PG-10-150/150", "56", "DN150", "1.5"),
           ("PG-20-50/50", "70", "DN50", "2.2"), ("PG-20-80/80", "80", "DN80", "2.2"),
           ("PG-20-100/100", "90", "DN100", "2.2"), ("PG-20-150/150", "100", "DN150", "2.2"),
           ("PG-20-200/200", "110", "DN200", "2.2"), ("PG-20-250/250", "110", "DN250", "2.2"),
           ("PG-30-100/100", "160", "DN100", "2.2"), ("PG-30-150/150", "170", "DN150", "2.2"),
           ("PG-30-200/200", "180", "DN200", "2.2"), ("PG-30-250/250", "190", "DN250", "2.2"),
           ("PG-30-300/300", "200", "DN300", "2.2"), ("PG-30-350/350", "200", "DN350", "2.2"),
           ("PG-40-200/200", "250", "DN200", "2.2"), ("PG-40-250/250", "270", "DN250", "2.2"),
           ("PG-40-300/300", "280", "DN300", "2.2"), ("PG-40-350/350", "290", "DN350", "2.2"),
           ("PG-40-400/400", "300", "DN400", "2.2")]

PZ1 = [("PZGD1-6X8", "900", "600", "1700", "800", "600", "3 / 1.5"),
       ("PZGD1-8X8", "1200", "800", "1900", "800", "600", "4 / 1.5"),
       ("PZGD1-10X8", "1500", "1000", "2100", "800", "600", "4 / 1.5"),
       ("PZGD1-10X10", "2000", "1000", "2100", "1000", "650", "4 / 1.5"),
       ("PZGD1-12X10", "2500", "1200", "2300", "1000", "650", "4 / 1.5"),
       ("PZGD1-15X10", "3000", "1500", "2500", "1000", "650", "4 / 1.5")]
PZ2 = [("PZGD2-6X12", "2400", "600", "1700", "1200", "580", "3 / 1.5"),
       ("PZGD2-8X12", "3200", "800", "1900", "1200", "580", "4 / 1.5"),
       ("PZGD2-10X12", "4000", "1000", "2100", "1200", "580", "4 / 1.5"),
       ("PZGD2-8X14", "4000", "800", "1900", "1400", "650", "4 / 1.5"),
       ("PZGD2-10X14", "4800", "1000", "2100", "1400", "650", "4 / 1.5"),
       ("PZGD2-12X14", "5500", "1200", "2300", "1400", "650", "4 / 1.5"),
       ("PZGD2-10X16", "5500", "1000", "2100", "1600", "650", "4 / 1.5"),
       ("PZGD2-12X16", "6200", "1200", "2300", "1600", "650", "4 / 1.5"),
       ("PZGD2-15X16", "6900", "1500", "2600", "1600", "650", "4 / 1.5")]

def build_crushing_grille():
    pzg1 = "".join("<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in PZG1)
    pzg2 = "".join("<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in PZG2)
    pg = "".join("<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in PG_ROWS)
    pz1 = "".join("<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in PZ1)
    pz2 = "".join("<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in PZ2)
    body = head("Crushing Grille — Inline and Open Channel Macerators | KINGDAO TECH",
                "PG tubular crushing grille (inline, DN50-DN400, 40-300 m3/h) and PZGD rotary drum crushing grille (open channel, 900-6900 m3/h). Manufactured by KINGDAO TECH, China.",
                1, "products.html")
    body += hero("Pre-treatment · Maceration", "Crushing Grille — inline and open channel",
                 "Four series: PG tubular for pipelines, and three rotary-drum channel series - PZG1 and PZG2 with a single motor, PZGD1 and PZGD2 with independent motors for the heaviest duties.",
                 '<a href="../index.html">Home</a> / <a href="../products.html">Products</a> / Crushing Grille')
    body += f"""
<section><div class="wrap two-col">
  <div class="prose">
    <h3>What it is for</h3>
    <p>A crushing grille — also called a macerator, grinder or comminutor — shreds the solids carried in wastewater into small particles instead of lifting them out. Everything downstream runs better: pumps stop blocking, the filter press stops being damaged by solids, pipelines stop plugging, and there is no raking labour and no screenings to dispose of.</p>
    <h3>Inline — PG series tubular crushing grille</h3>
    <p><strong>Use:</strong> installed in a pipeline, typically ahead of a sludge pump or a filter press, or in a chemical plant where lumps in the liquid have to be broken up to protect pipework and the next item of equipment.</p>
    <p><strong>Installation:</strong> flange connection, JB/T81-94, PN0.25 MPa. Bore and flange size can be customised to the site; 21 models cover DN50 to DN400 and 40 to 300 m³/h.</p>
    <h3>Open channel — PZGD series rotary drum crushing grille</h3>
    <p><strong>Use:</strong> installed directly in the channel, or inside an FRP prefabricated pumping station in place of the basket screen. It replaces the traditional basket screen and cuts the labour of manual raking, while removing the risk of the pump being blocked by screenings carried past it.</p>
    <p><strong>Single or double drum:</strong> the drum is driven by its own motor on the multi-motor design, which lowers the energy consumption of the crushing section and simplifies motor commissioning. Single-drum models cover 900–3,000 m³/h; double-drum covers 2,400–6,900 m³/h.</p>
    <h3>Control and protection</h3>
    <p>Both series can be supplied with an intelligent electric control cabinet. On blockage the unit reverses automatically to clear the obstruction, up to three attempts; if it is still blocked, the cabinet cuts the motor supply and raises a visual or audible alarm. Motor IP55 as standard, IP67/IP68 available (these will run submerged or in air), explosion-proof and high-altitude motors on request. Stainless steel or other blade materials can be specified.</p>
  </div>
  <div>
    <div class="kv">
      <div><b>Inline models</b><span>PG series, 21 models, DN50–DN400, 40–300 m³/h</span></div>
      <div><b>Inline power</b><span>1.5 kW (PG-10 series) / 2.2 kW (PG-20 to PG-40)</span></div>
      <div><b>Channel models</b><span>PZGD1 single drum 900–3,000 m³/h; PZGD2 double drum 2,400–6,900 m³/h</span></div>
      <div><b>Channel power</b><span>Crushing 3–4 kW + drum 1.5 kW (separate motors)</span></div>
      <div><b>Rating basis</b><span>30 ppm screenings, water level at the top of the opening, 1 m/s velocity, 10 mm drum gap</span></div>
      <div><b>Standard</b><span>Flange JB/T81-94, PN0.25 MPa; motor IP55 (IP67/IP68 optional)</span></div>
    </div>
    <div style="margin-top:22px"><a class="btn btn-primary" href="../contact.html">Request a Quotation</a></div>
  </div>
</div></section>

<section class="soft"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">Inline · PG series</div>
    <h2>Tubular crushing grille — model table.</h2>
    <p class="lead">21 models, DN50 to DN400. A = 100/200/300/400 mm and H = 1100/1200/1300/1400 mm by series; B = 360 mm and D = 240 mm across all models.</p></div>
  <div class="spec-wrap"><table class="spec">
    <thead><tr><th>Model</th><th>Capacity m³/h</th><th>Bore (in / out)</th><th>Motor kW</th></tr></thead>
    <tbody>{pg}</tbody>
  </table></div>
  <p class="note">Flange dimensions to JB/T81-94, PN0.25 MPa. Bore and flange sizes can be customised.</p>
</div></section>


<section><div class="wrap">
  <div class="sec-head"><div class="eyebrow">Open channel · PZG series (single motor)</div>
    <h2>Rotary drum crushing grille — single motor.</h2>
    <p class="lead">The economic option. One motor drives the cutter shaft and the drum through a gear train. Fewer components, lower capital cost, simpler maintenance — the right choice for most municipal and industrial channels.</p></div>
  <div class="kv" style="margin-bottom:24px">
    <div><b>PZG1 single drum</b><span>250–1,700 m³/h · 16 models · 3–4 kW · A 400–1,200 mm</span></div>
    <div><b>PZG2 double drum</b><span>1,050–6,400 m³/h · 23 models · 4–7.5 kW · A 600–1,800 mm</span></div>
    <div><b>Model code</b><span>PZG + drum count (1 / 2) + effective blade height × equipment height, e.g. PZG2-12X10</span></div>
  </div>
  <div class="spec-wrap"><table class="spec">
    <thead><tr><th>PZG1 single drum</th><th>Capacity m³/h</th><th>A mm</th><th>H mm</th><th>B mm</th><th>D mm</th><th>Motor kW</th></tr></thead>
    <tbody>{pzg1}</tbody>
  </table></div>
  <div class="spec-wrap" style="margin-top:26px"><table class="spec">
    <thead><tr><th>PZG2 double drum</th><th>Capacity m³/h</th><th>A mm</th><th>H mm</th><th>B mm</th><th>D mm</th><th>Motor kW</th></tr></thead>
    <tbody>{pzg2}</tbody>
  </table></div>
  <p class="note">Rating basis for both: 30 ppm screenings, water level at the upper limit of the grille opening, 1 m/s velocity, 10 mm drum gap. A is the channel/installation width — confirm against the approved drawing before civil works.</p>
</div></section>

<section class="soft"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">Which one to choose</div>
    <h2>Single motor or multi-motor — it is a cost and reliability decision.</h2></div>
  <div class="why-grid">
    <div class="why"><b>PZG · single motor</b><p>One motor, one gearbox, one set of electrical protection. Lower price, fewer parts to keep in stock. Right for normal municipal and industrial screening where the load is predictable.</p></div>
    <div class="why"><b>PZGD · multi-motor</b><p>The drum and the cutter shaft are driven separately, so blade overload and drum overload are monitored independently and the machine can be pushed to higher flows. Right for large pumping stations and heavy screenings load.</p></div>
    <div class="why"><b>Same protection</b><p>Both series can run the intelligent control cabinet: automatic reversal on blockage, up to three attempts, then power cut-off and alarm.</p></div>
    <div class="why"><b>Same options</b><p>IP55 as standard, IP67/IP68 available, explosion-proof motors on request, stainless steel blades on request, bore and flange sizes customised to site.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><div class="eyebrow">Open channel · PZGD1 single drum</div>
    <h2>Rotary drum crushing grille — single drum.</h2></div>
  <div class="spec-wrap"><table class="spec">
    <thead><tr><th>Model</th><th>Capacity m³/h</th><th>A mm</th><th>H mm</th><th>B mm</th><th>D mm</th><th>Crushing / drum kW</th></tr></thead>
    <tbody>{pz1}</tbody>
  </table></div>
  <p class="note">Capacities based on 30 ppm screenings, water level at the top of the opening, 1 m/s velocity and a 10 mm drum gap.</p>
</div></section>

<section class="soft"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">Open channel · PZGD2 double drum</div>
    <h2>Rotary drum crushing grille — double drum.</h2></div>
  <div class="spec-wrap"><table class="spec">
    <thead><tr><th>Model</th><th>Capacity m³/h</th><th>A mm</th><th>H mm</th><th>B mm</th><th>D mm</th><th>Crushing / drum kW</th></tr></thead>
    <tbody>{pz2}</tbody>
  </table></div>
  <p class="note">Same rating basis. A is the channel/installation width; confirm against the approved drawing before civil works.</p>
</div></section>

<section><div class="wrap"><div class="cta-band">
  <div><h2>Inline or channel — tell us the pipe size or the channel width.</h2>
  <p>With the flow rate, the bore or channel dimension and the supply voltage, we can name the model and issue the drawing.</p></div>
  <a class="btn" href="../contact.html">Get the Model</a>
</div></div></section>
"""
    body += foot(1)
    write("products/crushing-grille.html", body)

# ══════════════════════════════════════════════════════════
# PRODUCT DETAIL: MBR
# ══════════════════════════════════════════════════════════
def build_mbr():
    body = head("Curtain MBR Membrane — Hollow Fibre Modules | KINGDAO TECH",
                "Curtain MBR membrane modules with aeration frame for membrane bioreactor and water reuse applications. Supplied by KINGDAO TECH, Yixing China.",
                1, "products.html")
    body += hero("Biological treatment · Membrane", "Curtain MBR Membrane",
                 "Reinforced hollow-fibre curtain modules with aeration frame, for MBR trains and reuse applications. Supplied as modules or as a complete MBR package with process design.",
                 '<a href="../index.html">Home</a> / <a href="../products.html">Products</a> / MBR Membrane')
    body += """
<section><div class="wrap two-col">
  <div class="prose">
    <h3>What it is</h3>
    <p>A curtain MBR module is a set of reinforced hollow-fibre membranes suspended between headers, with an aeration frame underneath. Air scouring keeps the fibres clean while suction draws filtered water through the membrane wall, retaining solids and biomass in the tank.</p>
    <p>The result is a biological plant that separates sludge with a membrane instead of a clarifier — solids are held at high concentration, the footprint drops sharply, and the effluent is clean enough for reuse without further filtration.</p>
    <h3>Where it fits</h3>
    <ul>
      <li><strong>Reuse projects</strong> — effluent suitable for irrigation, toilet flushing or process make-up after disinfection</li>
      <li><strong>Space-constrained sites</strong> — an MBR train takes a fraction of the tank volume of conventional activated sludge</li>
      <li><strong>Retrofit and capacity upgrades</strong> — more treatment capacity inside existing tanks</li>
      <li><strong>Strict discharge limits</strong> — where suspended solids and turbidity have to be very low</li>
    </ul>
    <h3>What we supply</h3>
    <p>Modules and frames, or the complete membrane tank package: modules, aeration frame, permeate pump, backwash and chemical cleaning equipment, control cabinet, and the process design around it. We size the membrane area against your flux, your peak flow and your cleaning regime — not against a catalogue page.</p>
  </div>
  <div>
    <div class="kv">
      <div><b>Configuration</b><span>Curtain (submerged) hollow-fibre modules with aeration frame</span></div>
      <div><b>Application</b><span>MBR biological trains, water reuse, retrofit capacity upgrades</span></div>
      <div><b>Supply scope</b><span>Modules only, module + frame, or complete MBR tank package</span></div>
      <div><b>Control</b><span>Permeate pump, backwash and chemical cleaning sequence in the control cabinet</span></div>
      <div><b>Design support</b><span>Membrane area sizing, flux calculation and tank layout drawings</span></div>
    </div>
    <div style="margin-top:22px"><a class="btn btn-primary" href="../contact.html">Request Membrane Sizing</a></div>
  </div>
</div></section>

<section class="soft"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">What we need to size a membrane train</div>
    <h2>Six numbers, and we can issue a membrane area and a tank layout.</h2></div>
  <div class="why-grid">
    <div class="why"><b>1 · Design flow</b><p>Average and peak flow in m³/d, and whether it includes infiltration.</p></div>
    <div class="why"><b>2 · Influent quality</b><p>COD, BOD, SS, ammonia and oil/grease where relevant.</p></div>
    <div class="why"><b>3 · Discharge or reuse standard</b><p>What the effluent has to meet, and whether it will be reused.</p></div>
    <div class="why"><b>4 · Available tank volume</b><p>Existing tanks if it is a retrofit, or the space available for new ones.</p></div>
  </div>
</div></section>

<section><div class="wrap"><div class="cta-band">
  <div><h2>Not every project should use a membrane.</h2>
  <p>If a conventional process meets your standard at lower cost, we will say so. Send the flow and the discharge limit and we will tell you honestly which route fits.</p></div>
  <a class="btn" href="../contact.html">Ask Which Route Fits</a>
</div></div></section>
"""
    body += foot(1)
    write("products/mbr.html", body)

# ══════════════════════════════════════════════════════════
def build_extras():
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE)
    pages = ["index.html", "products.html", "projects.html", "solutions.html", "oem.html",
             "about.html", "contact.html", "products/screw-press.html",
             "products/crushing-grille.html", "products/mbr.html"]
    urls = "".join(
        "  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n" % (SITE, p.replace("index.html", ""), TODAY)
        for p in pages)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls)
    # 404
    b = head("Page not found | KINGDAO TECH", "Page not found.", 0, "")
    b += hero("404", "That page does not exist.",
              "It may have moved when we rebuilt the site. The product and project pages are the fastest way back.",
              '<a href="index.html">Home</a> / Not found')
    b += """
<section><div class="wrap"><div class="cta-band">
  <div><h2>Looking for something specific?</h2>
  <p>Products, projects, or just send us the enquiry — we answer directly.</p></div>
  <a class="btn" href="contact.html">Contact Us</a>
</div></div></section>
"""
    b += foot(0)
    write("404.html", b)

if __name__ == "__main__":
    print("Building site ...")
    build_products()
    build_projects()
    build_solutions()
    build_about()
    build_oem()
    build_contact()
    build_screw_press()
    build_crushing_grille()
    build_mbr()
    build_extras()
    print("Done.")
