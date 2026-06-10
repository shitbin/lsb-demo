---
name: lsb-ad-planner
description: >
 LSB Production 광고 기획안 생성 스킬. 분석해 쌓아둔 광고 데이터셋(lsb-ad-analyzer가
 만든 JSON entry들)을 입력받아, 카테고리 교차 참조(cross-pollination) 규칙으로 표절 위험 없는
 새 광고 기획안(컨셉·스토리보드·컷리스트·카피·타이포·VFX 방향)을 생성한다. 반드시 다음 상황에서
 사용한다: "이 브리프로 기획안 짜줘", "광고 컨셉 뽑아줘", "데이터셋 기반으로 기획해줘",
 "후보 컨셉 N개 만들어줘", 클라이언트 브리프와 데이터셋을 주며 기획을 요청할 때.
 AI가 후보를 대량 생성하고 사람이 판정하는 분업 구조를 따른다.
---

# lsb-ad-planner — LSB 광고 기획안 생성 스킬

클라이언트 브리프 + 데이터셋을 받아 **새 광고 기획안 후보**를 만든다.
핵심 철학(가이드라인 1.5절): **AI는 "좋다"고 주장하는 후보를 빠르게 대량 생성하고,
사람(디렉터)은 그 후보를 판정만 한다.** 그러니 이 스킬의 출력은 "완성 기획"이 아니라
"사람이 고를 후보들"이다. 사람의 시간을 제작이 아니라 판정에만 쓰게 하는 것이 목적이다.

## 입력
1. **클라이언트 브리프**: 브랜드, 제품, 카테고리, 타깃, 길이(초), 예산, 톤 요청, 필수 포함 요소.
2. **데이터셋**: 연결된 **`LSB_Ad_Datas`**(=`<LIBRARY>`) 안의 **`001_ad_video_dataset/`(=`<DATASET>`)** 의 `entries/` + `index/`. lsb-ad-analyzer가 만든 entry들.
 - 데이터셋은 시간이 쌓일수록 커지는 자산이다(가이드라인 1.4절 '중층 근육'). entry가 많아지면
 **전부 읽어 넣지 말고** STEP 2의 인덱스 검색·랭킹으로 어울리는 상위 N개만 골라 쓴다(규모 불변).

## 스키마·계약 참조
- 이 스킬의 입출력 계약(브리프 dict, cross-pollination 맵, treatment.json 출력, **analyzer→treatment 필드 매핑표**)은 `schema.md`에 있다.
- entry/shots 상세 필드는 `lsb-ad-analyzer/schema.md`, 영문 토큰·KO 별칭은 `lsb-treatment-builder/REFERENCE/keyword-vocabulary.md`.

## 절대 규칙 — Cross-Pollination (가이드라인 4.3절)

클라이언트 카테고리가 X일 때, 데이터셋에서 참조 후보를 다음 **v0 가중치**로 뽑는다.

| 매칭 | 가중치 | 의미 |
|---|---|---|
| 동일 카테고리 (X=X) | 0.2 | 참고만, 최하 우선순위 |
| 인접 (감성·타깃 유사) | 0.5 | |
| 원거리 | 1.0 | 기본적으로 여기서 영감 |
| 대조 (의도적 충돌) | 1.2 | 가장 강하게 끌어옴 |

**와우컷 하드밴**: 가장 임팩트 큰 1~2컷(후크/키/CTA직전)을 만들 때는 **동일 카테고리 출처 0개.** 가중치 0.2가 아니라 완전 차단.

인접/원거리/대조 판정의 **단일 출처는 `schema.md` §3 (영문 industry 기준 cross-pollination 맵)**. 거기 없는 industry는 1.0(원거리) 기본 + entry의 `cross_pollination_tags`(영문) 보조.

## 절대 규칙 — 컨셉 품질 & 브랜드 자산 (2606 세션 학습 · 디렉터 분노 포인트 방지)

이 스킬이 반복해서 까였던 지점들. 위반 시 출력 금지/재작성.

### R1. 안전빵 금지 — 날카로움 게이트 (STEP 3·5 강제)
'레퍼런스 평균내기'는 컨셉이 아니다. 각 후보 컨셉은 반드시 셋을 가진다:
- ⓐ **하나의 ownable 리프레임** — 제품 진실을 비트는 한 수(혜택 나열이 아니라 *관점 전환*).
- ⓑ **입에 붙는 한 줄** — 슬로건/펀치라인(정보 전달이 아니라 *각인*).
- ⓒ **과하지 않되 신선한 비주얼 디바이스** — *누구나 아는데 아무도 안 보여준 디테일* 한 방. 스펙터클·클리셰 금지.

**자동 리젝 신호:** 여러 레퍼런스를 안전하게 섞은 '무난한 평균', 혜택을 나열하는 카피, "본전/이득/절약액" 같은 회계사 말투, 카피·비주얼 어느 쪽도 안 꽂히는 후보, 피하겠다던 카테고리 클리셰를 그대로 쓰는 device(예: '숫자가 0원으로 깎임'). → STEP 5에서 한 줄 슬로건이 *리프레임인지 정보요약인지* 자가판정, 정보요약이면 재작성.

### R2. vibe 단어 해석 주의 — '팝하게/힙하게/감각적/세련되게'
추상 톤 단어를 *특정 미술 양식*으로 단정하지 마라(예: "팝하게" ≠ 팝아트). 먼저 의미를 가른다: "대중적이고 톡톡 튀는 에너지"냐 "특정 아트 스타일"이냐. **기본 해석 = 브랜드 고유 자산(컬러·서체·캐릭터·톤)으로 에너지를 증폭한다.** 모호하면 AskUserQuestion으로 한 번 되묻는다.

### R3. 브랜드 자산 선(先)리서치·고정 (STEP 0.6 선제 웹리서치의 일부)
브리프를 받으면 **컨셉 전에** 브랜드 자산을 확보해 plan에 박는다: 브랜드 컬러(정확 hex)·전용서체·마스코트/캐릭터·톤. 웹검색으로 확인하고, **공식 가이드 대조 권고**를 단다(리브랜딩으로 값이 바뀌었을 수 있음). 자산뿐 아니라 제품 실체·브랜드 톤·경쟁 클리셰까지 = STEP 0.6 전체.

