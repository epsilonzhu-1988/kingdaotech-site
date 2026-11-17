# -*- coding: utf-8 -*-
"""为 22 个产品生成详情页（已有 screw-press / crushing-grille / mbr 三个）
用法: python gen_product_pages.py
"""
import os, sys

ROOT = r"C:\Users\Administrator\kingdaotech_newsite"
sys.path.insert(0, ROOT)
from build_site import head, hero, foot, write

# slug, nav_name, category, title, tagline, intro[], points[(b,p)], apps, spec_note
P = [
 ("mechanical-bar-screen", "Mechanical Bar Screen", "Pre-treatment · Screening",
  "Mechanical Bar Screen",
  "Raked bar screen that lifts screenings out of the channel instead of shredding them.",
  ["A mechanical bar screen removes solids from the incoming flow by raking them off the bar rack and lifting them into a bin, conveyor or washer. It is the first barrier in most municipal and industrial plants, and the stage that decides how much maintenance everything downstream needs.",
   "The screen is installed in a channel, inclined at the angle that suits the bar spacing and the screenings load. Rake arms travel down the rack, collect the retained material and carry it up; cleaning can be triggered on a timer, on a differential level sensor, or manually."],
  [("Bar spacing", "Selected against the downstream equipment — coarse for pump protection, fine where the next stage is a membrane or a fine-bubble diffuser."),
   ("Automatic operation", "Timer, differential level or PLC control; manual override for maintenance."),
   ("Materials", "304 stainless steel in contact with the flow; the frame can be supplied in painted carbon steel where the budget requires."),
   ("Integrated handling", "Optional screenings washer-compactor or screw conveyor so wet material does not go straight into a bin.")],
  "Municipal intake · pump station protection · industrial pre-treatment", ""),

 ("fine-bar-screen", "Fine Bar Screen (hydraulic)", "Pre-treatment · Screening",
  "Mechanical Fine Bar Screen (hydraulic driven)",
  "Fine screening with hydraulic drive — for high screenings load and tight bar spacing.",
  ["Where the flow carries a heavy screenings load, or where the bar spacing has to be small to protect a membrane or a fine-bubble diffuser, a hydraulic-driven fine screen handles the duty more reliably than a mechanical rake: the stroke force is set by the hydraulic unit and the drive does not stall on a jam.",
   "The unit is mounted in the channel like a conventional bar screen, with the rake driven by hydraulic rams. Overload protection is inherent in the hydraulic circuit rather than in a mechanical shear pin."],
  [("Small bar spacing", "Down to fine screening, suitable ahead of MBR and filtration stages."),
   ("Hydraulic drive", "Force-limited stroke: the unit stalls rather than breaks when it meets an obstruction."),
   ("Level-based cleaning", "Runs on differential level, so energy is spent only when the rack is actually loading up."),
   ("304 stainless", "Bar rack and rake in 304 stainless steel.")],
  "MBR pre-screening · industrial intake · high screenings load", ""),

 ("rotary-drum-screen", "Rotary Drum Screen", "Pre-treatment · Screening",
  "Rotary Drum Screen",
  "Continuous fine screening with a rotating drum and internal spray cleaning.",
  ["A rotary drum screen filters the flow through a perforated or wedge-wire drum that turns slowly, with the retained solids carried up and off by the rotation, and the screen surface cleaned by internal spray water. There is no raking cycle, so the head loss stays steady instead of pulsing.",
   "It suits flows where a bar screen cannot achieve the required screening size — fine screening ahead of filtration, membrane protection, or industrial flows carrying fibrous material."],
  [("Continuous, no cycle", "Steady head loss; no rake stroke to time against the flow."),
   ("Fine apertures", "Perforated plate or wedge wire, selected against the downstream requirement."),
   ("Internal spray cleaning", "Keeps the drum open without manual intervention."),
   ("Compact footprint", "Drum configuration fits where a long inclined screen will not.")],
  "Municipal fine screening · MBR protection · textile and paper flows", ""),

 ("screw-screen", "Screw Screen", "Pre-treatment · Screening",
  "Screw Screen",
  "Screening, conveying and dewatering of screenings in one unit.",
  ["A screw screen combines three stages in one machine: the flow passes through a perforated screen basket, a screw conveys the retained material along the basket, and the last section dewaters and compacts it before discharge. What leaves the machine is a relatively dry plug of screenings, not a wet slurry.",
   "That matters where screenings disposal is expensive or where a wet product would drip through the plant floor. It is the compact answer to fine screening in industrial plants and packaged pumping stations."],
  [("Three stages, one machine", "Screen, convey and dewater — no separate washer-compactor needed."),
   ("Dry discharge", "Compacted plug, easier and cheaper to dispose of."),
   ("Small footprint", "Suitable for packaged pumping stations and retrofit installations."),
   ("Low maintenance", "Few moving parts; the screw runs continuously at low speed.")],
  "Packaged pumping stations · industrial plants · retrofit installations", ""),

 ("coarse-manual-screen", "Coarse & Manual Bar Screen", "Pre-treatment · Screening",
  "Coarse and Manual Bar Screen",
  "The first barrier, where flow is high and automation is not justified.",
  ["A coarse bar screen is the simplest and often the most robust pre-treatment step: a rack of bars at a wide spacing that stops the material which would damage pumps, with manual or semi-manual raking.",
   "It is the right choice for small stations, storm overflows, and installations where the screenings volume is low enough that automation would cost more than it saves. It also serves as a bypass-stage screen ahead of finer equipment."],
  [("Wide bar spacing", "Pump protection at the head of the works."),
   ("Manual or semi-manual", "Appropriate where screenings volume does not justify a drive."),
   ("Simple and robust", "Almost nothing to fail; the maintenance is the raking."),
   ("304 stainless", "Or painted carbon steel for dry, non-corrosive duties.")],
  "Small stations · storm overflow · bypass screening", ""),

 ("dm-dewatering", "DM Dewatering Machine", "Sludge treatment · Dewatering",
  "DM Dewatering Machine (plate and frame)",
  "High-dryness cake where the screw press is not enough.",
  ["The DM series is a plate-and-frame dewatering machine: sludge is pumped into chambers formed between filter plates under pressure, water passes through the filter cloth and the solids remain as a cake. Cake dryness is higher than a screw press can achieve, which matters where sludge has to be transported long distances or dried further.",
   "The trade-off is batch operation, filter cloth replacement and wash water. It suits plants where cake dryness is the controlling cost, or where the sludge is difficult — oily, fibrous or heavily conditioned."],
  [("Higher cake dryness", "The reason to choose it over a screw press."),
   ("Batch operation", "Fill, press, release, discharge — automated by the control cabinet."),
   ("Filter cloth", "A consumable, so factor the replacement cost into the comparison."),
   ("Rugged frame", "Welded plate pack for industrial duties.")],
  "High-dryness requirement · difficult sludge · plants with existing cloth handling", ""),

 ("sludge-dryer", "Sludge Drying Device (PID)", "Sludge treatment · Drying",
  "Sludge Drying Device (PID)",
  "Further volume reduction after mechanical dewatering.",
  ["Mechanical dewatering stops at 20–30% dry solids for most sludges. Where disposal is charged by weight, or where the sludge has to leave the site dry, a drying stage takes it further and cuts the mass that has to be moved.",
   "The drying stage is sized by what the dewatering stage delivers: a drier cake means less water to evaporate, a smaller dryer and a lower energy bill per tonne of dry solids. That is why the two stages should be chosen together, not separately."],
  [("Volume reduction", "Lower mass and lower disposal cost per tonne of dry solids."),
   ("Sized from the dewatering result", "Dryer selection follows cake dryness, not sludge flow."),
   ("Integrated control", "Interlocked with the dewatering stage so neither runs blind."),
   ("Heat source selected to site", "Steam, hot water or electric, depending on what the plant has.")],
  "Sludge disposal cost reduction · pre-incineration drying · volume-sensitive sites", ""),

 ("sludge-scraper", "Sludge Scraper", "Sludge treatment · Tank equipment",
  "Sludge Scraper",
  "Circular and rectangular tank sludge collection.",
  ["A sludge scraper removes settled sludge from the floor of a sedimentation tank and drives it to the collection point, while a surface skimmer can remove floating material at the same time. Without reliable scraping, the sludge layer builds, goes anaerobic and the tank stops doing its job.",
   "Both circular and rectangular configurations are available, with drive options matched to the tank size and the sludge volume."],
  [("Circular and rectangular", "Matched to the tank geometry, not forced into one design."),
   ("Sludge and scum", "Collection of both, in one pass where the tank requires it."),
   ("Drive protection", "Overload protection so a jam does not destroy the gearbox."),
   ("Wet-end materials", "Corrosion-resistant where the tank is aggressive.")],
  "Primary and secondary clarifiers · thickeners · industrial settling tanks", ""),

 ("screw-conveyor", "Screw Conveyor", "Sludge treatment · Handling",
  "Screw Conveyor",
  "Transport of dewatered cake, screenings and grit.",
  ["The screw conveyor moves dewatered cake or screenings horizontally or at a slight incline, in a closed trough, without spillage or odour escape. It is the piece of equipment that connects the dewatering stage to the skip, and the one most often forgotten in the layout.",
   "Length, diameter and pitch are selected against the material: cake is cohesive and moves well; screenings are irregular and need a larger trough and slower speed."],
  [("Closed trough", "No spillage, no odour release on the plant floor."),
   ("Horizontal or inclined", "Layout flexibility; incline limited by the material."),
   ("Wear liner", "Replaceable liner at the high-wear sections."),
   ("Integrated with dewatering", "Interlocked so the conveyor runs only when the press discharges.")],
  "Cake transport to skip · screenings handling · grit removal", ""),

 ("screw-pump", "Screw Pump", "Sludge treatment · Pumping",
  "Screw Pump",
  "Low-shear transfer of sludge and high-solids liquids.",
  ["A screw pump (progressive cavity pump) moves sludge by a rotating rotor inside a stationary stator, forming sealed cavities that travel along the pump. Because there is no impeller to shear the floc, the sludge arrives at the dewatering stage in the condition the polymer produced.",
   "That is the reason screw pumps are the standard choice ahead of a screw press or a plate press: a centrifugal pump would break the floc and the dewatering result would fall away."],
  [("Low shear", "Floc structure preserved, so polymer consumption and cake dryness hold."),
   ("Solids handling", "Handles sludge at the concentrations the dewatering stage needs."),
   ("Metered flow", "Speed control gives a stable feed rate to the press."),
   ("Wear parts", "Rotor and stator are the consumables; replaced as a set.")],
  "Sludge feed to dewatering · thickened sludge transfer · high-solids dosing", ""),

 ("aerators", "Aerators & Diffusers", "Biological · Aeration",
  "Aerators and Air Diffusers",
  "Fine-bubble aeration — the largest energy line in any biological plant.",
  ["Aeration is typically the single biggest electricity consumer in a biological wastewater plant, so the diffuser choice is a running-cost decision, not a capital one. Fine-bubble diffusers transfer oxygen more efficiently than coarse bubbles or surface aerators, but they need clean air and periodic cleaning to stay efficient.",
   "We supply disc and tubular fine-bubble diffusers with the associated pipework and lifting arrangements, and surface aerators where the tank geometry or the duty calls for them."],
  [("Fine bubble", "Highest oxygen transfer efficiency, lowest energy per kg O₂."),
   ("Disc and tubular", "Selected against tank depth and the aeration grid layout."),
   ("Lifting arrangement", "Diffusers can be raised for cleaning without draining the tank."),
   ("Air supply matched", "Blower selection follows the diffuser curve, not the other way round.")],
  "Activated sludge · MBBR · equalisation tanks · aerated grit chambers", ""),

 ("mixers", "Submersible Mixers", "Biological · Mixing",
  "Submersible Mixers and Agitators",
  "Low-speed mixing that keeps solids in suspension without adding oxygen.",
  ["In anoxic and equalisation tanks the job is to keep the contents mixed without introducing oxygen — an aerator would defeat the purpose. Submersible mixers run at low speed with a large propeller, moving a high volume at low velocity.",
   "Draft-tube mixers are used where a defined circulation pattern is needed, high-speed units where the tank is small or the solids tend to settle quickly."],
  [("Low-speed, high-flow", "Suspension without oxygen transfer."),
   ("Draft tube option", "Defined circulation for anoxic zones and sludge holding tanks."),
   ("Guide rail mounting", "The mixer can be raised for service without entering the tank."),
   ("Seal and motor protection", "Double mechanical seal with condition monitoring on the larger units.")],
  "Anoxic zones · equalisation tanks · sludge holding · MBR membrane tanks", ""),

 ("fillers", "Fillers (elastic / rope)", "Biological · Media",
  "Fillers — elastic and rope type",
  "Bio-media for fixed-film and moving-bed biological stages.",
  ["Fixed-film media give the biology a surface to grow on, which lets a plant carry more biomass in the same tank volume, or run at a longer sludge age without a larger clarifier. The two forms we supply serve different purposes: rope media in fixed or moving arrangements, elastic media where a simple, low-cost surface is enough.",
   "Media selection is about specific surface area, void ratio and how well the biofilm sheds. Too dense and the bed clogs; too open and there is not enough surface to be worth the tank."],
  [("Specific surface", "Selected against the organic load, not simply the tank volume."),
   ("Void ratio", "Open enough to avoid clogging, dense enough to be worth the space."),
   ("Biofilm shedding", "Structure that lets excess biomass detach instead of accumulating."),
   ("Rope and elastic forms", "Different arrangements for fixed-bed and moving applications.")],
  "MBBR · fixed-film upgrades · anoxic zones · aquaculture", ""),

 ("mbbr", "MBBR Media", "Biological · Media",
  "MBBR Media",
  "Moving bed biofilm carriers for capacity upgrades inside existing tanks.",
  ["Moving bed biofilm reactor media are small plastic carriers kept in motion by aeration or mixing, each carrying a protected biofilm. Because the biomass grows on carriers rather than as floc, an MBBR can carry far more treatment capacity in the same tank volume than activated sludge — which is why it is the standard answer to a plant that has run out of capacity but not out of space.",
   "The design questions are the fill fraction, the aeration or mixing energy to keep the carriers moving, and the screen that keeps them in the tank."],
  [("Capacity in existing tanks", "The retrofit route when there is no land for new basins."),
   ("Protected biofilm", "Less sensitive to load shocks and toxic upsets than floc."),
   ("Fill fraction design", "Selected against the load; over-filling costs energy for no gain."),
   ("Retention screen", "The detail that decides whether the system works long-term.")],
  "Capacity upgrades · industrial pre-treatment · nitrogen removal · nutrient-sensitive discharges", ""),

 ("daf", "Dissolved Air Flotation", "Tertiary · Physical separation",
  "Dissolved Air Flotation (DAF)",
  "Removes oil, grease and light suspended solids that settling will not catch.",
  ["Dissolved air flotation attaches microbubbles to particles and lifts them to the surface, where they are skimmed off. It is the right tool when the pollutant is lighter than water, or when the floc is too light to settle at a practical rate — oil and grease, algae, light biological solids.",
   "DAF is often the stage that makes the difference in food, slaughterhouse, refinery and paper effluents, and it is frequently used ahead of a biological stage to protect the biology from oil."],
  [("Oil and grease removal", "The duty that settling cannot do."),
   ("Chemical dosing integrated", "Coagulant and flocculant dosing matched to the DAF."),
   ("Compact vs settling", "A DAF is typically a fraction of the footprint of an equivalent settling tank."),
   ("Sludge handling", "Floated sludge is thicker than settled sludge and easier to dewater.")],
  "Food and slaughter effluent · refinery and oily water · paper · algae removal", ""),

 ("sand-filter", "Sand Filter", "Tertiary · Filtration",
  "Sand Filter (multi-media)",
  "Suspended solids polishing before discharge or reuse.",
  ["A multi-media sand filter removes the residual suspended solids that a biological stage leaves behind. It is the last physical barrier before discharge, or the pre-treatment before a membrane, a UV unit or a reuse distribution system.",
   "Backwash is the design question: the filter has to be able to clean itself with the water it has, and the backwash sequence has to be automatic or it will not be done."],
  [("Multi-media bed", "Graded layers for a higher solids holding capacity before breakthrough."),
   ("Automatic backwash", "Air scour and water backwash on differential pressure or timer."),
   ("Low turbidity outlet", "The prerequisite for UV disinfection or membrane duty."),
   ("Skid or concrete", "Supplied as a skid package or as internals for a concrete basin.")],
  "Tertiary polishing · reuse pre-treatment · membrane protection", ""),

 ("uv", "UV Sterilizer", "Tertiary · Disinfection",
  "UV Sterilizer",
  "Disinfection without chemical residual or disinfection by-products.",
  ["UV disinfection inactivates bacteria and viruses by damaging their DNA, with no chemical added and no residual to manage. Where the discharge goes to a sensitive watercourse, or where the effluent is reused for irrigation, that is often the deciding advantage over chlorination.",
   "The design constraint is water quality: UV only works if the water is clear. Suspended solids and colour shield the organisms, so a UV unit is always preceded by filtration and the transmittance of the water is a design input, not an afterthought."],
  [("No residual", "No chemical storage, no dosing, no by-products."),
   ("Lamp monitoring", "UV intensity sensors and lamp-hour logging in the control cabinet."),
   ("Automatic wiping", "Mechanical or chemical wiping to keep sleeve transmission up."),
   ("Transmittance-based sizing", "Sized on UVT and dose, not on flow alone.")],
  "Sensitive discharge · reuse for irrigation · aquaculture · food industry water", ""),

 ("dosing", "Automatic Dosing Devices", "Chemical · Dosing",
  "Automatic Dosing Devices (PAC / polymer)",
  "Preparation and dosing systems for PAC, polymer and other chemicals.",
  ["Dosing is where a plant most often loses performance for reasons that are not the process: the powder is not fully wetted, the solution strength drifts, the pump is not calibrated. An automatic preparation and dosing system takes those variables out of the operator's hands.",
   "For PAC we supply fully automatic and semi-automatic preparation units with metering pumps; for polymer, a three-chamber preparation tank with maturation and dilution, matched to the dewatering stage it serves."],
  [("Automatic preparation", "Powder wetting, mixing, maturation and dilution in one sequence."),
   ("Solution strength control", "Concentration held at the setpoint instead of drifting with the operator's day."),
   ("Metering pumps", "Selected against the dose range and the discharge pressure required."),
   ("Control integration", "Dose proportional to flow or to load, with the signal taken from the plant PLC.")],
  "Polymer for dewatering · PAC for coagulation · pH and nutrient dosing", ""),

 ("submersible-pumps", "Submersible Pumps", "Pumping",
  "Submersible Pumps",
  "Sewage, sludge and clean water — with cutter options where solids are the problem.",
  ["Submersible pumps are the workhorse of a wastewater plant: raw sewage transfer, sludge pumping, sump drainage and recirculation. The selection question is rarely the flow and head alone — it is what the pump has to pass.",
   "For raw sewage the impeller has to pass the solids without blocking; where the flow carries fibrous material, a cutter or grinder arrangement in front of the impeller is what keeps the pump running. For sludge, the viscosity and the solids content set the derating."],
  [("Solids handling", "Vortex or channel impeller selected against the solids size."),
   ("Cutter option", "For fibrous load that would otherwise wrap the impeller."),
   ("Wet or dry installation", "Guide-rail wet well mounting or dry chamber with the same pump end."),
   ("Seal monitoring", "Leakage sensor in the oil chamber on the larger units.")],
  "Sewage transfer · sludge pumping · sumps and storm tanks · recirculation", ""),

 ("frp-pumping-station", "FRP Pumping Station", "Packaged plants",
  "FRP Prefabricated Pumping Station",
  "A complete pumping station built in the factory and buried as one unit.",
  ["An FRP prefabricated pumping station arrives on site as a single unit: cylinder, pumps, pipework, valves, level control and control cabinet, all assembled and tested at the factory. Site work reduces to excavation, bedding and connection — which is the reason it is chosen where the site is tight, the water table is high, or the programme is short.",
   "A crushing grille can be integrated at the inlet, in place of the traditional basket screen, so the solids are shredded before they reach the pump and manual raking disappears from the maintenance schedule."],
  [("Factory-built and tested", "Site work reduced to excavation and connection."),
   ("Integrated crushing grille", "No basket screen, no manual raking, no pump blockage."),
   ("Level control", "Pump sequencing and duty standby in the station control cabinet."),
   ("Rapid installation", "Weeks off the civil programme compared with a concrete wet well.")],
  "Municipal pumping stations · estate and industrial park drainage · retrofit replacements", ""),

 ("small-integrated-stp", "Small Integrated STP", "Packaged plants",
  "Small Integrated Sewage Treatment Plant",
  "Packaged plants from 5 to 200 m³/d, skid or container mounted.",
  ["For a hotel, a school, a factory canteen or a small estate, a conventional concrete plant is disproportionate: too much civil work, too much operator attention, and a footprint nobody wants to give up. A packaged plant arrives as a unit, treats to the required standard and is commissioned in days.",
   "The process inside is chosen against the discharge standard and the load pattern — AO or MBBR for nitrogen, with the tank volume set by the retention the biology actually needs, not by what fits in the box."],
  [("5 – 200 m³/d", "Sized to the application rather than rounded up to a standard plant."),
   ("Skid or container", "Relocatable, and inspectable before it leaves the factory."),
   ("Low operator attention", "Automated aeration and sludge return; the operator checks, not operates."),
   ("Standards matched", "Process selected against the discharge standard that applies on site.")],
  "Hotels and resorts · schools and hospitals · factories and canteens · small estates", ""),
]

