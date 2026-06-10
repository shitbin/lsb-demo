# LSB ad-planner 입출력 스키마 (planner 전용 · lsb-ad-planner_2606021645)

> 버전: lsb-ad-planner_2606021645 · 2026-06-02 16:45 KST. planner가 소유하는 것만 정의: 브리프 입력 · cross-pollination 맵 · treatment.json 출력 · analyzer→treatment 매핑표. entry/shots 상세는 lsb-ad-analyzer/schema.md 참조(복제 안 함).

---

## 0. 데이터셋 resolve 계약 (크로스플랫폼 — mac/Win 공용)

planner는 세션 시작 시(STEP 0) 데이터셋 폴더를 **런타임에 resolve**한다. 절대경로 하드코딩 금지.

- 연결 폴더 `LSB_Ad_Datas` = `<LIBRARY>`. **`<DATASET>` = `<LIBRARY>/001_ad_video_dataset`** — 그 안에 `entries/`, `index/`, `dataset_view.md`. (카피뱅크 `<LIBRARY>/002_ad_copy_bank/`, 우수예시 `<LIBRARY>/003_reference_decks/`.)
- **카피뱅크 계약 (`<LIBRARY>/002_ad_copy_bank/` · STEP 3 (E)의 입력):** `copy_bank.json` = `{_meta, index_by_industry(카운트), entries[]}` — 각 entry: `industry`(영문 토큰)·`category_kr`·`brand`·`copy`(한국어 원문 verbatim)·`date`·`url`·`src`. `index_by_industry.json` = `{industry: [정수 인덱스 배열]}` — **그 정수로 `entries[i]` 접근**(빠른 추출용). `copy_bank.csv`는 사람 열람용(스킬은 안 읽음). 1MB급 — 통째 Read 금지, 인덱스로 골라 코드 추출만(SKILL.md STEP 3 (E) 코드). 산업 토큰 16종·한글 매핑은 `002_ad_copy_bank/README.md`.
 - mac 예: `/Users/<id>/Desktop/LSB_Ad_Datas` · Win 예: `C:\Users\<id>\Desktop\LSB_Ad_Datas`
- resolve 순서: (1) 연결된 `LSB_Ad_Datas`=`<LIBRARY>`, `<DATASET>`=`<LIBRARY>/001_ad_video_dataset`(entries/+index/ 그 안) → (2) 없으면 `request_cowork_directory`로 요청 → (3) 빈 폴더면 스킬의 `dataset_template/`를 복사해 시딩.
- 이렇게 얻은 **절대경로 = `DATASET`**. 이후 모든 경로는 `DATASET` 기준 상대경로(`entries/`, `index/`)로 다룬다.
- 파이썬 경로 결합은 `os.path.join`(슬래시 직접 박기보다 안전). 문서·예시의 `entries/`·`index/`는 양 OS 공통 표기.
- 이 한 폴더가 **중앙 라이브러리**다(프로젝트마다 새로 만들지 않음). 누적 자산이라 세션마다 같은 폴더를 연결한다.

---

## 1. 브리프 입력 스키마 (STEP 0 폼 결과)

`AskUserQuestion` 폼 응답을 다음 dict로 정규화. 값은 **영문 토큰**(keyword-vocabulary.md), 한국어 응답은 KO 별칭표로 매핑.

```python
brief = {
 "brand": str, # 자유 텍스트(고유명사 OK)
 "product": str,
 "industry": str, # 영문 토큰 1개 (예: "finance")
 "product_category": [str], # 영문 토큰
 "target_demo": [str], # 영문 토큰 (예: ["mz","early_career"])
 "media_format": str, # 영문 토큰 (예: "shortform_landscape_30s")
 "tone": [str], # 영문 토큰 (예: ["punchy_humor","friendly"])
 "must_include": str, # 자유
 "must_avoid": str, # 자유
 "visual_ref_attached": bool,
 "raw_text": str # 사용자 자유 서술(한국어 가능)
}
```

