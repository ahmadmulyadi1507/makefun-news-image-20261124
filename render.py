#!/usr/bin/env python3
"""Render the news-image-20261124 entry: a one-page front-page infographic
summing up Tuesday 24 November 2026's world news. Drawn from scratch with
PIL (flat shapes, no photos, no copied artwork).
Output: entry.png, 1024x1024, well under 1 MiB."""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
NAVY = (22, 35, 63)
GOLD = (201, 162, 39)
INK = (24, 28, 36)
GREY = (107, 101, 88)
CARD = (255, 255, 255)
BORDER = (216, 210, 196)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap, returns lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def mine(draw, cx, cy, r, fill=(30, 30, 36)):
    """Spiky naval mine: circle with radiating spikes."""
    for k in range(8):
        a = k * math.pi / 4
        x1, y1 = cx + r * 0.7 * math.cos(a), cy + r * 0.7 * math.sin(a)
        x2, y2 = cx + r * 1.5 * math.cos(a), cy + r * 1.5 * math.sin(a)
        draw.line([x1, y1, x2, y2], fill=fill, width=3)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    draw.ellipse([cx - r * 0.35, cy - r * 0.45, cx + r * 0.1, cy - r * 0.1],
                 fill=(120, 120, 130))


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------- header ----------------
d.rectangle([0, 0, W, 116], fill=NAVY)
d.rectangle([0, 116, W, 121], fill=GOLD)
f_date = font(FONT_BOLD, 25)
f_title = font(FONT_BOLD, 54)
t = "TUESDAY  \u2014  24 NOVEMBER 2026"
d.text(((W - d.textlength(t, font=f_date)) / 2, 14), t, font=f_date, fill=GOLD)
t = "THE WORLD IN A DAY"
d.text(((W - d.textlength(t, font=f_title)) / 2, 46), t, font=f_title, fill=(255, 255, 255))

# ---------------- story cards ----------------
# (accent, headline, fact, pictogram key)
STORIES = [
    ((178, 34, 34), "FOUR TANKERS MINED IN HORMUZ",
     "Four tankers hit naval mines in the Strait of Hormuz, and Iran's IRGC "
     "says its navy also attacked a container ship.", "hormuz"),
    ((20, 80, 110), "HUAWEI GUILTY ON TWO COUNTS",
     "A US jury finds Huawei guilty of trade-secret theft and bank fraud, "
     "but clears it of racketeering.", "court"),
    ((196, 120, 20), "UKRAINE HITS RUSSIAN SHIPS IN TWO SEAS",
     "Ukraine says its drones struck the Russian cargo ship Sparta II in the "
     "Gulf of Finland and another vessel off Libya.", "drones"),
    ((120, 60, 140), "HAMAS SECURITY CHIEF KILLED IN GAZA",
     "Israeli strikes kill Hamas internal security chief Naeem Abu Nahel and "
     "six others in Gaza.", "gaza"),
    ((0, 120, 190), "TURKISH HELICOPTER CRASH KILLS FIVE",
     "A Turkish Air Force helicopter crashes on a training flight in western "
     "T\u00fcrkiye, killing all five crew.", "heli"),
    ((150, 40, 40), "25 HOSTAGES IN CARTAGENA SIEGE",
     "Armed men seize a supermarket in Cartagena, Colombia, holding 25 "
     "people hostage.", "store"),
]

CARD_W, CARD_H, GAP, MARGIN = 480, 272, 16, 24
f_head = font(FONT_BOLD, 30)
f_fact = font(FONT_REG, 19)
f_num = font(FONT_BOLD, 22)


def pic_hormuz(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(242, 227, 198))
    d.ellipse([x0 + 26, y0 + 8, x0 + 62, y0 + 44], fill=(255, 196, 66))
    d.rectangle([x0, y0 + 58, x0 + w, y0 + h], fill=(20, 80, 110))
    d.line([x0, y0 + 58, x0 + w, y0 + 58], fill=(255, 255, 255), width=2)
    # tanker
    d.rectangle([x0 + 70, y0 + 74, x0 + 300, y0 + 94], fill=(30, 30, 36))
    d.rectangle([x0 + 252, y0 + 54, x0 + 300, y0 + 74], fill=(30, 30, 36))
    for i, c in enumerate([(200, 60, 60), (60, 160, 90), (240, 180, 40)]):
        d.rectangle([x0 + 92 + i * 52, y0 + 58, x0 + 138 + i * 52, y0 + 74], fill=c)
    # mines in the water ahead of the tanker
    mine(d, x0 + 350, y0 + 82, 11)
    mine(d, x0 + 412, y0 + 66, 9)
    # blast starburst where a mine meets the hull
    star(d, x0 + 330, y0 + 72, 22, 9, 8, (255, 176, 32))
    star(d, x0 + 330, y0 + 72, 12, 5, 8, (255, 110, 30))


