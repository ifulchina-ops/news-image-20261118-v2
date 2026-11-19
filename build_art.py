#!/usr/bin/env python3
"""Eighteen V2 — one front page summing up Wednesday 18 November 2026.

Draws a newspaper front page with PIL (stdlib + Pillow only, no network):
a masthead, count bars, a day-in-numbers strip, 13 illustrated numbered
stories, a world map with numbered pins, 29 numbered briefs in 3 columns,
and a DATE CHECK footer. Run:  python3 build_art.py  -> writes entry.png
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (25, 23, 19)
RED = (158, 27, 27)
NAVY = (31, 58, 95)
GREY = (90, 86, 78)
LINE = (60, 55, 48)
OCEAN = (207, 224, 232)
LAND = (157, 187, 122)
LAND_LINE = (110, 140, 85)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


REGION_COLORS = {
    "EUROPE": (38, 90, 150),
    "MIDDLE EAST": (176, 124, 22),
    "ASIA": (146, 58, 138),
    "AFRICA": (34, 128, 84),
    "AMERICAS": (178, 62, 52),
    "OCEANIA": (42, 140, 140),
    "WORLD": (70, 70, 70),
}

# (number, region, field, tag, headline, deck, lon, lat)
ILLUSTRATED = [
    (1, "MIDDLE EAST", "War & security", "MIDDLE EAST - IRAN WAR",
     "Kuwait and Bahrain intercept Iranian drones",
     "Iran says it aimed at US forces at Ali Al Salem.",
     47.5, 29.3, "drones"),
    (2, "ASIA", "Politics & diplomacy", "ASIA - APEC, CHINA",
     "Xi greets Trump as APEC opens in Shenzhen",
     "A first three-way meeting with Putin is set for Thursday.",
     114.0, 22.5, "summit"),
    (3, "WORLD", "Climate & space", "WORLD - CLIMATE",
     "COP31 splits over a fossil-fuel phase-out",
     "Antalya talks argue over the draft as Friday nears.",
     30.7, 36.9, "climate"),
    (4, "MIDDLE EAST", "War & security", "MIDDLE EAST - GAZA",
     "Board of Peace warns the Gaza truce may collapse",
     "Its report to the UN faults both Israel and Hamas.",
     34.45, 31.5, "peace"),
    (5, "ASIA", "Economy & labour", "ASIA - LABOUR",
     "Bangladesh wage protests shut 55 factories",
     "A highway blocked; police report about 300 arrests.",
     90.4, 23.8, "factory"),
    (6, "WORLD", "Climate & space", "WORLD - SPACE",
     "Voyager 1 is one light-day from Earth",
     "The first human-made object that far, 49 years on.",
     -150.0, -32.0, "voyager"),
    (7, "AMERICAS", "War & security", "AMERICAS - HAITI",
     "In Haiti, Salvadoran troops raid a gang boss's home",
     "El Salvador's president hails the raid in Canaan.",
     -72.3, 18.9, "haiti"),
    (8, "EUROPE", "War & security", "EUROPE - UKRAINE WAR",
     "Russian strikes kill at least 5 in Ukraine",
     "Officials report drone and missile hits, Odesa among them.",
     30.5, 50.45, "ukraine"),
    (9, "AFRICA", "War & security", "AFRICA - HORN",
     "Ethiopia and Eritrea mass troops on the border",
     "Both within striking distance, Reuters sources say.",
     39.0, 14.5, "troops"),
    (10, "WORLD", "Society & culture", "WORLD - GAMES",
     "GTA VI goes on sale at midnight",
     "The launch rolls out by time zone, New Zealand first.",
     174.0, -41.0, "gta"),
    (11, "EUROPE", "Economy & labour", "EUROPE - ECONOMY",
     "Bailey: a long Iran war could mean more rate rises",
     "The Bank of England governor warns on oil-led inflation.",
     -0.1, 51.5, "bailey"),
    (12, "OCEANIA", "Politics & diplomacy", "OCEANIA - DIPLOMACY",
     "Australia sanctions settler leader Daniella Weiss",
     "With the UK, it targets West Bank settler violence.",
     149.1, -35.3, "sanctions"),
    (13, "ASIA", "Disasters & weather", "ASIA - WEATHER",
     "Cyclone Akvan nears India's east coast",
     "Landfall in Andhra Pradesh is forecast for Friday.",
     88.0, 16.0, "cyclone"),
]

# (number, region, field, one-line brief, lon, lat)
BRIEFS = [
    (14, "AMERICAS", "Politics & diplomacy",
     "US: House Democrats list Trump-era probe targets.", -77.0, 38.9),
    (15, "AMERICAS", "Tech",
     "US: crisis talks over a string of tech outages.", -77.0, 38.9),
    (16, "AMERICAS", "Politics & diplomacy",
     "US: transport chief blames L3Harris for FAA stop.", -77.0, 38.9),
    (17, "AMERICAS", "Tech",
     "US: Senate plans AI hearings after strategy row.", -77.0, 38.9),
    (18, "AMERICAS", "Economy & labour",
     "US: strike fears at LA and Long Beach ports.", -118.2, 34.0),
    (19, "AMERICAS", "Disasters & weather",
     "Houston: explosion at a Clean Harbors plant.", -95.4, 29.8),
    (20, "AMERICAS", "Society & culture",
     "California: Six Flags coaster linked to third death.", -118.2, 34.0),
    (21, "AMERICAS", "Tech",
     "Canada: minister says Meta talks are confidential.", -75.7, 45.4),
    (22, "AMERICAS", "Politics & diplomacy",
     "Mexico: Sheinbaum says US trade talks progressing.", -99.1, 19.4),
    (23, "AMERICAS", "Politics & diplomacy",
     "Venezuela: Hegseth meets the interim leaders.", -66.9, 10.5),
    (24, "EUROPE", "War & security",
     "Russia: nuclear-capable bombers sent to Asia.", 37.6, 55.8),
    (25, "EUROPE", "Justice",
     "Poland: says it foiled a Russian sabotage plot.", 21.0, 52.2),
    (26, "EUROPE", "Politics & diplomacy",
     "UK: Lammy sketches a route back into the EU.", -0.1, 51.5),
    (27, "EUROPE", "Economy & labour",
     "Germany: first national financial-education plan.", 13.4, 52.5),
    (28, "EUROPE", "Society & culture",
     "Italy: fascist-era tribute in parliament angers MPs.", 12.5, 41.9),
    (29, "EUROPE", "Disasters & weather",
     "Scotland: Portobello beach rated \u201cpoor\u201d, first in 9 years.", -3.2, 55.95),
    (30, "EUROPE", "Economy & labour",
     "EU: proposes a \u20ac45bn loan for Ukraine in 2027.", 4.35, 50.85),
    (31, "EUROPE", "War & security",
     "Bulgaria: sunk LPG tanker was hit by projectiles.", 23.3, 42.7),
    (32, "ASIA", "Justice",
     "Myanmar: ICJ sets its Rohingya genocide ruling.", 96.1, 16.8),
    (33, "ASIA", "War & security",
     "Kashmir: Indian forces kill a militant commander.", 74.9, 34.1),
    (34, "ASIA", "War & security",
     "Bangladesh: MP\u2019s clinic bombed in Gopalganj.", 89.8, 23.0),
    (35, "ASIA", "Politics & diplomacy",
     "Philippines: Trump meets Imelda Marcos in Manila.", 121.0, 14.6),
    (36, "ASIA", "Politics & diplomacy",
     "South Korea: Lee seeks China\u2019s help for peace.", 127.0, 37.5),
    (37, "ASIA", "Politics & diplomacy",
     "Malaysia: minutes show AG opposed Najib house arrest.", 101.7, 3.1),
    (38, "MIDDLE EAST", "War & security",
     "Yemen: Saudi-led forces step up strikes on Houthis.", 44.2, 15.4),
    (39, "MIDDLE EAST", "Economy & labour",
     "Lebanon: World Bank says rebuilding is lagging.", 35.5, 33.9),
    (40, "MIDDLE EAST", "War & security",
     "Saudi Arabia: Houthi missile aimed at Riyadh downed.", 46.7, 24.7),
    (41, "AFRICA", "Economy & labour",
     "South Africa: inflation 5.2%, highest since 2024.", 28.0, -26.2),
    (42, "WORLD", "Society & culture",
     "World: Pew: Muslims could outnumber Christians by 2035.", 0.0, 20.0),
]

NUMBERS = [
    ("55", "factories shut"),
    ("~300", "arrests"),
    ("1 light-day", "Voyager 1 out"),
    ("49 years", "since launch"),
    ("5+", "killed in Ukraine"),
    ("300,000", "sign petition"),
]

REGION_ORDER = ["EUROPE", "MIDDLE EAST", "ASIA", "AFRICA", "AMERICAS",
                "OCEANIA", "WORLD"]
FIELD_ORDER = ["War & security", "Politics & diplomacy", "Economy & labour",
               "Society & culture", "Disasters & weather", "Tech",
               "Climate & space", "Justice"]


def check_counts():
    """The bars on the page must match the stories actually printed."""
    all_stories = [(r, f) for _, r, f, *_ in ILLUSTRATED]
    all_stories += [(r, f) for _, r, f, *_ in BRIEFS]
    assert len(ILLUSTRATED) == 13, len(ILLUSTRATED)
    assert len(BRIEFS) == 29, len(BRIEFS)
    assert len(all_stories) == 42, len(all_stories)
    regions = {r: sum(1 for rr, _ in all_stories if rr == r) for r in REGION_ORDER}
    fields = {f: sum(1 for _, ff in all_stories if ff == f) for f in FIELD_ORDER}
    assert regions == {"EUROPE": 10, "MIDDLE EAST": 5, "ASIA": 9, "AFRICA": 2,
                       "AMERICAS": 11, "OCEANIA": 1, "WORLD": 4}, regions
    assert fields == {"War & security": 11, "Politics & diplomacy": 10,
                      "Economy & labour": 7, "Society & culture": 4,
                      "Disasters & weather": 3, "Tech": 3,
                      "Climate & space": 2, "Justice": 2}, fields
    return regions, fields


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 3
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def num_badge(draw, x, y, n, size=20):
    draw.rectangle([x, y, x + size, y + size], fill=RED)
    f = font(SANS_B, 12 if size <= 20 else 14)
    tw = draw.textlength(str(n), font=f)
    draw.text((x + (size - tw) / 2, y + (size - f.size) / 2 - 1),
              str(n), font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- illustrations
def draw_drones(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 205, 222))
    d.polygon([(x, y + h * 0.62), (x + w * 0.4, y + h * 0.55),
               (x + w * 0.7, y + h * 0.7), (x + w, y + h * 0.6),
               (x + w, y + h), (x, y + h)], fill=(214, 196, 160))
    d.rectangle([x + w * 0.78, y + h * 0.42, x + w * 0.86, y + h * 0.62],
                fill=(120, 110, 95))
    for cx, cy in [(0.25, 0.25), (0.45, 0.18), (0.62, 0.3)]:
        px, py = x + w * cx, y + h * cy
        d.ellipse([px - 9, py - 3, px + 9, py + 3], fill=(40, 40, 40))
        d.line([px - 14, py - 6, px + 14, py - 6], fill=(40, 40, 40), width=2)
    for cx, cy in [(0.55, 0.55), (0.72, 0.45)]:
        px, py = x + w * cx, y + h * cy
        for k in range(8):
            ang = k * 0.785
            d.line([px, py, px + 13 * math.cos(ang),
                    py + 13 * math.sin(ang)], fill=(230, 170, 40),
                   width=3)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(230, 170, 40))
    d.line([x + w * 0.7, y + h * 0.62, x + w * 0.62, y + h * 0.75],
           fill=(255, 255, 255), width=2)
    d.line([x + w * 0.7, y + h * 0.62, x + w * 0.85, y + h * 0.78],
           fill=(255, 255, 255), width=2)


def draw_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 228))
    d.polygon([(x, y + h), (x + w * 0.25, y + h * 0.45), (x + w * 0.5, y + h),
               (x + w * 0.75, y + h * 0.5), (x + w, y + h)],
              fill=(150, 160, 170))
    for fx, col in [(0.08, (222, 40, 40)), (0.82, (60, 80, 180))]:
        d.rectangle([x + w * fx, y + h * 0.08, x + w * (fx + 0.13), y + h * 0.38],
                    fill=col)
        d.line([x + w * fx, y + h * 0.08, x + w * fx, y + h * 0.85],
               fill=(60, 60, 60), width=2)
    for px, suit, skin in [(0.38, (30, 30, 34), (232, 190, 150)),
                           (0.58, (40, 50, 90), (235, 195, 160))]:
        cx, cy = x + w * px, y + h * 0.62
        d.ellipse([cx - 13, cy - 26, cx + 13, cy], fill=skin)
        d.polygon([(cx - 20, y + h), (cx - 16, cy + 2), (cx + 16, cy + 2),
                   (cx + 20, y + h)], fill=suit)
        d.polygon([(cx - 5, cy + 2), (cx, cy + 16), (cx + 5, cy + 2)],
                  fill=(255, 255, 255))
    d.ellipse([x + w * 0.45, y + h * 0.52, x + w * 0.55, y + h * 0.62],
              fill=(240, 220, 180))


def draw_climate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 226))
    cx, cy, r = x + w * 0.30, y + h * 0.45, h * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 160, 200))
    d.ellipse([cx - r * 0.7, cy - r * 0.5, cx - r * 0.1, cy + r * 0.1],
              fill=(110, 180, 110))
    d.ellipse([cx + r * 0.15, cy + r * 0.2, cx + r * 0.75, cy + r * 0.7],
              fill=(110, 180, 110))
    d.rectangle([x + w * 0.62, y + h * 0.55, x + w * 0.92, y + h * 0.85],
                fill=(200, 200, 195))
    d.rectangle([x + w * 0.66, y + h * 0.38, x + w * 0.74, y + h * 0.55],
                fill=(150, 90, 80))
    d.rectangle([x + w * 0.80, y + h * 0.45, x + w * 0.86, y + h * 0.55],
                fill=(150, 90, 80))
    d.line([x + w * 0.66, y + h * 0.66, x + w * 0.88, y + h * 0.66],
           fill=(90, 90, 90), width=2)
    d.line([x + w * 0.66, y + h * 0.74, x + w * 0.88, y + h * 0.74],
           fill=(90, 90, 90), width=2)


def draw_peace(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 205))
    d.polygon([(x, y + h), (x + w * 0.3, y + h * 0.6), (x + w * 0.6, y + h * 0.75),
               (x + w, y + h * 0.55), (x + w, y + h)], fill=(190, 175, 150))
    d.line([x + w * 0.15, y + h * 0.85, x + w * 0.85, y + h * 0.15],
           fill=(90, 120, 60), width=4)
    for t in [0.2, 0.4, 0.6, 0.8]:
        px, py = x + w * (0.15 + 0.7 * t), y + h * (0.85 - 0.7 * t)
        d.ellipse([px - 16, py - 6, px + 2, py + 6], fill=(110, 150, 70))
        d.ellipse([px - 2, py - 14, px + 14, py + 2], fill=(130, 170, 85))
    d.line([x + w * 0.3, y + h * 0.62, x + w * 0.55, y + h * 0.9],
           fill=(90, 80, 70), width=3)


def draw_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 208, 192))
    d.rectangle([x + w * 0.08, y + h * 0.5, x + w * 0.6, y + h * 0.88],
                fill=(170, 120, 90))
    d.rectangle([x + w * 0.62, y + h * 0.62, x + w * 0.92, y + h * 0.88],
                fill=(90, 110, 140))
    for i in range(3):
        d.rectangle([x + w * (0.14 + i * 0.14), y + h * 0.58,
                     x + w * (0.22 + i * 0.14), y + h * 0.7], fill=(240, 220, 150))
    d.rectangle([x + w * 0.52, y + h * 0.25, x + w * 0.57, y + h * 0.5],
                fill=(120, 110, 100))
    for px in (0.15, 0.3, 0.45):
        cx = x + w * px
        d.ellipse([cx - 7, y + h * 0.72, cx + 7, y + h * 0.86], fill=(60, 60, 60))
        d.rectangle([cx - 9, y + h * 0.86, cx + 9, y + h], fill=(80, 90, 140))
    d.ellipse([x + w * 0.7, y + h * 0.68, x + w * 0.84, y + h * 0.82],
              fill=(240, 240, 240))
    d.rectangle([x + w * 0.68, y + h * 0.8, x + w * 0.86, y + h * 0.88],
                fill=(40, 70, 160))


def draw_voyager(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 48))
    import random
    rnd = random.Random(7)
    for _ in range(28):
        sx, sy = x + rnd.random() * w, y + rnd.random() * h
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    d.ellipse([x + w * 0.06, y + h * 0.62, x + w * 0.2, y + h * 0.86],
              fill=(90, 160, 200))
    d.ellipse([x + w * 0.09, y + h * 0.68, x + w * 0.15, y + h * 0.78],
              fill=(110, 180, 110))
    cx, cy = x + w * 0.68, y + h * 0.4
    d.line([cx - 18, cy - 8, cx + 18, cy + 8], fill=(200, 200, 200), width=3)
    d.ellipse([cx - 22, cy - 20, cx + 2, cy + 4], fill=(220, 220, 220))
    d.polygon([(cx - 6, cy + 4), (cx + 26, cy - 6), (cx + 20, cy + 14)],
              fill=(180, 180, 180))
    for i in range(6):
        px = x + w * (0.22 + i * 0.07)
        py = y + h * (0.8 - i * 0.06)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(240, 200, 90))


def draw_haiti(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 214, 200))
    d.rectangle([x + w * 0.1, y + h * 0.45, x + w * 0.45, y + h * 0.85],
                fill=(190, 170, 140))
    d.polygon([(x + w * 0.08, y + h * 0.45), (x + w * 0.28, y + h * 0.3),
               (x + w * 0.47, y + h * 0.45)], fill=(150, 70, 60))
    d.rectangle([x + w * 0.55, y + h * 0.6, x + w * 0.92, y + h * 0.85],
                fill=(90, 110, 80))
    d.ellipse([x + w * 0.58, y + h * 0.78, x + w * 0.66, y + h * 0.86],
              fill=(40, 40, 40))
    d.ellipse([x + w * 0.82, y + h * 0.78, x + w * 0.9, y + h * 0.86],
              fill=(40, 40, 40))
    for px in (0.62, 0.78):
        cx = x + w * px
        d.ellipse([cx - 6, y + h * 0.5, cx + 6, y + h * 0.62], fill=(210, 180, 140))
        d.rectangle([cx - 8, y + h * 0.62, cx + 8, y + h * 0.78], fill=(70, 90, 60))


def draw_ukraine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 44, 66))
    d.rectangle([x + w * 0.06, y + h * 0.35, x + w * 0.3, y + h * 0.9],
                fill=(24, 28, 44))
    d.rectangle([x + w * 0.4, y + h * 0.5, x + w * 0.62, y + h * 0.9],
                fill=(24, 28, 44))
    for bx, by in [(0.1, 0.45), (0.16, 0.55), (0.44, 0.6), (0.52, 0.7)]:
        d.rectangle([x + w * bx, y + h * by, x + w * bx + 5, y + h * by + 6],
                    fill=(240, 200, 90))
    d.line([x + w * 0.7, y + h * 0.15, x + w * 0.75, y + h * 0.9],
           fill=(120, 120, 120), width=4)
    d.line([x + w * 0.82, y + h * 0.15, x + w * 0.77, y + h * 0.9],
           fill=(120, 120, 120), width=4)
    d.line([x + w * 0.68, y + h * 0.3, x + w * 0.84, y + h * 0.3],
           fill=(120, 120, 120), width=3)
    for cx, cy in [(0.88, 0.3), (0.94, 0.55)]:
        px, py = x + w * cx, y + h * cy
        for k in range(8):
            ang = k * 0.785
            d.line([px, py, px + 10 * math.cos(ang),
                    py + 10 * math.sin(ang)], fill=(240, 170, 60),
                   width=2)


def draw_troops(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 206, 180))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(150, 140, 110))
    for tx in (0.12, 0.55):
        bx, by = x + w * tx, y + h * 0.62
        d.rectangle([bx, by - 18, bx + w * 0.3, by], fill=(90, 100, 70))
        d.rectangle([bx + w * 0.08, by - 30, bx + w * 0.2, by - 18],
                    fill=(90, 100, 70))
        d.line([bx + w * 0.2, by - 26, bx + w * 0.32, by - 26],
               fill=(70, 80, 55), width=3)
        d.ellipse([bx + 4, by - 2, bx + 14, by + 8], fill=(50, 50, 50))
        d.ellipse([bx + w * 0.3 - 14, by - 2, bx + w * 0.3 - 4, by + 8],
                  fill=(50, 50, 50))
    d.polygon([(x + w * 0.4, y + h * 0.15), (x + w * 0.55, y + h * 0.4),
               (x + w * 0.7, y + h * 0.15)], fill=(140, 130, 110))
    d.line([x + w * 0.85, y + h * 0.1, x + w * 0.85, y + h * 0.5],
           fill=(60, 60, 60), width=2)
    d.rectangle([x + w * 0.85, y + h * 0.1, x + w * 0.97, y + h * 0.2],
                fill=(200, 60, 50))


def draw_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(48, 32, 84))
    cx, cy = x + w * 0.32, y + h * 0.5
    d.rounded_rectangle([cx - 42, cy - 22, cx + 42, cy + 22], radius=14,
                        fill=(240, 240, 240))
    d.ellipse([cx - 32, cy - 6, cx - 18, cy + 8], fill=(60, 60, 60))
    for ox, oy in [(22, -8), (30, 0), (22, 8), (14, 0)]:
        d.ellipse([cx + ox - 4, cy + oy - 4, cx + ox + 4, cy + oy + 4],
                  fill=(200, 60, 90))
    cx2, cy2 = x + w * 0.78, y + h * 0.48
    d.ellipse([cx2 - 22, cy2 - 22, cx2 + 22, cy2 + 22], fill=(250, 250, 250),
              outline=(40, 40, 40), width=3)
    d.line([cx2, cy2, cx2, cy2 - 16], fill=(40, 40, 40), width=3)
    d.line([cx2, cy2, cx2 + 11, cy2], fill=(40, 40, 40), width=3)


def draw_bailey(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 226, 220))
    d.polygon([(x + w * 0.1, y + h * 0.35), (x + w * 0.3, y + h * 0.18),
               (x + w * 0.5, y + h * 0.35)], fill=(120, 110, 95))
    d.rectangle([x + w * 0.12, y + h * 0.35, x + w * 0.48, y + h * 0.85],
                fill=(180, 170, 155))
    for i in range(3):
        d.rectangle([x + w * (0.16 + i * 0.11), y + h * 0.42,
                     x + w * (0.22 + i * 0.11), y + h * 0.8], fill=(120, 110, 95))
    d.line([x + w * 0.58, y + h * 0.75, x + w * 0.68, y + h * 0.55,
            x + w * 0.78, y + h * 0.62, x + w * 0.92, y + h * 0.3],
           fill=(178, 40, 40), width=5)
    d.polygon([(x + w * 0.92, y + h * 0.3), (x + w * 0.84, y + h * 0.3),
               (x + w * 0.92, y + h * 0.42)], fill=(178, 40, 40))
    d.text((x + w * 0.6, y + h * 0.82), "\u00a3  rates",
           font=font(SANS_B, 13), fill=(60, 60, 60))


def draw_sanctions(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
    d.rectangle([x + w * 0.08, y + h * 0.2, x + w * 0.55, y + h * 0.8],
                fill=(250, 250, 250), outline=(120, 120, 120), width=2)
    d.line([x + w * 0.14, y + h * 0.34, x + w * 0.49, y + h * 0.34],
           fill=(90, 90, 90), width=2)
    d.line([x + w * 0.14, y + h * 0.46, x + w * 0.49, y + h * 0.46],
           fill=(90, 90, 90), width=2)
    d.line([x + w * 0.14, y + h * 0.58, x + w * 0.38, y + h * 0.58],
           fill=(90, 90, 90), width=2)
    d.rectangle([x + w * 0.14, y + h * 0.64, x + w * 0.3, y + h * 0.72],
                fill=(178, 40, 40))
    cx, cy = x + w * 0.76, y + h * 0.42
    d.rectangle([cx - 26, cy - 10, cx + 26, cy + 10], fill=(120, 85, 50))
    d.line([cx + 8, cy, cx + 34, cy + 26], fill=(120, 85, 50), width=5)
    d.ellipse([cx - 20, cy + 22, cx + 20, cy + 34], fill=(90, 60, 35))


def draw_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 210, 228))
    d.polygon([(x, y + h * 0.72), (x + w * 0.35, y + h * 0.66),
               (x + w * 0.5, y + h * 0.8), (x + w * 0.42, y + h),
               (x, y + h)], fill=(200, 185, 140))
    cx, cy = x + w * 0.58, y + h * 0.48
    for k in range(3):
        r0 = 8 + k * 11
        pts = []
        for a in range(0, 300, 12):
            ang = math.radians(a)
            r = r0 + a * 0.07
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.85))
        d.line(pts, fill=(255, 255, 255), width=4)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(240, 240, 240))
    d.text((x + 6, y + h - 16), "BAY OF BENGAL",
           font=font(SANS_B, 10), fill=(40, 70, 110))


ILLUS = {"drones": draw_drones, "summit": draw_summit, "climate": draw_climate,
         "peace": draw_peace, "factory": draw_factory, "voyager": draw_voyager,
         "haiti": draw_haiti, "ukraine": draw_ukraine, "troops": draw_troops,
         "gta": draw_gta, "bailey": draw_bailey, "sanctions": draw_sanctions,
         "cyclone": draw_cyclone}

CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-55, 62),
     (-60, 47), (-70, 42), (-80, 32), (-85, 26), (-90, 20), (-95, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-150, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-40, -10), (-35, -20), (-45, -30),
     (-55, -35), (-65, -40), (-70, -50), (-73, -40), (-75, -25), (-80, -15)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 20), (43, 12), (48, 10), (40, 0), (35, -10), (30, -20), (25, -30),
     (15, -30), (12, -18), (8, 0), (0, 5), (-8, 5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 60), (28, 62), (30, 60), (28, 55), (23, 45),
     (19, 42), (12, 44), (8, 44), (3, 42), (0, 39), (-2, 37), (-9, 37)],
    [(30, 60), (40, 68), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72),
     (160, 70), (178, 66), (170, 60), (160, 55), (142, 50), (140, 40),
     (130, 35), (127, 40), (120, 30), (110, 20), (105, 10), (100, 8),
     (95, 15), (90, 22), (80, 15), (75, 8), (70, 20), (60, 25), (55, 27),
     (50, 30), (45, 29), (40, 32), (35, 36), (30, 36), (30, 42), (30, 50)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (147, -39),
     (150, -37), (153, -27), (150, -22), (146, -19), (142, -11), (136, -12),
     (132, -12), (126, -14), (122, -17)],
]


def build():
    regions, fields = check_counts()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 22  # side margin

    # ---- kicker ------------------------------------------------------
    f_kick = font(SANS_B, 12)
    d.text((mx, 8), "THE WORLD'S NEWS IN ONE PICTURE", font=f_kick, fill=RED)
    right = "42 STORIES  \u00b7  7 REGIONS  \u00b7  8 FIELDS  \u00b7  13 ILLUSTRATED  \u00b7  ALL FROM WEDNESDAY"
    d.text((W - mx - d.textlength(right, font=f_kick), 8), right, font=f_kick,
           fill=RED)
    d.line([mx, 28, W - mx, 28], fill=INK, width=2)

    # ---- masthead ----------------------------------------------------
    f_head = font(SERIF_B, 56)
    d.text((mx, 34), "Wednesday 18 November 2026", font=f_head, fill=INK)
    d.line([mx, 98, W - mx, 98], fill=INK, width=3)

    # ---- region bar --------------------------------------------------
    y = 104
    seg_w = (W - 2 * mx) / 7.0
    f_reg = font(SANS_B, 11)
    for i, r in enumerate(REGION_ORDER):
        x0 = mx + i * seg_w
        d.rectangle([x0, y, x0 + seg_w - 2, y + 22], fill=REGION_COLORS[r])
        label = "%s %d" % (r, regions[r])
        tw = d.textlength(label, font=f_reg)
        d.text((x0 + (seg_w - 2 - tw) / 2, y + 5), label, font=f_reg,
               fill=(255, 255, 255))

    # ---- field bar ---------------------------------------------------
    y = 130
    d.rectangle([mx, y, W - mx, y + 20], fill=INK)
    f_field = font(SANS_B, 10)
    parts = ["BY FIELD:"] + ["%s %d" % (f, fields[f]) for f in FIELD_ORDER]
    txt = "   ".join(parts)
    while d.textlength(txt, font=f_field) > W - 2 * mx - 8 and f_field.size > 8:
        f_field = font(SANS_B, f_field.size - 1)
        txt = "   ".join(parts)
    d.text((mx + 6, y + 4), txt, font=f_field, fill=(255, 255, 255))

    # ---- day in numbers (auto-fit to one line) -----------------------
    y = 154
    f_num = font(SANS_B, 11)
    f_num_l = font(SANS, 10)

    def numbers_width(fn, fnl):
        total = d.textlength("THE DAY IN NUMBERS:  ", font=fn)
        for val, lab in NUMBERS:
            total += d.textlength(val + " ", font=fn)
            total += d.textlength(lab + "   \u00b7   ", font=fnl)
        return total

    while numbers_width(f_num, f_num_l) > W - 2 * mx and f_num.size > 8:
        f_num = font(SANS_B, f_num.size - 1)
        f_num_l = font(SANS, f_num_l.size - 1)
    x = mx
    d.text((x, y), "THE DAY IN NUMBERS:", font=f_num, fill=RED)
    x += d.textlength("THE DAY IN NUMBERS:  ", font=f_num)
    for val, lab in NUMBERS:
        d.text((x, y), val + " ", font=f_num, fill=RED)
        x += d.textlength(val + " ", font=f_num)
        d.text((x, y), lab + "   \u00b7   ", font=f_num_l, fill=INK)
        x += d.textlength(lab + "   \u00b7   ", font=f_num_l)
    d.line([mx, 176, W - mx, 176], fill=LINE, width=1)

    # ---- illustrated stories -----------------------------------------
    def card(story, x, y, w, h, large):
        n, region, field, tag, head, deck, lon, lat, art = story
        d.rectangle([x, y, x + w, y + h], outline=LINE, width=1)
        ah = 100 if large else 56
        ILLUS[art](d, x + 1, y + 1, w - 2, ah)
        num_badge(d, x + 5, y + 5, n, 22 if large else 18)
        ty = y + ah + 4
        col = REGION_COLORS[region]
        f_tag = font(SANS_B, 10 if large else 9)
        tw = d.textlength(tag, font=f_tag)
        d.rectangle([x + 6, ty, x + 6 + tw + 8, ty + 15], fill=col)
        d.text((x + 10, ty + 2), tag, font=f_tag, fill=(255, 255, 255))
        ty += 19
        f_head2 = font(SERIF_B, 19 if large else 13)
        lines = wrap(d, head, f_head2, w - 12)
        ty = text_block(d, x + 6, ty, lines[:3 if large else 4], f_head2,
                        leading=(20 if large else 14))
        f_deck = font(SANS, 11 if large else 10)
        dlines = wrap(d, deck, f_deck, w - 12)
        text_block(d, x + 6, ty + 1, dlines[:2], f_deck,
                   fill=(70, 66, 58), leading=(13 if large else 11))

    # row 1: 3 large cards
    y0 = 182
    cw = (W - 2 * mx - 16) // 3
    for i, s in enumerate(ILLUSTRATED[:3]):
        card(s, mx + i * (cw + 8), y0, cw, 204, True)
    # rows 2-3: 5 small cards each
    y1 = y0 + 210
    cw2 = (W - 2 * mx - 32) // 5
    for row, group in enumerate([ILLUSTRATED[3:8], ILLUSTRATED[8:13]]):
        yy = y1 + row * 156
        for i, s in enumerate(group):
            card(s, mx + i * (cw2 + 8), yy, cw2, 150, False)

    # ---- map + briefs ------------------------------------------------
    y2 = y1 + 2 * 156 + 8
    d.text((mx, y2), "WHERE IT HAPPENED", font=font(SERIF_B, 15), fill=RED)
    d.text((mx + 272, y2), "ALSO ON WEDNESDAY 18 NOVEMBER",
           font=font(SERIF_B, 15), fill=RED)
    d.line([mx, y2 + 22, W - mx, y2 + 22], fill=INK, width=2)

    map_x, map_y, map_w, map_h = mx, y2 + 28, 250, 158

    def proj(lon, lat):
        px = map_x + (lon + 180.0) / 360.0 * map_w
        py = map_y + (90.0 - lat) / 180.0 * map_h
        return px, py

    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=OCEAN,
                outline=LINE, width=1)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for n, region, field, tag, head, deck, lon, lat, art in ILLUSTRATED:
        if n == 6:  # Voyager 1 is in deep space, not on the map
            continue
        px, py = proj(lon, lat)
        px = min(max(px, map_x + 9), map_x + map_w - 9)
        py = min(max(py, map_y + 9), map_y + map_h - 9)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        f_pin = font(SANS_B, 9)
        tw = d.textlength(str(n), font=f_pin)
        d.text((px - tw / 2, py - 5), str(n), font=f_pin, fill=(255, 255, 255))
    # pin 6: a star at the map's lower edge for Voyager 1
    sx, sy = map_x + 14, map_y + map_h - 14
    d.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=RED,
              outline=(255, 255, 255), width=1)
    f_pin = font(SANS_B, 9)
    d.text((sx - 3, sy - 5), "6", font=f_pin, fill=(255, 255, 255))
    for n, region, field, brief, lon, lat in BRIEFS:
        px, py = proj(lon, lat)
        px = min(max(px, map_x + 4), map_x + map_w - 4)
        py = min(max(py, map_y + 4), map_y + map_h - 4)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=REGION_COLORS[region],
                  outline=(255, 255, 255), width=1)

    # legend under the map
    ly = map_y + map_h + 6
    f_leg = font(SANS, 9)
    d.text((map_x, ly), "Red pins = stories 1\u201313  \u00b7  dots = briefs 14\u201342",
           font=f_leg, fill=GREY)
    d.text((map_x, ly + 13), "Pin 6 (Voyager 1) is in deep space \u2014 at the edge.",
           font=f_leg, fill=GREY)

    # briefs in 3 columns
    bx0, by0 = mx + 272, map_y
    col_w = (W - mx - bx0 - 16) // 3
    f_br = font(SANS, 9)
    f_brn = font(SANS_B, 9)
    per_col = 10
    for ci in range(3):
        chunk = BRIEFS[ci * per_col:(ci + 1) * per_col]
        cx = bx0 + ci * (col_w + 8)
        cy = by0
        for n, region, field, brief, lon, lat in chunk:
            num = "%d " % n
            nw = d.textlength(num, font=f_brn)
            d.text((cx, cy), num, font=f_brn, fill=RED)
            lines = wrap(d, brief, f_br, col_w - nw - 2)
            text_block(d, cx + nw, cy, lines[:2], f_br, leading=10)
            cy += 10 * len(lines[:2]) + 2

    # ---- date check + footer -----------------------------------------
    fy = y2 + 28 + 158 + 34
    d.line([mx, fy, W - mx, fy], fill=INK, width=2)
    f_dc = font(SANS_B, 11)
    d.text((mx, fy + 6), "DATE CHECK", font=f_dc, fill=RED)
    dc = ("Left out on purpose because first reported on 17 Nov, not today: "
          "Peltola\u2019s Alaska Senate win, Nvidia\u2019s $115.8bn quarter, the "
          "Prague train crash, Mongolia\u2019s president resigning. Cyclone "
          "Akvan formed on 16 Nov; card 13 is today\u2019s approach.")
    f_dcb = font(SANS, 11)
    text_block(d, mx + 92, fy + 6, wrap(d, dc, f_dcb, W - 2 * mx - 92),
               f_dcb, leading=14)
    fy2 = fy + 52
    d.line([mx, fy2, W - mx, fy2], fill=LINE, width=1)
    f_src = font(SANS, 10)
    src = ("Every story here happened or was first reported on Wednesday, "
           "18 November 2026. Contested claims are attributed. Sources: "
           "Reuters, AP, AFP, Al Jazeera, Bloomberg.")
    text_block(d, mx, fy2 + 6, wrap(d, src, f_src, W - 2 * mx), f_src,
               fill=GREY, leading=13)
    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote %s %dx%d %d bytes" % (out, img.width, img.height,
                                       os.path.getsize(out)))


if __name__ == "__main__":
    main()
