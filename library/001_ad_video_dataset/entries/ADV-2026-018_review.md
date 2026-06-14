# ADV-2026-018 — Review

- **Video file:** 토스 숨은 서비스 2.mp4
- **ID:** ADV-2026-018
- **Duration:** 42.63s
- **FPS:** 29.97
- **Aspect:** 9:16 (1080x1920)
- **Shot count (corrected):** 13  (scenedetect raw scenes: 10)
- **Brand / Product:** Toss — Toss ATM 현금 출금 (cardless cash-withdrawal hidden feature)
- **Campaign:** 토스 숨은 서비스 2 — ATM 현금 출금 (creator series: Curator T / 토스를 발견하다)
- **Category:** finance.fintech
- **Capture style:** mixed — warm shallow-DOF live-action interior shots (empty wallet, woman with cash + editorial header) and cooler handheld on-location live action at a convenience-store cardless ATM, intercut with flat-lay phone-on-vivid-GREEN screen-demo shots for the step-by-step UI walkthrough.
- **Camera signature:** handheld_micro on the interior live action; handheld_active on the convenience-store ATM live action; locked_off on the flat-lay UI demo and the end card. **Wiggle: NONE** (mean_abs_shift_x 0.45 / sign_flips 0.30 = ordinary handheld, NOT stereoscopic parallax; confirmed visually).
- **Dominant technique:** Voice-and-caption-synced in-app feature walkthrough paid off in the real world; hardcoded lower-third dark caption pills on the green UI-demo shots and the location shots, large centered white supers + a flat editorial "CONTENT" header bar on the live-action opening; closes on a pixel/CRT series end card.
- **One-line summary:** A relatable cash crisis (empty wallet — no card, no cash) is solved by a guided cardless ATM withdrawal — choose "ATM 현금 출금" in the app, find a nearby convenience-store ATM, set the amount, get a 6-digit approval number, and collect cash at the machine with just a birth date and that number — paid off on a real-world thumbs-up cash reveal and signed with the retro pixel/CRT "Curator T / 토스를 발견하다" series badge.

## Structure
- 8 confirmed scenedetect hard cuts (diff>40) at f62/111/193/708/775/893/1093/1194 → cross-checked visually.
- The f193–708 green span is ONE constant green background but contains genuinely distinct app screens; split by SCREEN-STATE into shots 4–8 (all-tab menu → ATM-finder map → ATM-select + amount entry → confirm sheet + PIN → issued approval number). scenedetect's f626/694 (mid-action map→amount→confirm/PIN) helped place the splits and were not treated as separate hard scenes.
- The convenience-store ATM block (f775–1193) was split by action/screen-state into shots 9–12 (approach → input → count/dispense/collect → cash reveal + thumbs-up). The f1093 cut is a handheld re-frame (whip) within the same payoff.
- **wow cut = shot 12** (real-world cash-in-hand thumbs-up reveal).

## Audio / caption reconciliation
- faster_whisper **tiny** model, reconciled against authoritative on-screen captions/UI:
  - "현금" mis-heard as "형금"; "ATM" as "AT&"; "출금" as "사킬"; "주변 ATM 찾기" as "주변 AT&복이"; "생년월일" as "생련을과"; "편하게" as "평하게" — all corrected from the crisp captions.
  - VO/menu wording is "ATM 현금 출금" / "ATM에서 출금하기" while the synced caption pill reads **"'ATM 현금찾기'를 선택해보세요"** and the map step caption reads **"주변 ATM 보기를 누르면"** — captions kept verbatim.
- speech_coverage 0.859; bgm_likely was null in audio.json, set true on judgement (light instrumental bed). ATM hardware text (NICEPARK / PULOON / CU pins) is a real-world artifact captured in the footage.

