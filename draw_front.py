#!/usr/bin/env python3
"""Draw the front page for Wednesday 25 November 2026 as entry.png.

Built with Pillow from the machine's DejaVu fonts; no network, no
outside pictures. The page is a newspaper front: masthead naming the
day, a lead sea-strike story, COP31 and Riyadh panels, a row of three
shorter stories, and a ticker of the day's other headlines.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (22, 22, 20)
NAVY = (16, 32, 56)
SEA = (24, 68, 104)
SEA_DARK = (12, 40, 66)
RED = (178, 30, 30)
GOLD = (186, 128, 26)
TEAL = (16, 100, 96)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
GREY = (98, 96, 90)
RULE = (198, 190, 170)
ORANGE = (232, 110, 24)
EMBER = (244, 178, 44)
SKY = (214, 228, 238)
DUSK = (232, 196, 150)

FONTS = "/usr/share/fonts/truetype/dejavu"


def face(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size)


def serif_b(size):
    return face("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return face("DejaVuSerif.ttf", size)


def sans_b(size):
    return face("DejaVuSans-Bold.ttf", size)


def sans(size):
    return face("DejaVuSans.ttf", size)


def wrap(draw, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, width, fill=INK, gap=6):
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + gap
    return y


def rule(draw, x, y, w, fill=RULE, width=1):
    draw.line([(x, y), (x + w, y)], fill=fill, width=width)


def kicker(draw, x, y, text, colour=RED):
    f = sans_b(15)
    draw.text((x, y), text.upper(), font=f, fill=colour)
    return y + 22


def burst(draw, cx, cy, r, colour):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=colour)


def ship_scene(draw, x, y, w, h):
    """Night sea: a cargo ship, a drone above it, a blast astern."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    for i in range(5):  # moonlit wave bands
        yy = y + 40 + i * 34
        draw.arc([x - 30, yy, x + w + 30, yy + 46], 200, 340, fill=SEA, width=3)
    # moon
    draw.ellipse([x + w - 92, y + 22, x + w - 42, y + 72], fill=(240, 230, 190))
    # hull
    hx, hy = x + 60, y + h - 108
    draw.polygon([(hx, hy), (hx + 330, hy), (hx + 300, hy + 62),
                  (hx + 26, hy + 62)], fill=(38, 38, 40))
    draw.rectangle([hx + 40, hy - 58, hx + 300, hy], fill=(52, 52, 56))
    for i, c in enumerate([(178, 30, 30), (186, 128, 26), (16, 100, 96), (120, 120, 116)]):
        draw.rectangle([hx + 52 + i * 62, hy - 52, hx + 104 + i * 62, hy - 8], fill=c)
    draw.rectangle([hx + 316, hy - 88, hx + 332, hy], fill=(70, 70, 74))
    # drone
    dx, dy = x + w - 170, y + 66
    draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=(220, 220, 220))
    for sx, sy in [(-26, -16), (26, -16), (-26, 16), (26, 16)]:
        draw.line([(dx, dy), (dx + sx, dy + sy)], fill=(200, 200, 200), width=2)
        draw.ellipse([dx + sx - 8, dy + sy - 3, dx + sx + 8, dy + sy + 3],
                     outline=(230, 230, 230), width=2)
    # blast at the stern
    bx, by = x + 62, y + h - 96
    burst(draw, bx, by, 44, ORANGE)
    burst(draw, bx, by, 26, EMBER)
    burst(draw, bx, by, 13, WHITE)