### R4. 브랜드 IP는 내가 생성 금지 — 사용자 에셋 우선
실제 브랜드 **캐릭터·로고·마스코트**는 placeholder로 *그려서* 채우지 않는다. ⓐ 사용자에게 공식 에셋(PNG/JPG) 요청 또는 ⓑ 리서치로 외형·출처 확인. 부득이 시안용이면 'placeholder — 최종 공식 에셋 교체' 명시. 첨부는 **PNG/JPG로 요청**(SVG·벡터는 엉뚱한 레이어만 export돼 깨질 수 있음).

> **★ 사용자 명시 예외 우선 (A4).** 사용자가 "이번엔 성능테스트니 실제 로고/워드마크 써도 된다"처럼 **명시적·반복적으로 허용**하면, 그 세션 한정으로 GENERIC 대신 **사용자 지시를 우선**한다(R4를 이유로 임의 GENERIC 박지 말 것 — 한 번 더 돌리는 사고 A4). 단 '공식 에셋 아님/시안용' 메모는 유지, 모호하면 1회 되물어 확정. R5(한글)도 동일 — 절대규칙이라도 사용자 명시 예외는 그 세션 우선.

### R5. 한국어 카피·나레이션은 한글로만
태그라인·CTA·나레이션 등 모든 한국어는 **한글로** 적는다. **로마자 발음표기 절대 금지**(예: "baedalbi" 금지).

### R6. 역량 단정 금지 — 모델·도구 검증 후 발언
"그 모델/기능 없다"고 단정하기 전에 **전체 목록을 조회해 검증**(한 번 실패한 검색으로 단정 금지). 스킬·사용자가 특정 모델(예: GPT Image 2)을 지정하면 실제 존재를 먼저 확인하고 우선 사용. 모델 능력(예: 오디오 생성 여부)도 실제 파라미터·응답으로 확인 후 말한다.

### R7. 다중 인물·다중 공간은 '명단부터' (2606 세션 A3 학습)
영상에 사람이 둘 이상이거나 공간이 교차(교차편집)하면, 컷을 짜기 *전에* `character_pool[]`(누가 어느 컷)과 `narrative_structure`를 먼저 정의한다. 안 그러면 "주인공이 모든 컷을 다 한다"로 붕괴한다 — A3에서 주인공이 카페에 들어가 직접 결제하는, *트리트먼트와 정반대* 영상이 나온 원인. 컷마다 `subject_identity`로 인물을 못 박고, 화면에 또렷한 인물은 인물별 마스터시트를 따로 둔다(`requires_character_sheets`).

### R8. 산출물의 다운스트림 용도 1줄 명시 (허쉬 세션 A5·A6 학습)
각 산출물(제품시트·키비주얼·컷·카피)을 만들기 전에 **"이게 다음 단계에서 어떻게 쓰이나"를 1줄로 명시**한다. 빠뜨리면 엉뚱한 걸 박는다(A5: 제품 reference 시트에 스펙 텍스트를 박아 i2v reference로 못 씀 / A6: 한국 광고 메인 카피를 영문으로 박음).
- **제품 reference 시트 = 텍스트·치수·스펙표 없는 *순수 비주얼***(영상 i2v reference로 쓰이니까). 스펙은 plan 텍스트에만, 이미지엔 굽지 않는다.
- **화면 메인 카피 = 한글(R5).** 영문은 고유명·로고·브랜드 워드마크만. "영문 캠페인 카피"로 합리화 금지(A6).

### R9. 비싼 단계 전 컨펌 · 도구 호출 예고 금지 (공통 실행 규율)
- **비싼 단계(이미지·영상 생성, PDF 빌드) 전에 종횡비·톤·핵심 스펙을 컨펌**받는다(추론으로 단정 금지 — A12). 값싼 결정점에서 멈추는 게 14컷 갈아엎기보다 싸다.
- **도구를 호출할 거면 "이제 ~하겠다" 같은 예고 텍스트 없이 바로 호출**한다(예고만 하고 실행이 안 따라오면 루프의 씨앗 — 허쉬 A14). 긴 대기는 짧게 쪼개 폴링하지 말고 길게 한 번(영상 렌더는 video-crafter STEP 6 대기 프로토콜).

### R10. 더블(점프컷) 방지 — 컷 문법 게이트 (★ 컷리스트 작성 시 강제)

"더블" = 같은 피사체를 잇는 인접 두 컷의 **사이즈와 앵글이 둘 다 거의 안 변해**, 새 시점이 아니라 같은 그림이 살짝 어긋나 두 번 나온 것처럼 보이는 현상(한국 현장 은어 · 교과서 명칭 = 점프 컷, 30도 법칙 위반). 컷 = "새 시점·새 정보" 선언이다. 변화가 애매하면 시청자는 새 시점이 아니라 *카메라가 순간이동한 오류*로 읽는다. **컷을 했으면 시점이 확실히 바뀌었다는 게 한눈에 보여야 한다 — 컷의 명분 없는 경계는 컷이 아니다.**

**샷 스케일 사다리(7단):** `ECU → CU → MCU(bust) → MS → MLS → FS/LS → ELS`. `framing` 값은 이 사다리로 단계를 센다.

**인접 컷 성립 조건 — 같은 피사체·같은 공간이면 최소 하나 충족:**
1. **샷 사이즈 2단계 이상 점프** — CU→MS ○ / CU→MCU ✗ (1단계는 더블).
2. **카메라 앵글 30도 이상 변화** — `camera_angle`/`camera_facing`이 명확히 다른 값(정면→측면, 아이레벨→로우 등).
3. **피사체·공간·시간 변경** — `subject_identity` 교체, 장소 점프, 시간 점프. (인서트·리액션·장면전환은 이 조건으로 자동 성립.)

**셋 다 미충족이면 그 경계는 hard cut 금지 — 둘 중 하나로 처리:**
- **seamless 전환(기본):** 두 컷을 한 흐름으로 잇고 거리·각도 변화를 컷 내부 카메라 무빙으로 표현 — `transition_in/out`을 `push_in`·`pull_out`·`dolly_through`·`morph`·`match_action` 등 seamless 계열로 지정. (변화량이 작은데 화면을 바꾸고 싶다 = 컷이 아니라 *무빙*이 맞는 상황.)
- **컷 병합:** 정보가 겹치면 한 컷으로 합치고 duration 합산.

**예외(허용되는 의도적 장치):** ⓐ **펀치인/axial cut** — 같은 앵글에서 사이즈만 **2단계 이상** 점프(1단계 펀치인은 그냥 더블) ⓑ **매치컷(match_action)** — 동작 연결이 변화를 가림 ⓒ **의도적 점프컷 연출**(시간경과 몽타주 등) — `notes`에 "intentional jump cut" 명시된 것만.

