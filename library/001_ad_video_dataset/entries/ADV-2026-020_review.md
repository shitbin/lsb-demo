# ADV-2026-020 — Review

- **Video file:** 토스 숨은 서비스 4.mp4
- **ID:** ADV-2026-020
- **Duration:** 44.98s
- **FPS:** 29.97
- **Aspect:** 9:16 (1080x1920)
- **Shot count (corrected):** 17  (scenedetect raw scenes: 10 hard cuts → 11 scenes; the long f341–970 setup scene split by screen-state into 7 sub-shots)
- **Brand / Product:** Toss — Toss 자동이체 (recurring transfer; setting up a monthly rent / 월세 auto-transfer)
- **Campaign:** 토스 숨은 서비스 4 — 월세 자동이체 (creator series: Curator T / 토스를 발견하다)
- **Category:** finance.fintech
- **Capture style:** mixed — warm shallow-DOF live-action interior shots (a hand holding an iPhone showing an iMessage rent-reminder thread, then a young woman in a warm study who introduces, demonstrates and closes the spot) intercut with flat-lay phone-on-vivid-ORANGE screen-demo shots for the multi-step setup walkthrough; the payoff is a push-in close-up of the flat-lay completed-transfer screen.
- **Camera signature:** handheld_micro on the live-action beats (hand + woman); locked_off on the flat-lay UI demo (with a tight push-in for the payoff shot 14) and the end card. **Wiggle: NONE** (mean_abs_shift_x 0.4043 / sign_flips 0.28 = ordinary handheld micro on live action + locked-off flat-lay, NOT stereoscopic parallax; confirmed visually).
- **Dominant technique:** Voice-and-caption-synced in-app feature walkthrough; hardcoded lower-third dark caption pills on the orange UI-demo shots, large centered white supers over the iMessage opening + a flat editorial "CONTENT" header bar over the woman; closes on the pixel/CRT series end card.
- **One-line summary:** A renter who keeps forgetting rent (and gets nagged by the landlord over text) automates it — search "자동이체" in the all-tab and run it, build a "월세 자동이체" by picking the withdrawal account → setting the transfer date & repeat schedule (매월 10일) → the monthly amount (500,000원) → the recipient account → a name (자취방 월세) → final confirm, landing on the completed auto-transfer ("월세 자동이체가 완성됐어요", toggle ON) that now runs automatically every month, fee-free — signed with the retro pixel/CRT "Curator T / 토스를 발견하다" series badge.

## Structure
- 10 confirmed scenedetect hard cuts (diff>40) at f20/84/131/175/279/340/970/1101/1187/1277 → cross-checked visually.
- The f341–970 orange span is ONE constant orange background but contains the whole multi-step setup; split by SCREEN-STATE into shots 7–13: landing + tap 자동이체 추가하기 → withdrawal-account picker (출금 계좌를 선택해주세요) → date/repeat schedule (언제 보낼까요 / 매월 10일) → amount entry (얼마를 보낼까요 / 500,000원 / keypad) → recipient account (어떤 계좌로 보낼까요 / 은행 선택) → name the transfer (자동이체 제목 / 자취방 월세) → final confirmation review (이다연님에게 매월 10일 500,000원씩… + 추가 설정 + 추가하기).
- The f970 hard cut is the push-in from the wide flat-lay to the tight close-up of the completed-transfer list = shot 14 (the wow/payoff).
- Caption-only swaps within one continuous screen were kept as typo_motion (shot 5 search→landing; shot 9 "세팅해주세요"; shot 10 "설정하고"; shot 12 "적어주고"; shot 13 "최종 확인하면"; shot 14 "완성됐어요"→"이제 잊어버릴 일 없이").
- **wow cut = shot 14** ("월세 자동이체가 완성됐어요" completion reveal).

## Audio / caption reconciliation
- faster_whisper **tiny** model, reconciled against authoritative on-screen captions/UI:
  - tiny consistently mis-heard "자동이체" as "자동이 채", "계좌" as "계자", "전체 탭에서" as "전체퇴배서", "매달 보낼" as "매달 보내"; line 10 was badly garbled ("이제 이저버리를 러프시 매달 자동으로 계자이 채가 진행이 되는데요") and corrected against captions to **"이제 잊어버리고 살아도 매달 자동으로 계좌이체가 진행되는데요"**; final CTA reconciled to **"이체 수수료는 당연히 무료인 거, 아시죠?"**.
- speech_coverage 0.958; bgm_likely was null in audio.json, set true on judgement (light instrumental bed under VO). On-screen names ("이다연님", "김창선", the masked 받는 분) are in-app demo placeholders; the recipient account number is partly masked in the footage and kept masked in recreation prompts.

