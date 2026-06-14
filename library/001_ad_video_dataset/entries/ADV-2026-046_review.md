# ADV-2026-046 Review

**FILE:** 배민 1.mp4  
**BRAND:** 배달의민족 / 배민 (Baemin) — 배민오더 (Baemin Order, 미리 주문 픽업 / pre-order pickup)  
**DURATION:** 31.14s  
**SHOT COUNT:** 16  
**FPS:** 23.976  
**ASPECT:** 16:9  

## Cut-by-Cut Summary

| Cut | Time | Description |
|-----|------|-------------|
| 01 | 0.00–1.79s | Exterior night WS, long line of people waiting outside a restaurant ("Mark's" neon); cool-warm split, fades in from black. Pain setup. |
| 02 | 1.79–4.09s | MCU of a bored young man in a green track jacket waiting, earphones in, others on phones around him. Warm interior, green colour-pop. |
| 03 | 4.09–5.67s | MS of two waiting companions slumped together, eyes closed, exhausted. Dim, monochromatic warm-brown fatigue beat. |
| 04 | 5.67–7.47s | MCU of a sullen, tired young person in a bright orange hoodie waiting. Warm amber, orange colour-pop. |
| 05 | 7.47–8.72s | MWS from behind the crowd facing a glowing doorway; silver-haired woman (back to camera) centred, about to enter. Backlit silhouette, turn setup. |
| 06 | 8.72–10.59s | WS hero entrance — silver-haired woman strides out of the glowing doorway down a corridor; volumetric warm haze, crowd parts. |
| 07 | 10.59–12.30s | MCU hero approaching in a glamorous gold metallic jacket + statement necklace, proud smile. Rich golden grade. |
| 08 | 12.30–13.39s | Product insert — kraft 배민오더 takeout bag handed across a counter; ends on a gentle rack focus. Warm/appetising. |
| 09 | 13.39–14.47s | MCU reaction — the green-jacket man, mouth agape in astonishment (reverses his earlier boredom). |
| 10 | 14.47–15.56s | MS reaction — a couple look up in awe, phones forgotten in hand. Small teal hair-streak accent. |
| 11 | 15.56–16.68s | MCU reaction — the orange-hoodie person, mouth open in a gasp (clear boredom→awe reversal). |
| 12 | 16.68–20.44s | WOW climax — symmetrical golden-haze "runway" wide; hero walks the aisle between two rows of seated onlookers holding takeout bags. VO: "고생 끝에 낙이 오는 시대는 끝났다". |
| 13 | 20.44–22.61s | CU hero payoff — warm confident closed-mouth smile, over-ear headphones around neck. Golden grade. |
| 14 | 22.61–27.40s | Product demo — hand holds phone running the app (map → "우아한 치킨" → order/cart) at left; kinetic Korean copy builds at right: "미리 주문하면 / 바로 받아가는 / 손 안의 오더". |
| 15 | 27.40–29.28s | Tagline beat — hero on a night street holds up phone (mint app splash), knowing smile; kinetic copy stacks at left: "요즘은 / 이렇게 / 삽니다". |
| 16 | 29.28–31.14s | End card — white field, brand wordmark "배달의민족" animates (fade-and-scale swap) to product lockup "배민오더" with a teal circular order icon; cuts to black. |

## Narrative / Concept
Linear-continuous comedic narrative. Cuts 1–5 dramatize the misery of waiting in line (the "old way" — VO frames it as "고생 끝에 낙" suffering-then-reward). Cuts 6–7 reveal a confident pre-order hero who breezes past the line; cut 8 reveals the 배민오더 takeout bag; cuts 9–11 are a reaction-gasp montage of the formerly bored waiters; cut 12 is the spectacle climax (a literal fashion-runway metaphor for picking up a pre-ordered meal); cuts 13–15 land the feature via hero CU + phone-UI demo + kinetic-typography tagline; cut 16 is the minimal logo card. The joke: an ordinary food pickup played completely straight as a glamorous catwalk — "요즘은 이렇게 삽니다" / "these days, this is how we live."

## Judgment Calls
- **Cuts:** scenedetect's 16-cut segmentation confirmed exactly; **no merges or splits** (shot_count_corrected = false). All 15 boundaries verified on f(n-1)/f(n) native frames. The two long cuts (12 = 3.75s, 14 = 4.80s) were sampled internally and are each single continuous shots (cut 14's phone screen changes UI states and the side copy builds line-by-line, but the hand-held shot itself is continuous; cut 16's end card is one shot with an animated logotype→lockup swap).
- **Audio corrections** (raw whisper kept in `text_raw`): "네 차례 언제워" → "내 차례 언제야"; "백팔방고객님" → a customer name being called, normalized to "○○○ 고객님!"; "고생 끝에 날이 오는" → "고생 끝에 낙이 오는"; "미리 주문은 왔지" → "미리 주문은 옳지"; "손 안에 오더" → on-screen caption "손 안의 오더"; "베밍 오더" → "배민오더".
- **On-screen copy** preserved verbatim (captions/app text/end-card). People, logos and the app mascot described/rendered generically per copyright-safe abstraction; brand/product names confined to source_ref/copywriting.
- **Wiggle:** mean_abs_shift_x 1.83 / sign_flips 0.117 — consistent with intentional handheld + CG volumetric-haze drift on the runway beats (verified visually, not a hard cut artifact).
