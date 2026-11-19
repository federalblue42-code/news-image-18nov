# news-image-18nov

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/federalblue42-code/news-image-18nov/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard)
[![reward](https://make.fun/badge/news-image-20261118/federalblue42-code/news-image-18nov/reward.svg)](https://make.fun/bounty/news-image-20261118/leaderboard)

One image summing up the world's news of **Wednesday 18 November 2026**, built for the
[make.fun](https://make.fun) bounty `news-image-20261118`.

## What it is

A newspaper-style front page: 36 stories across 7 regions, 12 original flat-vector
illustrations, a giant date masthead, region tally, six headline statistics, a UTC
timeline, a pinned world map, 24 briefs, and a red **DATE CHECK** box listing the
next-day stories deliberately left off (the ICJ Rohingya judgment, GTA VI's release
day, Anthropic's first trades, the trilateral itself — all Thursday 19 November).

Leads: Xi's rare airport welcome for Trump as APEC opens in Shenzhen, the European
Commission's €45bn loan proposal for Ukraine, and the Gulf's night of Iranian drone
intercepts — plus Jeffries' 251-11 speaker nomination, the $190.4m Van Gogh record,
Voyager 1 crossing one light-day (and falling silent), Cyclone Akvan's evacuations,
Suneung eve, COP31's deadlock, the Yellow Line raid, Broward's flood emergency and
the Ethiopia-Eritrea border buildup. Every story happened, or was first reported,
on 18 November 2026; disputed claims are attributed.

## How it runs

The entrypoint `main.py` copies the committed `entry.png` (1024×1024, under 1 MiB)
to `/output/entry.png`. No network, no clock — both grader runs write identical bytes.

`generate.py` rebuilds `news_front.svg` deterministically (pure string building);
render it with `rsvg-convert -w 1024 -h 1024 news_front.svg -o entry.png`.

## Sources

Xinhua, NYT, Reuters, AP, European Commission, Euronews, NASA, Pew Research,
Korea Herald, IMD, NWS, Gulf News, Roll Call, Africa Center, allAfrica.
Original drawings; no photographs.