## Caption lines (verbatim, count = 27 across 17 shots, incl. editorial header lines + end card)
Live-action supers (opening): 월세 내는 거 / 맨날 까먹는 / 당신! — editorial CONTENT bar: 월세 낼 때 진짜 편한 / 토스 자동이체 (SERVICE 자동이체 · YEAR 2024 · CATEGORY 부동산·공공서비스·송금 · PRODUCTION TEAM #team_transfer).
Demo caption pills (synced to VO): '전체 탭'에서 · '자동이체'를 실행해주세요 · '월세 자동이체'를 만들어볼게요 · 출금할 계좌를 선택하고 · 이체 날짜와 반복 일정을 · 세팅해주세요 · 매달 보낼 금액을 · 설정하고 · 상대방 계좌도 입력해주세요 · 이렇게 자동이체 이름도 · 적어주고 · 자동이체 내역을 · 최종 확인하면 · 월세 자동이체가 · 완성됐어요 · 이제 잊어버릴 일 없이 · 계좌 이체가 진행되는데요 · 이체 수수료는 · 당연히 무료인 거 · 아시죠?
End card: **Curator T / 토스를 발견하다**.

## Cuts (one line each)
| # | Time (s) | Framing | What's on screen | Caption |
|---|----------|---------|------------------|---------|
| 1 | 0.00–0.67 | CU | Live-action: hand holds iPhone, iMessage thread w/ 집주인 ("이번 달 월세 제때 꼭 납부 해주세요" / "네 죄송합니다 ㅠㅠ"), warm bokeh | "월세 내는 거" |
| 2 | 0.67–2.80 | CU | Live-action: tighter on the thread; new bubble "어제 월세가 안 들어왔네요. 확인부탁드립니다!" | "맨날 까먹는" → "당신!" |
| 3 | 2.80–4.37 | MCU | Live-action: woman in khaki shirt at warm desk, smiles; editorial CONTENT header slides in | "월세 낼 때 진짜 편한 / 토스 자동이체" |
| 4 | 4.37–5.84 | MCU | Live-action: woman holds up phone (자동이체 setup screen), header persists | (editorial header) |
| 5 | 5.84–9.31 | MS | Orange flat-lay: in-app search "자동이체" (서비스 자동이체/자동이체 확인증/자동납부) → 자동이체 landing (수수료 무료·휴일 당일, 자동이체 추가하기) | "'전체 탭'에서" / "'자동이체'를 실행해주세요" |
| 6 | 9.31–11.35 | MCU | Live-action: woman holds dark phone, speaks | "'월세 자동이체'를 만들어볼게요" |
| 7 | 11.35–12.75 | MS | Orange flat-lay: 자동이체 landing, finger taps blue "자동이체 추가하기", screen slides | (none — between lines) |
| 8 | 12.75–14.25 | MS | Orange flat-lay: "어느 계좌에서 보낼까요?" + bottom-sheet "출금 계좌를 선택해주세요" (토스뱅크 통장 20,182,747원…), finger taps | "출금할 계좌를 선택하고" |
| 9 | 14.25–17.82 | MS | Orange flat-lay: "언제 보낼까요?" (반복/1회, 매월 10일 wheel), finger spins → 선택 | "이체 날짜와 반복 일정을" / "세팅해주세요" |
| 10 | 17.82–21.35 | MS | Orange flat-lay: "얼마를 보낼까요?" 금액 0→500,000원, 매월 10일, 토스뱅크 통장, keypad, 다음 | "매달 보낼 금액을" / "설정하고" |
| 11 | 21.35–23.96 | MS | Orange flat-lay: "어떤 계좌로 보낼까요?" 계좌번호 입력(masked)+은행 선택 chips, keypad | "상대방 계좌도 입력해주세요" |
| 12 | 23.96–27.63 | MS | Orange flat-lay: "마지막으로 / 자동이체 제목을 입력해주세요", types "자취방 월세", keyboard, 확인 | "이렇게 자동이체 이름도" / "적어주고" |
| 13 | 27.63–32.37 | MS | Orange flat-lay: confirm "이다연님에게 매월 10일 500,000원씩 자동이체를 등록할게요" + 추가 설정 (다음 이체일 2024년 3월 10일, 받는 분에게 표시 김창선…), 추가하기 | "자동이체 내역을" / "최종 확인하면" |
| 14 | 32.37–36.74 | CU | Orange flat-lay (push-in): completed 자동이체 list "자취방 월세 / 매월 10일 500,000 원", toggle ON, 자동이체 추가하기 | "월세 자동이체가 / 완성됐어요" → "이제 잊어버릴 일 없이" |
| 15 | 36.74–39.61 | MCU | Live-action: woman holds dark phone, reassuring smile | "이제 잊어버릴 일 없이" → "계좌 이체가 진행되는데요" |
| 16 | 39.61–42.61 | MCU | Live-action: woman (closer), hand gesture + playful point to camera | "이체 수수료는 / 당연히 무료인 거" → "아시죠?" |
| 17 | 42.61–44.98 | TITLE_CARD | Pixel/CRT label badge peels in on textured off-white paper, blue "Curator T" + tagline | "Curator T / 토스를 발견하다" |

## Validator
- `validate_entry.py` → **PASS (17 shots)**, no warnings.
- All 17 t2i_start_frame prompts 502–639 words (≥500 required).
- Strict JSON confirmed; frames_dir + contact_sheet + 17 cut mids present.