적용 지점: STEP 4 (B) 컷리스트 작성 시 매 인접 쌍 검사 + STEP 5 (A-3) 자가검사. builder도 Phase 1.1-b에서 같은 기준으로 재검증한다(이중 방어).

## 워크플로

### STEP 0.0 — 데이터셋 resolve (세션 시작 즉시, 크로스플랫폼)

planner 트리거 시 **가장 먼저** 데이터셋 폴더를 런타임 resolve한다. 경로 하드코딩 금지(mac `/Users/...`, win `C:\Users\...` 양쪽).

1. 연결된 `LSB_Ad_Datas` 폴더 = `<LIBRARY>`. **`<DATASET>` = `<LIBRARY>/001_ad_video_dataset`** (그 안에 `entries/`·`index/`·`dataset_view.md`). 그 외 라이브러리 자원: 카피뱅크 `<LIBRARY>/002_ad_copy_bank/`, 우수예시 `<LIBRARY>/003_reference_decks/`, 프로젝트 `<LIBRARY>/004_projects/`.
2. 없으면 `mcp__cowork__request_cowork_directory`로 폴더 요청. 빈 폴더면 analyzer의 dataset_template/를 복사해 시딩.
3. 이후 `entries/`·`index/`는 `<DATASET>` 기준 상대경로. 상세 계약: `schema.md` §0.

### STEP 0 — 첫 대화: 브리프 수집 폼 (AskUserQuestion 인터랙티브)

**사용자가 매번 긴 브리프를 자유 텍스트로 풀어쓰지 않도록 — *폼 형태*로 핵심을 빠르게 수집.** Cowork `AskUserQuestion`으로.

**0.1 첫 질문 묶음 (5개 동시):** 브랜드 / 제품·서비스 카테고리 / 톤·분위기(복수) / 매체·길이 / 비주얼 레퍼런스 유무.
**0.2 두 번째 묶음 (3개):** 타깃(복수) / 필수 포함 요소 / 피해야 할 요소.

> **★ 종횡비는 반드시 명시 질문 (A12 — 추론 금지).** "숏폼이니까 9:16" 같은 추론으로 단정하지 말 것. 매체·길이 질문에 **종횡비(9:16 / 16:9 / 1:1)를 별 보기로** 넣어 받는다. 비싼 이미지·영상 생성 **전에 반드시 확정**(14컷 만들고 갈아엎는 사고 방지). plan에 `aspect_ratio` 박음.
> **★ product_spec_lock (A10 — 제품 불변 스펙 고정).** 실제 제품이 나오는 캠페인은 제품의 *불변 형태 스펙*(그리드 수·비율·각인·소재 — 예 "정확히 3행×4열=12블록, 양각 'HERSHEY'S', 세로비")을 plan에 1회 정의(`product_spec_lock`)하고, **모든 이미지 프롬프트에 verbatim 삽입**(builder가 그대로 박음). 안 박으면 모델이 4×4 등으로 임의 변형(A10 사고).

(질문 보기 항목은 한국어로 보여주되, 응답은 아래 0.3에서 영문 토큰으로 정규화한다.)

**0.3 응답 → 브리프 dict 구성 (값은 영문 토큰):**

```python
brief = {
 "brand": "<응답>", # 고유명사 OK
 "product": "<응답>",
 "industry": "<영문 토큰>", # 예: "finance"
 "product_category": ["<영문 토큰>"],
 "tone": ["<영문 토큰>"], # 예: ["punchy_humor","friendly"]
 "media_format": "<영문 토큰>", # 예: "shortform_landscape_30s"
 "target_demo": ["<영문 토큰>"], # 예: ["mz","early_career"]
 "must_include": "<응답>",
 "must_avoid": "<응답>",
 "visual_ref_attached": True/False,
 "raw_text": "<자유 텍스트(한국어 가능)>"
}
```

**0.4 빠진 정보 추가 질문:** 최대 2~3 라운드. 넘으면 자유 텍스트로.

### STEP 0.5 — 비주얼 레퍼런스 분석 (옵션)

질문 5에서 "있음" + 이미지 첨부 시 진행. 추출은 *시각 시그니처*만(Level 2~3, 픽셀 베끼기 금지): color_palette/color_mood/lighting/composition/subject_type/subject_pose/texture_fx/tone_keywords/anti_referenced. 후속 컨셉의 *영감*으로만, 컷리스트 직접 인용 X. 추출 결과를 사용자에게 컨펌.

> **★ 표면 토큰 말고 '무드의 물리근거'를 정독 (A3 — 양 극단 진동 방지).** 레퍼런스(또는 데이터셋 entry)를 "필름UI·키네틱타이포·매거진" 같은 **결과 라벨(technique/vfx)로만 이해하지 않는다.** 그 룩이 *왜* 그렇게 보이는지의 물리근거를 읽어 룩 디렉션에 박는다:
> - `color_analysis`(palette_hex 정확값·saturation_strategy·contrast_type) · `lighting`(key_direction/hardness/key_to_fill_ratio/color_temp/overall_contrast) · `texture` · `style_prompt`.
> - **`style_prompt`의 형용사를 그대로 인용**한다: "clean digital with **light** film-grain" / "warm low-key" / "desaturated with pop". **"light grain"을 "heavy sepia"로, "warm"을 "dark low-key"로 바꾸지 말 것**(A8·A9: 세피아 떡칠↔어두움↔밝음 3극단 진동의 원인).
> - 데이터셋 entry가 있어도 **무드보드 1장으로 사용자 컨펌**(톤은 글로만 맞추면 두 번 빗나간다 — A8·A9).

### STEP 0.6 — 브랜드·제품 선제 웹리서치 (필수 · R3 포함)

브랜드+제품이 정해지면(STEP 0) **컨셉 생성·데이터셋 검색(STEP 2~3) 전에** 그 브랜드·제품을 **먼저 웹검색**한다. 허락 안 받고 선제적으로(검색은 기본 동작). 모르고 기획하면 제품 진실(`brand_right`)과 차별점이 비고, 컨셉이 붕 뜬다. 사용자는 보통 "어떤 브랜드의 어떤 제품 광고"만 던지므로, 그 한 줄을 받아 곧장 리서치한다.