def pic_court(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 238, 245))
    # courthouse: pediment, columns, steps
    cx = x0 + 150
    d.polygon([(cx - 110, y0 + 34), (cx + 110, y0 + 34), (cx, y0 + 8)],
              fill=NAVY)
    for i in range(4):
        px = cx - 84 + i * 56
        d.rectangle([px, y0 + 36, px + 16, y0 + 88], fill=(255, 255, 255),
                    outline=NAVY, width=2)
    d.rectangle([cx - 116, y0 + 88, cx + 116, y0 + 94], fill=NAVY)
    d.rectangle([cx - 128, y0 + 94, cx + 128, y0 + 100], fill=NAVY)
    # scales of justice
    sx, sy = x0 + 380, y0 + 50
    d.line([sx, sy - 30, sx, sy + 34], fill=GOLD, width=4)
    d.line([sx - 42, sy - 26, sx + 42, sy - 26], fill=GOLD, width=4)
    for sgn in (-1, 1):
        ex = sx + sgn * 42
        d.line([ex, sy - 26, ex, sy - 8], fill=GOLD, width=3)
        d.polygon([(ex - 16, sy - 8), (ex + 16, sy - 8), (ex, sy + 10)],
                  fill=GOLD)
    d.ellipse([sx - 6, sy - 36, sx + 6, sy - 24], fill=GOLD)


def pic_drones(x0, y0, w, h):
    # two seas: pale north, darker south, split down the middle
    d.rectangle([x0, y0, x0 + w // 2, y0 + h], fill=(178, 214, 230))
    d.rectangle([x0 + w // 2, y0, x0 + w, y0 + h], fill=(32, 110, 150))
    d.rectangle([x0, y0 + 62, x0 + w, y0 + h], fill=(20, 80, 110))
    d.line([x0, y0 + 62, x0 + w, y0 + 62], fill=(255, 255, 255), width=2)
    # drone above
    cx, cy = x0 + 240, y0 + 30
    d.rectangle([cx - 14, cy - 5, cx + 14, cy + 5], fill=(30, 30, 36))
    d.line([cx - 26, cy - 10, cx + 26, cy - 10], fill=(30, 30, 36), width=3)
    d.line([cx - 26, cy + 10, cx + 26, cy + 10], fill=(30, 30, 36), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 176, 32))
    # two ships, one in each sea
    for sx, flip in ((60, 0), (300, 0)):
        d.rectangle([x0 + sx, y0 + 76, x0 + sx + 130, y0 + 94], fill=(30, 30, 36))
        d.rectangle([x0 + sx + 88, y0 + 58, x0 + sx + 118, y0 + 76],
                    fill=(30, 30, 36))
        d.rectangle([x0 + sx + 20, y0 + 62, x0 + sx + 60, y0 + 76],
                    fill=(200, 60, 60))
    # blast on the first ship
    star(d, x0 + 150, y0 + 70, 20, 8, 8, (255, 176, 32))
    star(d, x0 + 150, y0 + 70, 11, 5, 8, (255, 110, 30))


def pic_gaza(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(64, 52, 66))
    d.ellipse([x0 + w - 70, y0 + 12, x0 + w - 38, y0 + 44], fill=(255, 196, 66))
    # skyline, one building broken
    base = y0 + h
    for bx, bw, bh in [(30, 52, 52), (92, 44, 70), (146, 58, 44),
                       (214, 48, 62), (272, 60, 38), (342, 52, 56)]:
        d.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(24, 22, 28))
        for wy in range(base - bh + 8, base - 6, 14):
            for wx in range(bx + 8, bx + bw - 6, 14):
                d.rectangle([x0 + wx, wy, x0 + wx + 6, wy + 7],
                            fill=(255, 196, 66))
    # broken top on the middle building + smoke
    d.polygon([(x0 + 214, base - 62), (x0 + 228, base - 78), (x0 + 244, base - 62),
               (x0 + 262, base - 74), (x0 + 262, base - 62)], fill=(24, 22, 28))
    for sx, sy, r in [(240, 26, 16), (256, 14, 12), (226, 12, 10)]:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                  fill=(150, 145, 150))


def pic_heli(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(220, 233, 245))
    d.rectangle([x0, y0 + 84, x0 + w, y0 + h], fill=(90, 100, 112))
    for i in range(9):
        d.rectangle([x0 + 14 + i * 52, y0 + 92, x0 + 40 + i * 52, y0 + 98],
                    fill=(255, 255, 255))
    # helicopter, tilted as if falling
    cx, cy = x0 + 210, y0 + 48
    d.line([cx - 110, cy - 26, cx + 110, cy - 34], fill=(30, 30, 36), width=5)
    d.ellipse([cx - 62, cy - 16, cx + 58, cy + 14], fill=NAVY)
    d.polygon([(cx + 58, cy - 8), (cx + 118, cy - 2), (cx + 118, cy + 6),
               (cx + 58, cy + 8)], fill=NAVY)
    d.polygon([(cx - 62, cy - 4), (cx - 92, cy + 22), (cx - 82, cy + 26),
               (cx - 52, cy + 8)], fill=NAVY)
    d.ellipse([cx - 44, cy - 8, cx - 18, cy + 4], fill=(178, 214, 230))
    # smoke trail behind
    for sx, sy, r in [(330, 22, 12), (352, 14, 9), (372, 8, 7)]:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                  fill=(150, 150, 155))
    # impact burst on the ground
    star(d, x0 + 400, y0 + 82, 20, 8, 8, (255, 176, 32))


