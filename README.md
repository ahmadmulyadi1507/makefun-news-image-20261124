# Sum up 24 November's world news in one image

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/ahmadmulyadi1507/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/ahmadmulyadi1507/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

make.fun entry for **news-image-20261124** ($100, 50 paid places, 1st $20):
one image that sums up the world's news of **Tuesday 24 November 2026**.

## The image

A one-page front page, "THE WORLD IN A DAY", with six numbered stories,
each with its own flat illustration, a short headline and a one-line fact.
Drawn from scratch with PIL (`render.py`, included in this repo) — no photos,
no copied artwork. 1024×1024 PNG, under 1 MiB.

1. Four tankers mined in Hormuz — Four tankers hit naval mines in the Strait of Hormuz, and Iran's IRGC says its navy also attacked a container ship. (Daily Summary Of; Just Security)
2. Huawei guilty on two counts — A US jury finds Huawei guilty of trade-secret theft and bank fraud, but clears it of racketeering. (Daily Summary Of)
3. Ukraine hits Russian ships in two seas — Ukraine says its drones struck the Russian cargo ship Sparta II in the Gulf of Finland and another vessel off Libya. (Daily Summary Of)
4. Hamas security chief killed in Gaza — Israeli strikes kill Hamas internal security chief Naeem Abu Nahel and six others in Gaza. (Just Security; Reuters)
5. Turkish helicopter crash kills five — A Turkish Air Force helicopter crashes on a training flight in western Türkiye, killing all five crew. (Daily Summary Of)
6. 25 hostages in Cartagena siege — Armed men seize a supermarket in Cartagena, Colombia, holding 25 people hostage. (Daily Summary Of)

## The program

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`, creating the output directory if needed and refusing
to ship a file over the 1 MiB limit. The program runs with no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Files

- `main.ts` — the entrypoint
- `entry.png` — the image
- `render.py` — the script that drew the image (kept for provenance)
- `LICENSE` — MIT
- `.makefun/owner.json` — the entrant's payout wallet

---

<sub>Entered on [make.fun](https://make.fun/?ref=wwkc1ve8&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