**무엇을 찾나:**
- **제품·서비스 실체** — 정확히 무엇인지, 핵심 기능·혜택·가격·차별점(= 팔 거리). 수치·혜택·가격은 변동 가능 → `fact_check_flag` + 집행 시 약관 확인.
- **브랜드** — 포지셔닝·브랜드 DNA·톤·기존 광고/캠페인·슬로건·키 메시지("그 브랜드다운" 톤).
- **브랜드 자산(R3)** — 컬러(정확 hex)·전용서체·로고·마스코트/캐릭터. 공식 가이드 대조 권고(리브랜딩 변동).
- **시장·경쟁·클리셰** — 경쟁사·카테고리 관용(피할 클리셰) → `must_avoid` 보강.
- **최근성** — 현재 진행 캠페인·신제품·이벤트. 지식 컷오프 이후일 수 있으니 **반드시 검색**.

**결과 처리:** brief dict에 병합 — `product_facts`(혜택·기능·가격 + 출처) / `brand_assets`(color hex·font·character) / `brand_voice`(톤·슬로건 DNA) / `category_cliches`→`must_avoid`. 출처 기록. 이 결과가 STEP 3 `strategy_spine`의 **`brand_right`·`insight` 근거**가 된다.

**원칙:** 검색 결과는 *근거·영감*으로만. 경쟁사·기존 슬로건을 단어만 바꿔 쓰지 말 것(표절·R1). 브랜드 IP(캐릭터·로고)는 생성 금지·사용자 에셋(R4). 한국어 카피·나레이션은 한글로(R5). 모델·도구 능력은 단정 전 검증(R6).

### STEP 1 — 브리프 정규화 (한국어 → 영문 토큰)

STEP 0의 dict를 `keyword-vocabulary.md`의 KO 별칭표로 영문 토큰화한다.

- "20대 사회 초년생" → `target_demo = ["late20s_early30s", "early_career"]`
- "재밌고 가볍게" → `tone = ["punchy_humor", "friendly"]`
- "기존 시중은행 광고 같지 않게" → `must_avoid = "bank_cliche"`

별칭표에 없으면 가장 가까운 토큰, 신규면 표에 추가. **인덱스가 영문이라 브리프도 영문 토큰으로 맞춰야 hit한다.**

### STEP 2 — 참조 선택 = 인덱스 직접 검색·랭킹 (cross-pollination)

데이터셋은 누적 자산이라 **통째로 안 읽는다.** 인덱스 파일(`<DATASET>/index/by_*.json`)에서 키워드 매칭으로 후보를 뽑아 가중치 적용해 상위 N개만 가져온다. entry가 2개든 300개든 동일하게 작동(규모 불변).

**index_helper를 import하지 않는다.** 인덱스는 평범한 JSON이라 planner가 직접 `json.load`로 읽는다(결합 제거). 인덱스 *쓰기*만 analyzer의 index_helper 담당.

```python
import json, os
AXES = ["industry","product_category","target_demo","media_format","tone",
 "pacing","technique","vfx_keywords","copy_strategy_keywords","concept_derivation_pattern"]

def search(DATASET, **brief_axes):
 """영문 토큰 다축 매칭. return [(entry_id, score, hits)] score=매칭 축 수."""
 matches = {}
 for axis, values in brief_axes.items:
 if axis not in AXES: continue
 if isinstance(values, str): values = [values]
 p = os.path.join(DATASET, "index", "by_%s.json" % axis)
 if not os.path.exists(p): continue
 idx = json.load(open(p, encoding="utf-8"))
 for v in values:
 for eid in idx.get(v, []):
 m = matches.setdefault(eid, {"score":0,"hits":{}})
 m["score"] += 1; m["hits"].setdefault(axis,[]).append(v)
 out = [(e,m["score"],m["hits"]) for e,m in matches.items]
 out.sort(key=lambda x:-x[1]); return out

def load_entry(eid, DATASET):
 return json.load(open(os.path.join(DATASET,"entries","%s.json"%eid), encoding="utf-8"))

def retrieve_references(brief, shot_type, DATASET, n=5):
 hits = search(DATASET, industry=brief["industry"], product_category=brief["product_category"],
 target_demo=brief["target_demo"], tone=brief["tone"],
 technique=brief.get("technique",[])) # 필요 축 추가
 ranked = []
 for eid, idx_score, hits_detail in hits:
 e = load_entry(eid, DATASET)
 cat = (e.get("search_keywords",{}).get("industry") or [None])[0] # 영문 토큰
 if shot_type == "wow_cut" and cat == brief["industry"]:
 weight = 0 # HARD BAN
 elif cat == brief["industry"]:
 weight = 0.2
 elif cat in adjacent_to(brief["industry"]): # schema.md §3 맵
 weight = 0.5
 elif cat in contrast_to(brief["industry"]):
 weight = 1.2
 else:
 weight = 1.0
 brief_match = semantic_match(e.get("inferred_brief",""), brief["raw_text"])
 final = idx_score * weight * (0.7 + 0.3*brief_match)
 ranked.append((eid, final, hits_detail, weight))
 ranked.sort(key=lambda x:-x[1])
 return ranked[:n]
```

**인덱스 검색의 강점 (영문 토큰 정규화):**
- 브리프 "MZ 사회초년생, 펀치 유머" → 정규화 `target_demo=["mz","early_career"]`, `tone=["punchy_humor"]`.
- lookup: `by_target_demo.json["mz"]` + `by_tone.json["punchy_humor"]` → ADV-2026-001 (score 2).
- 가중치: 브리프 industry=finance, entry=finance → 0.2(HARD BAN 아니면 참고). 최종 2×0.2=0.4.
- 사용자가 "20대"라고만 적어도 정규화에서 표준 토큰으로 → 같은 hit. **키워드 변화에 강함.**

- **무엇을 왜 뽑았는지 명시**(예: "핀테크 브리프인데 스트리트패션 광고의 컷 리듬을 끌어옴 — 대조 1.2, score 0.9").
- 데이터셋이 클수록 더 잘 맞는 원거리/대조 카드가 나올 확률↑(데이터셋=근육).
- (인프라: 규모 커지면 Postgres+pgvector RAG로. 지금은 인덱스 직접 읽기 — "전부 읽기"가 아니라 "골라 오기" 동작 유지.)

### STEP 2.5 — 데이터 활용

**:** production_signature·global_layout·typo_motion·audio를 cross-pollination 대상으로 끌어와 새 연출 제안. 나레이션 카피의 리듬·후렴 구조 참고하되 원문을 단어만 바꾸지 말 것.

