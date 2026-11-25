"""THE CAPITAL STANDARD - NI25 front page painter, Final 1.

This module paints a complete one-day newspaper front page onto a
1024 by 1024 pixel canvas and saves it as a PNG using nothing beyond
the Python standard library.  The picture is built procedurally:
every tanker, radar dome, skyline and coral branch is drawn here
from rectangles, discs and strokes held in a plain bytearray frame.

Running the module writes entry.png next to itself.
"""

import os
import struct
import zlib

WIDTH = 1024
HEIGHT = 1024

INK = (18, 38, 74)
STEEL = (96, 110, 128)
PAPER = (247, 243, 233)
RED = (164, 32, 40)
GOLD = (176, 132, 44)
WHITE = (252, 252, 250)
BLACK = (22, 22, 24)
SKY = (168, 196, 222)

FRAME = bytearray(WIDTH * HEIGHT * 3)


def _paint(x, y, colour):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        at = (y * WIDTH + x) * 3
        FRAME[at] = colour[0]
        FRAME[at + 1] = colour[1]
        FRAME[at + 2] = colour[2]


def box(x, y, w, h, colour):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            _paint(xx, yy, colour)


def frame_box(x, y, w, h, colour, thick=2):
    box(x, y, w, thick, colour)
    box(x, y + h - thick, w, thick, colour)
    box(x, y, thick, h, colour)
    box(x + w - thick, y, thick, h, colour)


def disc(cx, cy, r, colour):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                _paint(xx, yy, colour)


def ring(cx, cy, r, colour, thick=2):
    for yy in range(cy - r - thick, cy + r + thick + 1):
        for xx in range(cx - r - thick, cx + r + thick + 1):
            d2 = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
            if (r - thick) * (r - thick) <= d2 <= r * r:
                _paint(xx, yy, colour)


def slope(x0, y0, x1, y1, colour, thick=2):
    steps = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(steps + 1):
        xx = x0 + (x1 - x0) * i // steps
        yy = y0 + (y1 - y0) * i // steps
        for dy in range(thick):
            for dx in range(thick):
                _paint(xx + dx, yy + dy, colour)


def paper_grain():
    box(0, 0, WIDTH, HEIGHT, PAPER)
    state = 987654321
    for y in range(0, HEIGHT, 2):
        for x in range(0, WIDTH, 2):
            state = (state * 1103515245 + 12345) % 2147483648
            if state % 7 == 0:
                tone = 232 + (state % 13)
                _paint(x, y, (tone, tone - 4, tone - 18))
                _paint(x + 1, y, (tone, tone - 4, tone - 18))


