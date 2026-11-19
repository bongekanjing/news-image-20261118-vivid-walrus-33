"""Builds the front page PNG. Run: python3 build.py [out.png] [--debug]

Layout is fixed and measured: every block reports the baseline it reached, so
the page either fits the canvas or the debug output says exactly which block
overran. No block is positioned by a guessed constant.
"""
import json
import os
import sys

from PIL import Image, ImageDraw

import emblems
import fonts as F
import layout as L
import news as N

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

M = 24
COL = L.W - 2 * M
BOT = L.H - M
GUT = 13

# The band's reading order. Charts and stand-offs are spread so that no two
# panels of the same diagram type are neighbours.
CARD_ORDER = [0, 2, 1, 4, 3,
              5, 7, 6, 9, 8]

BRIEF_REGION = {
    "US": "AMERICAS", "CANADA": "AMERICAS", "BRAZIL": "AMERICAS", "HAITI": "AMERICAS",
    "UK": "EUROPE", "FRANCE": "EUROPE", "GERMANY": "EUROPE", "RUSSIA": "EUROPE",
    "POLAND": "EUROPE", "ITALY": "EUROPE", "SPAIN": "EUROPE",
    "JAPAN": "ASIA", "SOUTH KOREA": "ASIA", "CHINA": "ASIA", "MYANMAR": "ASIA",
    "THAILAND": "ASIA", "CAMBODIA": "ASIA", "VIETNAM": "ASIA", "SINGAPORE": "ASIA",
    "INDONESIA": "ASIA", "INDIA": "ASIA", "NEPAL": "ASIA", "BANGLADESH": "ASIA",
    "PAKISTAN": "ASIA", "MALAYSIA": "ASIA", "SRI LANKA": "ASIA",
    "SUDAN": "AFRICA", "NIGERIA": "AFRICA", "GHANA": "AFRICA", "GUINEA": "AFRICA",
    "KENYA": "AFRICA", "ANGOLA": "AFRICA", "SOUTH AFRICA": "AFRICA",
    "ZIMBABWE": "AFRICA", "MOZAMBIQUE": "AFRICA", "DR CONGO": "AFRICA",
    "UGANDA": "AFRICA", "MADAGASCAR": "AFRICA", "SENEGAL": "AFRICA",
    "TUNISIA": "AFRICA", "SOMALIA": "AFRICA", "LIBERIA": "AFRICA",
    "AUSTRALIA": "OCEANIA", "NEW ZEALAND": "OCEANIA", "NIUE": "OCEANIA",
    "IRAN": "MIDDLE EAST", "JORDAN": "MIDDLE EAST", "ISRAEL": "MIDDLE EAST",
    "WORLD": "WORLD",
}


def brief_region(place):
    return BRIEF_REGION.get(place, "WORLD")


def count_regions():
    counts = {}
    for it in N.LEADS + N.CARDS:
        k = L.region_of(it["kicker"])
        counts[k] = counts.get(k, 0) + 1
    for place, _ in N.SHORT_BRIEFS:
        k = brief_region(place)
        counts[k] = counts.get(k, 0) + 1
    return counts


def plaque(page, x, y, n, size=13.5):
    """A small numbered tab: the page's spine, echoed by the map pins."""
    ss = page.ss
    page.d.rectangle([x * ss, y * ss, (x + size) * ss, (y + size) * ss],
                     fill=(26, 22, 18))
    f = F.caps(size * 0.62, 700)
    t = str(n)
    w = page.tw(t, f)
    page.text(x + (size - w) / 2, y + size * 0.20, t, f, (250, 247, 240))