** (analyzer STEP 5.5):**
- `inferred_creative_thinking`(7단계) — 참조가 *어떤 사고로 도출됐는지* 직접 읽기(결과만 가진 보다 강한 retrieval 신호).
- `search_keywords`(10축, 영문) — 브리프 직접 매칭.
- `inferred_brief` — 브리프 vs entry 추정 brief 의미 매칭.
- `cross_pollination_tags`(영문 adjacent/distant/contrast) — entry 자체 라벨. 가중치 보조.
- `concept_derivation_pattern`(영문) — 사고법 분류명.

** 시각 필드:** 참조 entry의 `visible_elements·texture·lighting·color_analysis·style_prompt`와 `recreation_prompts`(t2i/i2v)는 비주얼 톤 *영감*으로 활용(픽셀 복제 금지). builder로 carry-through(STEP 4 B).

**confidence:** `inferred`면 추정값임을 알면서 사용(직접 인용 금지, 영감만). `human_verified`면 더 신뢰.

**사고법 카탈로그(`lsb-treatment-builder/REFERENCE/keyword-vocabulary.md`):** 12 사고법 카탈로그를 데이터셋 빈약 시/보강용 시드로. 50+ entries 쌓이면 cross-pollination 우선.

### STEP 3 — 후보 컨셉 5안 생성 (A~E)

서로 **질적으로 다른** 컨셉 5개(A·B·C·D·E). 각 컨셉마다 *모두* 출력:

**(A)** 한 줄 컨셉 + creative_device + concept_derivation_pattern(영문 토큰, 핸드북 12개 중 매칭 또는 신규).
**(B) 7단계 인지 경로 + 기획 논리 척추 (필수)**
- `client_perception_path`(감정 경로): insight/persona/moment/product_role/punchline/differentiator/brand_fit_one_liner.
- `strategy_spine`(비즈니스 논증 — builder STRATEGY 섹션의 *원천*): `brief`(과제) / `insight`(+`evidence[]`: 관찰·데이터·뉴스·타깃 발화 근거) / `strategy`(한 수) / `concept_rationale`(이 컨셉을 인사이트에서 *어떻게* 도출했나 — 점프 금지) / `brand_right`(왜 이 브랜드여야 하나 = product truth) / `payoff`(기대효과·평가기준 역산). 척추·매핑 틀: `lsb-treatment-builder/REFERENCE/deck-logic.md` §1.
- **컨셉(한 줄 컨셉·creative_device)은 반드시 `strategy_spine.insight`에서 도출**되어야 한다 — 인사이트 없이 컨셉부터면 재작성. one-liner만 박지 말고 evidence·도출 논리를 붙인다.
- brief(과제)·payoff(평가기준·KPI·공모전 배점)가 사용자 입력에 없으면 STEP 0.4 추가 질문으로 받아 채운다.
- 위 둘(인지 경로 + strategy_spine) 중 하나라도 비면 컨셉 출력 *금지*(builder가 받아 STRATEGY를 렌더해야).
**(C)** narrative_arc(Level 3 추상화 — 구조 베끼기 X, 원리만) + **`narrative_structure`**(서사 구조 enum: `linear_continuous` 한 공간 연속 동선 / `cross_cutting_montage` 같은 시간·다른 공간 교차 / `parallel_narrative` 두 인물 평행 / `nested_flashback` 시간 점프) + 톤·무드 키워드 + pacing_curve + music_tempo_curve.
**(C-2) 등장인물 명단 `character_pool[]` (인물 2명 이상 또는 교차편집이면 필수):** 컷을 짜기 *전에* 인물을 먼저 정의한다. 각 항목 = `id`(자유 문자열, 예 `protagonist_main`·`cafe_customer_A`·`cafe_barista`; 군중은 예약값 `background_crowd`, 인물 없는 환경컷은 `none_environment`) · `description`(한 줄) · `appears_in_cuts[]`. **이게 비면 다중 인물 영상이 '주인공이 모든 컷을 다 한다'로 붕괴**(A3 사고: 주인공이 카페 들어가 결제 — 트리트먼트 정반대). 예: `{"id":"protagonist_main","description":"횡단보도의 주인공","appears_in_cuts":[1,2,5,6,8,9,10,11,12]}`, `{"id":"cafe_customer_A","description":"카페에서 결제하는 다른 손님","appears_in_cuts":[3,7]}`.
**(D)** 6대 디렉터 키워드(선택) — 마침표로 끝나는 짧은 구 6개.
**(E)** 카피 시드 — tagline·CTA·핵심 라인 + 핸드북 12 카피 패턴 매칭.
- **카피 cross-pollination (copy_bank · ★ 기계적 절차 — 건너뛰기 금지):** 카피 시드를 쓰기 *전에* `<LIBRARY>/002_ad_copy_bank/`(COPYPEDIA 실제 카피 4,039건 · 2023-07~2026-01)를 **코드로** 읽는다. **결합 계약:** `index_by_industry.json` = `{industry(영문 토큰): [정수 인덱스 배열]}` — 그 정수가 `copy_bank.json`의 **`entries[i]` 위치**다(각 항목: `industry`·`category_kr`·`brand`·`copy` 한국어 원문·`date`). 파일이 1MB급이므로 **통째 Read 금지** — 아래처럼 인덱스로 골라 코드로만 추출:

```python
import json, os, random
CB = os.path.join(LIBRARY, "002_ad_copy_bank")
idx = json.load(open(os.path.join(CB, "index_by_industry.json"), encoding="utf-8"))
entries = json.load(open(os.path.join(CB, "copy_bank.json"), encoding="utf-8"))["entries"]
# 가중치(동일 0.2/인접 0.5/원거리 1.0/대조 1.2 — schema.md §3 맵)로 '일부러 먼' 산업 2~3개 선택
far = ["fashion", "public_gov"]  # 예: 브리프 industry=finance일 때
picks = [(i, entries[i]) for ind in far for i in random.sample(idx[ind], k=min(15, len(idx[ind])))]
```

 산업당 10~20건 × 2~3개 산업만 샘플링해 *접근법·구조(device)만* 차용, **새 카피로 변주**한다. 와우 카피는 동일 카테고리 차용 금지(하드밴). ⚠ **원문 verbatim 재사용·단어만 바꾸기 금지** — copy_bank는 *영감*이지 복붙 소스가 아니다. **기록 의무:** 각 카피 시드에 `copy_refs[]` = `[{bank_index, industry, brand, device_borrowed}]`를 붙이고 "원문 device → 새 카피" 변주 로그 1줄을 남긴다(STEP 5 (B)에서 검사). 뽑은 시드는 반드시 STEP 5 (A) 표절 유사도 게이트를 통과시킨다. **생략은 카피뱅크 폴더가 없을 때만** — 생략하면 그 사실과 사유를 출력에 명시한다.