def pic_store(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(240, 234, 220))
    # storefront
    d.rectangle([x0 + 70, y0 + 22, x0 + 410, y0 + h], fill=(255, 255, 255),
                outline=NAVY, width=3)
    # striped awning
    for i in range(8):
        c = (178, 34, 34) if i % 2 == 0 else (255, 255, 255)
        d.polygon([(x0 + 62 + i * 45, y0 + 22), (x0 + 62 + (i + 1) * 45, y0 + 22),
                   (x0 + 62 + (i + 1) * 45 + 8, y0 + 48),
                   (x0 + 62 + i * 45 + 8, y0 + 48)], fill=c,
                  outline=NAVY, width=2)
    # sign
    f_sign = font(FONT_BOLD, 22)
    t = "SUPERMARKET"
    d.text(((x0 + 240) - d.textlength(t, font=f_sign) / 2, y0 + 54), t,
           font=f_sign, fill=NAVY)
    # door and window, barred
    d.rectangle([x0 + 96, y0 + 84, x0 + 176, y0 + h], fill=(178, 214, 230),
                outline=NAVY, width=3)
    d.line([x0 + 136, y0 + 84, x0 + 136, y0 + h], fill=NAVY, width=3)
    d.rectangle([x0 + 208, y0 + 84, x0 + 384, y0 + h - 14], fill=(232, 238, 245),
                outline=NAVY, width=3)
    for wx in range(232, 380, 28):
        d.line([x0 + wx, y0 + 84, x0 + wx, y0 + h - 14], fill=NAVY, width=3)
    # warning tape across the door
    d.polygon([(x0 + 84, y0 + 88), (x0 + 188, y0 + 88), (x0 + 188, y0 + 100),
               (x0 + 84, y0 + 100)], fill=(255, 196, 66))
    d.line([x0 + 84, y0 + 88, x0 + 188, y0 + 100], fill=(178, 34, 34), width=2)
    d.line([x0 + 188, y0 + 88, x0 + 84, y0 + 100], fill=(178, 34, 34), width=2)


PICS = {"hormuz": pic_hormuz, "court": pic_court, "drones": pic_drones,
        "gaza": pic_gaza, "heli": pic_heli, "store": pic_store}

for i, (accent, headline, fact, key) in enumerate(STORIES):
    col, row = i % 2, i // 2
    x0 = MARGIN + col * (CARD_W + GAP)
    y0 = 134 + row * (CARD_H + GAP)
    d.rectangle([x0, y0, x0 + CARD_W, y0 + CARD_H], fill=CARD, outline=BORDER,
                width=1)
    d.rectangle([x0, y0, x0 + CARD_W, y0 + 6], fill=accent)
    PICS[key](x0, y0 + 6, CARD_W, 108)
    # number badge
    bx, by = x0 + 14, y0 + 20
    d.ellipse([bx, by, bx + 34, by + 34], fill=accent)
    d.text((bx + 17 - d.textlength(str(i + 1), font=f_num) / 2, by + 4),
           str(i + 1), font=f_num, fill=(255, 255, 255))
    # headline + fact
    lines = wrap(d, headline, f_head, CARD_W - 32)
    ty = y0 + 124
    for ln in lines[:2]:
        d.text((x0 + 16, ty), ln, font=f_head, fill=INK)
        ty += 36
    fact_lines = wrap(d, fact, f_fact, CARD_W - 32)
    ty = y0 + 124 + 72
    for ln in fact_lines[:3]:
        d.text((x0 + 16, ty), ln, font=f_fact, fill=GREY)
        ty += 23

# ---------------- footer ----------------
f_foot = font(FONT_REG, 16)
t = ("Six stories, one day  \u2014  Tuesday 24 November 2026  \u2014  "
     "Sources: Daily Summary Of, Just Security, Reuters")
d.text(((W - d.textlength(t, font=f_foot)) / 2, 992), t, font=f_foot, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
print("bytes:", os.path.getsize("entry.png"))
