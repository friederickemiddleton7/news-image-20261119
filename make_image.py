#!/usr/bin/env python3
"""Generate the 19 November 2026 world news image."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 1024, 1024

NAVY = (11, 18, 32)
CARD = (21, 31, 51)
RULE = (42, 58, 87)
BODY = (215, 222, 234)
HEAD = (255, 255, 255)
AMBER = (242, 179, 61)
TEAL = (79, 209, 197)
GREY = (120, 135, 160)

F = Path("/usr/share/fonts/truetype/dejavu")
FONT_SANS = F / "DejaVuSans.ttf"
FONT_BOLD = F / "DejaVuSans-Bold.ttf"
FONT_SERIF = F / "DejaVuSerif-Bold.ttf"
FONT_COND = F / "DejaVuSansCondensed-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(str(path), size)


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


def fit_font(draw, text, path, max_size, max_w, min_size=20):
    size = max_size
    while size >= min_size:
        f = font(path, size)
        if text_w(draw, text, f) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def wrap_lines(draw, text, f, max_w):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and text_w(draw, trial, f) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def card(draw, x0, y0, x1, y1, fill=CARD):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=fill, outline=RULE, width=1)


def chip(draw, x, y, text, color, size=24, bold=True):
    f = font(FONT_BOLD if bold else FONT_SANS, size)
    draw.text((x, y), text, font=f, fill=color)


def pictogram_three_lecterns(draw, cx, cy):
    blocks = [
        (cx - 90, cy, (0, 80, 200), (255, 255, 255)),  # USA
        (cx, cy - 10, (200, 30, 30), (255, 215, 0)),  # China
        (cx + 90, cy, (255, 255, 255), (0, 50, 120)),  # Russia
    ]
    labels = ["USA", "CHINA", "RUSSIA"]
    for i, (x, y, c1, c2) in enumerate(blocks):
        # pole
        draw.rectangle([x - 2, y - 60, x + 2, y + 40], fill=GREY)
        # flag
        draw.rectangle([x, y - 60, x + 52, y - 24], fill=c1)
        draw.rectangle([x, y - 42, x + 52, y - 24], fill=c2)
        # label
        lf = font(FONT_BOLD, 12)
        draw.text((x - 10, y + 44), labels[i], font=lf, fill=BODY)


def pictogram_gavel(draw, cx, cy):
    # head
    draw.rectangle([cx - 28, cy - 18, cx + 28, cy + 2], fill=BODY, outline=HEAD, width=2)
    # handle
    draw.rectangle([cx - 6, cy + 2, cx + 6, cy + 40], fill=AMBER)
    # base
    draw.rectangle([cx - 32, cy + 40, cx + 32, cy + 46], fill=GREY)


def pictogram_missile(draw, cx, cy):
    # dashed arc
    for i in range(0, 12):
        x = cx - 40 + i * 7
        y = cy - 10 - int(8 * (i / 11.0))
        draw.ellipse([x, y, x + 3, y + 3], fill=AMBER)
    # missile body
    draw.rectangle([cx + 30, cy - 14, cx + 56, cy + 6], fill=GREY)
    # nose
    draw.polygon([(cx + 56, cy - 14), (cx + 70, cy - 4), (cx + 56, cy + 6)], fill=AMBER)
    # fins
    draw.polygon([(cx + 30, cy - 14), (cx + 22, cy - 22), (cx + 30, cy - 6)], fill=GREY)
    draw.polygon([(cx + 30, cy + 6), (cx + 22, cy + 14), (cx + 30, cy - 2)], fill=GREY)


def pictogram_shield(draw, cx, cy):
    pts = [(cx, cy - 30), (cx + 26, cy - 18), (cx + 26, cy + 8), (cx, cy + 30), (cx - 26, cy + 8), (cx - 26, cy - 18)]
    draw.polygon(pts, fill=TEAL, outline=HEAD, width=2)
    draw.line([(cx - 10, cy), (cx - 2, cy + 8), (cx + 12, cy - 8)], fill=NAVY, width=3)


def pictogram_cyclone(draw, cx, cy):
    for r in range(6, 32, 6):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=0, end=270, fill=TEAL, width=2)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=AMBER)


def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Header band
    wf = font(FONT_BOLD, 26)
    draw.text((40, 30), "WORLD NEWS", font=wf, fill=AMBER)
    df = font(FONT_BOLD, 78)
    draw.text((40, 62), "19 NOVEMBER 2026", font=df, fill=HEAD)
    draw.rectangle([40, 150, W - 40, 153], fill=AMBER)

    # Lead card
    lx0, ly0, lx1, ly1 = 40, 170, W - 40, 470
    card(draw, lx0, ly0, lx1, ly1)
    chip(draw, lx0 + 24, ly0 + 20, "ASIA-PACIFIC  \u00b7  APEC, SHENZHEN", AMBER, 24)
    hl = ["TRUMP, XI AND PUTIN", "HOLD FIRST THREE-WAY", "SUMMIT IN CHINA"]
    hf = font(FONT_BOLD, 54)
    y = ly0 + 60
    for line in hl:
        draw.text((lx0 + 24, y), line, font=hf, fill=HEAD)
        y += 62
    bf = font(FONT_SANS, 25)
    draw.text((lx0 + 24, y + 4), "Trade, Ukraine and nuclear arms top the agenda of the APEC meeting.", font=bf, fill=BODY)
    pictogram_three_lecterns(draw, lx1 - 150, ly0 + 150)

    # 2x2 grid
    gx0, gy0 = 40, 490
    cw, ch = 490, 225
    gutter = 20
    cards = [
        ("WORLD COURT  \u00b7  THE HAGUE", "ICJ DELIVERS ROHINGYA GENOCIDE RULING", "The UN court's first genocide judgment, 7 years after the case was filed.", pictogram_gavel),
        ("MIDDLE EAST  \u00b7  GULF", "IRAN SAYS IT HIT KUWAIT AIR BASE", "Kuwait reports interceptions; the US strikes an Iranian island.", pictogram_missile),
        ("EUROPE  \u00b7  UKRAINE", "ZELENSKY TAKES DEFENCE PLEA TO BERLIN", "Allies meet on air defence as an Odesa strike kills four.", pictogram_shield),
        ("SOUTH ASIA  \u00b7  ODISHA", "SEVERE CYCLONE AKVAN NEARS COAST", "Red alerts in three coastal districts as the storm drives inland.", pictogram_cyclone),
    ]
    for i, (c, h, line, pic) in enumerate(cards):
        col = i % 2
        row = i // 2
        x0 = gx0 + col * (cw + gutter)
        y0 = gy0 + row * (ch + gutter)
        x1 = x0 + cw
        y1 = y0 + ch
        card(draw, x0, y0, x1, y1)
        chip(draw, x0 + 18, y0 + 14, c, TEAL, 20)
        hf2 = font(FONT_BOLD, 34)
        hl2 = wrap_lines(draw, h, hf2, cw - 36)
        # shrink if needed
        while len(hl2) > 2:
            hf2 = font(FONT_BOLD, 30)
            hl2 = wrap_lines(draw, h, hf2, cw - 36)
        y = y0 + 46
        for ln in hl2:
            draw.text((x0 + 18, y), ln, font=hf2, fill=HEAD)
            y += 40
        bf2 = fit_font(draw, line, FONT_SANS, 21, cw - 36, 20)
        draw.text((x0 + 18, y + 4), line, font=bf2, fill=BODY)
        pic(draw, x1 - 40, y0 + 44)

    # Bottom strip
    strip_y = H - 64
    draw.rectangle([0, strip_y, W, H], fill=CARD)
    draw.line([(0, strip_y), (W, strip_y)], fill=RULE, width=1)
    af = font(FONT_BOLD, 22)
    draw.text((40, strip_y + 20), "ALSO TODAY", font=af, fill=AMBER)
    aw = text_w(draw, "ALSO TODAY  ", af)
    sf = font(FONT_SANS, 22)
    draw.text((40 + aw + 4, strip_y + 20), "Nvidia lifts its sales outlook \u00b7 GTA VI launches to rave reviews \u00b7 North Korea expands its uranium plant", font=sf, fill=GREY)

    out = Path("entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