**(F)** 추적 — 참조 entry ID + 차용 필드/시그니처 명시(예: "ADV-2026-001#shot5의 풍선타이포 *형태만* 차용, 카피 새로 작성").

**서로 벌리기:** 톤 축 / 메커니즘 축(셀럽·의인화·메타포) / 사고법 축 / 매체 축 / 서사 구조 축에서 의도적 분리 — 5안이 같은 축에 몰리면 안 된다. 변주면 가치 없음.

**재생성 요청 처리:** 사용자가 "다 마음에 안 든다 — 새 후보"를 고르면, **이전 라운드 5안과 질적으로 다른 새 5안**을 만든다(같은 사고법·같은 메커니즘 재탕 금지, cross-pollination 출처도 갈아끼움). 직전 라운드에서 사용자가 무엇을 거른 셈인지 1줄로 추정해 새 라운드의 벌리기 축에 반영한다. 라운드 횟수 제한 없음.

**(G) 날카로움 게이트 (R1 필수):** 각 컨셉이 ⓐ ownable 리프레임 ⓑ 입에 붙는 한 줄 ⓒ 절제된 신선 비주얼 디바이스를 갖췄는지 확인. '레퍼런스 평균내기'·혜택 나열·회계사 카피·카테고리 클리셰 device면 컨셉 출력 *금지*, 재작성.

**(H) 한 장면 즉시 이해 게이트 (Q7):** 각 컨셉을 *제품이 주인공인, 촬영/렌더 가능한 한 장면*으로 묘사할 수 있나? **설명을 붙여야만 이해되는 순수 비유 단독**(예: 가상인간=물의 의인화만)은 통과 금지. ※ cross-pollination의 대담·추상 *장치 자체는 허용* — 핵심은 '추상 금지'가 아니라 *그 장치가 제품 주인공 + 한 장면으로 번역됐는가*. 번역이 안 되면 구체 장면으로 교체.

**(I) 간이 컷 구성 — 후보마다 필수 (★ 컨셉만 던지기 금지):** 각 후보는 *그 컨셉이 실제 영상에서 어떻게 흐르는지*가 보여야 고를 수 있다. 후보마다 **간이 컷리스트**를 붙인다 — 컷 수는 STEP 4의 길이별 밴드 준수(15초 8~11 / 30초 14~21 …), 컷마다 4필드: `cutNumber` · `duration`(예 "0-3초") · `scene`(장면 한 줄 — 누가 어디서 무엇을) · `caption`(화면 자막/카피, 없으면 "") · `voiceover`(**V.O/NA 한국어 라인** — 그 컷에서 들리는 말, 없으면 ""). 한국어는 한글로(R5). R10 더블 게이트를 간이 컷리스트에도 적용(인접 컷 변화량). 이미지 프롬프트·내부 토큰은 넣지 않는다(상세 30+필드는 선택된 1안의 STEP 4에서). 이 간이 컷리스트가 그대로 외부(script_options의 cuts[])로 나간다.

### STEP 4 — 선택된 1안 상세화 (treatment-builder 입력 스키마와 1:1 정렬)

STEP 4 출력은 그대로 builder가 받아 동작하는 *완전한 입력*. **analyzer→treatment 키 변환은 `schema.md` §5 매핑표를 따른다**(예: total_duration→total_duration_sec, typography→typography_global, vfx→vfx_global, inferred_creative_thinking→client_perception_path).

builder 입력 스키마(`lsb-treatment-builder/scripts/cut_template.json` + `treatment_global_template.json`)와 1:1 정렬.

**(A) 글로벌 메타 (treatment_global_template 동일 키):** brand·product·target_demo / total_duration_sec·shot_count·fps·aspect_ratio·hook_position_sec·cta_position_sec / narrative_arc·pacing_curve·music_tempo_curve·wow_cut_index[]·creative_device / production_signature.* / global_layout.* / recurring_motifs[] / typography_global.* / vfx_global.* / copywriting.* / **client_perception_path(7단계 감정, STEP 3 B 그대로)** / **strategy_spine(기획 논리 6필드 brief·insight+evidence·strategy·concept_rationale·brand_right·payoff, STEP 3 B 그대로 — builder가 STRATEGY 섹션으로 렌더)** / **narrative_structure(STEP3 (C))** / **character_pool[](인물 2명 이상 또는 교차편집이면 STEP3 (C-2) 그대로)** / audio_intent.bgm/narration.

**(B) 컷별 풀필드 (cut_template.json 동일 키):**
- 식별: index, no, duration, framing, function
- 인물·동작: **subject_identity**(이 컷의 인물 = character_pool의 id, 또는 background_crowd/none_environment — 다중 인물이면 필수), subject_position, subject_action, subject_motion, pose_description, gaze, eye_contact_effect
- 카메라: camera_motion, camera_motion_intensity, camera_angle, camera_facing, shot_scope, camera_effect_local, motion_blur
- 리듬·트랜지션: intra_cut_rhythm, transition_in, transition_out
- 소품·세트: props[], prop_motion, prop_semantics
- 컬러: color_mood, color_palette[], color_intent
- 타이포·자막: copy_overlay, layout_grid, subject_typo_layout, typo_motion, typo_color_strategy
- VFX: vfx_in_shot[], vfx_intensity_local, vfx_in_board_prompts
- 오디오: audio_intent.sfx / narration_line / bgm_change / silence
- 시각 인벤토리: visible_elements, texture, lighting, color_analysis, style_prompt
- 프레임 복제: **recreation_prompts** (t2i_start_frame·t2i_negative·i2v_motion·i2v_params·fidelity_note)
- 메타: wow_cut, fact_check_flag, notes, source_refs[]

> 시각 인벤토리·recreation_prompts는 참조 entry의 같은 필드를 *영감*으로 끌어와 새 컷용으로 작성. **자막·카피 원문은 보존**, 셀럽 *얼굴 사진복제*·실제 *로고 마크*만 generic(초상·상표). 픽셀 복제 금지.

