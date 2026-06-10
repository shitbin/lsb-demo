# LSB 광고 레퍼런스 데이터셋 — 뷰 (dataset_view)

총 **12개** entry · schema **v0.4++** (STEP 4.5 시각 인벤토리 + 신규 entry는 recreation_prompts 포함). 인덱스: `index/` (10축 + master.json, 전부 영문 토큰·`_meta.language=en`).

| ID | 브랜드 | 캠페인 | 카테고리 | 길이 | 컷 | 언어 | 비고 |
|---|---|---|---|---|---|---|---|
| ADV-2026-001 | 우리은행 | 우월한 월급통장 | `IT.fintech` | 21.47s | 15 | ko | style_prompt 4 |
| ADV-2026-002 | KGM | 프리윌루전-무쏘 (The Original) | `auto.pickup_truck` | 30.03s | 11 | ko | style_prompt 4 |
| ADV-2026-003 | 현대자동차 (Hyundai) | 디 올 뉴 팰리세이드 하이브리드 (source TcmmQmHGvzU) | `auto.suv_hybrid` | 30.03s | 27 | ko | style_prompt 6 |
| ADV-2026-004 | 한양립스 | 청주 한양립스 더 벨루체 (분양 TVC) | `realestate.apartment_presale` | 30.03s | 17 | ko | style_prompt 4 |
| ADV-2026-005 | 올리브영 | 올리브영 오늘드림 | `retail.beauty_platform` | 28.97s | 14 | ko | style_prompt 3 |
| ADV-2026-006 | ANTA (安踏) | 安踏速干之王 (속건 러닝웨어) | `apparel.sportswear` | 33.96s | 11 | zh | style_prompt 4 |
| **ADV-2026-007** | **신세계 (SHINSEGAE)** | **NEW SANTA · Epilogue 'Bye New Santa'** (카리나/돌고래유괴단·신우석, source ZpFAVJ4ND3g) | `retail.department_store` | 46.88s | 8 | ko | **recreation 8/8** |
| **ADV-2026-008** | **전북대학교 (JBNU)** | **전북대반전 (JBNU Big Reversal)** (source dH3B-Fy0mFQ) | `education.university` | 40.04s | 23 | ko | **recreation 23/23** |
| **ADV-2026-009** | **Alma / Tuneface (튠페이스)** | **NOTHING'S FOREVER (미용 의료기기 브랜드필름)** (source YcV3d-YIJT0) | `healthcare_pharma.aesthetic_device` | 20.02s | 14 | ko | **recreation 14/14** |
| ADV-2026-010 | 배민×신한 (abstracted) | 체크카드 셀럽 키네틱타이포 (source, 추상화) | `finance.card` | 19.4s | 19 | ko | recreation 19/19 |
| **ADV-2026-011** | **OpenAI — ChatGPT** | **Dish with ChatGPT** (source To04SSylvVY) | `IT.ai_product` | 30.03s | 7 | en | **recreation 7/7 · 전720프레임** |
| **ADV-2026-012** | **Nike** | **So Win (2025 Super Bowl)** (source FjwAk30N4I8) | `apparel.sportswear` | 60.1s | 60 | en | **recreation 60/60 · 전1441프레임** |

## 2026-06-10 추가 (신규 entry 2건 — 첫 영어/글로벌 레퍼런스, 전 프레임 전수판독)

- **ADV-2026-011 OpenAI ChatGPT 'Dish with ChatGPT'** — 첫 `IT.ai_product` 카테고리. **A24풍 따뜻한 로우키 실사 브랜드필름**(30초·2.39:1 레터박스). frame-diff 하드컷 0건 → **심리스 모핑/매치**가 시그니처. 구조: 무언의 친밀 비트(요리·식사·눈물·함께요리)를 **타이핑된 ChatGPT 프롬프트** `I need a recipe that says, "I like you, but want to play it cool."`가 사후 재맥락화 → 감성·위트 레시피 응답(`Above all, don't sweat it. You got this.`)이 스크롤되며 카메라가 **창밖 브릭 외관으로 연속 풀아웃** → ChatGPT 로고 엔드카드. 카피=화면 ChatGPT 대화 전문 verbatim. **기능 안 보임·감정 먼저** 공식 = 기능 직설형과 강한 contrast 신호.
- **ADV-2026-012 Nike 'So Win' (2025 Super Bowl)** — **고대비 흑백** 여성스포츠 매니페스토(60초·60컷). **스튜디오 하드라이트 포트레이트 ↔ 실제 방송 footage**(체조·WNBA/대학농구·육상·축구·테니스) 고속 교차 + 헤비 슬로모. 카피 withhold 후 **도발→반전 2비트 타이포** `YOU CAN'T WIN.` → `SO WIN.` → 스우시 엔드카드. 음성 VO는 샌드박스 ASR 차단으로 미전사(날조 안 함). 색 제거·실제 footage 신뢰성·타이포 반전 공식 = 컬러/VFX형 광고와 대조 신호.
- 두 entry 모두 **사용자 '모든 프레임 분석' 지시에 따라 전 프레임 개별 판독**(720+1441=2161프레임, 48프레임 단위 분할 에이전트). 컷별 중간프레임+컨택트시트 데이터셋 보존. 추상화: 출연자=익명 유형, 로고 generic, 화면 카피만 verbatim.
- **신규 토큰**: category `IT.ai_product`; industry `it_saas`/`sports`; media `tvc_60s`; vfx `black_and_white`·`high_contrast`·`slow_motion`·`kinetic_typography`·`morph`·`letterbox_cinematic`; technique `provocation_flip`(개념)·`empathy_copy_hook`; copy_strategy `imperative_slogan`·`empathy_to_solution`; concept_derivation `provocation_flip_manifesto`·`everyday_problem_metaphor_product_release`. (keyword-vocabulary.md 반영 권장.)
- ✅ **오디오 전사 완료(둘 다, faster-whisper base.en)**: 모델 다운로드가 40MiB 프록시 컷오프에 막혀, model.bin을 **HTTP byte-range 청크로 우회 다운로드**해 로컬 전사. 012=여성 매니페스토 VO 전수 확보(`You can't [X] / So [X]` → `Whatever you do, you can't win. So win.`, coverage 0.81) → copywriting.lines/audio.narration_lines verbatim. 011=음악 베드+faint 대사뿐(구조적 VO 없음 확인), 카피=화면 ChatGPT 텍스트. 둘 다 transcribed_by=faster_whisper.

