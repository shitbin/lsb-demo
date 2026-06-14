# ADV-2026-019 — Review

- **Video file:** 토스 숨은 서비스 3.mp4
- **ID:** ADV-2026-019
- **Duration:** 40.87s
- **FPS:** 29.97
- **Aspect:** 9:16 (1080x1920)
- **Shot count (corrected):** 11  (scenedetect raw scenes: 10 hard cuts; 11th = end card split)
- **Brand / Product:** Toss — Toss 정부지원금 찾기 (hidden government-subsidy / benefits finder)
- **Campaign:** 토스 숨은 서비스 3 — 정부지원금 찾기 (creator series: Curator T / 토스를 발견하다)
- **Category:** finance.fintech
- **Capture style:** mixed — warm shallow-DOF live-action interior shots (a high-angle handheld view of a laptop scrolling official government portal pages, then a young woman holding up an iPhone with an editorial CONTENT header) intercut with flat-lay phone-on-vivid-ORANGE screen-demo shots for the step-by-step UI walkthrough; the demo span alternates wide flat-lay and tight push-in close-ups by screen-state.
- **Camera signature:** handheld_micro on the interior live action (laptop + woman); locked_off on the flat-lay UI demo and end card, with two slow push-ins (shots 5, 9). **Wiggle: NONE** (mean_abs_shift_x 0.1232 / sign_flips 0.24 = ordinary handheld micro + locked-off flat-lay, NOT stereoscopic parallax; confirmed visually).
- **Dominant technique:** Voice-and-caption-synced in-app feature walkthrough; hardcoded lower-third dark-brown caption pills on the orange UI-demo shots, large centered white supers + a flat editorial "CONTENT" header bar on the live-action opening; closes on the pixel/CRT series end card.
- **One-line summary:** Scattered government subsidies (clicking around many official portal sites) are consolidated by a hidden in-app finder — search "지원금" in the all-tab, answer your address / family size / children / work-and-household situation, get a personalized at-a-glance list of the subsidies you qualify for (193 results), open one to read its eligibility/criteria/support content and application period & method, and set an alert for new ones — signed with the retro pixel/CRT "Curator T / 토스를 발견하다" series badge.

## Structure
- 10 confirmed scenedetect hard cuts (diff>40) at f35/84/154/280/397/683/774/856/992/1174 → cross-checked visually.
- The f154–683 orange span is ONE constant orange background but contains genuinely distinct app screens; split by SCREEN-STATE into shots 4–6 (search "지원금" → eligible-subsidies overview → short input form across district/household-size/children/situation screens + brief empty-state then results count).
- The f683–855 close-up results span was split at the f774 hard cut into shot 7 (results-list, tap 모두 보기) and shot 8 (category browse + open the 배우자 출산휴가 급여 row).
- Shot 9 (f856–991) is the chosen subsidy's detail page; shot 10 (f992–1173) is the alert step (favourite star + alert bottom-sheet). The f1067 scenedetect cut was NOT treated as a shot boundary — it is the alert bottom-sheet appearing/changing state within shot 10.
- Framing alternates wide flat-lay vs tight close-up within the same screen-states (shots 5 and 9 push in); kept as single shots.
- **wow cut = shot 7** (personalized "받을 수 있는 지원금 193개" result reveal).

## Audio / caption reconciliation
- faster_whisper **tiny** model, reconciled against authoritative on-screen captions/UI:
  - "정부지원금" mis-heard as "정소지원금"; "흩어져" as "특퓨저" (line 1, fixed from supers 이곳저곳/흩어져있는/정부지원금); "근로상황" as "글로상왕" (line 4); final clause mis-heard "노치지 않고 생길 수 있어요" corrected to the authoritative caption pill **"놓치지 않고 챙길 수 있어요"**.
- speech_coverage 0.939; bgm_likely was null in audio.json, set true on judgement (light instrumental bed). The on-screen name "김창선님" is an in-app demo placeholder; opening laptop pages (NTS/MOEL/정부24-style) are real-world artifacts captured in footage, abstracted to generic public-service interfaces in recreation prompts.

