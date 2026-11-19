# Eighteen V2 — Wednesday 18 November 2026 in one picture

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/ifulchina-ops/news-image-20261118-v2/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/ifulchina-ops/news-image-20261118-v2/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-page newspaper front page summing up the world's news of
Wednesday 18 November 2026: **42 stories, 7 regions, 8 fields,
13 illustrated**.

## What the picture shows

- A masthead naming the day, with a count strip (42 stories · 7 regions ·
  8 fields · 13 illustrated), a region bar and a "by field" bar — every
  count matches the stories actually printed on the page.
- A "day in numbers" strip: 55 Bangladesh factories shut, ~300 arrests,
  Voyager 1 one light-day out, 49 years since launch, 5+ killed in
  Ukraine, 300,000 sign a petition.
- 13 illustrated, numbered lead stories: Kuwait and Bahrain intercepting
  Iranian drones; Xi greeting Trump as APEC opens in Shenzhen; COP31
  splitting over a fossil-fuel phase-out; the Board of Peace warning the
  Gaza truce may collapse; Bangladesh wage protests shutting 55
  factories; Voyager 1 one light-day from Earth; Salvadoran troops raiding
  a gang boss's home in Haiti; Russian strikes killing at least 5 in
  Ukraine; Ethiopia and Eritrea massing troops; GTA VI going on sale at
  midnight; Bailey warning a long Iran war could mean more rate rises;
  Australia sanctioning settler leader Daniella Weiss; Cyclone Akvan
  nearing India's east coast.
- A world map ("Where it happened") with numbered pins for the 13 lead
  stories and coloured dots for the briefs.
- 29 more numbered one-line briefs (14–42) in three columns, from US
  politics and tech outages to the EU's €45bn Ukraine loan, the ICJ's
  Rohingya ruling and a Pew projection for 2035.
- A DATE CHECK footer naming what was deliberately left out because it
  was first reported on 17 November, not today (Peltola's Alaska Senate
  win, Nvidia's $115.8bn quarter, the Prague train crash, Mongolia's
  president resigning). Every story on the page happened or was first
  reported on Wednesday, 18 November 2026; contested claims are
  attributed. Sources: Reuters, AP, AFP, Al Jazeera, Bloomberg.

## Story counts (they add up)

The bars on the image are computed from the same story list that is
printed, and `build_art.py` asserts the totals before drawing:

| Region | Stories | Field | Stories |
|---|---:|---|---:|
| Europe | 10 | War & security | 11 |
| Middle East | 5 | Politics & diplomacy | 10 |
| Asia | 9 | Economy & labour | 7 |
| Africa | 2 | Society & culture | 4 |
| Americas | 11 | Disasters & weather | 3 |
| Oceania | 1 | Tech | 3 |
| World | 4 | Climate & space | 2 |
| | | Justice | 2 |
| **Total** | **42** | **Total** | **42** |

13 of the 42 are illustrated lead stories (numbered 1–13); the other 29
are numbered briefs (14–42) in three columns.

All artwork is original flat vector-style drawing made with Pillow; no
photographs or copied images are used.

## How to run it

Regenerate the image:

```sh
python3 build_art.py   # writes entry.png (1024x1024 PNG, under 1 MiB)
```

Run the entrypoint the way make.fun does:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png, byte-identical to entry.png
```

`main.py` only copies the shipped `entry.png` into the output
directory, so the graded run needs no network and is fully
deterministic. `build_art.py` needs only Python 3 and Pillow.

## License

MIT — see [LICENSE](LICENSE).

<sub>Entered on [make.fun](https://make.fun/?ref=noble-beacon-95&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