## Caption lines (verbatim, count = 20 across 13 shots)
Live-action supers: 카드도 안되고 / 현금도 없는 / 위기의 순간! — editorial bar: 지갑 없을 때 / 당장 현금 찾는 꿀팁.
Demo + location caption pills (synced to VO): 전체 탭에서 · 'ATM 현금찾기'를 선택해보세요 · 주변 ATM 보기를 누르면 · 가까운 ATM 위치를 확인할 수 있는데요 · 방문할 ATM을 선택하고 · 찾을 금액을 입력해주세요 · 찾기 버튼을 누르면 · 이렇게 승인번호가 발급되는데요 · 이제 ATM 기기에서 · 토스를 선택하고 · 생년월일과 승인번호를 입력하면 · 카드 없이도 이렇게 편하게 · 현금을 인출할 수 있습니다.
End card: **Curator T / 토스를 발견하다**.

## Cuts (one line each)
| # | Time (s) | Framing | What's on screen | Caption |
|---|----------|---------|------------------|---------|
| 1 | 0.00–2.04 | CU | Live-action hands open a brown wallet on a green table, pulling a slip; warm bokeh | "카드도 안되고" → "현금도 없는" |
| 2 | 2.04–3.67 | CU | Hands tilt the wallet up, spreading the empty bill compartment | "위기의" → "위기의 순간!" |
| 3 | 3.67–6.41 | MCU | Woman in grey hoodie at a warm desk holds up a cash fan; editorial CONTENT header bar | "지갑 없을 때 / 당장 현금 찾는 꿀팁" |
| 4 | 6.41–11.35 | MS | Green flat-lay: app "전체" all-tab menu; finger taps "ATM에서 출금하기" → amount landing | "전체 탭에서" → "'ATM 현금찾기'를 선택해보세요" |
| 5 | 11.35–17.02 | MS | Green flat-lay: "내 주변 ATM 찾기" map with purple CU pins + route; finger pans | "주변 ATM 보기를 누르면" / "가까운 ATM 위치를 확인할 수 있는데요" |
| 6 | 17.02–20.85 | MS | Green flat-lay: tap an ATM pin → "얼마를 찾을까요?" amount-entry keypad (1만원), blue 확인 | "방문할 ATM을 선택하고" / "찾을 금액을 입력해주세요" |
| 7 | 20.85–23.59 | MS | Green flat-lay: "이 계좌에서 찾을까요?" confirm sheet (토스뱅크 통장, 10,000원, 무료) → app PIN screen | "찾기 버튼을 누르면" |
| 8 | 23.59–25.83 | MS | Green flat-lay: "ATM 기기에 승인번호 여섯자리를 입력해주세요" (5분 0초 남음, number blurred) | "이렇게 승인번호가 발급되는데요" |
| 9 | 25.83–29.76 | MS | Live-action: woman (from behind) walks up to a blue convenience-store ATM, operates touchscreen | "이제 ATM 기기에서" → "토스를 선택하고" |
| 10 | 29.76–33.13 | MCU | Live-action: hoodie sleeve taps ATM screen "출금 승인 번호 / 승인번호(6자리) 입력" (NICEPARK/PULOON) | "생년월일과 승인번호를 입력하면" |
| 11 | 33.13–36.44 | MS | Live-action: ATM "현금을 세고 있습니다" → "현금 수취 / 인출액 30,000원 / 수수료 0원"; hand takes cash | "카드 없이도 이렇게 편하게" |
| 12 | 36.44–39.81 | MCU | Live-action: woman faces camera holding the cash fan + thumbs-up, warm smile beside the blue ATM | "현금을 인출할 수 있습니다" |
| 13 | 39.81–42.63 | TITLE_CARD | Pixel/CRT badge settles on textured off-white paper, blue "Curator T" + tagline | "Curator T / 토스를 발견하다" |

## Validator
- `validate_entry.py` → **PASS (13 shots)**, no warnings.
- All 13 t2i_start_frame prompts 504–700 words (≥500 required).
- Strict JSON confirmed; frames_dir + contact_sheet + 13 cut mids present.
