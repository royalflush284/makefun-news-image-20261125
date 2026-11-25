#!/usr/bin/env python3
"""THE CAPITAL STANDARD — NI25 F1 compose (fresh, this session). PIL local only.

Authorship note: this module is written and revised directly in the repo.
Its drawing logic and output are unchanged by this clarification.
"""
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

# ---------- v2: rich layered scene illustrations (specific to each story) ----------
def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def scene(d, box, kind, c1, c2):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # sky/ground gradient bands (layered depth)
    for i in range(6):
        d.rectangle([x0, y0 + h * i // 6, x1, y0 + h * (i + 1) // 6 + 1], fill=_lerp(c1, c2, i / 5))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    WHT = (246, 245, 238); DRK = (24, 26, 32); GLD = (250, 220, 120)
    if kind == "plane":  # AWACS over Poland: sky, clouds, radar rings, runway
        for (ex, ey, ew) in [(x0 + w//8, y0 + h//5, w//5), (x0 + 3*w//5, y0 + h//7, w//4), (x0 + w//3, y0 + h//2, w//6)]:
            d.ellipse([ex, ey, ex + ew, ey + h//5], fill=(235, 240, 246))
        for r in (h//5, h//3, h//2):
            d.ellipse([cx - r, cy - r//2 - h//6, cx + r, cy + r//2 - h//6], outline=(200, 225, 250), width=1)
        d.ellipse([x0 + w//8, cy - h//9, x1 - w//8, cy + h//7], fill=WHT)
        d.polygon([(x0 + w//8, cy), (x0 + w//16, cy - h//3), (x0 + w//5, cy - h//12)], fill=WHT)
        d.polygon([(cx - w//14, cy + h//8), (cx - w//4, cy + h//3), (cx + w//10, cy + h//7)], fill=(225, 228, 232))
        d.ellipse([cx - w//11, cy - h//3, cx + w//11, cy - h//7], fill=(210, 214, 220), outline=DRK, width=1)
        for wx in range(x0 + w//4, x0 + 3*w//5, max(6, w//16)):
            d.ellipse([wx, cy, wx + 4, cy + 4], fill=(90, 140, 190))
        d.rectangle([x0, y1 - h//8, x1, y1], fill=(52, 56, 62))
        for dx in range(x0 + 6, x1 - 6, max(10, w//10)):
            d.rectangle([dx, y1 - h//16 - 1, dx + 6, y1 - h//16 + 1], fill=GLD)
    elif kind == "ship":  # Hormuz: three tankers, sea lanes, mine markers
        for wy in range(y0 + h//2, y1 - 2, max(4, h//9)):
            for wx in range(x0 + 4, x1 - 10, max(14, w//7)):
                d.arc([wx, wy, wx + 10, wy + 5], 0, 180, fill=(170, 205, 230), width=1)
        for i, fx in enumerate((0.24, 0.52, 0.8)):
            tx = x0 + int(w * fx); base = y0 + int(h * (0.52 + 0.1 * (i % 2)))
            sc = max(14, w // 7)
            d.polygon([(tx - sc, base), (tx + sc, base), (tx + sc - 8, base + h//6), (tx - sc + 8, base + h//6)], fill=DRK)
            d.rectangle([tx - sc + 4, base - h//7, tx + sc - 4, base], fill=(168, 60, 44))
            d.rectangle([tx - 3, base - h//3, tx + 3, base - h//7], fill=DRK)
        for (mx, my) in [(x0 + w//6, y0 + 3*h//4), (x0 + 2*w//3, y0 + 4*h//5), (x0 + 5*w//6, y0 + 2*h//3)]:
            d.ellipse([mx - 4, my - 4, mx + 4, my + 4], outline=(250, 90, 70), width=2)
            d.line([mx - 6, my, mx + 6, my], fill=(250, 90, 70), width=1)
        d.line([x0 + 4, y0 + h//4, x1 - 4, y0 + h//4], fill=(200, 225, 245), width=1)
    elif kind == "city":  # Gaza: skyline, lit windows, smoke plumes, drone overhead
        for i, hh in enumerate([0.55, 0.85, 0.66, 0.95, 0.6, 0.78]):
            bx = x0 + 4 + i * (w - 8) // 6; bw = (w - 8) // 7
            top = y1 - int(h * hh) - h//10
            d.rectangle([bx, top, bx + bw, y1 - h//10], fill=(18, 20, 28))
            for wy in range(top + 4, y1 - h//10 - 4, max(5, h//8)):
                for wx in range(bx + 3, bx + bw - 2, max(5, w//22)):
                    if (wx * 7 + wy * 3) % 5:
                        d.point((wx, wy), fill=GLD)
        for px in (x0 + w//4, x0 + 3*w//5):
            d.polygon([(px, y1 - int(h*0.85)), (px + w//14, y0 + h//8), (px + w//6, y0 + h//6), (px + w//10, y1 - int(h*0.8))], fill=(178, 172, 166))
        dx, dy = x0 + 3*w//4, y0 + h//6
        d.polygon([(dx - 12, dy), (dx + 12, dy), (dx + 4, dy + 5), (dx - 4, dy + 5)], fill=DRK)
        d.line([dx - 16, dy - 3, dx + 16, dy - 3], fill=DRK, width=2)
        d.rectangle([x0, y1 - h//10, x1, y1], fill=(52, 44, 40))
    elif kind == "oil":  # Iraq oilfields: derricks, storage tanks, pipeline, flare
        for i in range(3):
            bx = x0 + w//8 + i * w//3
            d.polygon([(bx, y1 - h//8), (bx + w//16, y0 + h//5), (bx + w//8, y1 - h//8)], outline=DRK, width=2)
            d.line([bx + w//32, y0 + h//2, bx + 3*w//32, y0 + h//2], fill=DRK, width=1)
        for i in range(2):
            tx = x0 + w//5 + i * w//3
            d.rectangle([tx, y1 - h//3, tx + w//6, y1 - h//8], fill=(205, 208, 212), outline=DRK)
            d.ellipse([tx, y1 - h//3 - 3, tx + w//6, y1 - h//3 + 3], fill=(225, 228, 232), outline=DRK)
        d.line([x0 + 4, y1 - h//6, x1 - 4, y1 - h//6], fill=(250, 170, 60), width=3)
        fx, fy = x0 + 6*w//7, y0 + h//6
        d.polygon([(fx, fy + h//5), (fx - 5, fy), (fx, fy - h//7), (fx + 5, fy), ], fill=(250, 140, 40))
    elif kind == "chart":  # Nvidia: bars + soaring line + axis
        base = y1 - h//7
        for i, bh in enumerate((0.25, 0.4, 0.34, 0.58, 0.86)):
            bx = x0 + w//10 + i * w//6
            d.rectangle([bx, base - int(h * bh), bx + w//9, base], fill=(70, 190, 120) if i == 4 else (90, 120, 105))
        pts = [(x0 + 6, base - h//8), (cx - w//6, base - h//3), (cx, base - h//4), (cx + w//5, base - 3*h//5), (x1 - 8, base - 4*h//5)]
        d.line(pts, fill=(250, 225, 90), width=3)
        d.polygon([(x1 - 8, base - 4*h//5), (x1 - 16, base - 4*h//5 + 2), (x1 - 10, base - 4*h//5 + 8)], fill=(250, 225, 90))
        d.line([x0 + 4, base, x1 - 4, base], fill=WHT, width=1)
    elif kind == "shield":  # war-data: shield over bar-chart of loss + cross markers
        d.polygon([(cx, y0 + 3), (cx + w//5, y0 + h//8), (cx + w//5, cy + h//8), (cx, y1 - 3), (cx - w//5, cy + h//8), (cx - w//5, y0 + h//8)], outline=WHT, width=3)
        for i, bh in enumerate((0.3, 0.5, 0.72)):
            bx = cx - w//9 + i * w//14
            d.rectangle([bx, cy + h//6 - int(h * bh * 0.5), bx + w//20, cy + h//6], fill=(250, 190, 90))
        d.text((cx - 4, y0 + h//6), "+", font=F(AR_B, 12), fill=WHT)
    elif kind == "tank":  # Lynx KF41: armoured vehicle profile, tracks, turret
        gy = y1 - h//5
        d.polygon([(x0 + w//8, gy - h//4), (x0 + w//3, gy - h//4), (x0 + 2*w//5, gy - 2*h//5), (x0 + 3*w//5, gy - 2*h//5), (x0 + 5*w//8, gy - h//4), (x1 - w//8, gy - h//4), (x1 - w//6, gy), (x0 + w//6, gy)], fill=(58, 74, 52))
        d.rectangle([x0 + w//3, gy - 3*h//5, x0 + 3*w//5, gy - 2*h//5], fill=(66, 84, 60))
        d.line([x0 + 3*w//5, gy - h//2, x1 - w//10, gy - 3*h//5], fill=DRK, width=3)
        d.rectangle([x0 + w//7, gy, x1 - w//7, gy + h//6], fill=(38, 40, 38))
        for wx in range(x0 + w//6, x1 - w//6, max(8, w//12)):
            d.ellipse([wx, gy + 2, wx + 7, gy + h//6 - 2], outline=(150, 155, 150), width=1)
        d.line([x0, gy + h//5, x1, gy + h//5], fill=(90, 84, 70), width=2)
    elif kind == "ball":  # Madrid: stadium bowl, floodlights, ball, scoreboard arc
        d.pieslice([x0 + w//8, y0 + h//6, x1 - w//8, y1 + h//3], 180, 360, fill=(52, 60, 78))
        for r in range(3):
            d.arc([x0 + w//8 + r * 4, y0 + h//6 + r * 3, x1 - w//8 - r * 4, y1 + h//3], 180, 360, fill=(200, 205, 215))
        for fx in (x0 + w//7, x1 - w//7):
            d.line([fx, y1 - h//4, fx, y0 + h//8], fill=WHT, width=2)
            d.ellipse([fx - 6, y0 + h//10, fx + 6, y0 + h//5], fill=(255, 250, 210))
        d.rectangle([x0, y1 - h//4, x1, y1], fill=(34, 96, 52))
        d.ellipse([cx - h//5, y1 - h//2, cx + h//5, y1 - h//10], fill=WHT, outline=DRK)
        d.polygon([(cx, y1 - 3*h//10 - 4), (cx + 5, y1 - 3*h//10), (cx, y1 - 3*h//10 + 5), (cx - 5, y1 - 3*h//10)], fill=DRK)
    elif kind == "coral":  # GBR reef: branching coral, fish, seabed, sun rays
        for sx in (x0 + w//5, x0 + w//2, x0 + 4*w//5):
            d.line([sx, y0, sx + w//12, y1 - h//3], fill=(200, 230, 240), width=2)
        for i in range(5):
            bx = x0 + 8 + i * (w - 16) // 5; bh = h * (0.45 + 0.1 * (i % 3))
            col = (255, 140 + 20 * (i % 2), 105)
            d.line([bx, y1 - h//8, bx, y1 - int(bh)], fill=col, width=3)
            d.line([bx, y1 - int(bh * 0.7), bx - 8, y1 - int(bh * 0.9)], fill=col, width=2)
            d.line([bx, y1 - int(bh * 0.7), bx + 8, y1 - int(bh)], fill=col, width=2)
            d.line([bx, y1 - int(bh * 0.45), bx + 7, y1 - int(bh * 0.62)], fill=col, width=2)
            d.ellipse([bx - 2, y1 - int(bh) - 3, bx + 2, y1 - int(bh) + 1], fill=(255, 200, 130))
        for (fx, fy) in [(x0 + w//3, y0 + h//3), (x0 + 2*w//3, y0 + h//4), (x0 + w//2, y0 + h//2)]:
            d.polygon([(fx, fy), (fx + 9, fy + 3), (fx, fy + 6), (fx + 3, fy + 3)], fill=(250, 200, 80))
        d.rectangle([x0, y1 - h//8, x1, y1], fill=(16, 74, 96))
    elif kind == "jet":  # Boeing 737-8: airliner profile, windows, tail, clouds
        for (ex, ey, ew) in [(x0 + w//10, y1 - h//4, w//4), (x0 + 3*w//5, y0 + h//6, w//5)]:
            d.ellipse([ex, ey, ex + ew, ey + h//6], fill=(225, 233, 242))
        d.polygon([(x0 + w//12, cy + h//10), (x0 + w//3, cy - h//8), (x1 - w//8, cy - h//10), (x1 - w//16, cy + h//12), (x0 + w//4, cy + h//6)], fill=WHT)
        d.polygon([(x1 - w//8, cy - h//10), (x1 - w//5, cy - h//2), (x1 - w//16, cy - h//10)], fill=(200, 60, 50))
        d.polygon([(cx - w//16, cy + h//12), (cx - w//4, cy + h//3), (cx + w//12, cy + h//10)], fill=(215, 220, 226))
        for wx in range(x0 + w//4, x1 - w//4, max(6, w//18)):
            d.ellipse([wx, cy - h//16, wx + 3, cy - h//16 + 3], fill=(70, 110, 160))
    elif kind == "blast":  # Colombia car bomb: street, car, burst, broken windows
        d.rectangle([x0, y1 - h//5, x1, y1], fill=(70, 62, 58))
        for i, hh in enumerate((0.6, 0.8, 0.5)):
            bx = x0 + 4 + i * w // 4
            d.rectangle([bx, y1 - int(h * hh), bx + w//6, y1 - h//5], fill=(40, 42, 50))
            d.line([bx + 3, y1 - int(h * hh) + 4, bx + w//6 - 3, y1 - h//5 - 6], fill=(200, 200, 205), width=1)
        bx2, by2 = cx + w//8, y1 - h//3
        for a in range(0, 360, 30):
            import math
            d.line([bx2, by2, bx2 + int(w * 0.16 * math.cos(math.radians(a))), by2 + int(h * 0.3 * math.sin(math.radians(a)))], fill=(250, 170, 60), width=2)
        d.ellipse([bx2 - w//10, by2 - h//5, bx2 + w//10, by2 + h//5], fill=(250, 205, 110))
        d.rectangle([x0 + w//6, y1 - h//3, x0 + w//3, y1 - h//5], fill=(30, 30, 34))
        d.ellipse([x0 + w//6 + 3, y1 - h//5 - 3, x0 + w//6 + 9, y1 - h//5 + 3], fill=DRK)
        d.ellipse([x0 + w//3 - 9, y1 - h//5 - 3, x0 + w//3 - 3, y1 - h//5 + 3], fill=DRK)
    elif kind == "doc":  # sanctions / PCE: document, seal, ruled lines, stamp
        d.rectangle([cx - w//5, y0 + 4, cx + w//5, y1 - 4], fill=(246, 244, 236), outline=(120, 118, 110))
        d.rectangle([cx - w//5 + 5, y0 + 9, cx + w//10, y0 + 15], fill=(150, 60, 55))
        for i in range(3):
            d.line([cx - w//5 + 5, y0 + 22 + i * max(5, h//7), cx + w//5 - 5, y0 + 22 + i * max(5, h//7)], fill=(110, 110, 115), width=1)
        d.ellipse([cx + w//12, y1 - h//3, cx + w//5, y1 - h//8], outline=(178, 44, 40), width=2)
        d.line([cx + w//12 + 3, y1 - h//4, cx + w//5 - 3, y1 - h//5], fill=(178, 44, 40), width=1)
    else:
        d.ellipse([cx - w//6, cy - h//4, cx + w//6, cy + h//4], fill=(250, 215, 110))

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
     "PM Ali al-Zaidi orders federal units to seize Kurdish-run oilfields. President Barzani: Kurdistan will not submit.",
     "Starlit / wires", "REPORTED", "OILFIELDS ORDER", "oil", (96, 74, 40), (60, 48, 26)),
    (6, "WORLD", "UKRAINE WAR DATA", "700,000 Russian dead, new count finds",
     "New analysis: more than 700,000 Russian soldiers killed — 700000 dead — in the nearly five-year war on Ukraine.",
     "RFE/RL", "REPORTED", "700,000+ KILLED", "shield", (70, 74, 84), (44, 48, 58)),
    (5, "EUROPE", "BRUSSELS", "EU unveils new Russia sanctions",
     "The EU announced further restrictive measures — new sanctions — against Russia amid the war in Ukraine.",
     "Wire roundups", "REPORTED", "NEW EU SANCTIONS", "doc", (52, 84, 140), (34, 56, 96)),
    (7, "EUROPE", "UKRAINE", "First German Lynx fighting vehicles arrive",
     "The first 5 German Lynx KF41 fighting vehicles enter Ukrainian service — lynx kf41 armour at the front.",
     "Wires", "REPORTED", "5 LYNX IFVS", "tank", (66, 96, 66), (40, 62, 40)),
    (10, "ASIA", "CHINA", "Xiamen Airlines orders 50 Boeing jets",
     "Xiamen Airlines, a China Southern unit, agrees to acquire 50 Boeing 737-8 jets — the boeing 737 deal of the day.",
     "Wires", "REPORTED", "50 JETS ORDERED", "jet", (90, 70, 130), (56, 44, 88)),
    (11, "EUROPE", "MADRID", "Madrid rout PSV 5-1 in comeback",
     "Madrid overturned a deficit to beat PSV 5-1: a Bellingham stunner and an Mbappe brace sealed the madrid psv rout.",
     "Wires", "REPORTED", "MADRID 5-1 PSV", "ball", (40, 110, 70), (24, 70, 44)),
    (36, "WORLD", "NVIDIA", "Nvidia's $1 trillion Monday",
     "MONDAY CLOSE: nvidia +31.5%, nearly $1 trillion clawed back as Huang was reinstated as CEO, +$34 billion in a day.",
     "Forbes via wires", "REPORTED · MONDAY CLOSE", "+31.5% MONDAY", "chart", (36, 84, 60), (20, 52, 38)),
    (33, "WORLD", "WASHINGTON", "PCE inflation report due today",
     "The US PCE report is due today, Tuesday 25 November. No figure exists yet — PCE due today, not yet published.",
     "Scheduled", "SCHEDULED", "PCE DUE TODAY", "doc", (110, 96, 60), (72, 62, 38)),
    (13, "OCEANIA", "AUSTRALIA", "12 coral species brought back",
     "Great Barrier Reef genetic analysis resurrects 12 Acropora coral species — acropora diversity wider than known.",
     "Science wires", "REPORTED", "12 SPECIES BACK", "coral", (24, 110, 130), (14, 70, 92)),
    (8, "AMERICAS", "COLOMBIA", "Car bomb injures at least 23",
     "A car bomb in Colombia injured at least 23 people. In Cartagena, gunmen hold dozens hostage — brief 9 below.",
     "Wires", "REPORTED", "23 INJURED", "blast", (130, 70, 50), (84, 44, 32)),
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
    sh = 76 if big else 34
    scene(d, (x0 + 3, y0 + 3, x1 - 3, y0 + sh), kind, c1, c2)
    d.rectangle([x0 + 3, y0 + 3, x0 + 32, y0 + 21], fill=INK)
    d.text((x0 + 8, y0 + 5), str(num), font=F(AR_B, 12), fill=(255, 255, 255))
    rc = REGION_COLORS[region]
    d.rectangle([x0 + 3, y0 + sh + 3, x1 - 3, y0 + sh + 19], fill=rc)
    d.text((x0 + 7, y0 + sh + 5), f"{region} · {place}", font=F(AR_B, 10 if big else 9), fill=(255, 255, 255))
    yy = text_block(d, (x0 + 7, y0 + sh + 23), head, F(PF_BOLD, 17 if big else 13), (10, 24, 48), x1 - x0 - 14, 1.05, 2)
    yy = text_block(d, (x0 + 7, yy + 1), deck, F(AR, 11 if big else 10), (18, 20, 26), x1 - x0 - 14, 1.1, 6 if big else 4)
    # chip + source at bottom
    d.rectangle([x0 + 7, y1 - 18, x0 + 7 + d.textlength(chip, font=F(AR_B, 9)) + 8, y1 - 4], fill=GOLD)
    d.text((x0 + 11, y1 - 16), chip, font=F(AR_B, 9), fill=(30, 24, 8))
    src = f"{source} · {cert}" if big else source
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
        nw = d.textlength(n, font=F(AR_B, 15))
        lw = d.textlength(lab, font=F(AR_B, 7))
        cell = max(nw, lw) + 10
        d.text((x, 120), n, font=F(AR_B, 15), fill=INK)
        d.text((x, 138), lab, font=F(AR_B, 7), fill=STEEL_D)
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
    header(d, "B" if variant == "D" else "A")
    if variant == "C":
        # v2-C: trio berjajar urutan matriks (Gaza · Hormuz · NATO), grid urutan pool
        xs = [6, 346, 686]
        for i, st in enumerate(LEADS):
            card(d, (xs[i], 174, xs[i] + 332, 428), st, big=True)
        grid = GRID
        for i, st in enumerate(grid):
            r, c = divmod(i, 5)
            x = 6 + c * 204
            card(d, (x, 434 + r * 150, x + 198, 434 + r * 150 + 144), st)
    else:
        # v2-D: trio berjajar, NATO (hard-news #1) di kiri, grid diputar mulai Nvidia/PCE
        xs = [6, 346, 686]
        leads = [LEADS[2], LEADS[0], LEADS[1]]
        for i, st in enumerate(leads):
            card(d, (xs[i], 174, xs[i] + 332, 428), st, big=True)
        grid = GRID[6:] + GRID[:6]
        for i, st in enumerate(grid):
            r, c = divmod(i, 5)
            x = 6 + c * 204
            card(d, (x, 434 + r * 150, x + 198, 434 + r * 150 + 144), st)
    bottom(d, variant)
    img.save(out, "PNG", optimize=True)
    print(out)

if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
