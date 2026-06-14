# ADV-2026-038 분석 검토 보고서

| 항목 | 값 |
|------|-----|
| 파일명 | 현대카드 1.mp4 |
| ID | ADV-2026-038 |
| 브랜드 | 현대카드 |
| 제품 | MX BOOST (M BOOST / X BOOST 신용카드) |
| 캠페인 | MX BOOST '악플에 강경대응' |
| 길이 | 30.16초 |
| 프레임수 | 721 |
| FPS | 24.0 |
| 해상도 | 1280×720 (16:9) |
| 컷수 | 14 (정정 14) |
| 제작연도(추정) | 2021 |
| 검증 | PASS |

## 컷 요약

| # | 구간 | 길이 | 기능 | 한 줄 설명 |
|---|------|------|------|-----------|
| 1 | 0.00–0.875s | 0.88s | graphic_hook | 화이트 위 블루 'M' 카드형상 + 오렌지 'X' 마크가 회전·모핑하는 추상 디자인 그래픽 인트로 |
| 2 | 0.875–2.75s | 1.88s | product_reveal | 프리미엄 카드 플레이트(레드 MX·샴페인골드 플레임 등) 슬라이드·기립 히어로 |
| 3 | 2.75–4.958s | 2.21s | narrative_setup | 레드 MX카드 + 가짜 SNS 극찬 댓글 'xxyyoung123 / 현대카드 디자인 찢었 / 7.3만' |
| 4 | 4.958–8.00s | 3.04s | narrative_build | 옐로 카드 + 2단 댓글 '디자인 만든 사람 상줘라' / 답글 '혜택은 벌줘라!!!' |
| 5 | 8.00–10.083s | 2.08s | product_demo | 블루 M BOOST카드 + 레드 X카드 병치 (카드면 'Boost Your Everyday / Use M BOOST') |
| 6 | 10.083–12.833s | 2.75s | narrative_build | 화이트 발급기('HYUNDAI CARD')에서 블루 오브젝트 + 댓글 '잘 쓸게요, 카드 대신 책갈피로 / 4.6만' |
| 7 | 12.833–15.333s | 2.50s | twist_punchline | 화이트 위 대형 타이포 '현대카드 / 악플에 강경대응 하겠습니다' (반전 펀치라인) |
| 8 | 15.333–16.75s | 1.42s | product_benefit | 네온 다크 스테이지 블루 M + 오렌지 BOOST + 흰 카피 '온라인 페이 5% 적립 / M 위에 BOOST' |
| 9 | 16.75–19.00s | 2.25s | product_benefit | 밝은 콜드그레이 위 블루 카드조각 쏟아짐 + 거대 BOOST 형상 '보너스 10,000 M포인트 / M 위에 BOOST' |
| 10 | 19.00–21.667s | 2.67s | product_benefit | 시네마틱 모노 로켓 발사 스모크 + 레드 X카드 '할인율 2배로 / X 위에 BOOST' |
| 11 | 21.667–24.25s | 2.58s | product_hero | 무드 다크 스튜디오 레드 MX카드 반사 + 흰 카피 'MX 위에 BOOST' + 장문 고지 |
| 12 | 24.25–25.042s | 0.79s | twist_resolution | 그레이 전환, M카드 좌·X카드 우로 분리 + 중앙 카피 '열받은 거 아닙니다' (반전 해소) |
| 13 | 25.042–29.125s | 4.08s | product_lineup_cta | 카드 6종(레드 MX·블루·MORE OR LESS·골드·옐로·브론즈) 가로 라인업 + 'MX BOOST' 워드마크 정착 |
| 14 | 29.125–30.04s | 0.92s | brand_cta | 순흑 배경 + 라운드 브래킷 안 흰 'Hyundai Card' 워드마크 (브랜드 클로저) |

## 내러티브 구조

추상 디자인 그래픽(cut1) → 프리미엄 카드 히어로(cut2) → 가짜 '악플(=극찬)' 댓글 누적(cut3~6) → 반전 펀치라인 '악플에 강경대응'(cut7) → BOOST 혜택 3종 폭발(cut8~11) → '열받은 거 아닙니다' 반전 해소(cut12) → MX BOOST 라인업 + CTA(cut13) → 브랜드 각인(cut14)

**구조 유형:** twist_reveal (build_to_payoff)

**Creative Device:** fake_praise_comments_as_hate + deadpan_brand_clapback + kinetic_card_graphic_system

**핵심 카피:** '악플에 강경대응 하겠습니다' (cut7, 12.833s) — 극찬을 '악플'로 비튼 반전 훅. 해소는 '열받은 거 아닙니다'(cut12).

## 기술 메모

- **오디오:** faster_whisper 샌드박스 디스크 공간 부족(No space left on device)으로 ASR 실패 → 화면 자막 기반 수동 추론 (`transcribed_by: manual_from_captions`). BGM 존재 가능성 높음.
- **wiggle:** metrics mean_abs_shift_x=1.49, sign_flips_ratio=0.21 → 오프닝 그래픽(cut1~2) 카드형상 슬라이드/회전 모션 + BOOST 시퀀스 카메라 이동 기인. 순수 핸드헬드 wiggle_3d 부재.
- **컷 경계:** scenedetect(14씬) + metrics 교차검증. 주요 하드컷 diff: f369(163.3, →네온 M BOOST), f520(125.0, →다크 MX), f699(202.5, →엔드카드). 오프닝 추상 그래픽 과분할(f20/f45)은 병합, 댓글 구간 실제 컷 f192/193 추가 → 동일 14컷이나 경계 정정.
- **혜택 자막 verbatim:** 온라인 페이 5% 적립 / 보너스 10,000 M포인트 / 할인율 2배로. 고지: '당월실적 50만원 이상 이용 시 적립 (M BOOST, M2 BOOST 월 최대 1만 M포인트, M3 BOOST 월 최대 2만 M포인트)', 'M BOOST 게임, X BOOST 게임 매달 플레이트 추가 시 발급수수료 10만원 (~2021. 12. 31)'.
- **법적 고지:** X BOOST ISSUED BY HYUNDAI CARD, SEOUL, REPUBLIC OF KOREA. (C) ALL RIGHTS RESERVED.

## 창의적 역추정

**인사이트:** 디자인이 너무 좋으면 '쓰기 아깝다'는 역설적 칭찬이 나온다 — 칭찬을 '악플(불만)'처럼 비틀면 더 강한 자랑이 된다.

**타깃 모멘트:** 신상 카드 디자인을 본 사람들이 SNS에 '디자인 찢었' '상줘라'를 쏟아내는 댓글 반응 순간.

**제품 역할:** 디자인(MX 플레이트)과 혜택(M/X BOOST 적립·할인) 두 축을 모두 가진 카드 — '디자인도 혜택도 둘 다'를 증명.

**차별점:** 혜택 나열형 카드 광고를 '악플 클랩백'이라는 위트 포맷으로 비틀어 브랜드 자신감을 연출.

## 검증 정보

- 검증 도구: validate_entry.py
- 결과: PASS (14 shots)
- 완료 시각: 2026-06-13 (batch_10)
- 프레임 판독: ~70/721 native-res (전 컷 경계 + 각 컷 미드포인트 + diff 스파이크 f192/f369/f520/f699 + 모든 화면 카피 verbatim) + 100% per-frame metrics + scenedetect CSV 교차검증