**(C) 트랜지션 인벤토리 (transition_template.json):** no, from_cut, to_cut, type, direction, **`direction_observer_view`**(위에서 본 카메라 회전 + 그 결과 화면 streak 방향을 *둘 다* 명시: 카메라 좌→우면 세상 streak 우→좌. A3 whip pan 방향 혼선 방지), duration_sec, **single_canvas 자동 판단**(whip_pan/morph/match_action/push_in/pull_out/360_spin/dolly_through면 true), motion_blur_intensity, lighting_morph, narrative_role, audio_note. **교차편집(`cross_cutting_montage`)이면 트랜지션이 *공간 점프*임을 명시**(연속 동선 아님).

**(D) 카피 초안:** 데이터셋 카피 *감각*은 참고하되 원문을 단어만 바꾸지 말 것(표절). cross-pollination으로 다른 카테고리 표현 끌어와 새로. 핸드북 12 카피 패턴 매칭 명시.

**길이·컷수 = 톤/장르별 페이싱으로 결정 (Q5 · 블랭킷 숫자 금지).** 역동·펀치 톤이면 1~3초 빠른 다컷, 럭셔리·감성이면 소수 롱컷. 길이별 권장 밴드: 15초 8~11컷 / 30초 14~21컷 / 45초 21~55컷 / 60초는 여유. 인접 컷은 화면크기·동작·장소가 서로 달라야 하고 같은 동작 반복은 최소화한다. **매 인접 쌍에 R10 컷 문법 게이트 적용** — 같은 피사체·공간이면 ①사이즈 2단계+ ②앵글 30도+ ③피사체/공간/시간 변경 중 하나는 충족, 아니면 hard cut 금지(seamless 전환 또는 병합 — R10). (캠페인별 학습은 일반 규칙과 분리 — 예 "마시기 1회"는 그 세션 메모지 보편 규칙 아님.) 길이·종횡비가 브리프 사양(매체)에 맞는지 자가검증.

### STEP 5 — 자가검사 (출력 전 필수)

**(A) 표절 자가검사:** 시각·서사 유사도, narrative_arc, 카피 구조, 타이포 패턴, VFX 시그니처, creative_device 직접 매칭. 임계: <0.50 통과 / 0.50~0.65 경고 / 0.65~0.80 재생성 권고 / >0.80 차단 / **동일 카테고리 >0.60 차단**. 와우컷이 동일 카테고리와 닮으면 무조건 재생성.

**(A-2) 날카로움 자가검사 (R1):** 한 줄 슬로건이 *리프레임인가 정보요약인가* / 비주얼 device가 *클리셰('숫자 0원으로 깎임' 류)인가 신선한가* / 카피·비주얼이 실제로 꽂히나. 셋 중 하나라도 약하면 출력 전 재작성. ('무난한 평균'은 통과 아님.)

**(A-3) 더블(점프컷) 자가검사 (R10):** 컷리스트의 **모든 인접 쌍**을 훑어, 같은 피사체·같은 공간인데 ①샷 사이즈 2단계 미만 ②앵글 변화 30도 미만 ③피사체/공간/시간 동일 — 셋 다 해당하면 **더블 위반**. `transition_in/out`을 seamless 계열로 바꾸거나 컷을 병합해 수정 후 재검사(예외는 R10 ⓐⓑⓒ — 의도적 점프컷은 notes 명시된 것만 통과). 위반이 남아 있으면 출력 금지.

**(B) 스키마 완전성:** 7단계 인지 경로 7항목 + **strategy_spine 6필드(brief·insight+evidence·strategy·concept_rationale·brand_right·payoff)** / 글로벌 필수(brand·product·target_demo·total_duration_sec·aspect_ratio·narrative_arc·pacing_curve) / 컷 필수(index·no·duration·framing·function·intra_cut_rhythm·transition_in/out) / 자막 컷에 copy_overlay·layout_grid·typo_motion / VFX 컷에 vfx_in_shot·vfx_intensity_local·vfx_in_board_prompts / 트랜지션 single_canvas 표시 / **다중 인물·교차편집이면 character_pool[]·narrative_structure·각 컷 subject_identity 필수** / **카피뱅크(`002_ad_copy_bank`) 연결 시 카피 시드에 `copy_refs[]` 필수**(STEP 3 (E) — 미참조면 사유 명시 없이는 미통과) / **5안 모드면 후보마다 (I) 간이 컷리스트**(컷수 밴드·4필드·V.O/NA 라인) 포함. 빠지면 출력 *금지*.

**(C) 논리 게이트 (`lsb-treatment-builder/REFERENCE/deck-logic.md` §3):** strategy_spine가 (1) 컷 0장으로도 "왜 이 광고인지" 한 문장 답되나 (2) 컨셉이 인사이트에서 도출 (3) 브랜드를 경쟁사로 치환 시 말 안 되나(정당성) (4) 평가기준 각 항목에 논리가 닿나 (5) 비트가 "그래서/즉"으로 연결 — 실패 시 보강 후 재출력.

### STEP 6 — 출력 + 타율 기록 슬롯

**(A) 두 모드:** ① 5안 모드(A~E 마크다운 — 각 안에 STEP 3 (I) 간이 컷리스트 포함, 1안 고르면 STEP 4 / "다 별로" 선택지로 새 5안 재생성 가능). ② 1안 상세 모드(마크다운 + JSON 동시).
**(B) treatment-builder 입력 형식:**
```json
{ "global": { /* treatment_global_template */ }, "cuts": [ /* cut_template 배열 */ ], "transitions": [ /* transition_template 배열 */ ] }
```
이 JSON 그대로 builder Phase 0 입력. 사용자가 *수정 없이* builder 트리거 가능해야 합격.
**(B-2) 인물 시트 필요 플래그 `requires_character_sheets[]`:** character_pool 중 *화면에 또렷이 나오는* 인물마다 `{id, priority(critical/high), exists_in_session(bool)}`. builder는 `exists_in_session:false`인 인물의 마스터시트를 먼저 생성해 그 인물 컷 reference로 쓴다. 군중·엑스트라(`background_crowd`)는 시트 불필요.
**(C) 타율 기록 슬롯:** "생성 후보 수 / 통과 수 / 타율"(사람이 채움, 가이드라인 9.1절).
**(D) 추적 메타:** source_refs[] + copy_refs[](카피뱅크 출처, STEP 3 (E)) + 매칭한 사고법·카피 패턴 + 사람 판정 결과 기록 권장.

