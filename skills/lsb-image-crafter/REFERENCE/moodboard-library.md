# Moodboard Library — the director's taste, loaded like a dataset

> A curated library of reference images (currently ~80, from the director's Pinterest) that defines the
> studio's visual taste. The planner and the treatment-builder load it the same way they load the ad
> dataset — to ground concept mood and image generation in a real, human-curated aesthetic instead of a
> generic default. This is the missing piece earlier builds skipped.

## Where it lives (path contract)
- `<LIBRARY>` = the connected folder that contains `001_ad_video_dataset/` (same root the ad dataset and
  copy bank resolve from; locally `LSB_AD_ENGINE/library`, on API the repo root). Resolve by structure, not name.
- Moodboard library = **`<LIBRARY>/004_moodboard_library/`** (`<MOODBOARD>`). Do not hardcode an absolute path;
  resolve `<LIBRARY>` at runtime (mac `/Users/...`, win `C:\Users\...`).
- If the folder is absent, skip moodboard grounding and say so in the output (do not invent a taste).

## Structure
```
<MOODBOARD>/
├── 00_inbox_컬링용/            (downloader drop zone — new pins land here for culling)
├── 01_타이포_CJK포스터/        typography-led CJK posters   (strongest taste axis)
├── 02_타이포_영문포스터/        typography-led English posters
├── 03_미니멀_에디토리얼/        minimal editorial
├── 04_포토_에디토리얼/          photo editorial
├── 05_필름그레인_인물무드/      film-grain portrait mood
├── 06_드리미_플레어_자연/        dreamy flare / nature
├── 07_일러스트_아니메/          illustration / anime
├── 08_제품_오브제/             product / object
├── 09_그래픽_추상콜라주/        graphic / abstract collage
├── _README_사용법.md
└── _분석/
    ├── manifest.json           {filename: {bucket, tags, ...}} — the index
    ├── index_map.json          bucket → [filenames]
    ├── 스타일DNA_0613.md        the taste analysis (read this for the "why")
    └── contact_sheet_*.png     visual overviews
```

## The director's taste DNA (from _분석/스타일DNA_0613.md)
Typography-led editorial posters (the dominant axis) + film grain + collage + a witty concept twist.
What makes these read as "not AI": bold expressive typography integrated into the image, real film
texture, intentional imperfection, and a clear conceptual idea rather than a pretty average.

## How to load it (code)
The index is plain JSON — read it directly, do not load all 80 images.
```python
import json, os
MB = os.path.join(LIBRARY, "004_moodboard_library")
manifest = json.load(open(os.path.join(MB, "_분석", "manifest.json"), encoding="utf-8"))
index = json.load(open(os.path.join(MB, "_분석", "index_map.json"), encoding="utf-8"))
# pick a bucket that matches the brief's tone, then take a handful of files for the mood_board page
bucket = "01_타이포_CJK포스터"               # e.g. for a typography-driven concept
picks = [os.path.join(MB, bucket, f) for f in index[bucket][:6]]
```

## Where it plugs into the pipeline
1. **Planner (concept stage):** when proposing concepts, choose the moodboard bucket(s) that fit the
   brief's tone and cite them as the visual reference — so concepts inherit the director's taste, not a
   generic look. (Mirrors how the planner cross-references the ad dataset and copy bank.)
2. **Treatment-builder `mood_board` page:** render 3–6 picks from the chosen bucket as the tone/reference
   board (with `contain` = original ratio, per the IMAGE RATIO LAW).
3. **Image generation (photographic-treatment):** use the chosen bucket's aesthetic to pick the matching
   photographic preset (e.g. film-grain bucket → P1/P2; faded editorial bucket → P3) so generated stills
   match the moodboard rather than a default.

## Adding more references
`레퍼런스_다운로드.command` (gallery-dl) appends new Pinterest pins to `00_inbox_컬링용/`. After a download,
re-cull and re-bucket, then rebuild `manifest.json` / `index_map.json`. Do not rename the existing
buckets — the downloader writes into them.
