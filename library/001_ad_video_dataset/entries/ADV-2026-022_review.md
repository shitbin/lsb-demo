# ADV-2026-022 — Review

- **Video file:** 토스 숨은 서비스 6.mp4
- **ID:** ADV-2026-022
- **Duration:** 40.94s · **fps:** 29.97 · **aspect:** 9:16 (1080x1920) · **audio:** yes (ko)
- **Brand / product:** 토스 (Toss) — 부동산 시세 알림 (apartment real-estate market-price tracking + push alert)
- **Campaign:** 토스 숨은 서비스 6 — "찜해 둔 아파트, 토스로 시세 알림 받기"
- **Category:** finance.fintech (real_estate / proptech / price_tracking / push_notification)
- **Shot count:** 11
- **One-line summary:** A relatable "tired of re-searching apartment prices" hook leads into an overhead screen-recording walkthrough of registering an apartment in Toss to track its market price, 전세/월세 and nearby prices, paying off with a Toss push notification when a new transaction is recorded — closed by the "Curator T / 토스를 발견하다" brand sticker.
- **Dominant technique:** screen_ui_walkthrough / tutorial_demo on a locked overhead tabletop phone, with voiceover-synced bottom caption pills, bracketed by warm live-action presenter shots and a paper title card; push-notification payoff. Very low global motion (mean_abs_shift_x 0.198); hard cuts only.
- **Corrected VO (8 lines):** 매매 타이밍 놓치고 있는 아파트, 매번 시세 검색하기 귀찮다면 / 토스에서 시세 알림까지 받아볼 수 있대요. / 전체 탭에서 부동산 시세를 검색해 주세요. / 시세를 확인할 부동산 주소와 면적을 선택하고 / 만약 보유 중인 부동산이라면 내가 샀던 가격도 입력할 수 있어요. / 부동산 등록을 완료하면 내가 관심 있는 아파트의 거래 추이를 확인할 수 있고 / 전세와 월세, 주변 아파트의 시세까지 같이 볼 수 있어요. / 새로운 거래가 이루어지면 토스 알림을 통해 거래 내역과 시세를 바로 확인할 수 있습니다.

## Cut list (11 shots, 0 → 40.94s, no gaps)

| Cut | Time (s) | Framing | Function | What happens / on-screen text |
|-----|----------|---------|----------|-------------------------------|
| 01 | 0.000–1.735 | ECU | hook_pain_point | Warm-lit presenter (auburn hair, coral V-neck) gazes at phone, pensive; word overlay "매매 타이밍" fades in |
| 02 | 1.735–3.136 | CU | problem_context_screen_reveal | Hard cut to phone: Toss real-estate map dense with blue price pins (지도/주변/거리/정책/숨김); word "아파트" |
| 03 | 3.136–4.771 | CU | problem_context_price_chart | Price-trend screen (매매/전월세, "3억 8,200", 최고, tooltip "2022.11 평균 5억 300 (0건)"); words "시세 검색하기" → "귀찮다면?" |
| 04 | 4.771–7.774 | MS | title_card_setup_presenter | Hard cut to presenter at desk; torn-paper CONTENT card "찜해 둔 아파트 / 토스로 시세 알림 받기" (#team_homeloan) |
| 05 | 7.774–11.378 | CU | step1_search_service | Overhead tabletop phone: Toss search "부동산", taps 부동산 시세; pills "'전체 탭'에서" → "'부동산 시세'를 검색해주세요" |
| 06 | 11.378–26.093 | CU | step2_register_property_walkthrough | One continuous overhead take: register apt (참누리/행복마을, 경기도 화성시 기산동), 면적 선택 84.91㎡(33평), price modal 나중에 하기, 등록 완료 toast, 매매 trend chart; pills step the how-to |
| 07 | 26.093–31.465 | CU | step3_jeonse_wolse_and_nearby_prices | Same overhead: 전세(2억7,000만원)→월세(2,000만원·114만원) tabs + 주변 부동산 시세 (기산동/화성시/경기도, KB부동산 제공); pills "전세와 월세" → "주변 아파트의 시세까지" → "같이 볼 수 있어요" |
| 08 | 31.465–33.233 | CU | payoff_setup_push_notification_lockscreen | Hard cut: phone wakes to blue lockscreen (2월 23일 금요일 11:51), Toss push banner "토스 / 1 알림"; pill "새로운 거래가 이루어지면" |
| 09 | 33.233–36.003 | ECU | payoff_notification_detail | Macro push on notification "내 부동산에 새로운 거래가 감지됐어요"; pills "토스 알림을 통해" → "거래 내역과 시세를 바로 확인할 수 있습니다" |
| 10 | 36.003–39.406 | CU | recap_registered_property_detail | Hard cut back to overhead property detail (매매 84.91㎡, 3억 8,000만원, 최근 실거래 chart, 2024년 1월 19일 3억 8,500만원…); payoff caption continues |
| 11 | 39.406–40.940 | MS | brand_outro_title_card | Hard cut: paper sticker pops up centered "Curator T / 토스를 발견하다" (blue sketch wordmark on off-white paper) |

## Notes
- 12 scenedetect macro-scenes condensed to 11 shots. The long phone screen-recording (11.38–26.09) is one continuous locked overhead tabletop take (cut06); the 26.09 전세/월세 content boundary is opened as cut07. Hard camera cuts confirmed by diff spikes at frames 53, 95, 144, 234, 944, 997, 1080, 1182 (diff 52–134).
- Captions: word-by-word white overlays in the live-action/early-UI section; bottom-centered grey/black pill captions during the tabletop walkthrough — both mirror the single calm female VO.
- Demo property anonymized on-screen ("행복마을 …" 경기도 화성시 기산동). text_raw whisper corrected against the on-screen caption pills.
- Abstraction: persons described by type (no celebrity clone); Toss/KB/국토교통부 names kept verbatim only where they appear as in-app/caption text; image prompts keep app styling and the outro wordmark logo-free/generic.
- **Validator: PASS (11 shots).**
