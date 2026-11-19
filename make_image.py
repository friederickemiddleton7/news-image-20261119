#!/usr/bin/env python3
"""Generate the 19 November 2026 world news image."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

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


def font(path, size):
    return ImageFont.truetype(str(path), size)


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


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


def pictogram_gavel(draw, cx, cy):
    draw.rectangle([cx - 28, cy - 18, cx + 28, cy + 2], fill=BODY, outline=HEAD, width=2)
    draw.rectangle([cx - 6, cy + 2, cx + 6, cy + 40], fill=AMBER)
    draw.rectangle([cx - 32, cy + 40, cx + 32, cy + 46], fill=GREY)


def pictogram_missile(draw, cx, cy):
    for i in range(0, 10):
        x = cx - 36 + i * 7
        y = cy - 8 - int(6 * (i / 9.0))
        draw.ellipse([x, y, x + 3, y + 3], fill=AMBER)
    draw.rectangle([cx + 20, cy - 12, cx + 44, cy + 6], fill=GREY)
    draw.polygon([(cx + 44, cy - 12), (cx + 56, cy - 2), (cx + 44, cy + 6)], fill=AMBER)
    draw.polygon([(cx + 20, cy - 12), (cx + 12, cy - 20), (cx + 20, cy - 4)], fill=GREY)
    draw.polygon([(cx + 20, cy + 6), (cx + 12, cy + 14), (cx + 20, cy - 2)], fill=GREY)


def pictogram_shield(draw, cx, cy):
    pts = [(cx, cy - 30), (cx + 26, cy - 18), (cx + 26, cy + 8), (cx, cy + 30), (cx - 26, cy + 8), (cx - 26, cy - 18)]
    draw.polygon(pts, fill=TEAL, outline=HEAD, width=2)
    draw.line([(cx - 10, cy), (cx - 2, cy + 8), (cx + 12, cy - 8)], fill=NAVY, width=3)


def pictogram_cyclone(draw, cx, cy):
    for r in range(6, 28, 6):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=0, end=270, fill=TEAL, width=2)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=AMBER)


def flag_usa(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(255, 255, 255))
    stripe_h = h // 7
    for i in range(7):
        if i % 2 == 0:
            draw.rectangle([x0, y0 + i * stripe_h, x0 + w, y0 + (i + 1) * stripe_h], fill=(190, 20, 30))
    canton_w = int(w * 0.4)
    canton_h = int(h * 0.54)
    draw.rectangle([x0, y0, x0 + canton_w, y0 + canton_h], fill=(0, 40, 120))


def flag_china(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(200, 30, 30))
    star_cx = x0 + int(w * 0.22)
    star_cy = y0 + int(h * 0.35)
    r = int(min(w, h) * 0.12)
    pts = []
    for i in range(5):
        a = -90 + i * 72
        rad = math.radians(a)
        pts.append((star_cx + int(r * math.cos(rad)), star_cy + int(r * math.sin(rad))))
        a2 = -90 + i * 72 + 36
        rad2 = math.radians(a2)
        pts.append((star_cx + int(r * 0.4 * math.cos(rad2)), star_cy + int(r * 0.4 * math.sin(rad2))))
    draw.polygon(pts, fill=(255, 215, 0))


def flag_russia(draw, x0, y0, w, h):
    band = h // 3
    draw.rectangle([x0, y0, x0 + w, y0 + band], fill=(255, 255, 255))
    draw.rectangle([x0, y0 + band, x0 + w, y0 + 2 * band], fill=(0, 50, 120))
    draw.rectangle([x0, y0 + 2 * band, x0 + w, y0 + h], fill=(200, 30, 30))


def lead_columns(draw, rx0, ry0, rx1, ry1):
    col_w = 78
    col_h = 150
    gap = 18
    total = 3 * col_w + 2 * gap
    start_x = rx0 + (rx1 - rx0 - total) // 2
    names = [("TRUMP", "USA", flag_usa), ("XI", "CHINA", flag_china), ("PUTIN", "RUSSIA", flag_russia)]
    for i, (name, country, flagfn) in enumerate(names):
        cx = start_x + i * (col_w + gap)
        cy = ry0 + 10
        draw.rounded_rectangle([cx, cy, cx + col_w, cy + col_h], radius=8, fill=CARD, outline=RULE, width=2)
        fx0 = cx + 8
        fy0 = cy + 8
        fw = col_w - 16
        fh = 40
        flagfn(draw, fx0, fy0, fw, fh)
        nf = font(FONT_BOLD, 22)
        draw.text((cx + (col_w - text_w(draw, name, nf)) // 2, cy + col_h + 8), name, font=nf, fill=HEAD)
        cf = font(FONT_SANS, 15)
        draw.text((cx + (col_w - text_w(draw, country, cf)) // 2, cy + col_h + 34), country, font=cf, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)
    checks = []

    wf = font(FONT_BOLD, 26)
    draw.text((40, 30), "WORLD NEWS", font=wf, fill=AMBER)
    checks.append(("WORLD NEWS", wf, 944))
    df = font(FONT_BOLD, 78)
    draw.text((40, 62), "19 NOVEMBER 2026", font=df, fill=HEAD)
    checks.append(("19 NOVEMBER 2026", df, 944))
    draw.rectangle([40, 150, W - 40, 153], fill=AMBER)

    lx0, ly0, lx1, ly1 = 40, 170, W - 40, 470
    card(draw, lx0, ly0, lx1, ly1)
    chip(draw, lx0 + 24, ly0 + 20, "ASIA-PACIFIC  \u00b7  APEC, SHENZHEN", AMBER, 24)
    cfont = font(FONT_BOLD, 24)
    checks.append(("ASIA-PACIFIC  \u00b7  APEC, SHENZHEN", cfont, 944))
    hl = ["TRUMP, XI AND PUTIN", "HOLD FIRST THREE-WAY", "SUMMIT IN CHINA"]
    hf = font(FONT_BOLD, 40)
    y = ly0 + 60
    reserved_x = lx1 - 340
    max_head_w = reserved_x - (lx0 + 24) - 24
    for line in hl:
        draw.text((lx0 + 24, y), line, font=hf, fill=HEAD)
        checks.append((line, hf, max_head_w))
        y += 50
    bf = font(FONT_SANS, 20)
    body_line = "Trade, Ukraine and nuclear arms top the agenda of the APEC meeting."
    blines = wrap_lines(draw, body_line, bf, max_head_w)
    by = y + 4
    for bl in blines:
        draw.text((lx0 + 24, by), bl, font=bf, fill=BODY)
        checks.append((bl, bf, max_head_w))
        by += 24
    lead_columns(draw, reserved_x, ly0 + 20, lx1 - 20, ly1 - 20)

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
        checks.append((c, font(FONT_BOLD, 20), cw - 36))
        hf2 = font(FONT_BOLD, 34)
        hl2 = wrap_lines(draw, h, hf2, cw - 36)
        while len(hl2) > 2:
            hf2 = font(FONT_BOLD, 30)
            hl2 = wrap_lines(draw, h, hf2, cw - 36)
        y = y0 + 46
        for ln in hl2:
            draw.text((x0 + 18, y), ln, font=hf2, fill=HEAD)
            checks.append((ln, hf2, cw - 36))
            y += 40
        max_teaser_w = cw - 36
        teaser_lines = None
        chosen_size = None
        for size in (21, 20, 19):
            f = font(FONT_SANS, size)
            tl = wrap_lines(draw, line, f, max_teaser_w)
            if len(tl) <= 2:
                teaser_lines = tl
                chosen_size = size
                break
        if teaser_lines is None:
            raise RuntimeError(f"teaser cannot fit: {line}")
        tf = font(FONT_SANS, chosen_size)
        block_h = len(teaser_lines) * 26
        if y + 4 + block_h > y1 - 12:
            raise RuntimeError(f"teaser block overflows card: {line}")
        ty = y + 4
        for ln in teaser_lines:
            draw.text((x0 + 18, ty), ln, font=tf, fill=BODY)
            checks.append((ln, tf, max_teaser_w))
            ty += 26
        cx = x1 - 56
        cy = y0 + 52
        pic(draw, cx, cy)

    strip_y = H - 64
    draw.rectangle([0, strip_y, W, H], fill=CARD)
    draw.line([(0, strip_y), (W, strip_y)], fill=RULE, width=1)
    af = font(FONT_BOLD, 22)
    draw.text((40, strip_y + 20), "ALSO TODAY", font=af, fill=AMBER)
    aw = text_w(draw, "ALSO TODAY  ", af)
    checks.append(("ALSO TODAY", af, 944))
    ticker = "Nvidia lifts its sales outlook \u00b7 GTA VI launches to rave reviews \u00b7 North Korea expands its uranium plant"
    sf = font(FONT_SANS, 22)
    ticker_lines = wrap_lines(draw, ticker, sf, 944 - int(aw))
    if len(ticker_lines) > 2:
        ticker = "Nvidia lifts sales outlook \u00b7 GTA VI launches to rave reviews \u00b7 North Korea expands uranium plant"
        ticker_lines = wrap_lines(draw, ticker, sf, 944 - int(aw))
    if len(ticker_lines) > 2:
        raise RuntimeError("ticker cannot fit")
    tx = 40 + int(aw) + 4
    ty = strip_y + 20
    for ln in ticker_lines:
        draw.text((tx, ty), ln, font=sf, fill=GREY)
        checks.append((ln, sf, 944 - int(aw)))
        ty += 26

    for txt, f, mw in checks:
        if text_w(draw, txt, f) > mw + 0.5:
            raise RuntimeError(f"text exceeds max width: {txt!r} ({text_w(draw, txt, f):.1f} > {mw})")

    out = Path("entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
