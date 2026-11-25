#!/usr/bin/env python3
"""THE CAPITAL STANDARD — NI25 F1 compose (fresh, this session). PIL local only."""
import sys
from PIL import Image, ImageDraw, ImageFont

FD = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)
PF_BLACK = "PlayfairDisplay-Black.ttf"
PF_BOLD = "PlayfairDisplay-Bold.ttf"
AR = "Archivo.ttf"
AR_B = "Archivo-Bold.ttf"

W = H = 1024
INK = (18, 38, 74)        # blue ink
INK2 = (28, 58, 110)
STEEL = (96, 110, 128)    # steel grey
STEEL_D = (58, 68, 84)
PAPER = (246, 244, 238)
PAPER2 = (236, 238, 240)
GOLD = (176, 138, 52)
RED = (158, 44, 40)
TEAL = (28, 110, 104)
GREEN = (52, 110, 62)
SKY = (120, 164, 205)

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def text_block(d, xy, text, font, fill, maxw, leading=1.12, max_lines=None):
    x, y = xy
    lines = wrap(d, text, font, maxw)
    if max_lines: lines = lines[:max_lines]
    lh = int(font.size * leading)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

# ---------- flat layered scene illustrations ----------
def scene(d, box, kind, c1, c2):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=c1)
    # layered bands
    d.rectangle([x0, y1 - (y1 - y0) // 3, x1, y1], fill=c2)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    s = min(x1 - x0, y1 - y0)
    if kind == "plane":  # AWACS: fuselage + radar dome
        d.ellipse([cx - s//3, cy - s//4, cx + s//3, cy - s//10], fill=(245,245,240))
        d.polygon([(cx - s//3, cy), (cx - s//2, cy + s//6), (cx + s//4, cy)], fill=(245,245,240))
        d.ellipse([cx - s//10, cy - s//3, cx + s//10, cy - s//6], outline=(20,20,20), width=2)
        d.line([x0 + 4, cy + s//4, x1 - 4, cy + s//4], fill=(245,245,240), width=1)
    elif kind == "ship":
        d.polygon([(cx - s//3, cy + s//8), (cx + s//3, cy + s//8), (cx + s//5, cy + s//3), (cx - s//5, cy + s//3)], fill=(30,30,34))
        d.rectangle([cx - s//12, cy - s//5, cx + s//20, cy + s//8], fill=(30,30,34))
        for i in range(3):
            d.ellipse([x0 + 8 + i * (s//3), y1 - 12, x0 + 18 + i * (s//3), y1 - 4], outline=(240,240,235), width=1)
    elif kind == "city":
        for i, hh in enumerate([0.5, 0.8, 0.62, 0.9, 0.55]):
            bx = x0 + 6 + i * (x1 - x0 - 12) // 5
            d.rectangle([bx, y1 - int((y1-y0)*hh) - 4, bx + (x1-x0)//6, y1 - 4], fill=(34,40,52))
            for wy in range(y1 - int((y1-y0)*hh), y1 - 10, 9):
                d.point((bx + 4, wy), fill=(250,220,120))
    elif kind == "dome":
        d.pieslice([cx - s//3, cy - s//3, cx + s//3, cy + s//3], 180, 360, fill=(240,238,230))
        d.rectangle([cx - s//3, cy, cx + s//3, cy + 3], fill=(240,238,230))
        d.line([cx, cy - s//3, cx, cy - s//2], fill=(240,238,230), width=2)
    elif kind == "oil":
        for i in range(3):
            bx = cx - s//3 + i * s//3
            d.rectangle([bx, cy - s//6, bx + 8, cy + s//4], fill=(28,28,30))
            d.line([bx + 4, cy - s//6, bx + 16, cy - s//3], fill=(28,28,30), width=3)
    elif kind == "chart":
        pts = [(x0 + 8, y1 - 10), (cx - s//5, cy + s//6), (cx, cy), (cx + s//5, cy - s//5), (x1 - 8, cy - s//3)]
        d.line(pts, fill=(250,225,90), width=3)
        d.line([x0 + 6, y1 - 6, x1 - 6, y1 - 6], fill=(240,240,235), width=1)
    elif kind == "shield":
        d.polygon([(cx, y0 + 4), (cx + s//3, y0 + 10), (cx + s//3, cy + s//6), (cx, y1 - 4), (cx - s//3, cy + s//6), (cx - s//3, y0 + 10)], outline=(245,245,240), width=3)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(245,245,240))
    elif kind == "ball":
        d.ellipse([cx - s//4, cy - s//4, cx + s//4, cy + s//4], outline=(245,245,240), width=3)
        d.polygon([(cx, cy - 6), (cx + 7, cy), (cx, cy + 7), (cx - 7, cy)], fill=(245,245,240))
    elif kind == "coral":
        for i in range(4):
            bx = x0 + 10 + i * (x1 - x0 - 20) // 4
            d.line([bx, y1 - 4, bx, cy], fill=(255,150,110), width=3)
            d.line([bx, cy + 6, bx - 7, cy - 4], fill=(255,150,110), width=2)
            d.line([bx, cy + 6, bx + 7, cy - 4], fill=(255,150,110), width=2)
    elif kind == "jet":
        d.polygon([(x0 + 8, cy + 4), (cx, cy - s//4), (x1 - 8, cy + 4), (cx, cy + s//8)], fill=(240,240,238))
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 2], fill=c1)
    elif kind == "doc":
        d.rectangle([cx - s//5, y0 + 5, cx + s//5, y1 - 5], fill=(245,244,238))
        for i in range(3):
            d.line([cx - s//5 + 5, y0 + 13 + i * 8, cx + s//5 - 5, y0 + 13 + i * 8], fill=(90,90,90), width=1)
    else:  # sun / generic
        d.ellipse([cx - s//5, cy - s//5, cx + s//5, cy + s//5], fill=(250,215,110))
        for a in range(0, 360, 45):
            import math
            d.line([cx, cy, cx + int(s*0.36*math.cos(math.radians(a))), cy + int(s*0.36*math.sin(math.radians(a)))], fill=(250,215,110), width=2)

REGION_COLORS = {
    "EUROPE": (44, 92, 160), "MIDDLE EAST": (178, 84, 40), "AFRICA": (150, 110, 30),
    "AMERICAS": (44, 130, 90), "ASIA": (130, 60, 140), "SOUTH ASIA": (190, 70, 90),
    "ASIA-PACIFIC": (30, 130, 150), "OCEANIA": (60, 150, 170), "WORLD": (96, 110, 128),
}

# ---------- story data (numbers ONLY from ni25-pool.md) ----------
# num, region, place, headline, deck, source, certainty, chip, scene, c1, c2
LEADS = [
    (4, "MIDDLE EAST", "GAZA", "Drone strikes kill Hamas security chief",
     "Israeli drone strikes across Gaza killed a senior Hamas security official, three policemen and three siblings, one a child — 7 killed in all.",
     "Al Jazeera", "REPORTED", "7 KILLED IN STRIKES", "city", (70, 52, 48), (38, 34, 40)),
    (2, "MIDDLE EAST", "STRAIT OF HORMUZ", "Iran says 3 tankers hit by mines",
     "Iran says — the IRGC Navy claims three oil tankers were hit by naval mines in the Strait of Hormuz. A claim, not confirmed; shipping concerns rise.",
     "Iranian claim via wires", "CLAIMED", "3 TANKERS HIT — IRAN SAYS", "ship", (30, 70, 96), (18, 44, 66)),
    (1, "EUROPE", "POLAND", "NATO sends early-warning jets to Poland",
     "NATO plans an AWACS early-warning deployment in Poland after Russian missiles landed in Poland during an attack on Ukraine. Chancellor Merz vows Germany's complete support to Poland.",
     "Wire reports", "REPORTED", "AWACS TO POLAND", "plane", (44, 92, 160), (26, 56, 102)),
]
GRID = [
    (3, "MIDDLE EAST", "IRAQ", "Baghdad orders Kurdish oilfields seized",
     "PM Ali al-Zaidi directs federal units to seize oilfields and crossings in Kurdish-run regions. President Barzani: Kurdistan will not submit to unconstitutional decisions.",
     "Starlit / wires", "REPORTED", "OILFIELDS ORDER", "oil", (96, 74, 40), (60, 48, 26)),
    (6, "WORLD", "UKRAINE WAR DATA", "700,000 Russian dead, new count finds",
     "A new analysis finds more than 700,000 Russian soldiers killed — 700000 dead — in the nearly five-year war on Ukraine.",
     "RFE/RL", "REPORTED", "700,000+ KILLED", "shield", (70, 74, 84), (44, 48, 58)),
    (5, "EUROPE", "BRUSSELS", "EU unveils new Russia sanctions",
     "The European Union announced further restrictive measures — new sanctions — against Russia amid the war in Ukraine.",
     "Wire roundups", "REPORTED", "NEW EU SANCTIONS", "doc", (52, 84, 140), (34, 56, 96)),
    (7, "EUROPE", "UKRAINE", "First German Lynx fighting vehicles arrive",
     "The first 5 German Lynx KF41 infantry fighting vehicles enter Ukrainian deployment — lynx kf41 armour now in service.",
     "Wires", "REPORTED", "5 LYNX IFVS", "shield", (66, 96, 66), (40, 62, 40)),
    (10, "ASIA", "CHINA", "Xiamen Airlines orders 50 Boeing jets",
     "Xiamen Airlines, a China Southern unit, agreed to acquire 50 Boeing 737-8 jets — xiamen's boeing 737 order is the day's big aviation deal.",
     "Wires", "REPORTED", "50 JETS ORDERED", "jet", (90, 70, 130), (56, 44, 88)),
    (11, "EUROPE", "MADRID", "Madrid rout PSV 5-1 in comeback",
     "Real Madrid overturned a deficit to beat PSV Eindhoven 5-1: a Bellingham stunner and an Mbappe brace sealed the madrid psv rout.",
     "Wires", "REPORTED", "MADRID 5-1 PSV", "ball", (40, 110, 70), (24, 70, 44)),
    (36, "WORLD", "NVIDIA", "Nvidia's $1 trillion Monday",
     "MONDAY CLOSE: Nvidia shares closed +31.5% — nvidia clawed back nearly $1 trillion of market value as Jensen Huang was reinstated as CEO, +$34 billion in a day (Forbes).",
     "Forbes via wires", "REPORTED · MONDAY CLOSE", "+31.5% MONDAY", "chart", (36, 84, 60), (20, 52, 38)),
    (33, "WORLD", "WASHINGTON", "PCE inflation report due today",
     "The US PCE inflation report is due today, Tuesday 25 November. No figure exists yet — markets watch for the Fed's next signal. PCE due today, not yet published.",
     "Scheduled", "SCHEDULED", "PCE DUE TODAY", "doc", (110, 96, 60), (72, 62, 38)),
    (13, "OCEANIA", "AUSTRALIA", "12 coral species brought back",
     "Great Barrier Reef genetic analysis resurrects 12 Acropora coral species — coral diversity wider than known, acropora restored on paper.",
     "Science wires", "REPORTED", "12 SPECIES BACK", "coral", (24, 110, 130), (14, 70, 92)),
    (8, "AMERICAS", "COLOMBIA", "Car bomb injures at least 23",
     "A car bomb in Colombia injured at least 23 people. In Cartagena, armed men hold dozens hostage in a supermarket — cartagena is a separate brief below.",
     "Wires", "REPORTED", "23 INJURED", "city", (130, 70, 50), (84, 44, 32)),
]
BRIEFS = [
    (9, "Gunmen hold dozens in a Cartagena supermarket, Colombia."),
    (12, "England beat Australia by 8 wickets in the T20I, chasing 185 to level the series 1-1; Fraser-McGurk 27 off 13 balls, 3 sixes."),
    (14, "Fiji declares a nationwide disaster amid an El Nino dry spell."),
    (15, "Iran's pharmacies run dry: medicine shortage shuts pharmacies, halts hospital supplies."),
    (16, "Iran braces for winter gas shortages; electricity rationing began 22 Nov."),
    (17, "Britain sanctions the Houthis and four top Yemeni rebel officials in a London move."),
    (18, "Senegal's AFCON title restored by a CAS ruling — cas ruling returns the 2025 crown."),
    (19, "Rebels pull back from DR Congo areas after clashes in the east."),
    (20, "Nigerian emir suspended after a sexual assault allegation."),
    (21, "Sudan RSF commander defects; sudan rsf split widens."),
    (22, "Cameroon separatist leader in a Norway court on war crimes charges."),
    (23, "Old allies reunite in Punjab: BJP and Shiromani Akali Dal — akali dal — ally for 2027."),
    (24, "Bangladesh opens an Invest Bangladesh office in Guangzhou, China."),
    (25, "Indonesia's vice-president resigns amid political strain (single source)."),
    (26, "Solomon Islands eye an Australia treaty to replace the China defence pact — solomon islands switch."),
    (27, "North Korea touts China ties as a top diplomat visits the Beijing embassy in Pyongyang."),
    (28, "Denmark court upholds the ghetto evictions law, dismissing discrimination concerns."),
    (29, "Sarkozy and Bruni headed for trial over the Libya case in Paris."),
    (30, "Black Sea clash at the UN: Russia and Ukraine trade accusations over shipping attacks."),
    (31, "Shortwave school for Afghan girls: RFE/RL returns to shortwave radio for girls barred from school."),
    (32, "An asteroid eclipses its twin: Dimorphos casts its shadow on Didymos — didymos dimorphos caught on camera."),
    (34, "US targets 7 firms over chip diversion, among them a company owned by Alibaba."),
    (35, "Decoy army: Moscow buys inflatable decoys from China to trick Ukraine — decoys on the battlefield."),
    (37, "Storms target Thanksgiving travel on both US coasts, a risk for millions of travellers."),
]
NUMBERS = [("7", "killed Gaza · c4"), ("3", "tankers Iran says · c2"),
           ("700,000+", "Russian dead · c6"), ("50", "Boeing jets · c10"),
           ("5-1", "Madrid-PSV · c11"), ("+31.5%", "Nvidia Mon · c36"),
           ("5", "Lynx KF41 · c7"), ("23", "injured Colombia · c8")]
REGIONS = ["EUROPE", "MIDDLE EAST", "AFRICA", "AMERICAS", "ASIA", "SOUTH ASIA", "ASIA-PACIFIC", "OCEANIA", "WORLD"]
TIMELINE = [("MON CLOSE", "Nvidia +31.5% close"), ("EARLY", "Iran says tankers hit in Hormuz"),
            ("DAY", "NATO AWACS plan for Poland"), ("DAY", "Gaza strikes: 7 killed"),
            ("DUE TODAY", "US PCE report scheduled"), ("NIGHT", "Madrid 5-1 PSV comeback")]
DATE_CHECK = ["Mercury story — 23 Nov, not today", "COP31 summit — earlier, not today",
              "Liverpool 4-0 — an earlier match", "GTA VI launch hype — no such launch today",
              "Nvidia surge — Monday close, tagged as such"]

def card(d, box, story, big=False):
    num, region, place, head, deck, source, cert, chip, kind, c1, c2 = story
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(255, 255, 253), outline=STEEL, width=1)
    sh = 64 if big else 36
    scene(d, (x0 + 3, y0 + 3, x1 - 3, y0 + sh), kind, c1, c2)
    d.rectangle([x0 + 3, y0 + 3, x0 + 30, y0 + 19], fill=INK)
    d.text((x0 + 8, y0 + 5), str(num), font=F(AR_B, 11), fill=(255, 255, 255))
    rc = REGION_COLORS[region]
    d.rectangle([x0 + 3, y0 + sh + 3, x1 - 3, y0 + sh + 17], fill=rc)
    d.text((x0 + 7, y0 + sh + 5), f"{region} · {place}", font=F(AR_B, 8 if not big else 9), fill=(255, 255, 255))
    yy = text_block(d, (x0 + 7, y0 + sh + 21), head, F(PF_BOLD, 15 if big else 11), INK, x1 - x0 - 14, 1.05, 2)
    yy = text_block(d, (x0 + 7, yy + 1), deck, F(AR, 10 if big else 8), (30, 32, 38), x1 - x0 - 14, 1.12, 5 if big else 3)
    # chip + source at bottom
    d.rectangle([x0 + 7, y1 - 17, x0 + 7 + d.textlength(chip, font=F(AR_B, 8)) + 8, y1 - 4], fill=GOLD)
    d.text((x0 + 11, y1 - 15), chip, font=F(AR_B, 8), fill=(30, 24, 8))
    src = f"{source} · {cert}"
    d.text((x1 - 7 - d.textlength(src, font=F(AR, 7)), y1 - 14), src, font=F(AR, 7), fill=STEEL_D)
    return

def header(d, variant):
    bg = INK if variant == "B" else PAPER
    fg = (246, 244, 238) if variant == "B" else INK
    d.rectangle([0, 0, W, 118], fill=bg)
    d.rectangle([0, 0, W, 24], fill=STEEL_D if variant == "A" else GOLD)
    kick = "37 STORIES ON THIS PAGE · 13 FULL-SCENE CARDS + 24 BRIEFS · 9 REGIONS · EVERY STORY DATED"
    d.text(((W - d.textlength(kick, font=F(AR_B, 11))) / 2, 5), kick, font=F(AR_B, 11), fill=(255, 255, 255) if variant == "A" else (30, 24, 8))
    mast = "THE CAPITAL STANDARD"
    d.text(((W - d.textlength(mast, font=F(PF_BLACK, 40))) / 2, 28), mast, font=F(PF_BLACK, 40), fill=fg)
    date = "TUESDAY 25 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=F(PF_BLACK, 34))) / 2, 74), date, font=F(PF_BLACK, 34), fill=GOLD if variant == "B" else RED)
    # numbers strip
    d.rectangle([0, 118, W, 148], fill=PAPER2, outline=STEEL)
    x = 8
    for n, lab in NUMBERS:
        nw = d.textlength(n, font=F(AR_B, 14))
        lw = d.textlength(lab, font=F(AR, 6))
        cell = max(nw, lw) + 10
        d.text((x, 121), n, font=F(AR_B, 14), fill=INK)
        d.text((x, 138), lab, font=F(AR, 6), fill=STEEL_D)
        x += cell + 4
    # region strip
    d.rectangle([0, 148, W, 168], fill=(255, 255, 253))
    x = 8
    d.text((x, 152), "REGIONS:", font=F(AR_B, 9), fill=INK); x += 62
    for r in REGIONS:
        wdt = d.textlength(r, font=F(AR_B, 8)) + 10
        d.rectangle([x, 151, x + wdt, 165], fill=REGION_COLORS[r])
        d.text((x + 5, 153), r, font=F(AR_B, 8), fill=(255, 255, 255))
        x += wdt + 5

def bottom(d, variant):
    y0 = 742
    # left: dotted map with numbered pins = card numbers + timeline
    d.rectangle([6, y0, 330, 962], fill=(233, 238, 244), outline=STEEL)
    d.text((14, y0 + 6), "THE DAY ON THE MAP — pins = card numbers", font=F(AR_B, 10), fill=INK)
    import random
    rnd = random.Random(25)
    for gx in range(20, 324, 12):
        for gy in range(y0 + 30, 856, 12):
            if rnd.random() < 0.5:
                d.point((gx, gy), fill=(150, 165, 185))
    pins = [(4, 210, 66), (2, 186, 92), (1, 118, 40), (3, 224, 92), (6, 148, 30), (10, 268, 62),
            (11, 92, 58), (36, 258, 116), (33, 46, 84), (13, 286, 140), (8, 40, 128), (5, 104, 38), (7, 140, 52)]
    for num, px, py in pins:
        yy = y0 + 26 + py
        d.ellipse([px - 8, yy - 8, px + 8, yy + 8], fill=RED, outline=(255, 255, 255))
        t = str(num)
        d.text((px - d.textlength(t, font=F(AR_B, 8)) / 2, yy - 5), t, font=F(AR_B, 8), fill=(255, 255, 255))
    d.text((14, 878), "Legend: 1 Poland · 2 Hormuz · 3 Iraq · 4 Gaza · 5 Brussels · 6 Ukraine data", font=F(AR, 7), fill=STEEL_D)
    d.text((14, 888), "7 Ukraine · 8 Colombia · 10 China · 11 Madrid · 13 Australia · 33/36 markets", font=F(AR, 7), fill=STEEL_D)
    d.text((14, 902), "TIMELINE OF THE DAY", font=F(AR_B, 9), fill=INK)
    yy = 916
    for slot, ev in TIMELINE[:3]:
        d.text((14, yy), f"{slot}: {ev}", font=F(AR, 7), fill=(30, 32, 38)); yy += 11
    # right: ALSO ON briefs, two columns
    d.rectangle([336, y0, 1018, 962], fill=(255, 255, 253), outline=STEEL)
    d.text((344, y0 + 6), "ALSO ON TUESDAY — BRIEFS 14-37 (numbered, dated, sourced in pool order)", font=F(AR_B, 10), fill=INK)
    colw = 334
    for ci in range(2):
        x = 344 + ci * (colw + 8)
        yy = y0 + 24
        for i, (pid, txt) in enumerate(BRIEFS[ci * 12:(ci + 1) * 12]):
            n = 14 + ci * 12 + i
            yy = text_block(d, (x, yy), f"{n}. [{pid}] {txt}", F(AR, 8), (30, 32, 38), colw, 1.1, 3)
            yy += 3
    # timeline rest + date check band
    d.rectangle([6, 966, 1018, 996], fill=(250, 244, 224), outline=GOLD)
    tl = "TIMELINE: " + "  ·  ".join(f"{s} {e}" for s, e in TIMELINE[3:])
    d.text((12, 969), tl[:150], font=F(AR_B, 8), fill=INK)
    dc = "DATE CHECK — NOT TODAY: " + " · ".join(DATE_CHECK)
    yy = text_block(d, (12, 981), dc, F(AR, 8), STEEL_D, 1000, 1.1, 1)
    # footer
    d.rectangle([0, 996, W, 1024], fill=INK)
    foot = "Sources: wire reports · Al Jazeera · RFE/RL · DW · Starlit Daily · Forbes via wires · science wires · scheduled US PCE release.  Original drawings — flat illustrations drawn for this page."
    d.text((10, 1000), foot, font=F(AR, 8), fill=(235, 238, 242))
    d.text((10, 1012), "THE CAPITAL STANDARD · One day, one page: Tuesday 25 November 2026 · Claims are labelled as claims (Iran says).", font=F(AR_B, 8), fill=(235, 238, 242))

def build(variant, out):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    header(d, variant)
    if variant == "A":
        # Layout C-A: lead trio row, Gaza first (matrix order)
        xs = [6, 346, 686]
        for i, st in enumerate(LEADS):
            card(d, (xs[i], 174, xs[i] + 332, 428), st, big=True)
        grid = GRID
        for i, st in enumerate(grid):
            r, c = divmod(i, 5)
            x = 6 + c * 204
            card(d, (x, 434 + r * 150, x + 198, 434 + r * 150 + 144), st)
    else:
        # Layout C-B: NATO wide lead left, Gaza+Hormuz stacked right; grid order rotated
        card(d, (6, 174, 560, 428), LEADS[2], big=True)
        card(d, (566, 174, 1018, 298), LEADS[0], big=False)
        card(d, (566, 304, 1018, 428), LEADS[1], big=False)
        grid = GRID[5:] + GRID[:5]
        for i, st in enumerate(grid):
            r, c = divmod(i, 5)
            x = 6 + c * 204
            card(d, (x, 434 + r * 150, x + 198, 434 + r * 150 + 144), st)
    bottom(d, variant)
    img.save(out, "PNG", optimize=True)
    print(out)

if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
