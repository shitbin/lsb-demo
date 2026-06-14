# ADV-2026-051 — 검토용 리뷰

- **영상 파일:** `기아 ev.mp4`
- **브랜드 / 제품:** 기아 (Kia) / 전기차 라인업 — **EV9** ("The Kia EV Multiverse", 배우 류승룡 출연)
- **category_primary:** `auto.ev`  | industry `automotive`
- **길이 / fps / 비율:** 102.795s / 23.976 / 16:9 (1920×1080, rotation 0)
- **shot_count (보정):** 18  | scenedetect 원 검출 58 scenes (빠른 교차편집 → 18개 내러티브 비트로 통합)
- **narrative_structure:** cross_cutting_montage | pacing: steady
- **hook:** 0.0s (스카이라인 타이틀) | **cta:** 97.85s (브랜드 라인업)
- **creative_device:** 프리미엄 '성공' 내레이션 ↔ 엄마 잔소리 전화 코미디 디플레이션 + 셀럽 자기패러디 + 제품 히어로컷 교차
- **wow cuts:** 9 (히어로 워크 + 엄마 영상통화), 14 (명패 '상무이사 류승룡'), 15 (90도 회전 백일몽)
- **production_signature:** live_action, dolly/handheld/locked-off 혼재, cool grade, clean digital. **wiggle_3d 부재**(주행/트래킹 컷의 모션이 metrics 수치 원인 — f289/f292 육안 확인).
- **audio:** ko, speech_coverage 0.855, BGM 추정 존재. faster_whisper(base) — text_raw 오인식 다수를 화면 자막으로 보정(자막=음성 싱크).
- **frames_dir:** `ADV-2026-051_frames/` (cut01–cut18 mid + contact_sheet.png)

## 컨셉 한 줄
성공한 임원의 거창한 자기 서사를 엄마 영상통화 한 통이 무너뜨리는 위트로, 프리미엄 EV9를 "폼나는 차"가 아니라 "모든 삶에 함께하는 차(For Every Life)"로 포지셔닝.

## 핵심 카피 (화면 자막 = 음성, 원문 보존)
- VO: "성공이란 비단 / 물질적인 성취에만 / 국한되는 개념이 아닐 겁니다." → "후배들의 존경과 여유로운 태도 / 그리고 빛나는 존재감으로 완성되죠."
- 대사: "상무님 안녕하세요" · "어 김대리, 머리 했네?" · "위에서 봐~" · "자동이체 해놓으라니까!" · "예은이 학원비" · "그거 주말에 고치라고 했어 안 했어?" · "내가 이따 전화 다시 할게" · "상무 류승룡...!" · "하...이거지..." · "부드러워~" · "너 또 까먹었지?" · "아 맞다!"
- 펀치라인: **"아주 상무 됐다고 EV9 타고 신났지?"**
- 브랜드: **"For Every Life — The Kia EV"** / **"Movement that inspires"**
- 프롭 텍스트: 명패 "상무이사 류승룡" · 폰/차내 콜 "♥여봉봉♥" · 모델 리빌 "The Kia EV 9" · 타이틀 "The Kia EV MULTIVERSE" · 플레이트 "26더 3100"

## 컷별 표 (18 내러티브 샷)