print("待生成产品页:", len(P))

for slug, nav, cat, title, tagline, intro, points, apps, note in P:
    pts = "".join(f'<div class="kv"><div><b>{b}</b><span>{p}</span></div></div>' for b, p in points)
    body = head(f"{title} | KINGDAO TECH", tagline, 1, "products.html")
    body += hero(cat, title, tagline,
                 f'<a href="../index.html">Home</a> / <a href="../products.html">Products</a> / {nav}')
    paras = "".join(f"<p>{t}</p>" for t in intro)
    body += f"""
<section><div class="wrap two-col">
  <div class="prose">{paras}</div>
  <div>
    <div class="kv">{pts}</div>
    <div style="margin-top:22px"><a class="btn btn-primary" href="../contact.html">Request a Quotation</a></div>
  </div>
</div></section>

<section class="soft"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">Where it fits</div>
    <h2>Typical applications.</h2>
    <p class="lead">{apps}</p>
    {('<p class="note">' + note + '</p>') if note else ''}
  </div>
  <div class="cta-band">
    <div><h2>Send us the duty and we will name the model.</h2>
    <p>Flow, the medium, the installation and the discharge requirement — that is enough to select and quote.</p></div>
    <a class="btn" href="../contact.html">Talk to an Engineer</a>
  </div>
</div></section>
"""
    body += foot(1)
    write(f"products/{slug}.html", body)

print("完成")
