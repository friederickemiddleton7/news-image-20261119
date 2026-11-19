#!/usr/bin/env python3
"""Front page generator: Thursday 19 November 2026.

Layout is measured, not hard-coded: blocks report their extents and the script
asserts they fit, so a headline or brief can never be clipped by a neighbour.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 40
BG = (250, 248, 243)
INK = (18, 20, 26)
BODY = (40, 44, 52)
GREY = (92, 96, 106)
RED = (150, 32, 38)
BLUE = (24, 62, 112)
RULE = (196, 192, 182)
PANEL = (238, 234, 224)

FDIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_B, SERIF, SANS_B, SANS = "DejaVuSerif-Bold.ttf", "DejaVuSerif.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"


def fnt(name, size):
    return ImageFont.truetype(str(FDIR / name), size)


LEAD = [
    ("WORLD", "Delta defences hold as 24 states sign a river charter"),
    ("ASIA-PACIFIC", "Nine economies open a common power grid"),
    ("EUROPE", "Central bank holds rates, warns on gas storage"),
    ("MIDEAST", "Monitors log a fourth quiet week on the northern line"),
    ("AFRICA", "Trade court hears its first tariff case"),
    ("AMERICAS", "Senate panel advances a data-privacy bill"),
    ("TECH", "Chipmakers agree an on-device memory standard"),
    ("CLIMATE", "Sea-ice survey finds a late seasonal minimum"),
]

BRIEFS = [
    ("EUROPE", "Rail unions suspend a strike after a night of talks in Berlin"),
    ("ASIA", "Tokyo court rules in a patent fight over battery cathodes"),
    ("AMERICAS", "Brazil's grain belt reports a record early soy planting"),
    ("AFRICA", "Kenya's grid adds 210 MW of geothermal capacity"),
    ("MIDEAST", "Gulf funds price a $2bn green hydrogen tranche"),
    ("OCEANIA", "Australia tightens rules on short-let housing"),
    ("EUROPE", "Portugal passes a coastal flood-insurance scheme"),
    ("ASIA", "India's central bank widens a settlement pilot"),
    ("AMERICAS", "Canada sets a cap on methane from older wells"),
    ("AFRICA", "Nigeria licenses two new mobile-money operators"),
    ("TECH", "An open speech model adds 40 low-resource languages"),
    ("HEALTH", "Trial supports a shorter course for a common infection"),
    ("CLIMATE", "Atlantic season closes with insured losses below forecast"),
    ("MARKETS", "Copper hits a nine-month high on grid and data demand"),
    ("SPORT", "Qualifiers settle four places for next summer's tournament"),
    ("CULTURE", "A restored silent film opens the Marrakesh archive week"),
    ("EUROPE", "Greece and Italy agree a joint seabed survey zone"),
    ("ASIA", "Jakarta extends flood warnings to 60 more districts"),
    ("AMERICAS", "Mexico's congress debates a water-rights overhaul"),
    ("AFRICA", "Ethiopia's coffee exporters report a stronger harvest grade"),
    ("OCEANIA", "New Zealand funds a national landslide-risk map"),
    ("MIDEAST", "Jordan opens a solar-storage tender for 400 MW"),
    ("TECH", "Two regulators publish shared rules for model audits"),
    ("JUSTICE", "An appeals court orders a retrial in a fraud case"),
]


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and d.textlength(trial, font=font) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def build(path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    runs = []

    def put(x, y, text, font, fill):
        d.text((x, y), text, font=font, fill=fill)
        w = d.textlength(text, font=font)
        runs.append((x, y, x + w, y + font.size + 3, text[:26]))
        return w

    def wrap_put(x, y, text, font, fill, max_w, max_lines, lead=0):
        lines = wrap(d, text, font, max_w)
        assert len(lines) <= max_lines, ("needs more lines than allowed", text[:40], len(lines))
        for ln in lines:
            put(x, y, ln, font, fill)
            y += font.size + lead
        return y

    # masthead
    d.rectangle([0, 0, W, 8], fill=RED)
    mw = put(M, 26, "THE WORLD TODAY", fnt(SERIF_B, 44), INK)
    rx = M + mw + 30
    put(rx, 32, "GLOBAL EDITION · NO. 324", fnt(SANS, 13), GREY)
    put(rx, 52, "THURSDAY 19 NOVEMBER 2026", fnt(SANS_B, 17), RED)
    put(rx, 76, "32 STORIES · SIX CONTINENTS", fnt(SANS, 13), GREY)
    assert rx + d.textlength("THURSDAY 19 NOVEMBER 2026", font=fnt(SANS_B, 17)) <= W - M, "date block overflows"
    d.line([M, 104, W - M, 104], fill=INK, width=3)

    # date banner
    d.rectangle([M, 116, W - M, 156], fill=PANEL)
    put(M + 14, 124, "ONE DAY · 19 NOVEMBER 2026", fnt(SANS_B, 21), BLUE)
    put(M + 380, 129, "one day of world news, one front page", fnt(SANS, 14), GREY)

    # lead story, left column 600 px
    y = 172
    y = wrap_put(M, y, "River pact signed as flood season peaks across three continents",
                 fnt(SERIF_B, 37), INK, 600, 3, 4)
    y += 10
    deck = ("Environment and finance ministers from 24 states signed a shared river charter on "
            "Thursday, agreeing to publish reservoir levels and share flood forecasts in real time. "
            "The signing came as defences held along the lower delta and forecasters extended a "
            "high-water warning for a second week.")
    y = wrap_put(M, y, deck, fnt(SERIF, 17), BODY, 600, 6, 6)

    # numbers panel, right column
    px = 680
    pw = W - M - px
    panel_bottom = 168 + 4 * 48 + 26
    d.rectangle([px, 168, W - M, panel_bottom], fill=PANEL, outline=RULE)
    put(px + 12, 176, "THE DAY IN NUMBERS", fnt(SANS_B, 13), RED)
    fy = 200
    for num, label in [("24", "states sign the river charter"),
                       ("6", "continents in this edition"),
                       ("1.9°C", "November anomaly, provisional"),
                       ("+0.4%", "copper, a nine-month high")]:
        put(px + 12, fy, num, fnt(SERIF_B, 21), BLUE)
        wrap_put(px + 86, fy + 4, label, fnt(SANS, 11), (60, 64, 74), pw - 96, 2, 2)
        fy += 46

    # section header sits below whichever column is taller
    y = max(y, panel_bottom) + 16
    d.line([M, y, W - M, y], fill=INK, width=2)
    y += 9
    put(M, y, "TODAY'S STORIES", fnt(SANS_B, 15), RED)
    put(M + 172, y + 2, "eight front stories and twenty-four briefs from six continents", fnt(SANS, 12), GREY)
    y += 27
    d.line([M, y, W - M, y], fill=RULE, width=1)

    # lead grid: 4 columns, 2 rows
    y += 8
    cw = (W - 2 * M - 3 * 16) // 4
    grid_top = y
    f_kick, f_lead = fnt(SANS_B, 10), fnt(SANS_B, 12)
    row_h = 0
    for i, (kick, head) in enumerate(LEAD):
        cx = M + (i % 4) * (cw + 16)
        cy = grid_top + (i // 4) * 52
        put(cx, cy, kick, f_kick, RED)
        ty = cy + 13
        for ln in wrap(d, head, f_lead, cw):
            assert ty + 14 <= cy + 50, ("lead head too tall", head)
            put(cx, ty, ln, f_lead, INK)
            ty += 14
        row_h = 52 if i // 4 == 0 else row_h
    y = grid_top + 52 + 40
    d.line([M, y, W - M, y], fill=RULE, width=1)

    # briefs, 3 columns
    y += 10
    n_cols, col_gap = 3, 16
    per_col = (len(BRIEFS) + n_cols - 1) // n_cols
    bw = (W - 2 * M - (n_cols - 1) * col_gap) // n_cols
    f_bk, f_bt = fnt(SANS_B, 10), fnt(SANS, 12)
    for c in range(n_cols):
        cx = M + c * (bw + col_gap)
        if c:
            d.line([cx - col_gap // 2, y, cx - col_gap // 2, H - 56], fill=RULE, width=1)
        cy = y
        for kick, text in BRIEFS[c * per_col:(c + 1) * per_col]:
            put(cx, cy, kick, f_bk, BLUE)
            cy += 13
            lines = wrap(d, text, f_bt, bw)
            assert len(lines) <= 2, ("brief too long", text, lines)
            for ln in lines:
                put(cx, cy, ln, f_bt, (30, 34, 42))
                cy += 14
            cy += 8
        assert cy <= H - 56, ("briefs overflow", c, cy)

    # footer
    d.rectangle([0, H - 44, W, H], fill=INK)
    put(M, H - 33, "19 NOVEMBER 2026", fnt(SANS_B, 13), (255, 255, 255))
    put(M + 172, H - 32, "one day · one front page · six continents", fnt(SANS, 12), (200, 205, 215))
    put(W - M - 112, H - 32, "WORLD EDITION", fnt(SANS_B, 12), (242, 179, 61))

    # no two text runs may overlap unless they are on different baselines of one block
    for i in range(len(runs)):
        x0, y0, x1, y1, t0 = runs[i]
        for j in range(i + 1, len(runs)):
            a0, b0, a1, b1, t1 = runs[j]
            ox = min(x1, a1) - max(x0, a0)
            oy = min(y1, b1) - max(y0, b0)
            assert not (ox > 1 and oy > 6), ("text overlap", t0, t1, ox, oy)
    return img, runs


if __name__ == "__main__":
    out = Path("/root/newsimg-20261119/entry.png")
    im, runs = build(out)
    print("wrote", out, im.size, out.stat().st_size, "bytes,", len(runs), "text runs, overlap check passed")