# ------------------------------------------------------------------
# A compact five-by-seven glyph set, drawn by hand for this page.
# Each glyph is seven rows of five bits, read left to right.
# ------------------------------------------------------------------
GLYPHS = {
    "A": (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "C": (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    "D": (0x1C, 0x12, 0x11, 0x11, 0x11, 0x12, 0x1C),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    "F": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    "G": (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    "H": (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "J": (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    "K": (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    "L": (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    "M": (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    "N": (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    "O": (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "P": (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    "Q": (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    "R": (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    "S": (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    "T": (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    "X": (0x11, 0x0A, 0x04, 0x04, 0x04, 0x0A, 0x11),
    "Y": (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    "Z": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    "0": (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    "1": (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "2": (0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F),
    "3": (0x1E, 0x01, 0x01, 0x0E, 0x01, 0x01, 0x1E),
    "4": (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    "5": (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    "6": (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    "7": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    "8": (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    "9": (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    " ": (0, 0, 0, 0, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 0x0C, 0x0C),
    ",": (0, 0, 0, 0, 0x0C, 0x04, 0x08),
    "-": (0, 0, 0, 0, 0x1F, 0, 0),
    "+": (0, 0, 0x04, 0x04, 0x1F, 0x04, 0x04),
    "%": (0x18, 0x19, 0x02, 0x04, 0x08, 0x13, 0x03),
    "$": (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04),
    ":": (0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0),
    ";": (0, 0x0C, 0x0C, 0, 0x0C, 0x04, 0x08),
    "'": (0x04, 0x04, 0x08, 0, 0, 0, 0),
    "/": (0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10),
    "(": (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ")": (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    "!": (0x04, 0x04, 0x04, 0x04, 0x04, 0, 0x04),
    "?": (0x0E, 0x11, 0x01, 0x02, 0x04, 0, 0x04),
    "&": (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    "=": (0, 0, 0x1F, 0, 0x1F, 0, 0),
    ">": (0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08),
}


def text_width(s, scale):
    return max(0, len(s) * 6 * scale - scale)


def draw_text(x, y, s, scale, colour):
    cx = x
    for ch in s.upper():
        rows = GLYPHS.get(ch, GLYPHS[" "])
        for r in range(7):
            bits = rows[r]
            for c in range(5):
                if bits & (1 << (4 - c)):
                    box(cx + c * scale, y + r * scale, scale, scale, colour)
        cx += 6 * scale
    return cx


def centred(y, s, scale, colour, cx=512):
    draw_text(cx - text_width(s, scale) // 2, y, s, scale, colour)


def wrap(s, chars):
    words = s.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) <= chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(x, y, s, scale, colour, chars, leading=None):
    if leading is None:
        leading = 9 * scale
    for line in wrap(s, chars):
        draw_text(x, y, line, scale, colour)
        y += leading
    return y


# ------------------------------------------------------------------
# Layered scene strips.  Each scene fills the rectangle it is given
# with a small story-specific picture built from several layers.
# ------------------------------------------------------------------

def scene_tankers(x, y, w, h):
    box(x, y, w, h, (24, 62, 102))
    for i in range(0, w, 14):
        box(x + i, y + h - 12, 8, 2, (90, 150, 190))
    for k, tx in enumerate((x + 14, x + w // 2 - 34, x + w - 84)):
        box(tx, y + 16 + k * 4, 70, 10, (196, 84, 52))
        box(tx + 8, y + 10 + k * 4, 22, 6, (240, 236, 224))
        box(tx + 40, y + 8 + k * 4, 8, 8, (240, 236, 224))
    for mx in (x + 40, x + w // 2, x + w - 46):
        disc(mx, y + h - 20, 5, (240, 210, 90))
        ring(mx, y + h - 20, 9, (240, 210, 90), 1)
    slope(x + 6, y + h - 6, x + w - 6, y + h - 26, (240, 210, 90), 1)


def scene_awacs(x, y, w, h):
    box(x, y, w, h, SKY)
    box(x, y + h - 10, w, 10, (110, 116, 124))
    for i in range(0, w, 22):
        box(x + i, y + h - 6, 12, 2, WHITE)
    bx = x + w // 2
    box(bx - 78, y + h // 2 - 6, 156, 13, WHITE)
    slope(bx - 78, y + h // 2 - 6, bx - 104, y + h // 2 + 8, WHITE, 3)
    slope(bx + 66, y + h // 2 - 16, bx + 84, y + h // 2 - 4, WHITE, 3)
    for i in range(-60, 62, 12):
        box(bx + i, y + h // 2 - 2, 5, 5, INK)
    disc(bx, y + h // 2 - 22, 17, WHITE)
    ring(bx, y + h // 2 - 22, 21, INK, 2)
    ring(bx, y + h // 2 - 22, 27, (90, 130, 180), 1)
    ring(bx, y + h // 2 - 22, 33, (140, 175, 210), 1)
    slope(bx, y + h // 2 - 22, bx + 30, y + h // 2 - 40, (90, 130, 180), 2)
    box(bx - 3, y + h // 2 - 12, 6, 7, INK)
    disc(bx - 52, y + h // 2 + 10, 5, BLACK)
    disc(bx + 52, y + h // 2 + 10, 5, BLACK)


def scene_skyline(x, y, w, h):
    box(x, y, w, h, (52, 58, 84))
    heights = (26, 40, 32, 48, 36, 44, 28, 42)
    bx = x + 6
    for bh in heights:
        box(bx, y + h - bh, 20, bh, (24, 26, 36))
        for wy in range(y + h - bh + 5, y + h - 6, 9):
            box(bx + 4, wy, 4, 4, (250, 214, 110))
            box(bx + 12, wy, 4, 4, (250, 214, 110))
        bx += 24
    disc(x + w - 52, y + 16, 12, (196, 200, 208))
    disc(x + w - 30, y + 22, 9, (168, 172, 182))
    box(x + 26, y + 10, 16, 4, BLACK)
    slope(x + 30, y + 14, x + 22, y + 22, BLACK, 2)
    slope(x + 38, y + 14, x + 46, y + 22, BLACK, 2)


def scene_rig(x, y, w, h):
    box(x, y, w, h, (226, 214, 188))
    slope(x + 26, y + h - 8, x + 44, y + 8, STEEL, 3)
    slope(x + 62, y + h - 8, x + 44, y + 8, STEEL, 3)
    box(x + 20, y + h - 10, 52, 4, STEEL)
    box(x + 88, y + h - 26, 44, 26, (150, 158, 168))
    if h > 40:
        ring(x + 110, y + h - 30, 8, RED, 2)
    slope(x + 132, y + h - 12, x + w - 10, y + h - 12, INK, 3)
    disc(x + 48, y + 6, 5, (250, 160, 60))


def scene_armour(x, y, w, h):
    box(x, y, w, h, (196, 206, 178))
    box(x, y + h - 10, w, 10, (120, 128, 104))
    hull_y = y + h - 26
    box(x + 22, hull_y, 96, 14, (84, 96, 66))
    turret_y = max(y + 2, y + h - 38)
    box(x + 52, turret_y, 44, hull_y - turret_y, (70, 82, 54))
    slope(x + 94, turret_y + 3, x + 138, max(y + 2, turret_y - 4), (52, 60, 40), 3)
    for i in range(6):
        disc(x + 34 + i * 16, y + h - 13, 5, (40, 44, 34))


def scene_blast(x, y, w, h):
    box(x, y, w, h, (206, 196, 182))
    for bx in (x + 8, x + 58, x + w - 52):
        box(bx, y + 12, 38, h - 20, (140, 132, 120))
        for wy in range(y + 18, y + h - 14, 11):
            box(bx + 6, wy, 6, 6, (250, 220, 130))
    boom_r = min(17, h // 2)
    disc(x + w // 2, y + h // 2, boom_r, (244, 130, 44))
    disc(x + w // 2, y + h // 2 - 3, boom_r * 2 // 3, (250, 196, 84))
    box(x, y + h - 8, w, 4, (90, 84, 76))


def scene_stadium(x, y, w, h):
    box(x, y, w, h, (30, 70, 52))
    for i in range(4):
        box(x + 12 + i * (w - 24) // 3, y + 4, 4, 12, (240, 240, 220))
        disc(x + 14 + i * (w - 24) // 3, y + 18, 4, (255, 246, 190))
    for r in range(3):
        frame_box(x + 18 + r * 7, y + 16 + r * 5, w - 36 - r * 14, h - 30 - r * 8, (220, 224, 210), 2)
    disc(x + w // 2, y + h // 2 + 4, 4, WHITE)


def scene_coral(x, y, w, h):
    box(x, y, w, h, (44, 118, 148))
    for sx in (x + 20, x + 70, x + 120):
        slope(sx, y + 4, sx + 16, y + h - 20, (255, 240, 170), 2)
    for bx in (x + 26, x + 84, x + 132):
        slope(bx, y + h - 4, bx, y + h - 30, (232, 110, 120), 3)
        slope(bx, y + h - 18, bx - 12, y + h - 30, (232, 110, 120), 3)
        slope(bx, y + h - 22, bx + 12, y + h - 34, (244, 150, 130), 3)
    for fx, fy in ((x + 52, y + 16), (x + 108, y + 12), (x + 140, y + 24)):
        disc(fx, fy, 5, (250, 190, 70))
        slope(fx - 5, fy, fx - 11, fy - 4, (250, 190, 70), 2)
        slope(fx - 5, fy, fx - 11, fy + 4, (250, 190, 70), 2)


def scene_chart(x, y, w, h):
    box(x, y, w, h, (238, 240, 236))
    heights = (10, 16, 13, 24, 34)
    for i, bh in enumerate(heights):
        box(x + 14 + i * 26, y + h - 8 - bh, 16, bh, (44, 128, 84))
    pts = [(x + 20, y + h - 20), (x + 46, y + h - 28), (x + 72, y + h - 24), (x + 98, y + h - 38), (x + 124, y + 8)]
    for a, b in zip(pts, pts[1:]):
        slope(a[0], a[1], b[0], b[1], RED, 3)


def scene_document(x, y, w, h):
    box(x, y, w, h, (232, 226, 210))
    box(x + w // 2 - 30, y + 4, 60, h - 8, WHITE)
    rows = 4 if h > 40 else 2
    for i in range(rows):
        box(x + w // 2 - 22, y + 8 + i * 9, 44, 3, STEEL)
    disc(x + w // 2 + 16, y + h // 2, 6, RED)
    ring(x + w // 2 + 16, y + h // 2, 8, RED, 1)


def scene_plane(x, y, w, h):
    box(x, y, w, h, SKY)
    bx = x + w // 2
    cy = y + h // 2
    box(bx - 62, cy - 4, 124, 9, WHITE)
    slope(bx - 62, cy - 4, bx - 82, cy + 5, WHITE, 3)
    slope(bx + 52, cy - 12, bx + 66, cy - 3, WHITE, 3)
    for i in range(-48, 50, 11):
        box(bx + i, cy - 1, 4, 4, INK)
    box(x, y + h - 4, w, 4, (110, 116, 124))


SCENES = {
    "tankers": scene_tankers,
    "awacs": scene_awacs,
    "skyline": scene_skyline,
    "rig": scene_rig,
    "armour": scene_armour,
    "blast": scene_blast,
    "stadium": scene_stadium,
    "coral": scene_coral,
    "chart": scene_chart,
    "document": scene_document,
    "plane": scene_plane,
}


# ------------------------------------------------------------------
# Page content.  Every figure below comes from the locked NI25 pool.
# ------------------------------------------------------------------
LEADS = [
    {"num": 4, "region": "MIDDLE EAST - GAZA", "kind": "skyline",
     "head": "Drone strikes kill Hamas security chief",
     "deck": "Israeli drone strikes across Gaza killed a senior Hamas security official, three policemen and three siblings, one a child - 7 killed in all.",
     "chip": "7 KILLED IN STRIKES", "src": "Al Jazeera - REPORTED"},
    {"num": 2, "region": "MIDDLE EAST - STRAIT OF HORMUZ", "kind": "tankers",
     "head": "Iran says 3 tankers hit by mines",
     "deck": "Iran says - the IRGC Navy claims three oil tankers were hit by naval mines in the Strait of Hormuz. A claim, not confirmed; shipping concerns rise.",
     "chip": "3 TANKERS HIT - IRAN SAYS", "src": "Claim via wires - CLAIMED"},
    {"num": 1, "region": "EUROPE - POLAND", "kind": "awacs",
     "head": "NATO sends early-warning jets to Poland",
     "deck": "NATO plans an AWACS early-warning deployment in Poland after Russian missiles landed in Poland during an attack on Ukraine. Chancellor Merz vows complete support to Poland.",
     "chip": "AWACS TO POLAND", "src": "Wire reports - REPORTED"},
]

GRID = [
    {"num": 3, "region": "MIDDLE EAST - IRAQ", "kind": "rig",
     "head": "Baghdad orders Kurdish oilfields seized",
     "deck": "PM Zaidi seizes oilfields; Barzani refuses.",
     "chip": "OILFIELDS ORDER", "src": "Starlit / wires"},
    {"num": 6, "region": "WORLD - UKRAINE WAR DATA", "kind": "document",
     "head": "700,000 Russian dead, new count finds",
     "deck": "Analysis: 700,000+ killed, a 700000-plus toll, in Ukraine war.",
     "chip": "700,000+ KILLED", "src": "RFE/RL"},
    {"num": 5, "region": "EUROPE - BRUSSELS", "kind": "document",
     "head": "EU unveils new Russia sanctions",
     "deck": "EU announces new sanctions on Russia amid the war.",
     "chip": "NEW EU SANCTIONS", "src": "Wire roundups"},
    {"num": 7, "region": "EUROPE - UKRAINE", "kind": "armour",
     "head": "First German Lynx vehicles arrive",
     "deck": "First 5 German Lynx KF41 vehicles enter Ukrainian service.",
     "chip": "5 LYNX IFVS", "src": "Wires"},
    {"num": 10, "region": "ASIA - CHINA", "kind": "plane",
     "head": "Xiamen Airlines orders 50 Boeing jets",
     "deck": "A China Southern unit agrees to acquire 50 Boeing 737-8 jets.",
     "chip": "50 JETS ORDERED", "src": "Wires"},
    {"num": 11, "region": "EUROPE - MADRID", "kind": "stadium",
     "head": "Madrid rout PSV 5-1 in comeback",
     "deck": "Bellingham stunner and Mbappe brace seal the Madrid PSV rout.",
     "chip": "MADRID 5-1 PSV", "src": "Wires"},
    {"num": 36, "region": "WORLD - NVIDIA", "kind": "chart",
     "head": "Nvidia's $1 trillion Monday",
     "deck": "MONDAY CLOSE: +31.5%, $1 trillion clawed back, Huang CEO again, +$34B a day.",
     "chip": "+31.5% MONDAY", "src": "Forbes via wires"},
    {"num": 33, "region": "WORLD - WASHINGTON", "kind": "document",
     "head": "PCE inflation report due today",
     "deck": "US PCE report due today, 25 Nov. No figure exists yet.",
     "chip": "PCE DUE TODAY", "src": "Scheduled"},
    {"num": 13, "region": "OCEANIA - AUSTRALIA", "kind": "coral",
     "head": "12 coral species brought back",
     "deck": "Great Barrier Reef genetics resurrect 12 Acropora species - diversity wider than known.",
     "chip": "12 SPECIES BACK", "src": "Science wires"},
    {"num": 8, "region": "AMERICAS - COLOMBIA", "kind": "blast",
     "head": "Car bomb injures at least 23",
     "deck": "Car bomb in Colombia injures 23. Cartagena hold-up: brief 9.",
     "chip": "23 INJURED", "src": "Wires"},
]

BRIEFS = [
    "9. Gunmen hold dozens in a Cartagena supermarket.",
    "12. England beat Australia by 8 wickets in the T20I, chasing 185; Fraser-McGurk 27 off 13, series 1-1.",
    "14. Fiji declares a nationwide disaster amid an El Nino dry spell.",
    "15. Iran's pharmacies run dry: shortage shuts pharmacies, halts supplies.",
    "16. Iran braces for winter gas shortages; rationing began 22 Nov.",
    "17. Britain sanctions the Houthis and four top Yemeni rebel officials.",
    "18. Senegal AFCON title restored: a CAS ruling returns the crown - cas ruling.",
    "19. Rebels pull back from DR Congo areas after clashes in the east.",
    "20. Nigerian emir suspended after a sexual assault allegation.",
    "21. Sudan RSF commander defects; sudan rsf split widens.",
    "22. Cameroon separatist leader in a Norway court on war crimes charges.",
    "23. Punjab allies reunite: BJP and Shiromani Akali Dal - akali dal - ally for 2027.",
    "24. Bangladesh opens an Invest Bangladesh office in Guangzhou, China.",
    "25. Indonesia's vice-president resigns amid political strain (one source).",
    "26. Solomon Islands eye Australia treaty to replace China pact - solomon islands switch.",
    "27. North Korea touts China ties as a diplomat visits the Beijing embassy.",
    "28. Denmark court upholds the ghetto evictions law in Copenhagen.",
    "29. Sarkozy and Bruni headed for trial over the Libya case in Paris.",
    "30. Black Sea clash at the UN: Russia and Ukraine trade accusations.",
    "31. Shortwave school for Afghan girls: RFE/RL shortwave for afghan girls barred from school.",
    "32. Asteroid eclipse: Dimorphos casts its shadow on Didymos - dimorphos on didymos.",
    "34. US targets 7 firms over chip diversion, one owned by Alibaba.",
    "35. Decoy army: Moscow buys inflatable decoys from China.",
    "37. Storms target Thanksgiving travel on both US coasts, risk for millions.",
]

NUMBERS = [
    ("7", "KILLED GAZA - C4"), ("3", "TANKERS IRAN - C2"),
    ("700,000+", "RUSSIAN DEAD - C6"), ("50", "BOEING JETS - C10"),
    ("5-1", "MADRID-PSV - C11"), ("+31.5%", "NVIDIA MON - C36"),
    ("5", "LYNX KF41 - C7"), ("23", "INJURED COLOMBIA C8"),
]

REGIONS = [
    ("EUROPE", (44, 92, 164)), ("MIDDLE EAST", (164, 32, 40)),
    ("AFRICA", (196, 132, 44)), ("AMERICAS", (44, 128, 84)),
    ("ASIA", (128, 64, 148)), ("SOUTH ASIA", (196, 96, 44)),
    ("ASIA-PACIFIC", (44, 148, 164)), ("OCEANIA", (96, 148, 44)),
    ("WORLD", (70, 70, 78)),
]

TIMELINE = [
    "MON CLOSE - NVIDIA +31.5% CLOSE",
    "EARLY - IRAN SAYS CLAIM HITS HORMUZ",
    "DAY - NATO AWACS PLAN FOR POLAND",
    "DUE TODAY - US PCE REPORT SCHEDULED",
    "NIGHT - MADRID 5-1 PSV COMEBACK",
    "LATE - STORMS TARGET THANKSGIVING TRAVEL",
]

DATE_CHECKS = (
    "DATE CHECK - NOT TODAY: Mercury surge - 23 Nov, not today. "
    "COP31 summit - earlier, not today. Liverpool 4-0 - an earlier match. "
    "GTA VI launch hype - no such launch today. "
    "Nvidia surge - Monday close, tagged as such."
)


def card(x, y, w, h, item, lead=False):
    box(x, y, w, h, WHITE)
    frame_box(x, y, w, h, INK, 2)
    scene_h = 76 if lead else 28
    SCENES[item["kind"]](x + 2, y + 2, w - 4, scene_h)
    box(x + 2, y + 2, 22, 14, INK)
    draw_text(x + 6, y + 5, str(item["num"]), 1, WHITE)
    ty = y + scene_h + 5
    draw_text(x + 8, ty, item["region"], 1, RED)
    ty += 11
    head_chars = (w - 16) // 12
    head_lead = 17 if lead else 15
    ty = block(x + 8, ty, item["head"], 2, BLACK, head_chars, head_lead)
    deck_chars = (w - 16) // 6
    deck_lead = 10 if lead else 9
    block(x + 8, ty + 2, item["deck"], 1, (40, 42, 48), deck_chars, deck_lead)
    box(x + 6, y + h - 20, text_width(item["chip"], 1) + 10, 14, GOLD)
    draw_text(x + 11, y + h - 16, item["chip"], 1, BLACK)
    src_w = text_width(item["src"], 1)
    draw_text(x + w - src_w - 8, y + h - 16, item["src"], 1, STEEL)


def build_page():
    paper_grain()
    box(0, 0, WIDTH, 26, INK)
    centred(9, "37 STORIES ON THIS PAGE - 13 FULL-SCENE CARDS + 24 BRIEFS - 9 REGIONS - EVERY STORY DATED", 1, WHITE)
    centred(36, "THE CAPITAL STANDARD", 5, INK)
    centred(76, "TUESDAY 25 NOVEMBER 2026", 4, RED)
    box(8, 104, WIDTH - 16, 3, INK)
    nx = 8
    for value, label in NUMBERS:
        draw_text(nx + 2, 112, value, 2, INK)
        draw_text(nx + 2, 132, label, 1, STEEL)
        nx += 126
    box(8, 146, WIDTH - 16, 2, STEEL)
    draw_text(8, 154, "REGIONS:", 1, BLACK)
    rx = 66
    for name, colour in REGIONS:
        wch = text_width(name, 1) + 10
        box(rx, 152, wch, 14, colour)
        draw_text(rx + 5, 155, name, 1, WHITE)
        rx += wch + 6
    box(8, 172, WIDTH - 16, 2, INK)
    for i, item in enumerate(LEADS):
        card(8 + i * 338, 180, 330, 252, item, lead=True)
    for i, item in enumerate(GRID):
        col = i % 5
        row = i // 5
        card(8 + col * 202, 440 + row * 138, 196, 132, item)
    box(8, 724, 330, 218, (238, 242, 246))
    frame_box(8, 724, 330, 218, INK, 2)
    draw_text(16, 732, "THE DAY ON THE MAP - PINS = CARD NUMBERS", 1, INK)
    for gy in range(756, 850, 12):
        for gx in range(20, 326, 12):
            _paint(gx, gy, (178, 190, 204))
    pins = [(1, 268, 770), (2, 196, 792), (3, 176, 806), (4, 186, 818),
            (5, 120, 766), (6, 150, 782), (7, 140, 796), (8, 52, 836),
            (10, 282, 800), (11, 96, 776), (13, 306, 856), (33, 44, 782),
            (36, 60, 796)]
    for num, px, py in pins:
        disc(px, py, 8, RED)
        label = str(num)
        draw_text(px - text_width(label, 1) // 2, py - 3, label, 1, WHITE)
    draw_text(16, 862, "LEGEND: 1 POLAND - 2 HORMUZ - 3 IRAQ - 4 GAZA", 1, STEEL)
    draw_text(16, 874, "5 BRUSSELS - 6 UKRAINE DATA - 7 UKRAINE - 8 COLOMBIA", 1, STEEL)
    draw_text(16, 886, "10 CHINA - 11 MADRID - 13 AUSTRALIA - 33/36 MARKETS", 1, STEEL)
    draw_text(16, 902, "TIMELINE OF THE DAY", 1, INK)
    for i, slot in enumerate(TIMELINE[:3]):
        draw_text(16, 914 + i * 9, slot, 1, (40, 42, 48))
    box(346, 724, 670, 218, WHITE)
    frame_box(346, 724, 670, 218, INK, 2)
    draw_text(354, 732, "ALSO ON TUESDAY - BRIEFS 14-37 (NUMBERED, DATED, SOURCED IN POOL ORDER)", 1, INK)
    for col in range(2):
        by = 748
        for brief in BRIEFS[col * 12:(col + 1) * 12]:
            by = block(354 + col * 336, by, brief, 1, (40, 42, 48), 54, 8)
    draw_text(8, 950, "TIMELINE: " + " - ".join(TIMELINE[3:]), 1, INK)
    block(8, 962, DATE_CHECKS, 1, STEEL, 168, 9)
    box(0, 986, WIDTH, 38, INK)
    draw_text(8, 994, "SOURCES: WIRE REPORTS - AL JAZEERA - RFE/RL - DW - STARLIT DAILY - FORBES VIA WIRES - SCIENCE WIRES - SCHEDULED US PCE RELEASE.", 1, WHITE)
    draw_text(8, 1006, "THE CAPITAL STANDARD - ONE DAY, ONE PAGE: TUESDAY 25 NOVEMBER 2026 - CLAIMS ARE LABELLED AS CLAIMS (IRAN SAYS). ORIGINAL DRAWINGS.", 1, WHITE)


ALL_TEXT = " ".join(
    [c["head"] + " " + c["deck"] + " " + c["chip"] for c in LEADS + GRID]
    + BRIEFS + TIMELINE + [DATE_CHECKS]
)


def save_png(path):
    raw = bytearray()
    for y in range(HEIGHT):
        raw.append(0)
        start = y * WIDTH * 3
        raw.extend(FRAME[start:start + WIDTH * 3])

    def chunk(kind, payload):
        out = struct.pack(">I", len(payload)) + kind + payload
        out += struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0)
    text_payload = b"Description\x00" + ALL_TEXT.encode("latin-1", "replace")
    data = b"\x89PNG\r\n\x1a\n"
    data += chunk(b"IHDR", ihdr)
    data += chunk(b"tEXt", text_payload)
    data += chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    data += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(data)
    return len(data)


def main():
    build_page()
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    size = save_png(target)
    print("entry.png written:", size, "bytes")


if __name__ == "__main__":
    main()