def draw_map(page, x, y, w, h):
    """Locator map on its own canvas, so stray geometry is clipped, not bled."""
    with open(os.path.join(HERE, "land.json")) as fh:
        polys = json.load(fh)
    lon0, lon1 = -170.0, 185.0
    lat0, lat1 = 74.0, -56.0
    k = min(w / (lon1 - lon0), h / (lat0 - lat1))
    ox = (w - (lon1 - lon0) * k) / 2
    oy = (h - (lat0 - lat1) * k) / 2
    ss = page.ss

    tile = Image.new("RGB", (max(2, int(round(w * ss))), max(2, int(round(h * ss)))),
                     (222, 228, 233))
    td = ImageDraw.Draw(tile)

    def proj(lon, lat):
        return ((ox + (lon - lon0) * k) * ss, (oy + (lat0 - lat) * k) * ss)

    for poly in polys:
        for ring in poly:
            pts = [proj(lo, la) for lo, la in ring]
            if len(pts) >= 3:
                td.polygon(pts, fill=(201, 197, 185))

    from collections import Counter
    counts = Counter(pl for pl, _ in N.SHORT_BRIEFS)
    for it in N.CARDS + N.LEADS:
        counts[it["place"]] = counts.get(it["place"], 0) + 3

    for place, n in counts.items():
        if place not in N.LOC:
            continue
        lat, lon = N.LOC[place]
        cx, cy = proj(lon, lat)
        if not (2 <= cx <= w * ss - 2 and 2 <= cy <= h * ss - 2):
            continue
        if n >= 3:
            r = 3.0 * ss
            td.ellipse([cx - r, cy - r, cx + r, cy + r],
                       fill=(152, 34, 34), outline=(250, 248, 243), width=2)
        else:
            r = 1.7 * ss
            td.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(104, 96, 86))

    page.im.paste(tile, (int(round(x * ss)), int(round(y * ss))))
    page.d.rectangle([x * ss, y * ss, (x + w) * ss, (y + h) * ss],
                     outline=(203, 199, 189), width=1)
    page.text(x + 4.5, y + 3.2, "WHERE IT HAPPENED", F.caps(7.0, 700),
              (92, 86, 78), track=0.9)
    ly = y + h - 8.8
    page.d.ellipse([(x + 5.5) * ss, (ly + 1.5) * ss,
                    (x + 9.7) * ss, (ly + 5.7) * ss], fill=(152, 34, 34))
    page.text(x + 12.5, ly, "LEAD OR CARD", F.caps(5.7, 600), (118, 111, 100), track=0.4)
    page.d.ellipse([(x + 68) * ss, (ly + 2.0) * ss,
                    (x + 72.2) * ss, (ly + 6.2) * ss], fill=(104, 96, 86))
    page.text(x + 75, ly, "BRIEF", F.caps(5.7, 600), (118, 111, 100), track=0.4)


