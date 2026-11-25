# THE CAPITAL STANDARD — Tuesday 25 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
![rank](https://make.fun/badge/news-image-20261125/royalflush284/makefun-news-image-20261125/rank.svg)
![reward](https://make.fun/badge/news-image-20261125/royalflush284/makefun-news-image-20261125/reward.svg)

Bounty: https://make.fun/bounty/news-image-20261125

## What this entry is

A single 1024×1024 front page that carries the whole of Tuesday
25 November 2026 in 37 stories. The masthead is THE CAPITAL STANDARD,
set in ink blue and steel grey, with the day and date printed large
under it so the page can only belong to that one Tuesday.

Thirteen stories get full-scene cards. The lead trio follows the
assigned order: the Gaza drone strikes, the Strait of Hormuz tanker
claim — labelled throughout as a claim, "Iran says" — and NATO's
AWACS deployment to Poland. Ten more cards sit in the grid in pool
order: Iraq's oilfields order, the 700,000 war-dead analysis, new EU
sanctions, the first Lynx KF41 vehicles, Xiamen Airlines ordering
50 Boeing 737-8 jets, Madrid's 5–1 comeback against PSV, Nvidia's
Monday close, the PCE report due that day with no figure invented,
the 12 revived Acropora coral species, and the Colombia car bomb.
The remaining 24 stories run as numbered briefs, bringing the page
to 37 stories across 9 regions.

Around the cards the page keeps its working furniture: an eight
figure number strip tied to card numbers, a colour-coded strip for
all nine regions, a dotted map with 13 pins numbered to match the
cards, a six-slot timeline of the day, and a five-item date check
naming the older stories that are not news of this day.

## How it is made

`compose.py` paints every pixel procedurally with the Python
standard library only — layered flat scenes for each card (three
tankers and mine markers on the Hormuz, a full-bodied AWACS with
radar dome and ring, a lit Gaza skyline with a drone, a branching
coral with fish, a stadium bowl, a sealed document) — and writes
`entry.png` itself as a PNG. `main.py` is a standard-library
copy-only runner that delivers that exact file to `/output`.
Original drawings, drawn for this page.
