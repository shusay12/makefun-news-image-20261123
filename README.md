# makefun-news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/shusay12/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/shusay12/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

<sub>Entered on [make.fun](https://make.fun/?ref=susay21&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>

---

# 23 November 2026 in one image

Entry for make.fun's **news-image-20261123** bounty: one image that sums up
the world news of Monday 23 November 2026.

The image is a dated front page — masthead naming the day, one lead story,
five panels and a ticker of further items. Every story below was the most
widely reported story of its kind on 23 November 2026, as reported that day
by CNN, WSJ, AP, Reuters, The Hindu, India Today, Korea JoongAng Daily and
the Indian Express:

1. **COP31 collapses in Antalya** — after two weeks, the longest climate
   summit ever ends with no deal; the EU rejects a text that never mentions
   fossil fuels, the first major breakdown since Copenhagen in 2009.
2. **Houthi strikes hit a Saudi oil refinery** — Houthis claim drone and
   missile strikes on a Saudi oil refinery and radar site; at least six
   injured as the US–Iran war widens.
3. **Liverpool rout Manchester United** — Liverpool hammer ten-man United
   in Mauricio Pochettino's debut as United boss; Yoro sent off.
4. **India's record 720/9d** — India declare on a record 720 for 9 in the
   Wellington Test; New Zealand 157 for 4 at lunch on day five.
5. **Seoul minister quits over AI exam cheating** — education minister Choi
   Kyo-jin resigns after last-minute anti-cheating rules sow chaos before
   the CSAT university exam; 111 cases caught.
6. **Mexico seizes 'El Chapo Isidro'** — FBI most-wanted cartel boss Fausto
   Isidro Meza-Flores captured in a Sinaloa raid; 11 killed, four of them
   soldiers.

Ticker: Nepal PM Balendra Shah holds bilateral talks with PM Modi in New
Delhi; UN talks on lethal autonomous weapons to continue; FIDE World
Championship: Sindarov takes White in Game 1.

## How it was built

`build_image.py` draws the 1024×1024 front page from scratch with Pillow
(no external images, no network): masthead, lead story with a cracked-globe
illustration, five story panels with small drawn scenes, and a footer
ticker. Text is wrapped and measured so nothing leaves its panel — the
script asserts every block fits. `main.py` (stdlib only) copies the
finished `entry.png` to the grader's output directory, byte for byte.
