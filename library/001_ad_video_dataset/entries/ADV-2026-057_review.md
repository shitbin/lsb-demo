# ADV-2026-006 — Review

## Source
ANTA (安踏) running sportswear — **athlete profile of young female sprinter 陈妤颉** (ANTA running ambassador, Asian women's 100m youth record holder). Vertical short-form cinematic sport film. Reference copy carries a **TVCBOOK.com watermark top-right on every frame** (not part of the ad, noted once).

## Top meta
- **Duration** 34.007s · **fps** 25 · **720×1280** · **aspect 9:16** · 849 frames · has_audio true
- **Shots** 16 · **pacing** accelerating (build to a 23–28s rapid-cut climax montage)
- **category_primary** apparel.sportswear · **year** 2024 (inferred)
- **Mood** cinematic / aspirational / determined / athletic
- **Look** warm golden-hour cinematic grade + lens flare + film grain; **lime-yellow (#c8e639/#d9e84a) kinetic Chinese type**, frequently SPLIT left/right over the running subject; intentional desaturated high-grain blur beats in the climax
- **Camera** dynamic handheld + tracking + whip-pans (metrics mean_abs_shift_x 1.72 / sign_flips 0.18 = handheld + fast motion, NOT wiggle_3d; camera_effect_local = none)
- **Audio** music-driven, minimal VO; ko-forced faster_whisper unreliable — returned "시작!" which is the Chinese shout cue **开始** at 28.6–30.6s (matches the on-screen tagline 开始)
- **Copyright-safe**: athlete rendered as a generic young East Asian sprinter (no specific real face); ANTA logo rendered generically (white arc/swoosh, no exact trademark); all on-screen Chinese copy preserved verbatim as caption text

## 16 cuts (one-liners)
1. **0–7.52** — Slow tilt-up reveal: empty blue sky to her serene golden-hour upturned profile, eyes closed; lime vertical credits 陈妤颉 / 安踏跑步代言人 / 亚洲女子一百米青年纪录 fade in.
2. **7.52–8.16** — Brief near-monochrome macro of her closed eye, a held contemplative breath.
3. **8.16–12.04** — Low full shot at the starting blocks, "set" crouch on red track in an empty stadium; lime race timer **0.00"**.
4. **12.04–15.52** — Tight spike-on-block detail to **explosive block start**, body pitched forward into the drive phase; dynamic low tracking.
5. **15.52–18.6** — Full-speed side-tracking sprint, hair streaming, heavy backlit sun flare; timer ticks **0.23"→0.25"**.
6. **18.6–20.84** — Determined profile face close-up mid-run, pink-magenta lens flare across her cheek; timer **0.31"**.
7. **20.84–23.36** — Extreme macro of the lime jersey: printed **ANTA RUNNING** + reflective **RUN** graphic; timer climbs to **1.00"** (lands the one-second idea on the product).
8. **23.36–24.0** — B/W motion-blurred high-angle whip of runners; split lime text **你以为 / 这只是一秒？** snaps in.
9. **24.0–25.28** — Color slams back: low side-tracking drive sprint, **你以为 / 这只是一秒？** holds split.
10. **25.28–26.04** — Clean top-down overhead of three sprinters down the lanes with long golden shadows (graphic breath).
11. **26.04–26.64** — B/W motion-blurred jolt of two sprinters streaking past (no text).
12. **26.64–27.4** — B/W blurred running legs vs city skyline; split lime text **年轻 / 力量** (youthful power).
13. **27.4–28.08** — Final B/W whip-blur of 2–3 sprinters, ponytail flaring (no text).
14. **28.08–29.24** — Color **victory**: arms thrown up at the finish; split lime tagline **从这一秒 / 开始** lands on her shout.
15. **29.24–32.32** — Calm hero standing against sky + city skyline; lime claim **安踏速干之王** / sub-line **一秒瞬吸汗　速干不粘身**; small white ANTA arc mark above.
16. **32.32–34.007** — End card: white **ANTA arc/swoosh mark on pure black**, holds to the end.

## Tagline + key Chinese copy (verbatim)
- **Tagline:** 从这一秒开始 (shown split 从这一秒 … 开始 = "from this very second … begin")
- Credits: 陈妤颉 · 安踏跑步代言人 · 亚洲女子一百米青年纪录
- Climax kinetic: 你以为 · 这只是一秒？ · 年轻 · 力量
- Product claim: 安踏速干之王 · 一秒瞬吸汗　速干不粘身
- Shout cue: 开始 (whisper ko-forced "시작!")
- Race timer overlay: 0.00" → 0.23" → 0.25" → 0.31" → 0.35" → 1.00"
- Jersey print: ANTA RUNNING

## Validation
`validate_entry.py` → **PASS (16 shots)**, no warnings. All 16 t2i_start_frame prompts ≥500 words; all required top/per-shot keys present; search_keywords all-English tokens; frames_dir / contact_sheet / 16 mid-frames exist next to the entry.
