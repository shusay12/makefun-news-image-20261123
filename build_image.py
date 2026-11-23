#!/usr/bin/env python3
"""Draw the 23 November 2026 front page (1024x1024) with Pillow.

Run:  python3 build_image.py            -> writes entry.png next to this file
Everything is drawn programmatically from scratch: no external images,
no network. Only the Python standard library + Pillow are used at build
time; the graded entrypoint (main.py) is stdlib-only and just copies the
finished PNG.

Layout (1024x1024, all boxes measured so text never leaves its panel):
  masthead 14-118 | lead story 132-452 | grid row 1 468-668 |
  grid row 2 684-868 | footer ticker 884-1010

Stories (all the most widely reported stories of Monday 23 Nov 2026,
as reported that day by CNN, WSJ, AP, Reuters, The Hindu, India Today,
Korea JoongAng Daily and the Indian Express):
  1. COP31 climate talks collapse in Antalya (lead)
  2. Houthi strikes hit a Saudi oil refinery; US-Iran war widens
  3. Liverpool rout Manchester United in Pochettino's debut
  4. India post a record 720/9d in the Wellington Test
  5. South Korea's education minister quits over AI exam cheating
  6. Mexico seizes FBI most-wanted cartel boss 'El Chapo Isidro'
Ticker: Nepal PM's talks with Modi; UN lethal-weapons talks continue;
FIDE World Championship Game 1.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# ---- palette ------------------------------------------------------------
PAPER = (247, 243, 234)      # warm newsprint
INK = (24, 28, 36)           # near-black text
NAVY = (18, 34, 58)          # masthead
NAVY2 = (28, 52, 86)
GOLD = (214, 164, 65)
RED = (178, 34, 34)
WHITE = (255, 255, 255)
GREEN = (46, 125, 72)
SKY = (58, 110, 165)
MUTED = (110, 104, 92)
PANEL = (255, 255, 255)


def font(name, size):
    paths = {
        "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    }
    return ImageFont.truetype(paths[name], size)


def wrap(d, text, fnt, width):
    """Greedy word wrap returning lines fitting `width` px."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if d.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, fill, width, leading=None):
    """Draw wrapped text; return y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(d, text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(d, x0, x1, y, fill, w=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


# ---- small drawn illustrations ------------------------------------------
def draw_globe(d, cx, cy, r):
    """Blue globe with green land blobs and a red crack, on a pale disc."""
    d.ellipse([cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14],
              fill=(226, 233, 240), outline=NAVY, width=3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY, outline=NAVY, width=3)
    d.ellipse([cx - r + 18, cy - r + 26, cx - r + 78, cy - r + 62],
              fill=GREEN)
    d.ellipse([cx + 6, cy + 8, cx + 62, cy + 52], fill=GREEN)
    d.ellipse([cx - r + 30, cy + r - 58, cx - r + 66, cy + r - 26],
              fill=GREEN)
    # crack: red zigzag across the globe
    pts = [(cx - r + 8, cy - r + 30), (cx - r + 44, cy - r + 58),
           (cx - r + 30, cy - r + 86), (cx + 8, cy - 6),
           (cx - 6, cy + 30), (cx + 34, cy + 58), (cx + 18, cy + r - 12)]
    d.line(pts, fill=RED, width=5, joint="curve")
    # small flame/sun above
    d.ellipse([cx + r - 42, cy - r - 26, cx + r - 6, cy - r + 10],
              fill=GOLD, outline=RED, width=2)


def draw_refinery(d, x0, y0, x1, y1):
    """Night refinery: dark sky, towers, orange blast, small drone.
    All shapes stay inside the (x0, y0, x1, y1) box."""
    d.rectangle([x0, y0, x1, y1], fill=(30, 34, 48))
    bh = y1 - y0
    d.ellipse([x1 - 46, y0 + 4, x1 - 14, y0 + 36], fill=(240, 214, 130))
    # towers: heights scaled to the box
    for tx, tw, th in [(x0 + 14, 26, int(bh * 0.62)),
                       (x0 + 52, 20, int(bh * 0.80)),
                       (x0 + 88, 30, int(bh * 0.55)),
                       (x0 + 130, 18, int(bh * 0.72))]:
        d.rectangle([tx, y1 - th, tx + tw, y1], fill=(70, 76, 92),
                    outline=(160, 166, 180), width=1)
        d.rectangle([tx + tw // 2 - 3, y1 - th - 10, tx + tw // 2 + 3,
                     y1 - th], fill=(160, 166, 180))
    # blast starburst
    bx, by = x0 + 150, y0 + int(bh * 0.62)
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([(bx, by), (bx + 22 * math.cos(a), by + 22 * math.sin(a))],
               fill=(255, 176, 32), width=4)
    d.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=(255, 214, 90))
    # drone silhouette
    dx, dy = x0 + 216, y0 + 14
    d.polygon([(dx, dy - 7), (dx + 20, dy), (dx, dy + 7), (dx - 20, dy)],
              fill=(200, 204, 212))
    d.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=(220, 224, 232))


def draw_football(d, x0, y0, x1, y1):
    """Green pitch, goal and ball."""
    d.rectangle([x0, y0, x1, y1], fill=(52, 138, 72))
    d.rectangle([x0, y0, x1, y1], outline=WHITE, width=2)
    d.line([(x0, (y0 + y1) // 2), (x1, (y0 + y1) // 2)], fill=WHITE, width=2)
    d.ellipse([x0 + 90, y0 + 18, x1 - 90, y1 - 18], outline=WHITE, width=2)
    # goal
    d.rectangle([x1 - 62, y0 + 16, x1 - 14, y0 + 52], outline=WHITE, width=3)
    # ball
    bx, by = x0 + 62, y1 - 34
    d.ellipse([bx - 16, by - 16, bx + 16, by + 16], fill=WHITE,
              outline=INK, width=2)
    d.polygon([(bx, by - 7), (bx + 7, by - 2), (bx + 4, by + 6),
               (bx - 4, by + 6), (bx - 7, by - 2)], fill=INK)


def draw_cricket(d, x0, y0, x1, y1):
    """Pitch strip, stumps, bat and red ball."""
    d.rectangle([x0, y0, x1, y1], fill=(96, 160, 84))
    d.rectangle([x0 + 30, y0 + 8, x1 - 30, y1 - 8], fill=(214, 190, 148))
    # stumps
    sx = x1 - 66
    for i in range(3):
        d.line([(sx + i * 10, y0 + 18), (sx + i * 10, y0 + 52)],
               fill=(255, 214, 90), width=4)
    # bat
    d.polygon([(x0 + 52, y1 - 18), (x0 + 66, y1 - 18), (x0 + 78, y0 + 30),
               (x0 + 64, y0 + 26)], fill=(196, 148, 92), outline=INK)
    # red ball
    d.ellipse([x0 + 118, y1 - 34, x0 + 146, y1 - 6], fill=RED,
              outline=(120, 20, 20), width=2)
    d.text((x0 + 158, y1 - 34), "720/9d", font=font("sans_b", 22), fill=WHITE)


def draw_exam(d, x0, y0, x1, y1):
    """Exam paper, pencil and an AI chip."""
    d.rectangle([x0, y0, x1, y1], fill=(232, 228, 218))
    # paper
    px0, py0, px1, py1 = x0 + 16, y0 + 6, x0 + 150, y1 - 6
    d.rectangle([px0, py0, px1, py1], fill=WHITE, outline=INK, width=2)
    d.text((px0 + 8, py0 + 4), "CSAT", font=font("sans_b", 15), fill=RED)
    for i in range(3):
        ly = py0 + 26 + i * 9
        d.line([(px0 + 8, ly), (px1 - 8, ly)], fill=(150, 148, 140), width=2)
    # pencil
    d.polygon([(x0 + 168, y1 - 12), (x0 + 184, y1 - 12), (x0 + 202, y0 + 14),
               (x0 + 186, y0 + 10)], fill=(255, 214, 90), outline=INK)
    d.polygon([(x0 + 202, y0 + 14), (x0 + 210, y0 + 24), (x0 + 194, y0 + 26)],
              fill=(240, 200, 170), outline=INK)
    # AI chip
    cx0, cy0, cx1, cy1 = x1 - 74, y0 + 10, x1 - 14, y0 + 48
    d.rectangle([cx0, cy0, cx1, cy1], fill=NAVY, outline=GOLD, width=2)
    d.text((cx0 + 12, cy0 + 8), "AI", font=font("sans_b", 20), fill=GOLD)


def draw_badge(d, x0, y0, x1, y1):
    """Sheriff-style badge star and handcuffs on a dark band."""
    d.rectangle([x0, y0, x1, y1], fill=(30, 34, 48))
    cx, cy = x0 + 64, (y0 + y1) // 2
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        r = 24 if i % 2 == 0 else 11
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=GOLD, outline=(120, 84, 20), width=2)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=NAVY)
    # handcuffs: two rings + link
    for hx in (x1 - 118, x1 - 66):
        d.ellipse([hx - 15, cy - 15, hx + 15, cy + 15], outline=WHITE, width=4)
    d.line([(x1 - 98, cy), (x1 - 86, cy)], fill=WHITE, width=5)
    d.text((x0 + 118, cy - 16), "FBI MOST WANTED",
           font=font("sans_b", 20), fill=WHITE)


# ---- build ----------------------------------------------------------------
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer frame
    d.rectangle([8, 8, W - 9, H - 9], outline=NAVY, width=4)

    # ---- masthead ---------------------------------------------------------
    d.rectangle([14, 14, W - 15, 118], fill=NAVY)
    d.rectangle([14, 14, W - 15, 118], outline=GOLD, width=2)
    d.text((28, 34), "THE WORLD TODAY", font=font("serif_b", 54), fill=WHITE)
    d.text((W - 28 - d.textlength("MONDAY", font=font("sans_b", 26)),
            26), "MONDAY", font=font("sans_b", 26), fill=GOLD)
    d.text((W - 28 - d.textlength("23 NOVEMBER 2026",
                                  font=font("sans_b", 30)), 58),
           "23 NOVEMBER 2026", font=font("sans_b", 30), fill=WHITE)
    hline(d, 28, W - 28, 128, GOLD, 3)

    # ---- lead story: COP31 ----------------------------------------------
    lx0, ly0, lx1, ly1 = 28, 140, W - 28, 444
    d.rectangle([lx0, ly0, lx1, ly1], fill=PANEL, outline=INK, width=2)
    d.text((lx0 + 16, ly0 + 12), "CLIMATE  •  LEAD STORY",
           font=font("sans_b", 20), fill=RED)
    y = text_block(d, lx0 + 16, ly0 + 44, "COP31 COLLAPSES\nIN ANTALYA",
                   font("serif_b", 44), INK, 600, leading=50)
    y = text_block(
        d, lx0 + 16, y + 10,
        "After two weeks of talks — the longest climate summit ever — "
        "the world's nations end with no deal. The EU rejects a text "
        "that never mentions fossil fuels, the first major breakdown "
        "since Copenhagen in 2009.",
        font("sans", 20), INK, 600, leading=26)
    y = text_block(d, lx0 + 16, y + 8,
                   "Antalya, Turkey  •  194 nations split over a phase-out",
                   font("sans_b", 18), MUTED, 600, leading=24)
    assert y <= ly1 - 8, f"lead text overflows: {y} > {ly1}"
    # globe illustration, right of the lead text
    draw_globe(d, 824, 268, 92)
    d.text((716, 386), "NO DEAL", font=font("sans_b", 30), fill=RED)
    d.text((716, 420), "after 14 days of talks",
           font=font("sans", 17), fill=MUTED)

    # ---- grid of five stories --------------------------------------------
    def panel(x0, y0, x1, y1, kicker, headline, dek, draw_fn, hsize=22,
              ill_h=60):
        d.rectangle([x0, y0, x1, y1], fill=PANEL, outline=INK, width=2)
        draw_fn(d, x0 + 2, y0 + 2, x1 - 2, y0 + 2 + ill_h)
        d.text((x0 + 12, y0 + ill_h + 8), kicker, font=font("sans_b", 18),
               fill=RED)
        yy = text_block(d, x0 + 12, y0 + ill_h + 32, headline,
                        font("serif_b", hsize), INK, (x1 - x0) - 24,
                        leading=hsize + 5)
        end = text_block(d, x0 + 12, yy + 4, dek, font("sans", 16), INK,
                         (x1 - x0) - 24, leading=21)
        assert end <= y1 - 4, f"panel '{headline}' overflows: {end} > {y1}"

    gx0, gx1 = 28, W - 28
    gap = 12
    pw3 = (gx1 - gx0 - 2 * gap) // 3          # 314
    pw2 = (gx1 - gx0 - gap) // 2              # 478
    r1y0, r1y1 = 456, 668
    r2y0, r2y1 = 684, 876

    panel(gx0, r1y0, gx0 + pw3, r1y1,
          "MIDDLE EAST",
          "HOUTHI STRIKES HIT SAUDI REFINERY",
          "Houthis claim strikes on a Saudi oil refinery; six injured.",
          draw_refinery)
    panel(gx0 + pw3 + gap, r1y0, gx0 + 2 * pw3 + gap, r1y1,
          "FOOTBALL",
          "LIVERPOOL ROUT UNITED",
          "Liverpool hammer ten-man United in Pochettino's debut; "
          "Yoro sent off.",
          draw_football)
    panel(gx0 + 2 * pw3 + 2 * gap, r1y0, gx1, r1y1,
          "CRICKET",
          "INDIA'S RECORD 720/9d",
          "India declare on a record 720 for 9 in Wellington; NZ "
          "157 for 4.",
          draw_cricket)

    panel(gx0, r2y0, gx0 + pw2, r2y1,
          "ASIA  •  EDUCATION",
          "SEOUL MINISTER QUITS OVER AI EXAM CHEATING",
          "Minister Choi Kyo-jin resigns over AI-cheating chaos before "
          "the CSAT; 111 cases caught.",
          draw_exam, hsize=23, ill_h=52)
    panel(gx0 + pw2 + gap, r2y0, gx1, r2y1,
          "AMERICAS  •  CRIME",
          "MEXICO SEIZES 'EL CHAPO ISIDRO'",
          "FBI most-wanted boss Fausto Isidro Meza-Flores seized in "
          "Sinaloa; 11 killed, four soldiers.",
          draw_badge, hsize=23, ill_h=52)

    # ---- footer ticker ------------------------------------------------------
    fy0, fy1 = 892, 1010
    d.rectangle([28, fy0, W - 28, fy1], fill=NAVY)
    d.text((44, fy0 + 10), "ALSO TODAY", font=font("sans_b", 20), fill=GOLD)
    y = text_block(
        d, 44, fy0 + 38,
        "•  Nepal PM Balendra Shah holds bilateral talks with PM Modi "
        "in New Delhi   •   UN talks on lethal autonomous weapons to "
        "continue   •   FIDE World Championship: Sindarov takes White "
        "in Game 1",
        font("sans", 19), WHITE, W - 88, leading=26)
    d.text((44, fy1 - 26),
           "Stories as reported on Monday 23 November 2026  •  Sources: "
           "CNN, WSJ, AP, Reuters, The Hindu, Korea JoongAng Daily, "
           "Indian Express",
           font=font("sans", 14), fill=(200, 205, 215))

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}, {size} bytes")
    assert img.size[0] <= 1024 and img.size[1] <= 1024
    assert size <= 1048576, f"over 1 MiB: {size}"


if __name__ == "__main__":
    main()