## 사람(디렉터)이 하는 일 — AI가 침범하지 말 것
- 최종 컨셉 선택(미적 판정)은 사람. 시대감각 판단도 사람.
- AI는 후보를 빠르게 많이 + 표절 안전하게 줄 뿐, 고르지 않는다.

## 하지 말 것
- 데이터셋 카피를 단어만 바꿔 출력 금지. 와우컷에 동일 카테고리 출처 금지.
- "완성됐다"고 단정 금지 — 출력은 사람이 판정할 후보다.
- 데이터셋이 비었으면 먼저 lsb-ad-analyzer로 entry를 쌓아야 한다고 알린다.
- 브리프 정규화·인덱스 키는 **영문 토큰**(KO 별칭표 경유). 한국어로 lookup 금지.
- **(R1)** '레퍼런스 평균내기'·혜택 나열·회계사 카피로 무난한 후보 내기 금지 — 리프레임·꽂히는 한 줄·신선한 device 없으면 재작성.
- **(R2)** '팝하게' 등 추상 톤어를 특정 아트 양식으로 단정 금지 — 의미 확인 후 브랜드 자산으로 해석.
- **(R4)** 실제 브랜드 캐릭터·로고·마스코트를 placeholder로 생성 금지 — 사용자 에셋(PNG/JPG) 요청/리서치.
- **(R5)** 한국어를 로마자 발음으로 표기 금지(한글만).
- **(R6)** 모델·기능이 "없다/안 된다"고 단정 금지 — 전체 목록·실제 응답으로 검증 후 발언, 지정 모델(GPT Image 2 등) 우선 확인.
- **(R10)** 같은 피사체·공간의 인접 컷을 1단계 사이즈 변화·30도 미만 앵글로 hard cut 금지 — 더블(점프컷). 변화량이 부족하면 cut이 아니라 seamless 전환·병합이다.

---
## 사고법 카탈로그 — 사용 가이드
`lsb-treatment-builder/REFERENCE/keyword-vocabulary.md` 참조: 11 카테고리 / 12 사고법 / 12 카피 / 6대 디렉터 키워드 / 제품×비주얼 코드 매핑 / Runway / 광고주 협의 흔적 / 8 특수 패턴 / 페이지 구조.
직접 참조: ① 데이터셋 빈약(<10) 시 시드 ② 카테고리 결정 ③ 컨셉 도출 ④ 카피 ⑤ 광고주 협의 흔적. 50+ entries면 cross-pollination 우선.

---
## STEP 0의 폼이 왜 첫 단계인가 (UX)
세션 켜자마자 긴 자유 텍스트 브리프를 싫어함. 폼이 5초 안에 핵심을 받고 자유 텍스트는 옵션. 5분 핑퐁을 1분으로 압축. 사용자 시간 = 가치.

---
*버전: lsb-ad-planner_2606101200 · 2026-06-10 KST. (_2606101200 = **5안 체제 + 간이 컷 구성 필수** — STEP 3 후보 3안→5안(A~E)·벌리기 5축·재생성 요청 처리(이전 라운드와 질적 분리), STEP 3 (I) 후보마다 간이 컷리스트(컷수 밴드·cutNumber/duration/scene/caption/voiceover V.O·NA 한국어 라인) 필수 — script_options cuts[]로 직결, STEP 5 (B)·STEP 6 (A) 연동.) 이전 _2606101100 = **STEP 3 (E) copy_bank 실배선 수리** — 그동안 이름만 참조되고 결합 계약이 없어 실제로 안 읽히던 문제: `index_by_industry.json`{industry: [정수 인덱스]} → `copy_bank.json` `entries[i]` 결합 계약 + 추출 코드 명시(1MB 통째 Read 금지·먼 산업 2~3개 × 10~20건 샘플링), 카피 시드 `copy_refs[]` 기록 의무 + STEP 5 (B) 검사·STEP 6 (D) 추적 연동, 생략은 카피뱅크 부재 시만(사유 명시). schema.md §0 카피뱅크 계약 추가. _2606101000 = **R10 더블(점프컷) 방지 컷 문법 게이트** — 샷 스케일 7단 사다리(ECU→CU→MCU→MS→MLS→FS/LS→ELS), 같은 피사체·공간 인접 컷 성립 조건(사이즈 2단계+ / 앵글 30도+ / 피사체·공간·시간 변경 중 1), 미충족 시 hard cut 금지 → seamless 전환·병합, 예외(펀치인 2단계+·매치컷·의도적 점프컷 notes 명시) + STEP 4 인접 쌍 검사 + STEP 5 (A-3) 자가검사 + builder Phase 1.1-b 이중 방어.) 이전 lsb-ad-planner_2606041500 · 2026-06-04 15:00 KST. 변경 내역은 적용방법.md 참조. (_2606041500 = **허쉬 세션 사후분석 반영**: STEP 0.1 종횡비 명시 질문(A12)·product_spec_lock(A10) · STEP 0.5 무드 물리근거 정독·style_prompt 형용사 인용·무드보드 컨펌(A3·A8·A9) · R4 사용자 명시 예외 우선(A4) · R8 산출물 다운스트림 용도 1줄(A5·A6) · R9 비싼 단계 전 컨펌·도구 예고 금지(A12·A14) · analyzer panel_layout `layered_collage` 인지. _2606032200 = 라이브러리 폴더 재구성 — `<DATASET>`=연결폴더(`<LIBRARY>`)/001_ad_video_dataset · copy_bank→`<LIBRARY>/002_ad_copy_bank`. _2606022203 = STEP 0.6 브랜드·제품 선제 웹리서치. 신규 _2606032044 = **다중 인물·교차편집 지원(A3 학습)**: R7 + STEP3 (C) narrative_structure·(C-2) character_pool[]·(H) 한 장면 즉시이해 게이트(Q7) + STEP4 글로벌에 narrative_structure·character_pool·컷별 subject_identity·트랜지션 direction_observer_view + 톤별 페이싱(Q5, 블랭킷 컷수 폐기) + STEP6 (B-2) requires_character_sheets + STEP5 완전성검사 갱신. _2606032130 = STEP3 (E) **카피 cross-pollination**(`<LIBRARY>/002_ad_copy_bank/` COPYPEDIA 4천+ 실제 카피 — 원문 보존·industry 영문 라벨 — 먼 카테고리 카피를 영감으로 새 카피 변주, verbatim 금지·표절 게이트 통과).)*