def globe_crack(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    for k in range(6):  # latitude bands
        yy = cy - r + (2 * r * k) // 5
        chord = int(math.sqrt(max(r * r - (yy - cy) ** 2, 0)))
        draw.arc([cx - chord, yy - 8, cx + chord, yy + 8], 0, 360, fill=(140, 200, 190), width=2)
    # land blobs
    draw.ellipse([cx - r + 12, cy - 26, cx - 8, cy + 18], fill=(86, 150, 84))
    draw.ellipse([cx + 6, cy + 4, cx + r - 14, cy + 42], fill=(86, 150, 84))
    # the crack
    pts = [(cx - 6, cy - r + 4), (cx + 10, cy - r // 2), (cx - 8, cy - 6),
           (cx + 12, cy + r // 3), (cx - 2, cy + r - 6)]
    draw.line(pts, fill=WHITE, width=5)
    draw.line(pts, fill=INK, width=2)


def tower_scene(draw, x, y, w, h):
    """Riyadh at dusk: the tall tower, lit windows, smoke."""
    draw.rectangle([x, y, x + w, y + h], fill=DUSK)
    draw.ellipse([x + w - 66, y + 16, x + w - 26, y + 56], fill=(246, 222, 170))
    # skyline
    for bx, bw, bh in [(0, 44, 66), (52, 36, 96), (96, 40, 58), (196, 34, 84), (238, 42, 60)]:
        draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(94, 78, 92))
    # the tall tower
    tx = x + 128
    draw.polygon([(tx, y + 14), (tx + 62, y + 14), (tx + 54, y + h),
                  (tx + 8, y + h)], fill=(52, 58, 84))
    draw.polygon([(tx + 18, y + 14), (tx + 44, y + 14), (tx + 40, y + 52),
                  (tx + 22, y + 52)], fill=(120, 130, 170))
    for row in range(9):
        for col in range(3):
            wx = tx + 16 + col * 14
            wy = y + 66 + row * 16
            draw.rectangle([wx, wy, wx + 7, wy + 9],
                           fill=EMBER if (row + col) % 3 else (210, 210, 200))
    # smoke from the top
    for i, r in enumerate([10, 16, 22]):
        draw.ellipse([tx + 30 - r + i * 4, y + 2 - i * 12, tx + 30 + r + i * 4,
                      y + 2 - i * 12 + 2 * r], fill=(120, 116, 110))
    burst(draw, tx + 31, y + 26, 16, ORANGE)


def medal(draw, cx, cy, r):
    draw.polygon([(cx - 22, cy - r - 6), (cx + 22, cy - r - 6),
                  (cx + 10, cy - r + 34), (cx - 10, cy - r + 34)], fill=RED)
    draw.polygon([(cx - 22, cy - r - 6), (cx, cy - r - 6),
                  (cx - 2, cy - r + 34), (cx - 10, cy - r + 34)], fill=(140, 20, 20))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD, outline=(120, 80, 10), width=3)
    draw.ellipse([cx - r + 12, cy - r + 12, cx + r - 12, cy + r - 12],
                 outline=(120, 80, 10), width=2)
    draw.text((cx - 11, cy - 16), "★", font=sans_b(30), fill=(120, 80, 10))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 30  # margin
    inner = W - 2 * m

    # ---- masthead ----
    d.text((m, 18), "THE WORLD", font=serif_b(96), fill=INK)
    rule(d, m, 128, inner, fill=INK, width=3)
    rule(d, m, 134, inner, fill=INK, width=1)
    d.text((m, 142), "WEDNESDAY 25 NOVEMBER 2026", font=sans_b(20), fill=INK)
    tag = "THE DAY'S NEWS IN ONE PICTURE"
    d.text((W - m - d.textlength(tag, font=sans_b(20)), 142), tag,
           font=sans_b(20), fill=RED)
    rule(d, m, 172, inner, fill=INK, width=2)

    # ---- lead story: ships struck at sea ----
    lx, ly, lw = m, 190, 600
    y = kicker(d, lx, ly, "War at sea · Ukraine")
    d.text((lx, y), "KYIV HITS RUSSIAN", font=serif_b(40), fill=INK)
    d.text((lx, y + 46), "SHIPS AT SEA", font=serif_b(40), fill=INK)
    y += 100
    y = para(d, lx, y,
             "Zelenskiy confirms a drone strike on a Russian cargo ship "
             "in the Gulf of Finland — and a second vessel was hit off "
             "Benghazi, Libya. Moscow calls the attacks “terrorism” and "
             "warns of severe consequences; Norway urges caution.",
             serif(19), lw, gap=4)
    ship_scene(d, lx, y + 6, lw, 236)
    rule(d, lx, y + 252, lw, width=1)

    # ---- right column: COP31 ----
    rx, rw = 662, 332
    y = kicker(d, rx, ly, "Climate · Antalya", colour=TEAL)
    d.text((rx, y), "COP31", font=serif_b(38), fill=INK)
    d.text((rx, y + 44), "COLLAPSES", font=serif_b(38), fill=INK)
    y += 94
    y = para(d, rx, y,
             "The UN climate summit ends with no deal: major oil and gas "
             "producers block fossil-fuel phaseout language, leaving "
             "vulnerable nations waiting on finance.",
             serif(18), rw, gap=4)
    globe_crack(d, rx + rw // 2, y + 66, 56)
    rule(d, rx, y + 132, rw, width=1)

    # ---- right column: Riyadh ----
    y = kicker(d, rx, y + 148, "Middle East · Riyadh", colour=RED)
    d.text((rx, y), "HOUTHI DRONE HITS", font=serif_b(26), fill=INK)
    d.text((rx, y + 32), "RIYADH TOWER", font=serif_b(26), fill=INK)
    y += 68
    y = para(d, rx, y,
             "Eleven wounded as a drone strikes the capital's tallest "
             "tower. Yemeni forces say the rebels, 60 km from Aden, "
             "will not take the city.",
             serif(18), rw, gap=4)
    rule(d, rx, y + 12, rw, width=1)

    # ---- middle row: three short stories ----
    my = 792
    rule(d, m, my - 16, inner, fill=INK, width=2)
    cols = [
        (m, 300, "Washington", RED, "TRUMP HONOURS GIULIANI",
         "The president awards Rudy Giuliani the Medal of Freedom, "
         "the nation's highest civilian honour."),
        (m + 322, 300, "Cyber", NAVY, "CIA AND ODNI BREACHED",
         "US intelligence is hit by a cyber breach, a source says. "
         "Huawei is found guilty of trade-secret theft."),
        (m + 644, 320, "Sport · Cricket", TEAL, "ENGLAND LEVEL THE T20s",
         "England beat Australia by eight wickets in the second T20, "
         "chasing 185 to square the five-match series."),
    ]
    for cx, cw, kick, colour, head, body in cols:
        yy = kicker(d, cx, my, kick, colour=colour)
        yy = para(d, cx, yy, head, serif_b(21), cw, gap=3)
        para(d, cx, yy + 2, body, serif(15), cw, gap=3)

    # ---- ticker ----
    ty = 946
    rule(d, m, ty - 12, inner, fill=INK, width=2)
    d.text((m, ty), "ALSO TODAY", font=sans_b(17), fill=RED)
    tick = ("NATO to send early-warning aircraft to Poland  ·  BJP and Akali Dal "
            "ally for Punjab 2027  ·  Nvidia shares fall 7%  ·  Dell lifts forecasts "
            "on record AI servers  ·  Gaza toll reaches 74,746")
    para(d, m, ty + 26, tick, sans(15), inner, fill=GREY, gap=2)

    # ---- footer ----
    d.text((m, 1008), "THE WORLD · Drawn by an AI agent for make.fun's news-image bounty",
           font=sans(13), fill=GREY)
    return img


if __name__ == "__main__":
    page = build()
    page.save("entry.png", optimize=True)
    import os
    print("wrote entry.png", os.path.getsize("entry.png"), "bytes", page.size)
