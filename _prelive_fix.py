# -*- coding: utf-8 -*-
"""上线前 SEO 元信息终检修复：meta description 统一 120–160 字；m3/h → m³/h"""
import re, os, html, glob

ROOT = r"C:\Users\Administrator\kingdaotech_newsite"
os.chdir(ROOT)

META = {
 "index.html":
   "KINGDAO TECH designs wastewater treatment plants and builds the equipment inside them: screening, "
   "sludge dewatering, membranes, aeration and dosing. Factory in Yixing, China.",
 "projects.html":
   "18 wastewater design references grouped by type — municipal, tannery, dyeing, PCB, electroplating, "
   "slaughterhouse, livestock, down and feather. Capacities to 100,000 m3/d.",
 "solutions.html":
   "Process routes for 12 wastewater types — municipal, tannery, dyeing, PCB, electroplating, "
   "slaughterhouse, livestock, down and feather, plus water reuse and supply.",
 "oem.html":
   "OEM manufacturing for water treatment suppliers and EPC contractors: your brand on the equipment, "
   "our plant in Yixing, our drawings and commissioning support.",
 "about.html":
   "WuXi KingDao Environmental Technology Co., Ltd — water treatment equipment manufacturer and process "
   "design house in Yixing, Jiangsu, China. 20 years, 17 equipment lines.",
 "products/mechanical-bar-screen.html":
   "Mechanical bar screens in four drives — rotary rake, chain rake, travelling grab and rotary cleaner. "
   "10-50 mm gaps, 0.5-8 m channels, 0.55-5.5 kW, capture 95% and above.",
 "products/fine-bar-screen.html":
   "Fine screening from 0.5 to 25 mm: in-flow perforated plate, stepped plate with brush and backwash, "
   "and horizontal drum. Separation 97-98%, head loss 300 mm and below.",
 "products/coarse-manual-screen.html":
   "Coarse and hand-cleaned bar screens: chain rake and travelling grab for 10-50 mm gaps, plus "
   "fabricated hand-raked racks where automation is not justified.",
 "products/screw-screen.html":
   "Screw screens and presses for screenings: GP-200/300/400 high-drainage press, 1-4 m3/h, inlet "
   "85-95% dry solids down to 40-45%, shaftless conveyors and grit separators.",
 "products/sludge-scraper.html":
   "ZQ(B)GN sludge scrapers, full-bridge and half-bridge, with a helical scraping path, scum skimming "
   "in the same revolution and torque-protected drives.",
 "products/dosing.html":
   "Automatic and semi-automatic dosing devices for PAC and polymer — dissolving tank, mixer, metering "
   "pumps and PLC control assembled on one skid.",
 "products/fillers.html":
   "Bio-media for fixed-film and moving-bed stages: elastic and rope fillers at 260-380 m2/m3, combined "
   "and suspended ball media, and MBBR carriers.",
 "products/rotary-drum-screen.html":
   "Rotary drum screens with internal spray cleaning for continuous fine screening — 13 specifications, "
   "wedge-wire or perforated drum, 0.5-5 mm apertures.",
 "products/mixers.html":
   "Submersible mixers and agitators, QJB range: 63 models from 0.37 to 22 kW, impellers 220-2500 mm, "
   "thrust 115-8540 N, dual mechanical seals, IP68.",
 "products/aerators.html":
   "Fine-bubble aeration, the largest energy line in any biological plant: disc, tube, rubber-membrane "
   "and cyclone diffusers, with full performance data.",
 "products/propellers.html":
   "Large-diameter submersible propellers for basin circulation — 46 models from 1.5 to 7.5 kW, "
   "low-speed thrust without adding oxygen.",
 "products/submersible-pumps.html":
   "Sewage, sludge and clean-water pumps, WQ range: 93 models from 1 to 75 kW, 10-2700 m3/h, DN50-DN500, "
   "with cutter options where solids are the problem.",
 "products/frp-pumping-station.html":
   "A complete pumping station built in the factory and buried as one FRP unit — pumps, piping, valves, "
   "controls and level instruments pre-assembled and tested.",
 "products/crushing-grille.html":
   "PG tubular crushing grille for inline installation — 21 models DN50 to DN400, 40 to 300 m3/h, plus "
   "the PSL series for channel mounting.",
 "products/channel-crushing-grille.html":
   "PZG and PZGD rotary drum crushing grille for open channels — single and multi-motor versions, "
   "250 to 6400 m3/h, 16 to 23 models per series.",
}

fixed = []
for p, d in META.items():
    if not os.path.exists(p):
        print("缺文件", p); continue
    s = open(p, encoding="utf-8").read()
    new = html.escape(d, quote=True)
    s2, n = re.subn(r'(name="description"\s+content=")[^"]*(")', lambda m: m.group(1) + new + m.group(2), s, count=1)
    if n == 0:
        print("⚠ 未找到 meta:", p); continue
    open(p, "w", encoding="utf-8").write(s2)
    fixed.append((p, len(d)))

# m3/h → m³/h（页面上统一用 m³）
cnt = 0
for p in glob.glob("*.html") + glob.glob("products/*.html"):
    s = open(p, encoding="utf-8").read()
    s2 = s.replace(" m3/h", " m³/h").replace("m3/h ", "m³/h ")
    if s2 != s:
        open(p, "w", encoding="utf-8").write(s2); cnt += 1
print(f"m³ 统一：{cnt} 个文件")

print("\n改写后长度检查：")
for p, n in fixed:
    flag = "✅" if 110 <= n <= 160 else ("偏短" if n < 110 else "偏长")
    print(f"  {flag} {n:>4} | {p}")
