# -*- coding: utf-8 -*-
"""把去水印+已打商标的格栅/螺旋图挂到 4 个产品页（img-grid + 型号参数 figcaption）"""
import os, re

ROOT = r"C:\Users\Administrator\kingdaotech_newsite"
os.chdir(ROOT)

GRID = {
 "mechanical-bar-screen.html": [
   ("grille-mech-rotary-rake.jpg", "Rotary rake bar screen",
    "Rotary rake · 1–50 mm gap · 0.5–3 m channel · 0.55–5.5 kW · capture ≥95%"),
   ("grille-mech-coarse.jpg", "Mechanical coarse bar screen",
    "Chain rake · 10 / 20 / 30 / 40 / 50 mm gap · 0.5–3.5 m channel · 0.75–5.5 kW"),
   ("grille-mech-grab.jpg", "Grab type mechanical bar screen",
    "Grab type · 1–8 m channel · 1.5–8 m deep · hoist 4–8 m/min · travel 6–12 m/min"),
   ("grille-mech-rotary-cleaner.jpg", "Rotary screen cleaner for pump stations",
    "Rotary cleaner (GSHZ) · 10–50 mm gap · compact single-frame pump-station unit"),
 ],
 "fine-bar-screen.html": [
   ("grille-fine-step.jpg", "Stepped fine bar screen",
    "Stepped fine screen · 1–10 mm aperture · static steps, no drive"),
   ("grille-fine-drum.jpg", "Horizontal drum fine screen",
    "Horizontal drum · 0.5–5 mm wedge-wire · variable drum speed"),
   ("grille-fine-plate-step.jpg", "Stepped perforated plate screen",
    "Stepped plate · 1 / 3 / 5 / 6 / 10 / 15 / 25 mm · 50–5,000 m3/h · 0.75–3.0 kW"),
   ("grille-fine-plate-step2.jpg", "Stepped plate screen with rotary brush",
    "Plate + brush + backwash · 1–20 mm · capture ≥98% · 0.55–3.0 kW"),
   ("grille-fine-inflow.jpg", "In-flow perforated plate fine screen",
    "In-flow plate · 3 / 5 / 6 mm · separation ≥97% · head loss ≤300 mm at 40% blinded"),
 ],
 "coarse-manual-screen.html": [
   ("grille-mech-coarse.jpg", "Mechanical coarse bar screen",
    "Chain rake coil screen · 10–50 mm gap · continuous, unmanned stations"),
   ("grille-mech-grab.jpg", "Grab type coarse bar screen",
    "Travelling grab · wide and deep inlets · no submerged drive"),
 ],
 "screw-screen.html": [
   ("screw-screen-wshaft.jpg", "Shaftless screw conveyor-press",
    "Shaftless conveyor-press · conveying and dewatering in one trough"),
   ("screw-screen-press.jpg", "Screw press for screenings",
    "Screw press · 85–95% inlet dry solids → 40–45% outlet"),
   ("screw-screen-gp.jpg", "GP high drainage screw press",
    "GP-400 · Ø400 mm screw · 4.0 m3/h · 3.0 kW · L 1,800 × B 420 mm"),
   ("screw-screen-grit.jpg", "Spiral grit separator",
    "Spiral grit separator · grit settles, organics carried back to the flow"),
 ],
}

def build(items):
    cells = ""
    for fn, alt, cap in items:
        cells += (f'  <figure><img src="../images/products/{fn}" alt="{alt}" loading="lazy">\n'
                  f'    <figcaption>{cap}</figcaption></figure>\n')
    return ('\n<section class="soft"><div class="wrap">\n'
            '  <div class="sec-head"><div class="eyebrow">Hardware</div>\n'
            '    <h2>What the unit looks like.</h2>\n'
            '    <p class="lead">Drive arrangement, bar or plate face, and the frame that carries it — '
            'the same order as the selection tables above.</p></div>\n'
            f'  <div class="img-grid" style="grid-template-columns:repeat({min(len(items),4)},1fr)">\n'
            f'{cells}  </div>\n</div></section>\n')

for fn, items in GRID.items():
    p = os.path.join("products", fn)
    s = open(p, encoding="utf-8").read()
    if "img-grid" in s:
        print("SKIP 已有图区:", fn); continue
    i = s.find("<!-- KINGDAO_A_GROUP -->")
    assert i > 0, fn
    j = s.find("</section>", i)
    assert j > 0, fn
    j += len("</section>")
    s = s[:j] + build(items) + s[j:]
    open(p, "w", encoding="utf-8").write(s)
    print(f"OK {fn}: 加 {len(items)} 张图 ({os.path.getsize(p)//1024} KB)")
