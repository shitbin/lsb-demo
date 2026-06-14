# copy_bank — COPYPEDIA 카피 레퍼런스 뱅크

실제 한국 광고 카피 **4,039건**(중복 제거)을 단일 뱅크로 통합. 출처는 COPYPEDIA 월간 아카이브 20개월분(2023-07 ~ 2026-01, 링크는 tvcf.co.kr). `lsb-ad-planner`의 **카피 cross-pollination 입력**으로 쓴다.

## 파일
- `copy_bank.json` — 전체. `_meta` + `index_by_industry`(카운트) + `entries[]`. 각 entry = `industry`(영문 토큰)·`category_kr`·`brand`·`copy`(원문)·`date`·`url`·`src`(월).
- `index_by_industry.json` — `{industry: [entries 인덱스 배열]}` (빠른 추출용).
- `copy_bank.csv` — 사람이 엑셀로 훑어보기용.

## 산업 토큰 매핑 (한글 카테고리 → 영문 토큰)
planner cross-pollination 맵(영문 industry)에 맞추려고 변환해 둠.

| 한글 카테고리 | 영문 토큰 | | 한글 카테고리 | 영문 토큰 |
|---|---|---|---|---|
| 식품/제과 | `fnb` | | 패션/스포츠 | `fashion` |
| 제약/의료/복지 | `healthcare_pharma` | | 자동차/정유 | `automotive` |
| 전기전자 | `home_appliance` | | 생활/가정용품 | `home_living` |
| 정보통신 | `telecom` | | 출판/교육/문화 | `education` |
| 관공서/단체·지자체 | `public_gov` | | 기업PR | `corporate_pr` |
| 금융/보험 | `finance` | | 아파트/건설 | `construction_realestate` |
| 음료/기호식품 | `beverage_alcohol` | | (데이터오류 2건) | `other` |
| 화장품 | `beauty` | | | |
| 서비스/유통/레저 | `retail` | | | |

## 쓰는 법 (planner)
- 카피를 쓸 때 cross-pollination 가중치(**동일 0.2 / 인접 0.5 / 원거리 1.0 / 대조 1.2**)로 **일부러 먼 카테고리의 카피를 끌어와 접근법·구조(device)만 차용 → 새 카피로 변주**. 와우 카피는 동일 카테고리 차용 금지(하드밴).
- `index_by_industry.json`으로 원하는(또는 의도적으로 먼) 산업의 카피 인덱스를 추려 `entries[i]`를 읽는다.

## ⚠ 저작권·사용 경계 (중요)
- 실제 브랜드의 **저작권 있는 카피 모음**이다. **내부 영감용으로만** 쓴다.
- **verbatim(원문 그대로) 재사용 금지**, 이 뱅크 자체의 **재배포 금지**.
- planner STEP 5 표절 유사도 게이트를 반드시 통과시킨다(단어만 바꾼 수준 = 표절).

## 빌드 노트
- 소스: `../006_raw_sources/카피모음 데이터셋/*.xlsx`(COPYPEDIA 20개). 헤더 2변형(`Brand Name`/`Brand`) 정규화, `(brand, copy)` 기준 중복 145건 제거. 빌드일 2026-06-03.
- 미분류 `other` 2건: "판콜 에스"(카테고리칸에 브랜드 오기), "자동차"(→ automotive 의도) — 무시 가능.
