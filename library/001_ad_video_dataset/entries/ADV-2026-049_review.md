# ADV-2026-049 Review

**FILE:** 빙그레 2.mp4  
**BRAND:** 빙그레 (Binggrae) / 빙그레 왕실커피 스페셜티 — a Café la 스페셜티 (Royal Coffee Specialty)  
**DURATION:** 19.087s  
**SHOT COUNT:** 15 (detector gave 14; corrected +1)  
**FPS:** 23.976  
**ASPECT:** 16:9 (image letterboxed to ~2.39:1 cinemascope throughout)  

## Summary

A mixed-media **mock blockbuster film-trailer parody** for Binggrae's specialty RTD coffee, built on the brand's animated "royal kingdom" mascot universe. A generic red-haired prince mascot breaks the fourth wall, then a full fake-trailer arc plays out — premise card, hero entrance, ensemble cast, comedic struggle, breakthrough, triumph — before the product is "premiered." Deliberately switches between **flat 2D cel-shaded** visual-novel close-ups, **volumetric 3D-CG** cinematics, **gold-on-black ember title cards**, and **live-action** cast/product cutaways. Persistent white top-left channel-bug logo ("aCaféla 스페셜티") and cinemascope letterbox sell the film-credibility. Closes on the punning archaic royal command **"대개봉하시오"** ("let it be grandly premiered").

## Judgment Calls

- **Cut count 14 → 15 (shot_count_corrected: true).** Scenedetect merged two distinct full-frame title beats into its scene 3. A hard cut at **frame 106 (4.42s)** — diff 111, hist_corr 0.71, then dead-still after — separates the live-action cityscape "Presented by Binggrae" card from the gold ember card "잊혀진 왕실 커피를 되살리기 위해". Split into cut03 (3.96–4.42) and cut04 (4.42–5.67).
- **~11.68s spike inside cut09 = intra-cut gag, NOT a cut.** The sustained moderate diffs at 11.7–12.1s (high hist_corr ~1.0) are the prince's repeated lunging/reaching across the jar counter — the "다시! 다시!" (again! again!) retake joke. Kept as one shot.
- **Cut01/Cut02 kept as two cuts.** diff 62 / shift_x -14 at frame 50 is a hard reframe to a tighter, more level framing with a new dialogue line, not a continuous push.
- **CG vs live-action: it is mixed-media CG/animated for the hero.** Confirmed on native frames: 2D cel-shaded (cuts 1,2,11), 3D-CG (cuts 5,6,9,10,12,14); live-action only for the cast triptych (cut 8), aerial city plate (cut 3), product shots (cut 13), in-hand bottle (cut 15). Characters described generically (stylized animated prince / generic specialists).
- **Global wiggle negligible** (mean_abs_shift_x 0.482) — apparent motion is deliberate CG camera moves (push-ins, overhead rise), not handheld.

## Audio corrections (whisper text_raw → corrected via on-screen subtitles)

- "빙그레 웃길 바라" → **"끝까지 보고 빙그레 웃길 바라오!"** (caption)
- "재원하겠어" → **"재현하겠어"** ("recreate", caption)
- "꿈건가?" → **"왕실 커피는 꿈인 건가..."** (caption)
- "죽었어!" → **"좋았어!"** ("alright!", caption)
- product line "빙그레 웃의 왕실 커피" → lockup **"빙그레우스의 왕실커피"**

## Cut-by-Cut Summary

| Cut | Time | Description |
|-----|------|-------------|
| 01 | 0.00–2.09s | 2D cel prince under coffee-bean parasol, smug look up, "내 데뷔작인데 그냥 지나칠 텐가?" |
| 02 | 2.09–3.96s | 2D cel prince, tighter/level, confident, "끝까지 보고 빙그레 웃길 바라오!" |
| 03 | 3.96–4.42s | Live-action aerial city skyline; white trailer title "Presented by Binggrae" |
| 04 | 4.42–5.67s | Gold ember title card: "잊혀진 왕실 커피를 되살리기 위해" |
| 05 | 5.67–7.63s | 3D-CG hero entrance: prince in red royal regalia, backlit doorway, "왕실 커피의 그 맛과 향!" |
| 06 | 7.63–9.34s | 3D-CG prince MCU, determined vow, "내가 반드시 재현하겠어!" |
| 07 | 9.34–10.01s | Gold ember title card: "빙그레우스와 스페셜리스트들이 뭉쳤다!" |
| 08 | 10.01–11.18s | Live-action 3-panel cast triptych: 프레스토/완다/로스티노 + role labels (split-screen) |
| 09 | 11.18–12.18s | 3D-CG prince in white barista uniform lunging across jar counter, retake gag, "다시!" |
| 10 | 12.18–14.56s | 3D-CG prince at coffee-lab bench, clasped hands, eyes closed, "왕실 커피는 꿈인 건가..." |
| 11 | 14.56–15.31s | 2D cel ECU of prince's eye snapping open, breakthrough, "바로 이거야!" |
| 12 | 15.31–16.31s | 3D-CG prince raises metal cup, crowd cheers, "좋았어!" |
| 13 | 16.31–17.14s | Product hero shot: 6 packages (3 bottles + 3 cups), logo "스페셜티 / 빙그레우스의 왕실커피" |
| 14 | 17.14–18.02s | 3D-CG overhead birdseye celebration ring, beans on floor, red title burst "아카페라 스페셜티" |
| 15 | 18.02–19.09s | Live-action hands twisting open dark glass "스페셜티 COFFEE" bottle, CTA "대개봉하시오" |

## Verification

39/456 native-res frames read across all 15 finalized cuts (every detector boundary f(n-1)/f(n), the discovered 4.42s cut, the 11.68s intra-cut gag and 4.42s spike, plus starts/mids/ends and lower-third caption reads) + 100% per-frame metrics.json + scenedetect CSV + 3 generated mid-frames spot-checked. Validator: **PASS (15 shots)**.
