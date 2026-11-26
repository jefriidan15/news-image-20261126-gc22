[![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/jefriidan15/news-image-20261126-gc22/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/jefriidan15/news-image-20261126-gc22/reward.svg)](https://make.fun/bounty/news-image-20261126)

# The World in One Image — 26 November 2026

A program that draws one newspaper front page summing up Thursday
26 November 2026's world news, for the
[news-image-20261126](https://make.fun/bounty/news-image-20261126) bounty.

## The day in one image

- **Lead:** Houthis hit Saudi Arabia's Ras Tanura refinery and Riyadh;
  Brent crude tops $94.
- **US proposes new tariffs on 14 trading partners**, China hit hardest
  as markets fall.
- **Ukraine strikes a Russian air base**, five planes damaged.
- **Kim orders more tactical nukes** as Pyongyang widens deployment.
- **Birthright-citizenship order blocked again** by a second judge.
- **Pakistan's first astronaut flies** to China's Tiangong station.
- **Duran Duran guitarist Andy Taylor dies at 65.**
- Also today: Lebanon plans a second airport, Sudan drone strikes kill
  19, a Gaza strike kills a Hamas official, and Bangladesh raises
  garment pay 36%.

## How it works

`main.py` is pure Python standard library (`zlib` + `struct` only). It
paints the front page on a 1024x1024 canvas with a hand-written 5x7
bitmap font and writes a PNG with no timestamps, so two runs produce
byte-identical output.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes `out/entry.png` (1024x1024, under 1 MiB) and prints its
size and sha256 after a read-back check.

## License

MIT — see [LICENSE](LICENSE).