| # | 시간(s) | framing | function | 한 줄 요약 | 핵심 자막 |
|---|---|---|---|---|---|
| 1 | 0.00–4.96 | EWS | brand_hook_title | 항공 도시 스카이라인 + 타이틀, 글래스 타워 푸시인 | The Kia / EV MULTIVERSE |
| 2 | 4.96–8.93 | LS | product_reveal | 로우앵글 고속 주행 + 대형 '9' 모델명 와이프 | The Kia EV 9 |
| 3 | 8.93–11.51 | MCU | narrative_setup | 뒷좌석 사색하는 임원 + 대리석 로비 도착 | (VO 시작) |
| 4 | 11.51–16.52 | CU | product_hero | EV9 전면 디테일(별지도 LED) + 블루 앰비언트 대시 터치 | 성공이란 비단 |
| 5 | 16.52–19.27 | MCU | narrative_setup | 룸미러 반영 사색 + 구두 하차 | 물질적인 성취에만 / 국한되는 개념이 아닐 겁니다. |
| 6 | 19.27–22.69 | MLS | narrative_dialogue | EV 옆 도착·인사, 후배 접근 | 상무님 안녕하세요 / 어 김대리, 머리 했네? |
| 7 | 22.69–27.32 | MCU | narrative_dialogue | 따뜻한 임원 클로즈업, 손가락 제스처 | 어 김대리, 머리 했네? / 위에서 봐~ |
| 8 | 27.32–34.24 | WS | narrative_montage | 노스탤직 오피스, 후배들 존경 + 그린스웨터 청년 | 후배들의 존경과 여유로운 태도 / 그리고 빛나는 존재감으로 완성되죠. |
| 9 | 34.24–40.12 | WS | wow_comedy_reveal | 역광 복도 히어로 워크 + 엄마 영상통화 '여봉봉' | ♥여봉봉♥ |
| 10 | 40.12–46.38 | MCU | narrative_comedy | 전화 잔소리 견디는 표정, 동료들 웃음 | 자동이체 해놓으라니까! / 예은이 학원비 / 아 이제 그건 말씀이시군요 |
| 11 | 46.38–53.34 | WS | narrative_comedy | 럭셔리 임원 라운지 통화 워크 | 그거 주말에 고치라고 했어 안 했어? / 내가 이따 전화 다시 할게 |
| 12 | 53.34–61.65 | WS | narrative_comedy | 임원실 와이드 + 다른 임원과 대화(골프채) | 어 알았어~ |
| 13 | 61.65–67.03 | MS | narrative_comedy | 흐뭇한 기립 + 소파에 몸 던지는 장난 | (자막 없음) |
| 14 | 67.03–71.11 | MCU | wow_name_reveal | 명패 '상무이사 류승룡' 트로피처럼 들고 감상 | 상무 류승룡...! |
| 15 | 71.11–78.70 | MCU | wow_daydream | 90도 회전 프레이밍 백일몽, 황홀한 미소 | 하...이거지... |
| 16 | 78.70–85.42 | LS | product_hero_feature | 골든아워 EV9 주행 + 차내 커넥티드콜 '여봉봉' | 부드러워~ |
| 17 | 85.42–91.80 | MCU | product_feature_comedy | 직접 운전 리액션 + 후미등(EV9 배지) 디테일 | 너 또 까먹었지? / 아 맞다! |
| 18 | 91.80–102.73 | WS | brand_cta | 펀치라인 + 강변 스카이라인 히어로 + EV 라인업 로고 락업 | 아주 상무 됐다고 EV9 타고 신났지? / For Every Life The Kia EV / Movement that inspires |

## 분석 메모
- **컷 통합 근거:** scenedetect 58개는 1초 미만 인서트가 많은 빠른 교차편집의 산물. 동일 셋업/로케이션/내러티브 비트 단위로 18개 샷으로 통합(각 샷 notes에 원 scene 범위·프레임 명기).
- **wiggle 판정:** metrics `mean_abs_shift_x=1.55, sign_flips=0.15`는 다수의 빠른 주행/트래킹 컷에서 기인. 정적 인테리어 인접 프레임(f289 vs f292) 육안 확인 결과 좌우 시점 진동 없음 → 순수 wiggle_3d 시그니처 **부재**로 기록.
- **메타 셀럽 장치:** 주인공의 명패가 배우 본명 '류승룡'(상무이사 류승룡) — 셀럽 자기패러디. recreation_prompts에서는 인물 얼굴을 generic(초상 회피), 자막·프롭 텍스트는 원문 보존.
- **프레임 보완:** ffmpeg 1차 추출이 2441프레임에서 중단되어 tail 22프레임(f2442–f2463)을 별도 추출·해시검증 후 보완(전 2463프레임 확보, ffprobe count와 일치).
