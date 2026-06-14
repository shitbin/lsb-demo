# ADV-2026-014 — Review

- **Source file:** `토스 미니앱 5.mp4`
- **Folder:** `01_금융·핀테크/토스/토스 미니앱`
- **Brand / product:** Toss (Viva Republica) — 토스 미니앱 (in-app mini-app marketplace inside the Toss super-app)
- **Category:** finance.fintech_platform · super-app / mini-app showcase
- **Duration:** 33.507s · 60 fps · 1920x1080 · 16:9 · 6 cuts
- **Audio:** has_audio true, BGM-only / caption-led, **no voiceover** (faster_whisper found 0 speech segments). All copy is on-screen captions.
- **Production:** pure motion-graphics + app-UI montage, locked-off camera. mean_abs_shift_x 1.23 / sign_flips 0.187 = sliding/scrolling UI motion, **not** a camera wiggle (no wiggle_3d).
- **Hook:** 0.0s (cut 1, "토스에서 할 수 있는 수백 가지 일들"). **CTA / signoff:** 27.617s (thesis card → product name 토스 미니앱 → toss logo).
- **WOW cut:** 4 (the accumulating chip wall pouring into one phone).

## Cut-by-cut (6 cuts)
1. **0.00–10.85s** — Hook: blank → centered title "토스에서 할 수 있는 수백 가지 일들" (지 일들 keyed blue) → slot-machine vertical service list ("토스에서 할 수 있는" + 인기 알바 찾기 / 실시간 뉴스 보기 / greyed 부동산 안전 거래·따릉이 타기·수영 기록하기·용달 예약하기·장학금 알림 받기·여행 코스 AI 추천) → value-prop "설치할 필요 없이 [3D Toss app icon] 토스 앱 하나로". Transition out: dissolve.
2. **10.85–12.317s** — Converging photo collage: floating rounded lifestyle photo cards (running, cycling+skyline, train window, iced coffee, chess, apartments, shopping bag) drift inward to a central cluster. No text. Dissolve in/out.
3. **12.317–16.75s** — Horizontal carousel of real mini-app feature cards scrolling R→L: bike-rental map (대여하기), Japanese-learning feedback (だいじょうぶ [다이죠부] / 괜찮아요·즐거웠어요), swim tracker (총 수영 거리 1.0km / 1h 07m), KTX ticket (11:58→14:35 부산역), game character, Animation Style AI card (716,836개), flight ticket (ICN→CEB 244,950 ↓50% 티항공).
4. **16.75–27.617s** — WOW beat: dense scrolling wall of named service chips (웨이·택시 호출·알바몬·디스팟·팜픽·기차 예약·뉴스보이·마이클·머지푸르트 …) + floating glossy 3D objects, swept into a blue liquid morph that pours into one centered phone — mini-app store screen under "일상 앱부터", then casual-game screen (수박게임, 실시간 인기 게임) under "게임까지". Hard cut out.
5. **27.617–28.85s** — Hard-cut thesis card: centered charcoal "앱을 쓰는 새로운 방식" on light grey (the metrics-flagged 27.62s cut). Color-shift morph out.
6. **28.85–33.507s** — Brand reveal: kinetic color-typo ("새로운 방식" pink-orange) → 3D category objects (money bag/car/house + apple/controller/diamond) joined by a glowing blue beam → multi-color product name "토스 미니앱" → centered toss logo lockup + fineprint "*토스 미니앱 서비스는 만 19세 이상부터 이용할 수 있어요." End.

## Concept
Repositions Toss from "just a finance app" to a super-app by piling real, surprising everyday services + games into one phone with no installs, then branding the experience "토스 미니앱 — 앱을 쓰는 새로운 방식". Surprise-reveal + breadth-demo + accumulation montage.

## Validation
`validate_entry.py` → **PASS (6 shots)**. t2i word counts: 547 / 553 / 590 / 598 / 633 / 574 (all ≥500). frames_dir, contact_sheet and all six cutNN_mid.png present.
