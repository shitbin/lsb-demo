# ADV-2026-042 분석 검토 보고서

| 항목 | 값 |
|------|-----|
| 파일명 | 29cm 1.mp4 |
| ID | ADV-2026-042 |
| 브랜드 | 29CM |
| 제품 | 셀렉트숍 플랫폼 (취향 큐레이션 라이프스타일 커머스) |
| 캠페인 | 당신2 9하던 삶 (브랜드 필름 60s) |
| 길이 | 60.16초 |
| 프레임수 | 1441 |
| FPS | 23.976 |
| 해상도 | 1920×1080 (16:9) |
| 컷수 (검출/보정) | 57 / 57 |
| 의미 단위(shots) | 12 |
| 제작연도(추정) | 2023 |
| 검증 | PASS |

## 의미 단위(시퀀스) 요약

> 57개 빠른 컷의 cross-cutting 몽타주를 12개 의미 단위(인물 챕터/디바이스 모먼트)로 묶어 기록. 컷수 57은 shot_count/shot_count_corrected에 보존.

| # | 구간 | 길이 | 기능 | 한 줄 설명 |
|---|------|------|------|-----------|
| 1 | 0.04–3.13s | 3.13s | brand_hook | 시네마틱 바다 부두 와이드 + 키네틱 카피 빌드 '29CM→당신2 9하던 삶' |
| 2 | 3.17–6.63s | 3.50s | narrative_setup | 낚시 친구들 전리품 사진 프린트 PIP + 태그 'NEITHERS / 유틸리티 셔츠' |
| 3 | 6.67–9.05s | 2.42s | transition_glitch | 글리치·CRT·데이터모시 트랜지션(웃는 얼굴 ECU·해변 질주) + '그냥 흘러가는 대로 살고 싶어요' |
| 4 | 9.09–15.02s | 5.96s | narrative_vignette | 밤 캠핑 랜턴 키아로스쿠로 + 태그 STANLEY 진공 캠프머그·커피 드리퍼 세트·lawn chair usa 론체어 클래식 / '재밌게' '즐겁게' |
| 5 | 15.06–21.48s | 6.46s | narrative_vignette | 사진가 화이트 미니멀 아파트 + 태그 Ma Journée·LIFE ARCHIVE·HermanMiller + 분할 제품그리드 artek/Hem/txture / '예쁜 걸' '멋진 거' |
| 6 | 21.52–26.65s | 5.17s | narrative_vignette | 오버헤드 누운 셀프포트레이트 + 흑백 사진 프린트 PIP + 햇살 플레어 / '놓칠 수 없죠' |
| 7 | 26.69–35.66s | 9.01s | narrative_vignette | 웜 텅스텐 화가 아틀리에(2인) + 태그 MERGE Bubble mug·BLUE BRICK 톤 턱 데님 / '할 수 있는 만큼' |
| 8 | 35.70–42.38s | 6.72s | narrative_vignette | 꽃 그린하우스 플로리스트 태블릿 스케치 + 태그 Mardi Mercredi 플라워 임브로이더리 스웨트 셔츠 / '할 수 있는 만큼 나를 사랑해 줄 거예요' |
| 9 | 42.42–46.38s | 4.00s | wow_moment | 러너 360 little-planet 셀카 + 소셜 UI(@alldaysmileboy #긍정 파워로 #나만의 길) + New Balance ML860 + VHS UI / '나로 태어났으니까' |
| 10 | 46.42–53.01s | 6.63s | narrative_vignette | 스트리트웨어 친구들(버거집) ↔ 뮤지션 여성 노래(피아노/신스) + 태그 GRAMICCI·BIG UNION·audio-technica·SNOWMAN22 + '다 내꺼' 스티커 |
| 11 | 53.05–58.27s | 5.26s | emotional_climax | 포스터/스티커(새로운 도전·멋진 실수)·35mm 필름 네거티브·환희의 춤 + 스왑워드 마스터 카피 / '어떤 삶을 구하던' '깊이 행복해질 수 있도록' |
| 12 | 58.31–60.10s | 1.84s | brand_cta | 순흑 화면 + 흰 '감도 깊은 취향 셀렉트샵' / '29CM' 워드마크 |

## 내러티브 구조

잔잔한 바다 오프닝·카피 빌드(인식) → 다섯 갈래 인물(낚시친구·사진가·화가·플로리스트·러너·뮤지션)이 각자 '구하던 삶'을 사는 cross-cutting 몽타주(공감) → 큐레이션 제품 태그가 각 라이프스타일을 받쳐줌(솔루션) → '어떤 삶을 구하던 깊이 행복해질 수 있도록' 정서적 클라이맥스(고양) → 검은 화면 '감도 깊은 취향 셀렉트샵 29CM'(브랜드 각인)

**구조 유형:** cross_cutting_montage

**Creative Device:** swap_word_kinetic_tagline + multi_persona_lifestyle_montage + product_curation_tags

**핵심 카피:** 마스터 태그라인 '당신2 9하던 ___ 삶' — 숫자 워드플레이(2·9=29CM) + 인물별 스왑형 수식어(감각적인/여행같은/몰입하는/나를 사랑하는/멈추지 않는). 마무리 '당신이 구하던 삶, 여기 29cm에서'.

## 기술 메모

- **오디오:** faster_whisper base 전사 성공 (speech_coverage=0.743). 여성 나레이션 1인 + 초반 남성 인물 대사. whisper 오인식('들을 점분께','살려줘','다닛고') 화면 자막·문맥으로 보정. BGM 잔잔한 무드 음악 추정(bgm_likely=true).
- **wiggle:** metrics mean_abs_shift_x=2.80, sign_flips_ratio=0.219 → 빠른 컷 몽타주 + 공격적 핸드헬드 + 글리치/데이터모시 + 360 little-planet 회전 합산. 순수 lenticular wiggle_3d 아님(인접 프레임 f820-821 확인 = 구체 투영 전체 회전, 정적 컷엔 미세 시점 떨림 없음).
- **컷 경계:** scenedetect(58씬) × metrics(55 cut candidates) 교차검증 + 3개 불일치 존(f419-515, f640-780, f1158-1230) 경계 프레임 직접 확인 → 모두 실제 컷으로 판정. 평균 샷 길이 약 1.0초의 빠른 몽타주.
- **반복 모티프:** 스왑워드 키네틱 카피 / 브랜드명+오렌지(+)배지+한국어 제품명 큐레이션 태그 / 떠 있는 사진 프린트·필름 콜라주 PIP / 글리치·CRT 트랜지션 / VHS 카세트 플레이어 UI 프레임 / 360 little-planet / 35mm 필름 네거티브.
- **제품 태그 verbatim:** NEITHERS 유틸리티 셔츠 · STANLEY 진공 캠프머그 · STANLEY 커피 드리퍼 세트 · lawn chair usa 론체어 클래식 · Ma Journée 크링클 셔츠 원피스 · LIFE ARCHIVE 일회용 카메라 · HermanMiller 임스 몰디드 암 체어 · artek STOOL 60 · Hem Hide Side Table H40 · txture STI · MERGE Bubble mug · BLUE BRICK 톤 턱 데님 · Mardi Mercredi 플라워 임브로이더리 스웨트 셔츠 · new balance ML860 · GRAMICCI 릴렉스드 캡 · BIG UNION 피그먼트 스웨트 셔츠 · audio-technica USB 타입 다이내믹 스피커 · SNOWMAN22 Stand.

## 창의적 역추정

**인사이트:** 취향 큐레이션 커머스는 '무엇을 파느냐'보다 '어떤 삶을 가능하게 하느냐'로 차별화 — 소비자는 물건이 아니라 자기다운 삶의 장면을 산다.

**타깃 모멘트:** 좋아하는 일에 몰입하며 '이게 내가 원하던 삶'이라 느끼는 일상의 순간.

**제품 역할:** 29CM 큐레이션 패션·리빙·취미 제품이 각 인물의 '구하던 삶'을 구성하는 소품으로 등장 — 제품은 라이프스타일의 조력자.

**차별점:** 단일 제품 광고가 아니라 다수 큐레이션 브랜드를 한 편의 정서적 브랜드 필름에 녹여, 플랫폼 자체를 '취향의 큐레이터'로 포지셔닝.

## 검증 정보

- 검증 도구: validate_entry.py
- 결과: PASS (12 shots)
- 완료 시각: 2026-06-13
- 프레임 판독: ~94/1441 native-res(57개 scenedetect 씬 중간프레임 전부 + 3개 불일치 경계존 경계 프레임 + 오프닝 타이포 빌드 + 글리치 트랜지션 + 360 little-planet 인접쌍 + 제품 태그·엔드카드 줌 크롭) + 100% per-frame metrics + scenedetect 58씬 + faster_whisper 전사