class Builder:
    def __init__(self, debug=False):
        self.p = L.Page()
        self.pg = self.p
        self.debug = debug
        self.log = []

    def mark(self, name, y):
        self.log.append((name, round(y, 1)))

    def run(self, path):
        p = self.pg
        y = M

        # ---------------- nameplate ----------------
        # A solid ink band across the top, the way a front page is anchored:
        # it also gives the page a dark mass that survives at 300 px.
        counts = count_regions()
        total_stories = sum(counts.values())
        arts = len(N.CARDS) + len(N.LEADS)

        band_top = M
        band_h = 80.0
        p.rect(M, band_top, COL, band_h, L.INK)

        # the paper's name, big and tracked out
        f_logo, lsize = p.fit("THE WORLD IN ONE DAY", lambda z: F.caps(z, 800),
                              COL * 0.55, 34)
        p.text(M + 15, band_top + 12.0, "THE WORLD IN ONE DAY", f_logo,
               (247, 243, 234), track=lsize * 0.13)

        # the date, set as the second-largest thing on the page
        f_day, dsize = p.fit(f"{N.DAY} {N.DATE}", lambda z: F.serif(z, 700),
                             COL * 0.40, 32)
        day_s = f"{N.DAY} {N.DATE}"
        dw = p.tw(day_s, f_day)
        p.text(M + COL - 15 - dw, band_top + 15.0, day_s, f_day, (247, 243, 234))

        # a red flash and the day's tally, on one baseline under the logo
        p.rect(M + 15, band_top + 55.0, 96.0, 3.6, L.RED)
        f_meta = F.caps(9.0, 700)
        meta = f"{total_stories} STORIES \u00b7 {len(counts)} REGIONS \u00b7 {arts} DRAWN"
        mx0 = M + 121
        p.text(mx0, band_top + 50.0, meta, f_meta, (216, 206, 190), track=1.35)
        mw = p.tw(meta, f_meta) + 1.35 * (len(meta) - 1)

        # a hairline crosses the void from the tally to the dateline, so the
        # gap reads as an interval between two anchors rather than a hole
        hx0, hx1 = mx0 + mw + 14, M + COL - 15 - dw - 14
        if hx1 > hx0 + 20:
            p.d.rectangle([hx0 * L.SS, (band_top + 51.6) * L.SS,
                           hx1 * L.SS, (band_top + 52.6) * L.SS],
                          fill=(92, 86, 78))

        y = band_top + band_h + 7.0
        self.mark("masthead", y)

        # ---------------- region key ----------------
        # One equal tile per region, each tile filled with its own colour and
        # labelled inside it. An earlier version drew a proportional bar and
        # then spaced the labels evenly underneath, so MIDDLE EAST sat 86 px
        # left of its own segment and OCEANIA 110 px left of its: the key read
        # as two grids that shared no axis. Equal tiles make the label-to-colour
        # binding unambiguous at any width.
        segs = [(r, counts[r]) for r in L.REGION_ORDER if counts.get(r)]
        nseg = len(segs)
        tile_w = COL / nseg
        tile_h = 13.6
        f_leg = F.caps(8.0, 700)

        def _lum(c):
            def ch(v):
                v /= 255.0
                return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
            return (0.2126 * ch(c[0]) + 0.7152 * ch(c[1])
                    + 0.0722 * ch(c[2]))

        def _contrast(a, b):
            la, lb = _lum(a), _lum(b)
            return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

        for i, (r, c) in enumerate(segs):
            tx = M + i * tile_w
            fill = L.REGION_COLOUR[r]
            p.d.rectangle([tx * L.SS, y * L.SS,
                           (tx + tile_w - 2.0) * L.SS, (y + tile_h) * L.SS],
                          fill=fill)
            # The gold MIDDLE EAST tile is light enough that cream-on-colour is
            # only 3.4:1; pick whichever ink reaches the higher contrast so
            # every label stays legible rather than most of them.
            light, dark = (250, 247, 240), (24, 20, 16)
            ink = light if _contrast(light, fill) >= _contrast(dark, fill) else dark
            lab = f"{r} {c}"
            lw = p.tw(lab, f_leg) + 0.8 * (len(lab) - 1)
            p.text(tx + (tile_w - 2.0 - lw) / 2, y + 3.4, lab, f_leg,
                   ink, track=0.8)
        y += tile_h + 5.2

        # ---------------- the day in numbers ----------------
        colw = COL / len(N.STATS)
        top = y
        cap_f = F.caps(8.6, 600)
        for i, (num, cap) in enumerate(N.STATS):
            x = M + i * colw
            fn, ns = p.fit(num, lambda z: F.serif(z, 800), colw - 16, 25)
            p.text(x, top, num, fn, L.RED if i == 0 else L.INK)
            cy = top + ns * 0.90 + 1.5
            for ln in cap.split("\n"):
                p.text(x, cy, ln, cap_f, L.GREY, track=0.35)
                cy += 9.6
            if i:
                p.vline(x - 8, top + 2, top + 30, L.FAINT, 1.0)
        y = top + 36
        p.hline(M, y, L.W - M, L.FAINT, 1.0)
        y += 7
        self.mark("stats", y)

        # ---------------- the lead: art left, type right ----------------
        art_w = COL * 0.455
        text_w = COL - art_w - GUT
        art_h = art_w * 0.62
        lead = N.LEADS[0]
        acc = L.col_for(lead["kicker"])
        emblems.draw(p, lead["art"], M, y, art_w, art_h, acc, lead.get("tag"))
        plaque(p, M, y, 1)

        tx = M + art_w + GUT
        ty = y
        p.text(tx, ty, lead["kicker"], F.caps(10.0, 700), acc, track=1.1)
        ty += 15
        # headline: shrink until no line is a lonely short word, then until
        # it fits three lines. A one-word line is the worst hole on a front page.
        def _break(sz):
            f_ = F.serif(sz, 800)
            if "\n" in lead["headline"]:
                return lead["headline"].split("\n"), f_
            return p.wrap(lead["headline"], f_, text_w), f_

        size = 39.0
        lines, fh = _break(size)
        while size > 20:
            last = lines[-1]
            lonely = len(lines) > 1 and (
                len(last.split()) == 1 or p.tw(last, fh) < text_w * 0.55)
            if (len(lines) > 3 or lonely):
                size -= 1.0
                lines, fh = _break(size)
            else:
                break
        for ln in lines:
            p.text(tx, ty, ln, fh, L.INK)
            ty += size * 0.92
        ty += 5
        ty = p.para(tx, ty, lead["dek"], F.text(13.0, 400), text_w, 15.8,
                    (38, 34, 29), maxlines=3)
        ty += 10
        p.hline(tx, ty, L.W - M, L.FAINT, 1.0)
        ty += 8

        # two secondary leads, compact, still in the type column
        for n, it in enumerate(N.LEADS[1:], start=2):
            sacc = L.col_for(it["kicker"])
            plaque(p, tx, ty - 0.8, n, size=11.5)
            p.text(tx + 16, ty, it["kicker"], F.caps(8.2, 700), sacc, track=0.9)
            ty += 11
            sfh, ssz = F.serif(16.4, 800), 16.4
            slines = p.wrap(it["headline"], sfh, text_w)
            while len(slines) > 2 and ssz > 11:
                ssz -= 0.4
                sfh = F.serif(ssz, 800)
                slines = p.wrap(it["headline"], sfh, text_w)
            for ln in slines:
                p.text(tx, ty, ln, sfh, L.INK)
                ty += ssz * 0.94
            ty += 1.5
            ty = p.para(tx, ty, it["dek"], F.text(9.8, 400), text_w, 11.4,
                        (60, 55, 48), maxlines=2)
            ty += 8

        y = max(y + art_h, ty) + 9
        p.hline(M, y - 5, L.W - M, L.INK, 1.5)
        self.mark("lead", y)

        # ---------------- cards: two bands of five ----------------
        per_row = 5
        cw = (COL - (per_row - 1) * GUT) / per_row
        art_h2 = cw * 0.56
        ck = F.caps(8.8, 700)
        for band in range(2):
            band_bottom = y
            for i in range(per_row):
                k = band * per_row + i
                if k >= len(N.CARDS):
                    break
                # order chosen so like art never sits beside like art
                it = N.CARDS[CARD_ORDER[k]]
                x = M + i * (cw + GUT)
                acc = L.col_for(it["kicker"])
                # no figure chip at card size: at 300px it reads as a smear
                emblems.draw(p, it["art"], x, y, cw, art_h2, acc, None)
                plaque(p, x, y, k + 2, size=11.5)
                ky = y + art_h2 + 4.0
                p.text(x, ky, it["kicker"], ck, acc, track=0.5)
                ky += 11.4
                fh, size = F.cond(17.6, 600), 17.6
                lines = p.wrap(it["headline"], fh, cw)
                while len(lines) > 3 and size > 12.0:
                    size -= 0.4
                    fh = F.cond(size, 600)
                    lines = p.wrap(it["headline"], fh, cw)
                for ln in lines:
                    p.text(x, ky, ln, fh, L.INK)
                    ky += size * 0.98
                band_bottom = max(band_bottom, ky)
            y = band_bottom + (10 if band == 0 else 0)
        y += 6
        p.hline(M, y - 4, L.W - M, L.FAINT, 1.0)
        self.mark("cards", y)

        # ---------------- index left, map right ----------------
        map_w = COL * 0.315
        idx_w = COL - map_w - GUT - 4
        p.text(M, y, f"ALSO ON {N.DAY.upper()}, {N.DATE.upper()}",
               F.caps(9.2, 700), L.INK, track=1.0)
        by = y + 12
        items = N.SHORT_BRIEFS
        foot_h = 34
        room = BOT - foot_h - by - 6

        best = None
        for ncol in (2, 3):
            cgap = 11.0
            bw_col = (idx_w - cgap * (ncol - 1)) / ncol
            for fs in (10.8, 10.4, 10.0, 9.6, 9.2, 8.8):
                fb, fp = F.text(fs, 400), F.text(fs, 700)
                row_h = fs * 1.34
                per = int(room // row_h)
                if per < 4:
                    continue
                n = min(len(items), per * ncol)
                if any(p.tw(t, fb) > bw_col - p.tw(pl + " ", fp) - 1.2
                       for pl, t in items[:n]):
                    continue
                if best is None:
                    best = (fs, fb, fp, row_h, ncol, cgap, bw_col, per, n)
                break
        if best is None:
            ncol, cgap = 3, 9.0
            bw_col = (idx_w - cgap * (ncol - 1)) / ncol
            fs = 8.2
            per = int(room // (fs * 1.32))
            best = (fs, F.text(fs, 400), F.text(fs, 700), fs * 1.32,
                    ncol, cgap, bw_col, per, len(items))
        fs, fb, fp, row_h, ncol, cgap, bw_col, per, n = best
        items = items[:n]
        self.log.append(("index", f"{ncol} cols, {fs}px, {n} items"))
        idx_bottom = by
        for c in range(ncol):
            cx = M + c * (bw_col + cgap)
            cy = by
            for k in range(per):
                idx = c * per + k
                if idx >= len(items):
                    break
                place, t = items[idx]
                tag = place + " "
                p.text(cx, cy, tag, fp, L.RED)
                p.text(cx + p.tw(tag, fp), cy, t, fb, (44, 40, 36))
                cy += row_h
            if c:
                p.vline(cx - cgap / 2 + 0.5, by - 2, cy - row_h * 0.45,
                        L.FAINT, 0.8)
            idx_bottom = max(idx_bottom, cy - row_h * 0.45)

        mx = M + idx_w + GUT + 4
        mh = min(BOT - foot_h - 10 - y, idx_bottom - y + 10)
        draw_map(p, mx, y, map_w, max(96, mh))
        y = max(idx_bottom, y + max(96, mh)) + 8
        self.mark("index", y)

        # ---------------- date check ----------------
        p.hline(M, y - 1, L.W - M, L.INK, 1.3)
        fy = y + 4
        p.text(M, fy, "DATE CHECK", F.caps(8.6, 700), L.RED, track=1.1)
        dy = p.para(M + 52, fy, N.NOT_TODAY, F.text(8.2, 400), COL - 52,
                    9.9, (92, 86, 78), maxlines=2)
        dy += 2.5
        p.text(M, dy, "SOURCES", F.caps(6.5, 700), (140, 133, 122), track=0.8)
        p.para(M + 46, dy - 0.5, N.SOURCES, F.caps(6.3, 500), COL - 46, 7.6,
               (140, 133, 122), maxlines=1)
        y = dy + 8
        self.mark("foot", y)

        img = p.save(path)
        if self.debug:
            for k, v in self.log:
                print(f"  {k:>9}: {v}")
            print(f"bottom of ink: {y:.1f} (limit {BOT})")
        return img


def build(path=OUT, debug=False):
    return Builder(debug=debug).run(path)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    target = args[0] if args else OUT
    img = build(target, debug="--debug" in sys.argv)
    print(f"wrote {target} {img.size} {os.path.getsize(target)} bytes")
