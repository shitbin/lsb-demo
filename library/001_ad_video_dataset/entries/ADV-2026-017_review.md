# ADV-2026-017 — Review

- **Video file:** 토스 숨은 서비스 1.mp4
- **ID:** ADV-2026-017
- **Duration:** 35.81s
- **FPS:** 29.97
- **Aspect:** 9:16 (1080x1920)
- **Shot count (corrected):** 9  (scenedetect raw scenes: 7)
- **Brand / Product:** Toss — Toss 신용점수 올리기 (credit-score boosting hidden feature)
- **Campaign:** 토스 숨은 서비스 1 — 신용점수 올리기 (creator series: Curator T / 토스를 발견하다)
- **Category:** finance.fintech
- **Capture style:** mixed — warm shallow-DOF live-action interior shots (hand/woman with the app on an iPhone) intercut with flat-lay phone-on-vivid-orange screen-demo shots for the step-by-step UI walkthrough.
- **Camera signature:** handheld_micro on the live-action interior shots; locked_off on the flat-lay UI demo and the end card. **Wiggle: NONE** (mean_abs_shift_x 0.16; confirmed visually — no stereoscopic parallax).
- **Dominant technique:** Voice-and-caption-synced in-app feature walkthrough; hardcoded lower-third dark caption pills on the orange UI-demo shots, large centered white supers + a flat editorial "CONTENT" header bar on the live-action opening; closes on a pixel/CRT series end card.
- **One-line summary:** A relatable money pain point (credit score one point short for a loan) is resolved by a guided one-tap in-app feature that auto-submits score-raising documents and reveals an improved score (KCB 945, +54점 / NICE 950), signed off with the retro pixel/CRT "Curator T / 토스를 발견하다" series badge.

## Structure
- 6 confirmed scenedetect hard cuts (diff>50) at f48/102/199/321/500/989 → cross-checked visually.
- The f200–989 orange span is ONE constant orange background but contains genuinely distinct app screens, split by screen-state into shots 4–8 (search → explainer → document-finding → success/confetti → score-reveal). Hard cuts at f321 and f500 fall mid-screen (caption/scroll changes) and were NOT treated as shot boundaries.
- **wow cut = shot 8** (KCB 945 +54점 / NICE 950 numeric reveal).

## Audio / caption reconciliation
- faster_whisper **tiny** model, reconciled against authoritative on-screen captions:
  - "버튼 한 번" mis-heard as "파티 한 번" (separate on-screen editorial bar reads "터치 한 번으로").
  - "올랐어요" mis-heard as "올렸어요".
  - Final CTA mis-heard as "대출 좋아요 때" → corrected to on-screen caption **"대출 조회할 때 잊지 말고 꼭 체크해보세요"**.
- speech_coverage 0.881; BGM judged likely (light instrumental bed). Names on screen (김창선님 / 김토오스님) are in-app demo placeholders.

## Caption lines (verbatim, count = 18 across 9 shots)
Live-action supers: 대출 앞에서 / 1점이 아쉬운 / 내 신용점수 — editorial bar: 터치 한 번으로 / 신용점수 올리는 치트키.
Demo caption pills (synced to VO): 전체 탭에서 · '신용점수 올리기'를 선택해주세요 · 자동으로 제출하고 · 그 결과를 확인할 수 있는데요 · 버튼을 눌러 '올리기'를 선택하면 · 신용점수를 높일 수 있는 · 문서를 찾아 · 제출을 진행하게 됩니다 · 와! · 신용점수가 올랐어요! · 대출 조회할 때 잊지 말고 · 꼭 체크해보세요!
End card: **Curator T / 토스를 발견하다**.

## Cuts (one line each)
| # | Time (s) | Framing | What's on screen | Caption |
|---|----------|---------|------------------|---------|
| 1 | 0.00–1.60 | CU | Live-action hand holds iPhone; credit-score gauge counts up (55→60) in warm interior | "대출 앞에서" → "1점이 아쉬운" |
| 2 | 1.60–3.40 | MCU | Young woman in blue shirt at a warm desk, chin on hand, studying her phone | "1점이 아쉬운" → "내 신용점수" |
| 3 | 3.40–6.64 | MCU | Same woman looks to camera, explains, smiles; flat editorial CONTENT header bar | "터치 한 번으로 / 신용점수 올리는 치트키" |
| 4 | 6.64–9.01 | MS | Orange flat-lay: in-app search "신용" → autocomplete list; finger taps "신용점수 올리기" | "전체 탭에서" |
| 5 | 9.01–17.25 | MS | Orange flat-lay: "올리기" explainer (rocket, 3,156,445명, benefits, 3-step, blue button) | "'신용점수 올리기'를 선택해주세요" / "자동으로 제출하고" / "그 결과를 확인할 수 있는데요" |
| 6 | 17.25–24.36 | MS | Orange flat-lay: "제출할 수 있는 문서를 찾고 있어요" doc list; green check on 국민연금 | "버튼을 눌러 '올리기'를 선택하면" / "신용점수를 높일 수 있는" / "문서를 찾아" / "제출을 진행하게 됩니다" |
| 7 | 24.36–27.03 | MS | Orange flat-lay: loading → confetti "축하해요!" + blue up-arrow; "점수가 올랐어요" begins | "제출을 진행하게 됩니다" → "와!" → "신용점수가 올랐어요!" |
| 8 | 27.03–33.00 | MS | Orange flat-lay: score-reveal card — KCB 945점 (54점 상승) / NICE 950점 (변동없음), 확인 button | "신용점수가 올랐어요!" / "대출 조회할 때 잊지 말고" / "꼭 체크해보세요!" |
| 9 | 33.00–35.81 | TITLE_CARD | Pixel/CRT badge peels onto textured off-white paper, settles centered | "Curator T / 토스를 발견하다" |

## Validator
- `validate_entry.py` → **PASS (9 shots)**, no warnings.
- All 9 t2i_start_frame prompts 501–611 words (≥500 required).
- Strict JSON confirmed; frames_dir + contact_sheet + 9 cut mids present.
