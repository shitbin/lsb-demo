# ADV-2026-002 — Review

- **ID:** ADV-2026-002
- **File:** 프리윌루전-무쏘.mp4
- **Brand:** KGM (KG Mobility, ex-SsangYong)
- **Product / Model:** Musso pickup truck (Musso)
- **Production:** Freewillusion; partly produced with generative AI (disclosed on-screen)
- **Duration:** 30.03s @ 29.97fps, 1920x1080 landscape (16:9), 900 frames, has audio (music-driven)
- **shot_count_corrected:** 10
- **capture_style:** mixed — photoreal 3D-CG vehicle renders composited over generative-AI environment plates (explicitly disclosed)
- **camera_signature:** cinematic forward push-in, macro whip into grille, aerial canyon flythrough, low tracking off-road chase, slow studio orbit, slow lineup dolly, static logo end card
- **Wiggle:** NONE (mean_abs_shift_x 0.68 = ordinary cinematic camera movement, not lenticular/stereoscopic) — signature_effect "none" on every shot

**One-line summary:** A cinematic CG / generative-AI hero film that reveals the KGM Musso pickup out of darkness in a white-rock canyon, soars through a warm stormy mountain flythrough, unleashes a golden-hour desert dust chase intercut with moody studio beauty macros and a tailgate-badge reveal, then resolves on a two-color "The Original MUSSO" lineup and the "KGM — Enjoy with Confidence" end card.

## Cuts (gapless, seconds)
`0:3.27,3.27:10.444,10.444:12.679,12.679:16.783,16.783:18.185,18.185:19.686,19.686:21.255,21.255:23.257,23.257:29.029,29.029:30.03`

## Per-cut table
| # | Time (s) | Frames | Content | Key on-screen text |
|---|----------|--------|---------|--------------------|
| 1 | 0:00–0:03.27 | f1–98 | Dark fade-in; truck front emerges, segmented LED grille bar + vertical headlights ignite out of black | — |
| 2 | 3.27–10.44 | f99–313 | Hero reveal: graphite truck parked in white rocky CG canyon, slow push-in, scene brightens | "MUSSO" (grille plate + hood emboss) |
| 3 | 10.44–12.68 | f314–380 | Macro light-streak whip into the lit grille → warm stormy aerial cliff/mountain flythrough | "*이 영상은 생성형 AI를 활용하여 일부 제작되었습니다" (bottom-left) |
| 4 | 12.68–16.78 | f381–503 | Brief aerial vista → low rear-tracking desert chase, white truck throwing huge dust plume | disclaimer (BL) + "\|파워풀한 디젤 & 가솔린\|" (BR) |
| 5 | 16.78–18.19 | f504–545 | Golden-hour side-profile drift / power-slide, dust + grit fan, glowing mountains | "\|파워풀한 디젤 & 가솔린\|" (bottom-right) |
| 6 | 18.19–19.69 | f546–590 | Dark-studio side-profile beauty shot, single warm overhead spotlight, red tail light | — |
| 7 | 19.69–21.26 | f591–637 | Dark-studio macro: lower body panel, black cladding, side step, machined alloy wheel | — |
| 8 | 21.26–23.26 | f638–697 | Tailgate close-up in white canyon: embossed "KGM" + "MUSSO" badges, red vertical tail light | "KGM" + "MUSSO" (embossed on vehicle) |
| 9 | 23.26–29.03 | f698–870 | Calm studio lineup: silver-grey + brown/bronze Musso side by side, blue-sky/mountain backdrop, slow dolly | "The Original" / "MUSSO" (centered title) |
| 10 | 29.03–30.03 | f871–900 | Black end card: brand logotype + tagline, static hold | "KGM" / "Enjoy with Confidence" |

## All on-screen text captured (verbatim)
- **Grille plate + hood emboss:** `MUSSO` (hero shots ~5s+, and on both lineup trucks)
- **Generative-AI disclaimer (bottom-left, flythrough ~11–13s):** `*이 영상은 생성형 AI를 활용하여 일부 제작되었습니다`
- **Feature caption (bottom-right, desert montage ~14–21s):** `|파워풀한 디젤 & 가솔린|` ("파워풀한" regular weight, "디젤 & 가솔린" bold, flanked by vertical bars)
- **Tailgate (cut 8):** embossed `KGM` (large) + `MUSSO` (corner badge and rear-bumper emboss)
- **Lineup title (cut 9, centered):** `The Original` / `MUSSO`
- **End card (cut 10):** `KGM` / `Enjoy with Confidence` ← brand tagline

## Notes
- Audio is music-dominant; faster_whisper (tiny) transcript is garbled/low-confidence (speech_coverage 0.665; fragments resembling "절대적 존재감" / "무쏘"). On-screen text is authoritative. bgm_likely set true.
- The 332–338 metrics spike cluster is a fast macro grille light-streak whip transition inside shot 3 (push-in into the lit grille bursting into the canyon flythrough), not a separate location — folded into shot 3.
- Brand/product/model names confined to source_ref + copywriting; t2i prompts describe the truck and badges abstractly and reproduce no trademarked logo geometry. No celebrity faces.
- Validator: **PASS (10 shots)**. Frames: 10 cut mids + contact_sheet.png in `ADV-2026-002_frames/`.