## Caption lines (verbatim, count = 22 across 11 shots, incl. end card)
Live-action supers: 이곳저곳 / 흩어져있는 / 정부지원금 — editorial bar: 정부지원금 / 놓치지 않고 받는 꿀팁 (SERVICE 숨은정부지원금찾기 · YEAR 2024 · CATEGORY 부동산·공공서비스·송금 · PRODUCTION TEAM #team_금금프로덕트).
Demo caption pills (synced to VO): '지원금'을 검색해보세요 · 수많은 정부지원금 중에서 · 나에게 맞는 지원금을 · 찾을 수 있는데요 · 살고 있는 주소 · 가족 형태 · 근로 상황 등을 입력하면 · 내가 받을 수 있는 · 정부지원금을 · 한눈에 확인할 수 있어요 · 지원 대상과 기준 · 신청 기간과 방법까지 · 꼼꼼히 확인할 수 있고 · 알림 신청을 해두면 · 새로운 지원금이 올라올 때 · 놓치지 않고 챙길 수 있어요.
End card: **Curator T / 토스를 발견하다**.

## Cuts (one line each)
| # | Time (s) | Framing | What's on screen | Caption |
|---|----------|---------|------------------|---------|
| 1 | 0.00–1.17 | CU | Live-action: high-angle handheld view of a laptop showing a govt tax-portal page (국세청-style, 알림·소식, 2023 banner), warm bokeh | "이곳저곳" → "흩어져있는" |
| 2 | 1.17–2.80 | CU | Live-action: laptop scrolled to a govt ministry portal page (고용노동부/정부24-style, navy 민원 tab), keyboard in foreground | "흩어져있는" → "정부지원금" |
| 3 | 2.80–5.14 | MCU | Live-action: woman in beige shirt holds up an iPhone to camera, gentle smile; editorial CONTENT header bar | "정부지원금 / 놓치지 않고 받는 꿀팁" |
| 4 | 5.14–9.34 | MS | Orange flat-lay: in-app search "지원금" + suggestions/서비스 list (숨은 정부지원금 찾기 …) + keyboard | "'지원금'을 검색해보세요" |
| 5 | 9.34–13.25 | MS | Orange flat-lay (push-in): eligible-subsidies overview "김창선님이 받을 수 있는 정부지원금…" list (근로장려금 150만원, 청년희망키움통장 538,000원…), blue 내 지원금 확인하기 | "수많은 정부지원금 중에서" / "나에게 맞는 지원금을" / "찾을 수 있는데요" |
| 6 | 13.25–22.79 | MS | Orange flat-lay: short input form — 군·구 선택 → 몇 명이 함께 사나요? → 아이가 있나요? → 해당되는 상황 (결과 보기) → 0개 empty → 193개 results | "살고 있는 주소" / "가족 형태" / "근로 상황 등을 입력하면" / "내가 받을 수 있는" / "정부지원금을" |
| 7 | 22.79–25.83 | MS | Orange flat-lay (close-up): results "받을 수 있는 지원금 193개", 알림 받기, category tabs (주거/일자리/출산…), tap 정부 지원금 모두 보기 이동 | "한눈에 확인할 수 있어요" |
| 8 | 25.83–28.56 | MS | Orange flat-lay: results list scrolls 일자리/출산/교육 categories; finger taps "배우자 출산휴가 급여" row | "지원 대상과 기준" |
| 9 | 28.56–33.10 | MS | Orange flat-lay (push-in): detail "배우자 출산휴가 급여" — 지원 대상 / 선정 기준 / 지원 내용, blue 이 지원금에 관심있어요 | "지원 대상과 기준" / "신청 기간과 방법까지" / "꼼꼼히 확인할 수 있고" |
| 10 | 33.10–39.17 | MS | Orange flat-lay: 관심 지원금 (배우자 출산휴가 급여 starred) + alert bottom-sheet "새로운 지원금이 올라오면 알려드릴까요? / 등록하고 알림 받기 / 닫기" | "알림 신청을 해두면" / "새로운 지원금이 올라올 때" / "놓치지 않고 챙길 수 있어요" |
| 11 | 39.17–40.87 | TITLE_CARD | Pixel/CRT badge on textured off-white paper, blue "Curator T" + tagline | "Curator T / 토스를 발견하다" |

## Validator
- `validate_entry.py` → **PASS (11 shots)**, no warnings.
- All 11 t2i_start_frame prompts 525–676 words (≥500 required).
- Strict JSON confirmed; frames_dir + contact_sheet + 11 cut mids present.
