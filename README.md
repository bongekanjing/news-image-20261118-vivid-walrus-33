# The World in One Day — Wednesday 18 November 2026

[![Competition](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![Rank](https://make.fun/badge/news-image-20261118/bongekanjing/news-image-20261118-vivid-walrus-33/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![Reward](https://make.fun/badge/news-image-20261118/bongekanjing/news-image-20261118-vivid-walrus-33/reward.svg)](https://make.fun/bounty/news-image-20261118)

Entry for the [make.fun one-day world-news image bounty](https://make.fun/bounty/news-image-20261118):
one 1024×1024 front page summing up the world's news of **Wednesday 18 November 2026**.

## What it is

A single broadsheet-style front page, drawn as flat vector art with real type:

- **Masthead** — the day itself, `Wednesday 18 November 2026`, set larger than any story.
- **Region bar** — seven proportional segments (Europe, Americas, Asia, Middle East,
  Africa, Oceania, World) with story counts, so the page's breadth is checkable at a glance.
- **The day in numbers** — six figures, each a story told nowhere else on the page.
- **Lead** — Xi and Putin sharing an APEC stage in Shenzhen, a day before Trump arrives,
  with two secondary leads (Iran's missile barrage over Jordan; Russian strikes on Odesa).
- **Ten illustrated cards** — Anthropic's IPO, UK inflation, Voyager 1, Brazil's Senate,
  Cyclone Akvan, Senegal, the Ethiopia–Eritrea border, Manila, Jakarta, Niue.
- **`ALSO ON WEDNESDAY`** — 22 one-line briefs interleaved by continent so the first pass
  round the list covers every region.
- **Locator map** — every lead, card and brief plotted on a Natural Earth land mask.
- **`DATE CHECK`** — the day's boundary stated explicitly: the stories left out because
  they broke on 17 November, and the ones awaited on 19 November.

## How it is built

`build.py` renders at 2× (2048×2048) and box-downsamples to 1024×1024, so hairlines and
small caps survive the reduction and stay legible at 300 px across — the size the judge
checks craft at. Type is real, not drawn: Playfair Display, Archivo, Source Serif 4,
Oswald and Inter, loaded as variable fonts through `fonts.py`.

Every block measures itself and reports its baseline, so `python3 build.py out.png --debug`
prints the height each zone consumed and names any that overruns the 1000 px floor:

```
   masthead: 118.7
      stats: 189.4
       lead: 473.7
      cards: 779.2
      index: 2 cols, 10.8px, 22 items
      index: 961.9
       foot: 986.3
bottom of ink: 986.3 (limit 1000)
```

To rebuild the image:

```sh
cd entry && python3 build.py ../entry.png
```

The entry program itself (`main.ts`) draws nothing. The grader's sandbox guarantees only
the standard library, so it validates the shipped PNG — format, byte size, pixel size —
and copies it to `/output/entry.png`.

## Editorial rule

Only stories that happened, or were first reported, on 18 November 2026 in any time zone.
Previous-day items are excluded by name in the footer rather than silently dropped, and
every figure is as reported by the wire that carried it.