## 2026-06-03 추가 (신규 entry 1건)

- **ADV-2026-009 Alma / Tuneface 'NOTHING'S FOREVER'** — **미용 의료기기**(피부 탄력·리프팅) 브랜드필름(20초·16:9). 첫 신규 카테고리 `healthcare_pharma.aesthetic_device`. **아날로그 필름 카메라 뷰파인더/필름스트립 그래픽 + 필름그레인 + 시네마스코프**를 전역 모티프로, **라벤더×머스타드 보색 키네틱 타이포**('TUNEFACE'·'stay the same')와 **매거진 커버 레이아웃**('TUNE FACE / ALMA 01 2026')으로 의료기기를 동경의 에디토리얼 오브제로 격상. 카피 긴장 **'NOTHING'S FOREVER'(영원한 건 없다)↔'stay the same'(본연 유지)**, 효능 카피 '섬세하게 탄탄하게'(음성+자막 동기), 엔딩 **한자/영어 이중 펀 'To 美 Continued → To Me Continued'** + 코퍼레이트 'Alma(For You. For Life.)'. 의료기기 법정 고지(심의번호 32023-010-49-0130) 하단 상시. 셀럽 없음(모델 generic). 전 14컷 recreation_prompts(t2i+i2v).

## 2026-06-02 추가 (신규 entry 2건)

- **ADV-2026-007 신세계 'NEW SANTA / Bye New Santa'** — 카리나 주연 시네마틱 브랜드필름(돌고래유괴단·신우석). 해변 휴양↔어두운 서재(과태료 통지서 개그) 교차, 'Bye New Santa' 타이틀, 영화식 풀 크레딧. 시네마스코프 레터박스·따뜻한 필름 그레이드.
- **ADV-2026-008 전북대학교 '전북대반전'** — **생성형 AI 제작**(오프닝 'AI로 제작' 고지) 헤리티지(한옥)↔첨단/미래(AI·로봇·VR·네온도시) 반전·모핑 + 애너포라 카피('대학의 상식을/교육의 방식을/사람의 인식을') + 클레임(글로컬대학30, 6년 연속 학생 만족도 1위, 피지컬 AI/1조 투자).
- 두 신규 entry는 신스킬(2606021505) STEP4.5.6에 따라 **전 컷 recreation_prompts(t2i+i2v)** 포함. (기존 001~006은 style_prompt 방식 유지.)

### v2 정정 (2026-06-02, 전프레임 고해상도 재검수)
- 007·008은 처음에 저해상 컨택트시트 썸네일로 판독했으나 **전 프레임(1124·1200)을 940px/프레임 몽타주로 shot별 서브에이전트 17개가 전수 재판독**해 정정. 주요: 007 shot2 스마트폰+칵테일(빨간수화기 오독)·올드/뉴 전화 대비·shot7 tilt-up+'only SHINSEGAE'·shot8 정지카드 하드컷; 008 capture_style **ai_generated**(AI 제작 고지)·shot16 한옥→네온도시 모핑·신규 클레임(피지컬 AI/1조 투자). 신규 vfx 토큰 `ai_generated`.

> **중복 처리:** 업로드된 3편 중 **TcmmQmHGvzU(현대 팰리세이드)는 이미 ADV-2026-003**으로 존재해 신규 entry를 만들지 않았다. recreation_prompts까지 보강한 재분석본은 `outputs/palisade_TcmmQmHGvzU_reanalysis_for_ADV-003.json`에 보관(원하면 003 업그레이드용).

## 신규 토큰 (이번 추가, keyword-vocabulary.md 반영 권장)
- category: `retail.department_store`, `education.university`
- product_category: `department_store`, `university`
- technique: `cinematic_brandfilm`
- copy_strategy: `story_led_minimal_copy`
- concept_derivation_pattern: `keyword_reversal_montage`

## 카테고리 다양성 (cross-pollination 자산)
금융 · 자동차(픽업·하이브리드SUV) · 건설부동산 · 유통리테일(H&B·백화점) · 스포츠웨어 · 교육(국립대) · **헬스케어/미용 의료기기**. 한국어 8 + 중국어 1. AI생성/위글 ~ 실사 시네마틱 ~ 키네틱 타이포 ~ 헤리티지+첨단 반전 ~ **아날로그 필름 에디토리얼 뷰티**까지.

## 신규 토큰 (2026-06-03, ADV-009)
- category: `healthcare_pharma.aesthetic_device`
- product_category: `aesthetic_device`
- technique: `analog_film_camera_ui`, `filmstrip_collage`, `magazine_cover_layout`, `editorial_fashionfilm`
- copy_strategy: `double_wordplay`(美↔Me 한자/영어 펀)
- concept_derivation_pattern: `editorial_fashionfilm_beauty`

## 폴더 구조
```
LSB_Ad_Datas/
  entries/   ADV-2026-001~009 .json + *_review.md
  index/     by_<10축>.json + master.json  (_meta.language=en)
  dataset_view.md
```