**정규화:** 한국어 브리프 → `keyword-vocabulary.md`의 KO 별칭으로 영문 토큰 치환.
예: "MZ 사회초년생" → `target_demo=["mz","early_career"]`, "재밌고 가볍게" → `tone=["punchy_humor","friendly"]`.

---

## 2. 검색 계약 — 인덱스 직접 읽기 (index_helper import 불필요)

인덱스(`index/by_<axis>.json`)는 평범한 JSON이라 planner가 **직접 읽어** 매칭한다. (analyzer의 `index_helper.py`를 import하지 않는다 — 그 파일은 analyzer 쓰기 전용.)

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
```

entry 본문이 필요하면 `os.path.join(DATASET,"entries","%s.json"%eid)`를 json.load. `master.json`으로 brand/title/category_primary 빠른 조회 가능.

---

## 3. Cross-pollination 카테고리 맵 (영문 industry 기준)

매칭 가중치: **동일 0.2 / 인접 0.5 / 원거리 1.0 / 대조 1.2**. 와우컷은 동일 카테고리 **0 (HARD BAN)**.
판정 기준은 entry의 `search_keywords.industry`(영문 토큰). 아래에 없는 산업은 `1.0`(원거리) 기본값 + entry의 `cross_pollination_tags`를 보조로 사용.

| industry (X) | adjacent (0.5) | contrast (1.2) |
|---|---|---|
| finance | insurance, telecom, it_saas | sportswear, fnb, public_gov |
| automotive | mobility, luxury, construction_realestate | beauty, fnb, public_gov |
| construction_realestate | finance, luxury, home_appliance | sportswear, fnb, content_ott |
| retail | ecommerce, fnb, beauty | industrial_b2b, automotive, finance |
| sportswear | sports, fashion, beauty | finance, construction_realestate, public_gov |
| telecom | it_saas, content_ott, finance | luxury, construction_realestate, fnb |
| fashion | beauty, luxury, content_ott | industrial_b2b, automotive, finance |
| fnb | beverage_alcohol, retail | luxury, automotive, industrial_b2b |
| beauty | fashion, retail, healthcare_pharma | industrial_b2b, automotive, sports |
| public_gov | healthcare_pharma, education | luxury, fashion, automotive |

> 나머지 조합은 `1.0`(원거리). 데이터셋이 커지면 entry별 `cross_pollination_tags`(adjacent/distant/contrast)가 이 표를 보강·대체한다.
> 각 entry의 `cross_pollination_tags`도 이번 버전부터 영문 토큰 권장(현재 데이터에는 한국어 서술이 남아 있을 수 있음 — 보조 신호로만 사용).

---

## 4. treatment.json 출력 계약 (builder Phase 0 입력)

planner STEP 6의 1안 상세 출력은 다음 JSON. builder가 **수정 없이** 받는다.

```json
{ "global": { /* §4.1 */ }, "cuts": [ /* §4.2 */ ], "transitions": [ /* §4.3 */ ] }
```

- §4.1 global = `lsb-treatment-builder/scripts/treatment_global_template.json` 키와 1:1.
- §4.2 cuts[] = `lsb-treatment-builder/scripts/cut_template.json` 키와 1:1 (** 시각 인벤토리 5축 포함** — §5 매핑표 참조).
- §4.3 transitions[] = `lsb-treatment-builder/scripts/transition_template.json` 키와 1:1.

필수 완전성(빠지면 출력 금지): global의 `client_perception_path` 7항목 + **`strategy_spine` 6필드(brief·insight+evidence[]·strategy·concept_rationale·brand_right·payoff)**, `brand/product/target_demo/total_duration_sec/aspect_ratio/narrative_arc/pacing_curve`; 각 cut의 `index/no/duration/framing/function/intra_cut_rhythm/transition_in/out`. (`strategy_spine`은 builder가 STRATEGY 섹션으로 렌더 — `lsb-treatment-builder/REFERENCE/deck-logic.md` §1.)

---

## 5. analyzer entry → treatment 필드 매핑표 (핵심 — 드리프트 방지)

analyzer entry(분석 스키마)와 treatment(제작 스키마)는 **키 이름이 다르다.** planner가 번역자다.
(entry 필드 정의: `lsb-ad-analyzer/schema.md`. treatment 필드: builder의 template json들.)

### 5.1 글로벌

| analyzer entry | → treatment global | 비고 |
|---|---|---|
| `total_duration` | `total_duration_sec` | `_sec` 접미 |
| `hook_position` | `hook_position_sec` | |
| `cta_position` | `cta_position_sec` | |
| `shot_count_corrected`(있으면) / `shot_count` | `shot_count` | 보정값 우선 |
| `fps`,`aspect_ratio`,`narrative_arc`,`pacing_curve`,`music_tempo_curve`,`wow_cut_index`,`creative_device` | 동일 | 그대로 |
| `production_signature.*`,`global_layout.*`,`recurring_motifs` | 동일 | 그대로 |
| `typography` | `typography_global` | `typography.animation_style` → `typography_global.animation_style_default` |
| `vfx` | `vfx_global` | 키 이름만 다름(서브필드 동일) |
| `copywriting.*` | `copywriting.*` | 동일 |
| `inferred_creative_thinking`(7 one-liner) | `client_perception_path` | 같은 7키. `confidence`는 제외(analyzer 추정 라벨) |
| `inferred_creative_thinking` + `inferred_brief`(근거) | `strategy_spine`(brief·insight+evidence·strategy·concept_rationale·brand_right·payoff) | **planner가 논증으로 확장 작성** — one-liner→근거·도출 붙인 논리 단락. 매핑: deck-logic §1 |
| `audio`(Whisper 관측) | `audio_intent`(제작 의도) | **직접 매핑 아님.** analyzer.audio=들린 것, treatment.audio_intent=만들 것. planner가 새로 작성 |

### 5.2 컷 (analyzer `shots[i]` → treatment cut)

대부분 **동일 키 = 동일 의미**. 다른 점만:

| 상황 | 처리 |
|---|---|
| analyzer엔 `no` 없음 | planner가 부여 (C1, C2A…) |
| analyzer엔 per-cut `wow_cut` 없음 | global `wow_cut_index`로 유도 |
| `typo_color_strategy`(cut) | 없으면 `typography_global.color_strategy`에서 상속 또는 작성 |
| `source_refs`,`still_path`,per-cut `audio_intent`,`vfx_in_board_prompts` | planner/builder가 작성(분석 entry엔 없음) |
| ** 5축** `visible_elements`,`texture`,`lighting`,`color_analysis`,`style_prompt` | **그대로 carry-through.** cross-pollination 참조 entry의 이 필드를 *영감*으로 끌어와 새 컷용으로 작성(픽셀 복제 금지). builder가 보드 프롬프트에 사용 |

> 핵심: cross-pollination으로 참조 entry를 끌어올 때 analyzer 키로 읽고, 출력은 treatment 키로 쓴다. 이 표가 그 변환 규칙이다.

---

## 6. 참조
- entry/shots 상세 필드·vocabulary: `lsb-ad-analyzer/schema.md` + `lsb-treatment-builder/REFERENCE/cut-schema.md`
- 영문 토큰·KO 별칭: `lsb-treatment-builder/REFERENCE/keyword-vocabulary.md`
- 사고법·페이지 패턴: `lsb-treatment-builder/REFERENCE/keyword-vocabulary.md` (§8)
- 기획 논리 척추(strategy_spine 틀·QA): `lsb-treatment-builder/REFERENCE/deck-logic.md`
- 덱 디자인·용도×톤 트랙·이미지수 결정표: `lsb-treatment-builder/REFERENCE/presentation-rules.md`
