# ADV-2026-028 — 토스 숨은 서비스 12 (연말정산 사전점검)

- **Source file**: 토스 숨은 서비스 12.mp4
- **Brand / series**: 토스 (Toss) — "토스 숨은 서비스" 시리즈 episode 12
- **Feature**: 연말정산 사전점검 (year-end tax settlement preview — estimate how much more to spend/contribute to maximize the refund)
- **Spec**: vertical 1080x1920, 9:16, ~59.28s, 29.97fps, 1775 frames
- **Format**: live-action presenter intro (handheld) → one continuous real-device handheld in-app demo with step-numbered torn-paper captions (badges 1–6) → live-action presenter outro sign-off. Same female presenter ("Toss Onboarding Coordinator 최유정") narrates throughout.
- **Audio**: faster-whisper ko (base), speech_coverage 0.994, likely soft BGM bed; narration corrected against on-screen captions (whisper mis-heard 전검→점검, 공제 예상드맥→공제 예상 금액, 연금조측→연금저축, 하늘을→한 해를).
- **shot_count (detected scenedetect)**: 6 → **shot_count_corrected: 4**
- **Cuts (gapless, 0→59.28)**: `0:5.873,5.873:30.397,30.397:53.153,53.153:59.28`
- **Cut decision**: scenedetect's 30.397/34.868/40.874s boundaries fall inside ONE continuous demo take (status-bar clock 3:55→3:56→3:57 runs continuously). Treated the gentle camera push-in at ~30.4s (medium-distance nav → closer results framing) as the only internal shot boundary; 34.87 & 40.87 hits and the 27.39s metrics cut_candidate are in-app caption/tab/page-transition changes, not camera cuts. Wiggle metric (mean_abs_shift_x 0.1447, sign_flips 0.244) = ordinary handheld micro-motion, NOT lenticular wiggle_3d.

## Cuts (one line each)

- **cut01 — 0.00–5.87s (MS, intro/hook)**: Presenter walks through a warm wood-paneled office lounge in an olive-green sweater + jeans, lanyard ID, holding a notebook then a phone; top marker-highlight title "연말정산 최대로 돌려 받으려면? / 토스로 미리 점검하기" (연말정산 circled yellow) + lower-third name tag "Toss Onboarding Coodinator / 최유정"; handheld follow, motion blur. VO: premise about pre-checking year-end tax in Toss.
- **cut02 — 5.87–30.40s (CU, demo nav, steps 1–4)**: Hard cut to a real iPhone in palm (warm-amber bokeh). Step-1 torn-paper captions (badge 1) walk through: open Toss home → 전체 (All) tab → search "연말" → select 연말정산 사전점검 → enter expected salary 3,000만원 on keypad → card/pension intro → consent bottom-sheet → tap 동의하기 → calculating screen ("김토스님의 소득공제 금액을 계산하고 있어요"). Badges increment 1→2 (예상 연봉 입력)→3 (연말정산 준비하기 터치)→4 (동의하기). Clock 3:55→3:56. Caption typo "사전전검" preserved.
- **cut03 — 30.40–53.15s (CU, demo results, steps 5–6, WOW)**: Continuous gentle push-in to a closer phone. Card 소득공제 result: headline "김토스님은 앞으로 체크카드·현금으로 써보세요", two-bar chart 최대 300만원 vs 내 공제 2,250,000원, "2,500,000원 더 쓰면 돼요 / 30% 공제 (추천)", spending breakdown (올해 쓴 금액 20,000,000원). Tab switch → 연금 세액공제: 660,000원 세액공제 예상 / 최대 1,485,000원, 연금저축 200만원·퇴직연금(IRP) 300만원 더. Badges 5 then 6 + no-badge benefit/caveat captions ("앞으로 얼마나 더 써야 / 최대로 공제받을 수 있는지도 / 확인하실 수 있어요", "물론 예상 금액이기 때문에 / 실제와 다소 차이가 있을 수 있습니다"). Clock 3:56→3:57.
- **cut04 — 53.15–59.28s (MS, outro/sign-off)**: Hard cut back to the presenter leaning on the counter, both hands on phone, warm smile, camera slowly widens (frosted-glass partition revealed). Lower-center marker-highlight caption "토스의 숨은 꿀기능 / 다시 찾아올게요!" (꿀기능 circled yellow); VO differs: "한 해를 마무리하는 연말정산 사전점검 / 토스로 똑똑하게 준비하세요."

## Notes
- App uses placeholder username "김토스" and illustrative demo figures — preserved verbatim as on-screen text.
- No real third-party logo marks recreated; presenter rendered generic in recreation prompts per copyright rules.
- Frames reviewed: ~33 native-res frames across all boundaries (±1/2) and every distinct caption/app-screen state + dense demo sampling; one caption crop zoomed to confirm the "사전전검" typo; cross-checked vs 100% per-frame metrics.
