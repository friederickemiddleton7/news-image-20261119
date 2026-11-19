#!/usr/bin/env python3
"""Front-page generator: Thursday 19 November 2026 (dense, multi-region)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (250, 248, 243)
INK = (18, 20, 26)
GREY = (92, 96, 106)
RED = (150, 32, 38)
BLUE = (24, 62, 112)
RULE = (196, 192, 182)
PANEL = (238, 234, 224)

F = Path("/usr/share/fonts/truetype/dejavu")


def fnt(name, size):
    return ImageFont.truetype(str(F / name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

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
    ("ASIA", "Tokyo court rules on a patent fight over battery cathodes"),
    ("AMERICAS", "Brazil's grain belt reports a record early soy planting"),
    ("AFRICA", "Kenya's grid adds 210 MW of geothermal capacity"),
    ("MIDEAST", "Gulf funds price a $2bn green hydrogen tranche"),
    ("OCEANIA", "Australia tightens rules on short-let housing in two cities"),
    ("EUROPE", "Portugal's parliament passes a coastal flood-insurance scheme"),
    ("ASIA", "India's central bank widens a pilot for cross-border settlement"),
    ("AMERICAS", "Canada sets a national cap on methane from older wells"),
    ("AFRICA", "Nigeria's regulator licenses two new mobile-money operators"),
    ("TECH", "An open speech model adds 40 low-resource languages"),
    ("HEALTH", "Trial results support a shorter course for a common infection"),
    ("CLIMATE", "Atlantic hurricane season closes with insured losses below forecast"),
    ("MARKETS", "Copper hits a nine-month high on grid and datacentre demand"),
    ("SPORT", "Qualifiers settle four places for next summer's tournament"),
    ("CULTURE", "A restored silent film opens the Marrakesh archive week"),
    ("EUROPE", "Greece and Italy agree a joint seabed survey zone"),
    ("ASIA", "Jakarta extends its flood-warning network to 60 more districts"),
    ("AMERICAS", "Mexico's congress debates a water-rights overhaul"),
    ("AFRICA", "Ethiopia's coffee exporters report a stronger harvest grade"),
    ("OCEANIA", "New Zealand funds a national landslide-risk map"),
    ("MIDEAST", "Jordan opens a solar-storage tender for 400 MW"),
    ("TECH", "Two regulators publish shared rules for model audits"),
    ("JUSTICE", "An appeals court orders a retrial in a landmark fraud case"),
]

COL_TOP = 556
COL_W = 300
GAP = 16
LEFT = 40


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and draw.textlength(trial, font=font) > max_w:
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

    # masthead
    d.rectangle([0, 0, W, 8], fill=RED)
    d.text((LEFT, 28), "THE WORLD TODAY", font=fnt(SERIF_B, 44), fill=INK)
    d.text((LEFT + 452, 34), "GLOBAL EDITION  ·  NO. 324", font=fnt(SANS, 14), fill=GREY)
    d.text((LEFT + 452, 56), "THURSDAY 19 NOVEMBER 2026", font=fnt(SANS_B, 17), fill=RED)
    d.text((LEFT + 452, 80), "32 STORIES  ·  SIX CONTINENTS", font=fnt(SANS, 13), fill=GREY)
    d.line([LEFT, 100, W - LEFT, 100], fill=INK, width=3)
    d.line([LEFT, 106, W - LEFT, 106], fill=RULE, width=1)

    # date banner
    d.rectangle([LEFT, 116, W - LEFT, 156], fill=PANEL)
    d.text((LEFT + 14, 126), "ONE DAY · 19 NOV 2026", font=fnt(SANS_B, 22), fill=BLUE)
    d.text((LEFT + 330, 130), "A front page for the day's world news", font=fnt(SANS, 15), fill=GREY)

    # lead story block
    y = 172
    headline = "River pact signed as flood season peaks across three continents"
    for line in wrap(d, headline, fnt(SERIF_B, 38), 600)[:3]:
        d.text((LEFT, y), line, font=fnt(SERIF_B, 38), fill=INK)
        y += 44
    y += 2
    deck = ("Environment and finance ministers from 24 states signed a shared river charter on "
            "Thursday, agreeing to publish reservoir levels and share flood forecasts in real time. "
            "The signing came as defences held along the lower delta and forecasters extended a "
            "high-water warning for a second week.")
    for line in wrap(d, deck, fnt(SERIF, 17), 600)[:5]:
        d.text((LEFT, y), line, font=fnt(SERIF, 17), fill=(40, 44, 52))
        y += 23
    # side facts panel
    px = 672
    d.rectangle([px, 172, W - LEFT, 392], fill=PANEL, outline=RULE)
    d.text((px + 14, 182), "THE DAY IN NUMBERS", font=fnt(SANS_B, 14), fill=RED)
    facts = [("24", "states sign the river charter"),
             ("6", "continents in this edition"),
             ("1.9°C", "November anomaly, provisional"),
             ("+0.4%", "copper, nine-month high")]
    fy = 208
    for num, label in facts:
        d.text((px + 14, fy), num, font=fnt(SERIF_B, 24), fill=BLUE)
        for line in wrap(d, label, fnt(SANS, 12), 150)[:2]:
            d.text((px + 96, fy + 4), line, font=fnt(SANS, 12), fill=(60, 64, 74))
            fy += 16
        fy += 26
    d.line([LEFT, 404, W - LEFT, 404], fill=INK, width=2)
    d.text((LEFT, 412), "TODAY'S STORIES", font=fnt(SANS_B, 15), fill=RED)
    d.text((LEFT + 150, 412), "eight front stories, twenty-four briefs", font=fnt(SANS, 13), fill=GREY)
    d.line([LEFT, 436, W - LEFT, 436], fill=RULE, width=1)

    # two-column lead grid: 4 columns x 2 rows between y=448 and y=544
    cw = (W - 2 * LEFT - 3 * GAP) // 4
    for i, (kick, head) in enumerate(LEAD):
        cx = LEFT + (i % 4) * (cw + GAP)
        cy = 448 + (i // 4) * 48
        d.text((cx, cy), kick, font=fnt(SANS_B, 11), fill=RED)
        ty = cy + 14
        for line in wrap(d, head, fnt(SANS_B, 12), cw)[:2]:
            assert ty + 14 <= 545, (kick, head, ty)
            d.text((cx, ty), line, font=fnt(SANS_B, 12), fill=INK)
            ty += 14
    d.line([LEFT, 548, W - LEFT, 548], fill=RULE, width=1)

    # briefs: 3 columns
    n_cols = 3
    per_col = (len(BRIEFS) + n_cols - 1) // n_cols
    bw = (W - 2 * LEFT - (n_cols - 1) * GAP) // n_cols
    for c in range(n_cols):
        cx = LEFT + c * (bw + GAP)
        if c:
            d.line([cx - GAP // 2, COL_TOP, cx - GAP // 2, 966], fill=RULE, width=1)
        y = COL_TOP
        for kick, text in BRIEFS[c * per_col:(c + 1) * per_col]:
            d.text((cx, y), kick, font=fnt(SANS_B, 10), fill=BLUE)
            y += 13
            lines = wrap(d, text, fnt(SANS, 12), bw)
            assert len(lines) <= 2, (kick, text, lines)
            for line in lines:
                d.text((cx, y), line, font=fnt(SANS, 12), fill=(30, 34, 42))
                y += 14
            y += 8
        assert y <= 966, ("column overflow", c, y)
    # footer
    d.rectangle([0, 968, W, H], fill=INK)
    d.text((LEFT, 980), "19 NOVEMBER 2026", font=fnt(SANS_B, 14), fill=(255, 255, 255))
    d.text((LEFT + 190, 981), "one day · one front page · six continents", font=fnt(SANS, 12), fill=(200, 205, 215))
    d.text((W - LEFT - 120, 981), "WORLD EDITION", font=fnt(SANS_B, 12), fill=(242, 179, 61))

    img = img.convert("RGB")
    img.save(path, "PNG", optimize=True)
    return img


if __name__ == "__main__":
    out = Path("/root/newsimg-20261119/entry.png")
    im = build(out)
    print("wrote", out, im.size, out.stat().st_size, "bytes")