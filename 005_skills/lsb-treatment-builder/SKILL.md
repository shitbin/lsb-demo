---
name: lsb-treatment-builder
description: >-
 LSB Production 광고 기획안(트리트먼트) 제작 스킬. lsb-ad-planner가 만든
 기획안 마크다운(컨셉·카피·컷리스트)을 입력으로 받아, 주인공 캐릭터 마스터시트 →
 씬별 멀티패널 보드 → 컷 슬라이스 → 스튜디오급 시각 기획안 PDF까지
 완성한다. 데이터셋이 있으면 cross-pollination으로 장표 비주얼 톤
 (레이아웃·타이포·컬러·구조)을 끌어와 디자인 결정에 쓴다. 반드시 다음 상황에서
 사용한다: "기획안 PDF 만들어줘", "트리트먼트 짜줘", "이 컨셉으로 장표 만들어줘",
 "캐릭터시트 + 콘티 + 장표 한 번에", "양반김 식으로",
 "우리은행 식으로", lsb-ad-planner 출력을 던지며 비주얼 제작을 요청할 때.
 컨셉을 잡는 일(cross-pollination, 후보 N안 생성)은 lsb-ad-planner가 담당하므로
 이 스킬은 그걸 다시 하지 않는다.
---

# lsb-treatment-builder — LSB 광고 트리트먼트(PDF) 제작 스킬

## 이 스킬이 어디에 들어가는가

LSB Production 스킬 생태계는 셋이 분업한다.

```
 광고 mp4들 브리프 + 데이터셋 기획안 마크다운 + 브랜드
 │ │ │
 ▼ ▼ ▼
┌──────────────┐ ┌──────────────┐ ┌─────────────────────┐
│lsb-ad-analyzer│ ───▶ │lsb-ad-planner│ ───▶ │lsb-treatment-builder│
│ (눈·이해) │ 데이터셋 │ (머리·기획) │ 기획안 │ (손·제작) │
└──────────────┘ └──────────────┘ └─────────────────────┘
 │
 ▼
 ┌──────────────────┐
 │ 트리트먼트 PDF │
 │ + 캐릭터·컷 폴더 │
 └──────────────────┘
```

- **lsb-ad-analyzer**: 광고 영상을 메타데이터(JSON entry)로 분해해 데이터셋을 쌓는다.
- **lsb-ad-planner**: 데이터셋 + 브리프 → cross-pollination으로 컨셉 후보 N안 + 카피 + 컷리스트(treatment.json).
- **lsb-treatment-builder (이 스킬)**: 위 기획안을 받아 비주얼·콘티·장표를 만들어 PDF로 묶는다.

**이 스킬은 컨셉을 새로 잡지 않는다.** 컨셉은 planner가 한 것으로 보고, 받은 기획안을 시각화·장표화하는 일에만 집중한다. 사용자가 컨셉 작업을 부탁하면 lsb-ad-planner로 보내라.

## 가이드라인의 어디에 닿아 있는가

- **§3 Wrapper = 손, 데이터셋 = 근육**: 이 스킬이 '손'. 사용자(뇌)가 정한 방향을 데이터셋(근육)으로 산출물로.
- **§4.3 Cross-pollination**: 비주얼 톤 레퍼런스를 끌어올 때 가중치 0.2(동일)/0.5(인접)/1.0(원거리)/1.2(대조). 와우컷 하드밴. (판정 맵 단일 출처 = `lsb-ad-planner/schema.md` §3, 영문 industry 기준.)
- **§5 분업의 비대칭**: AI가 캐릭터·씬보드·슬라이스·장표를 빠르게 뱉고, 사람이 미적 판정·컷 선택. AI는 미적 판정을 신뢰하지 않는다.
- **§6 타율**: 마스터시트·씬보드를 다량 생성 후 사람이 1차로 솎는 슬롯.
- **저작권 안전**: 데이터셋에서 끌어오는 것은 Level 2~3 추상화(공식·구조·시그니처). 픽셀 따라 그리기 금지. **자막·카피 원문은 보존**(짧은 카피 verbatim), 셀럽 *얼굴 사진복제*·실제 *로고 마크*만 generic.

## 작업 흐름 (Phase 0 → 6)

각 Phase 끝에서 멈추고 사용자에게 보여준 뒤 다음으로. 비싼 단계(이미지 생성, PDF 빌드) 전에는 반드시 컨펌.

### Phase 0 — 입력 검증 & 작업 폴더 잡기

트리거 시 사용자는 보통 다음을 던진다.

1. **기획안(treatment.json 또는 마크다운)** — lsb-ad-planner 출력. 없으면 요청하거나 직접 작성 안내.
2. **브랜드 가이드라인** — 컬러 팔레트(hex), 로고, 폰트, 톤. 없으면 브랜드 공식 자산을 찾아 정리(hex까지).
3. **데이터셋 (선택)** — 연결된 `LSB_Ad_Datas`(=`<LIBRARY>`) 안의 `001_ad_video_dataset/`(=`<DATASET>`)의 `entries/`+`index/`. **경로 하드코딩 금지** — 런타임 resolve(mac `/Users/...`, win `C:\Users\...` 공용). 있으면 cross-pollination에, 없으면 카탈로그에서 직접 선택.
4. **출력 폴더** — Cowork 작업 폴더. 없으면 `mcp__cowork__request_cowork_directory`.

**전략 입력 (필수 — 가장 먼저).** 컷·비주얼보다 *기획 논리*를 먼저 확보한다: 과제(브랜드 숙제) / 타깃 인사이트 + 근거 / 전략(한 수) / 컨셉 도출 이유 / 브랜드 정당성(product truth) / 기대효과·평가기준. **이 입력이 비면 빌드 금지** — planner의 `strategy_spine`(또는 `client_perception_path`)을 논리 단락으로 확장해 받거나, 없으면 planner로 돌려보내거나 사용자와 함께 도출한 뒤 진행. (척추 틀: `REFERENCE/deck-logic.md` §1.)

그다음 **실행 체크리스트**(빠지면 사용자에게 묻는다): 컨셉명·해시태그·한 줄 요약 / 영상 카피(자막·Na·O.V 구분) / 컷리스트 / 주인공·등장인물 / 배경·로케이션 / 톤앤매너 / 매체·규격(9:16/16:9, 길이) / 브랜드 필수 요소(로고·컬러 1순위·자막 고지).

작업 폴더 구조:
```
{출력폴더}/{프로젝트명}/
├── assets/ # 캐릭터시트·씬보드 원본 (멀티패널 풀이미지)
├── frames/ # 슬라이스된 컷별 프레임
├── 확정컷/ # 사람이 큐레이션한 최종 컷
├── fonts/ # 빌드 폰트
├── plan.md # 입력 기획안 사본
├── treatment.json # 풀필드 데이터 (글로벌+컷+트랜지션)
├── build_treatment.py # 재생산 빌드 스크립트
└── treatment.pdf # 최종 산출물
```

### Phase 1 — Plan 해체 + Deck Style 결정

**1.1 Plan 해체 — 글로벌 메타 + 컷별 풀 필드.**

핵심 원칙: **트리트먼트 컷 데이터는 `lsb-ad-analyzer` entry의 `shots[]`와 동일 스키마(30+ 필드)로 적는다.** "SCENE/COPY/NOTE 3블록"으로 줄이면 안 된다 — 후속 제작자가 추측해 채우면 의도가 흐려지고 cross-pollination 양식이 안 맞는다. analyzer→treatment 키 변환은 `lsb-ad-planner/schema.md` §5 매핑표를 따른다(예: total_duration→total_duration_sec, typography→typography_global).

**(A) 글로벌 메타 (treatment 전체 한 번)**

| 묶음 | 필드 |
|------|------|
| 식별 | `id`, `schema_version`, `source_plan_ref`, `brand`, `product`, `target_demo` |
| 길이·구조 | `total_duration_sec`, `shot_count`, `fps`, `aspect_ratio`, `hook_position_sec`, `cta_position_sec` |
| 서사 | `narrative_arc`, `pacing_curve`, `music_tempo_curve`, `wow_cut_index[]`, `creative_device` |
| 촬영 시그니처 | `production_signature.capture_style/.camera_signature[]/.color_grade/.texture_fx` |
| 글로벌 레이아웃 | `global_layout.grid_system/.subject_placement_dominant/.subject_typo_relation/.negative_space_use` |
| 모티프 | `recurring_motifs[]` |
| 타이포 글로벌 | `typography_global.primary_font_class/.secondary_font_class/.animation_style_default[]/.subtitle_position_dominant/.color_strategy` |
| VFX 글로벌 | `vfx_global.primary_effects[]/.effect_intensity/.transition_style_dominant` |
| 카피 글로벌 | `copywriting.tagline_text/.cta_text/.copy_tone[]` |
| 인지 경로 | `client_perception_path`(7단계, 감정 경로) |
| 기획 논리 | `strategy_spine.brief / .insight(+evidence[]) / .strategy / .concept_rationale / .brand_right / .payoff` — 비즈니스 논증(planner 산출). builder가 STRATEGY 섹션으로 렌더. 비면 사용자와 도출. 매핑·틀 = `REFERENCE/deck-logic.md` §1 |

**(B) 컷별 풀 필드 (모든 컷)**

| 묶음 | 필드 |
|------|------|
| 식별 (필수) | `index`, `no`, `duration`, `framing`, `function` |
| 인물·동작 | `subject_position`, `subject_action`, `subject_motion`, `pose_description`, `gaze`, `eye_contact_effect` |
| 카메라 | `camera_motion`, `camera_motion_intensity`, `camera_angle`, `camera_facing`, `shot_scope`, `camera_effect_local`, `motion_blur` |
| 리듬·트랜지션 (필수) | `intra_cut_rhythm`, `transition_in`, `transition_out` |
| 소품·세트 | `props[]`, `prop_motion`, `prop_semantics` |
| 컬러 | `color_mood`, `color_palette[]` (HEX 4~6색), `color_intent` |
| 타이포·자막 (자막 컷만) | `copy_overlay`, `layout_grid`, `subject_typo_layout`, `typo_motion`, `typo_color_strategy` |
| VFX (있는 컷만) | `vfx_in_shot[]`, `vfx_intensity_local`, `vfx_in_board_prompts` |
| 시각 인벤토리 | `visible_elements`, `texture`, `lighting`, `color_analysis`, `style_prompt` |
| 프레임 복제 | `recreation_prompts` (`t2i_start_frame`·`t2i_negative`·`i2v_motion`·`i2v_params`·`fidelity_note`) |
| 메타 | `wow_cut`, `fact_check_flag`, `notes`, `source_refs[]`, `still_path` |

vocabulary(framing/camera_angle/typo_motion 등)와 필드 정의는 `REFERENCE/cut-schema.md`. **반드시** 그 vocabulary(영문 토큰) 안에서 값을 골라야 cross-pollination 매칭이 안 깨진다.

시각 인벤토리·`recreation_prompts`는 analyzer가 핵심 컷에 만들어 둔 *이미지/영상 생성 입력*이다. cross-pollination 참조 entry에서 *영감*으로 끌어오거나(픽셀 복제 금지) 이 컷용으로 작성하고, Phase 3 보드 프롬프트에 결합한다.

빠진 필드는 추측하지 않는다. 특히 **카메라(앵글·방향·움직임)·전환·타이포 모션**은 비워두면 안 된다. 작성 순서: ①5필수 → ②인물·소품 → ③카메라 → ④트랜지션·리듬 → ⑤컬러·타이포 → ⑥VFX·시각 인벤토리 → ⑦recreation_prompts → ⑧메타.

**1.1-b 컷 문법 게이트 재검증 (더블 방지 — planner R10 이중 방어).** plan 해체 직후, 컷리스트의 **모든 인접 쌍**을 planner R10 기준으로 재검증한다: 같은 피사체(`subject_identity`)·같은 공간인데 ①`framing` 사이즈 변화 2단계 미만(7단 사다리 `ECU→CU→MCU→MS→MLS→FS/LS→ELS`) ②`camera_angle`/`camera_facing` 변화 30도 미만 ③피사체/공간/시간 동일 — 셋 다면 **더블(점프컷) 위반**: 그 경계는 컷이 아니다. 처리: ⓐ `transition_in/out`을 seamless 계열(`push_in`/`pull_out`/`dolly_through`/`morph`/`match_action`)로 교체하고 3.0 분기에서 단일 캔버스 트랜지션 보드로 흡수(기본) 또는 ⓑ 컷 병합을 사용자에게 제안(builder는 컷 구조를 임의로 늘리거나 지우지 않는다 — 병합은 확인 후). 예외: 펀치인(같은 앵글, 사이즈 **2단계+**)·매치컷·`notes`에 "intentional jump cut" 명시된 컷. **위반이 남은 채로 보드 생성(Phase 3)·빌드(Phase 4)에 들어가지 않는다.**

**1.2 Deck Style 결정.** 장표 스타일은 한 톤이 아니다.

| 스타일 | 언제 | 특징 |
|--------|------|------|
| 양반김식 (시네마틱) | 영상 중심, 고급, 인물 드라마 | 검정 BG, 한 구절씩 빌드업 "생각의 흐름" + 컷별 풀스틸 콘티 |
| 우리은행식 (서비스) | 셀럽/모델 중심, 카피 펀치 | 흰 BG, 카피 가운데, 인물 사진 모듈 |
| 신세계 럭셔리식 | 럭셔리·패션 | 큰 여백, 세리프, 미니멀 그리드 |
| KG INSTEROID식 (오브제) | 제품 KV필름 | 오브제 클로즈업 그리드, 짧은 캡션 |
| G-EYE식 (세계관) | 캐릭터·세계관 바이럴 | 일러스트형 일관 캐릭터, 코믹 컷 분할 |

데이터셋이 있으면 cross-pollination으로 비슷한 톤의 entry를 가중치 0.2~1.2로 끌어와 후보 정렬 후 사용자에게. 없으면 위 5개에서 선택. `REFERENCE/deck-styles.md`(디자인 시그니처) 참조. **스타일은 용도(기획안/트리트먼트/PPM) × 톤(시네마틱/서비스·펀/럭셔리/세계관/공익/컨퍼런스/B2B/교육)으로 트랙을 고른다** — `REFERENCE/presentation-rules.md` §0·§5. 5종은 시드일 뿐, 트랙 매트릭스로 *어떤 도메인 기획서든* 매핑된다.

**1.3 Style 컨펌.** "이 스타일로 가는 게 맞아?" 한 번 묻고 넘어간다. 비싼 단계 전 마지막 값싼 결정점.

**1.4 서사 구조·인물 판정 (다중 인물·교차편집 대응 — A3 학습).** plan의 `narrative_structure`·`character_pool[]`을 읽어 처리 방식을 가른다.
- `linear_continuous`: 기존대로 공간 연속 흐름.
- `cross_cutting_montage`(같은 시간·다른 공간 교차): **공간을 억지로 이어붙이지 않는다.** 각 공간을 별도 reference 그룹으로 분리, 같은 시점의 다른 공간 컷에 *동일 시간 상태*(예: 시간정지) 명시, 트랜지션은 *공간 점프*로 표기. 영상화는 공간/인물 세그먼트별 클립으로 쪼갠다(영상 스킬).
- `character_pool[]`이 2인 이상이면: 각 컷 `subject_identity` 확인 → **주인공 컷엔 주인공 시트만 / 다른 인물 컷엔 그 인물 시트만** reference 배치(Phase 2·3). 안 그러면 A3처럼 *주인공이 모든 컷을 다 하는* 영상이 된다.

### Phase 2 — 마스터 캐릭터시트

비주얼 일관성의 뼈대. (REFERENCE/scene-boards.md + prompts/master_character.md)

**2.0 인물 수 결정 (다중 인물 — A3 학습).** plan의 `requires_character_sheets[]`를 본다. *화면에 또렷이 나오는* 인물(주인공·핵심 조연)마다 마스터시트를 **각각** 만든다(주인공용·카페손님용·알바생용 …). 군중·엑스트라(`background_crowd`)는 시트 없이 "익명의 다른 사람들"로 처리. 각 시트는 그 인물이 나오는 컷에서만 reference로 쓴다.

**2.1 프롬프트 원칙.** 단일 인물·단일 의상(시트 1장당), 정면 + 사이드 1~2컷이 한 캔버스에. 의상에 브랜드 컬러(hex 명시). 액세서리 최소화. 표정 평온/중립. 배경 무지. 4K, GPT Image 2 high. **실존 셀럽 얼굴을 사진수준으로 복제하지 않는다** — 유형(연령대·스타일링·포즈)으로 정의하고 스튜디오 자체 모델/탤런트 전제.

**2.2 생성 후 처리.** 결과를 사용자에게 컨펌 → job id 저장 → 이후 모든 씬 보드 reference로(Higgsfield `medias`). reference 슬롯엔 마스터시트 1장만.

**2.3 자주 실패 & 교정.** 얼굴이 매번 다름 → reference 빠짐(medias 확인). 의상색 비뚤 → hex + "exactly this color". 두 사람 → "single subject" + negative "no second person". 안 시킨 액세서리 → negative 명시.

### Phase 3 — 씬 보드 (멀티패널) + 트랜지션 보드 (단일 캔버스) + VFX 인-보드 + 슬라이스

영상의 모든 시각 자산을 만드는 단계. 세 보드 유형을 *분기 판단*해서 만든다.

**3.0 보드 유형 분기 (자동 판단).**

| 보드 유형 | 언제 | 단일/분할 |
|----------|------|-----------|
| 씬 보드 | 같은 배경 컷 2+ 묶일 때 | 분할 멀티패널 |
| 트랜지션 보드 | transition_in/out이 whip_pan/morph/match_action/push_in/pull_out/360_spin/dolly_through | 단일 캔버스 |
| 단독 컷 | 다른 컷과 안 묶이는 펀치라인·엔딩 | 단일 1패널 |

plan을 받으면 모든 컷의 transition_in/out을 스캔해 분기 결정 후 사용자에게 보여주고 컨펌. 자세한 룰: REFERENCE/transitions.md.

**3.1 컷 그룹핑.** 같은 배경·시점 묶음으로 재배치(카페 안 3컷 → 가로 3패널 / 마지막 펀치라인 → 단독). 멀티패널 이유: 배경 일관성, 크레딧 절약, 직관 검토.
**페이지당 이미지 수 = `REFERENCE/presentation-rules.md` §3 결정표** (Phase 4.2 렌더에도 동일 적용): 디바이더·전략텍스트·슬로건·나레이션 자막 = **0장** / 키비주얼·제품 히어로·시네마틱 서사 = **1장**(풀블리드/레터박스) / 비교·A안B안·과거vs현재 = **2장** / 무드·바리에이션·캐릭터 = **3장** / 콘티 그리드 = **5열(기획안)·3열(트리트먼트)** / 톤앤무드 대량 = **6~16 그리드** / 전체 흐름 = **컨택트시트 1장**. 원리: 숫자↑=무드/요약, 1장=서사/임팩트. 정보밀집↔임팩트 교대로 호흡.

**3.2 보드 생성 프롬프트 원칙.**
- **컷 생성 기본 = 2×2 그리드 (★ 한 장에 4컷 · 2K · 무시 금지).** 컷 이미지는 한 컷씩 따로 생성하지 말고 **2×2 그리드(2행 2열, 한 이미지에 4개 컷)** 로 묶어 생성한다 — 스토리보드처럼. 생성 횟수↓·4컷 간 톤/캐릭터 일관성↑. 컷이 5개 이상이면 4컷씩 여러 장(6컷=4+2, 9컷=4+4+1). 프롬프트에 `"2x2 storyboard grid, 4 equal quadrants, 2 rows by 2 columns, symmetric centered thin white gutters, no overlap, each cell's subject fully inside its cell with margin, nothing cropped at cell edges"` 명시(셀 경계 잘림 예방 — 3.3 프리셋 슬라이스와 한 쌍). 해상도는 2K(3.2-c). (장표·영상엔 슬라이스해 컷별로 분리 사용 — 3.3.)
- **셀(컷)마다 별도 묘사 + 컷당 500단어 이상 (★ 무시 금지):** `"Cell 1 (top-left): … | Cell 2 (top-right): … | Cell 3 (bottom-left): … | Cell 4 (bottom-right): …"`. **각 셀(컷) 묘사는 최소 500단어(word — 글자 수가 아니라 영어 단어 수 기준)** — 인물·동작·표정·카메라(앵글·렌즈·거리)·조명(방향/경도/색온도)·전경·배경 요소·질감·팔레트·분위기·VFX·타이포까지 빠짐없이. 한두 줄짜리 빈약한 셀 묘사는 품질 저하의 직접 원인이므로, 500단어 미만이면 더 채운 뒤 생성한다.
- (단순 가로 스토리보드가 더 맞는 특수 경우만 "horizontal storyboard, N panels, equal width, thin white gutter" — 기본은 2×2 그리드.)
- **금지(주석/낙서만)**: "no handwriting, no annotations, no labels, no storyboard markings, no timecode" — GPT 자동 주석 방지. **단 '텍스트 전면 금지'는 아니다** — 강조어·슬로건·키네틱/모션 타이포는 이미지에 *박아* 생성한다. 컷별 타이포 모드(none/subtitle/baked)·baked 프롬프트·데이터셋 판정은 `REFERENCE/typography-in-image.md`.
- 마스터 캐릭터시트를 reference로. **캐릭터 일관성 — 마스터시트 강제(A3 학습):** 보드(확정컷) 생성 시 마스터시트 제약(예: no necklace, short hair, plain jacket)을 프롬프트·negative에 그대로 박아 *보드가 마스터와 안 어긋나게* 한다(예방 우선). 이미 만든 확정컷이 충돌하면(목걸이·머리길이 등) 그 디테일 제거한 정리본을 만들거나, 충돌 컷은 reference에서 빼고 마스터+컨택트시트만 쓴다(폴백). Seedance는 풍부한 확정컷을 마스터보다 강하게 따라가므로 강제 없으면 negative가 무시된다.
- 종횡비: 9:16 영상이면 패널 9:16, 전체 가로 N배. Higgsfield 캡이면 16:9로 받고 슬라이스 시 trim.
- **시각적 비유 함정 주의**: 사람을 사물에 빗대면(회색 돌·마네킹) 보통 미적으로 망함. 시간정지는 "alive, normal, just paused mid-motion".
- **제품 충실도 (라벨·패키지) — product-lock:** 실제 제품이 정확히 나와야 하는 캠페인은 사용자 공식 제품 이미지를 **product-lock 레퍼런스로 고정**(planner R4: 브랜드 IP는 내가 생성 금지·사용자 에셋 우선)하고, 모든 보드 프롬프트에 "실제 라벨/패키지가 정확히·항상 보인다" 명시 + **negative "무라벨/빈 병/라벨 없는 제품 금지"**. 제품 이미지가 `uploads/`에 없다고 단정 말 것 — 대화 트랜스크립트(.jsonl) base64 폴백 후 사용자 확인(Phase 0). 메인 카피 baked는 **KV·타이틀·CTA 프레임에 한해 기본값**(전 프레임 아님), 한글은 굽지 말고 후보정 합성. (영상 단계의 라벨·VO는 영상 스킬에서 동일 product-lock 참조.)
- **컷의 시각 입력을 패널 묘사에 결합 (핵심):**
 - 컷에 `recreation_prompts.t2i_start_frame`(또는 `style_prompt`)이 있으면 그 프롬프트를 **패널 묘사의 베이스**로 쓴다(셀럽 얼굴 사진복제·실제 로고 마크는 제외, 자막·카피 원문은 보존).
 - `lighting`(방향/경도/색온도)·`texture`(표면 질감)·`visible_elements`(전경/중경/배경/대기)·`color_analysis`(팔레트·강조색)를 각 패널 필드로 풀어 넣는다. 빠지면 같은 컨셉도 보드마다 톤·질감이 달라진다.
 - 영상화(i2v) 단계에서 `recreation_prompts.i2v_motion` + `i2v_params`로 스틸을 컷 모션으로 움직인다.
- 자세한 템플릿: `prompts/scene_board.md`.

**3.1-b 레이어드 콜라주 분기 (★ 베이스 위 조각 겹침 — 한 장 생성 금지).** 컷/키비주얼이 *원본 위에 여러 이미지 조각이 콜라주처럼 겹치는* 구조(GMA 2018 식)면, 생성 모델에 "콜라주 한 장 만들어라"라고 시키지 않는다. **3단 분리**: ① 조각별(베이스·눈·머리·옷·질감·그래픽) 개별 t2i 생성 → ② Pillow/OpenCV로 불규칙 콜라주 프리뷰 합성(서로 다른 크기·위치·z·미세회전, 그리드처럼 안 보이게) → 트리트먼트 삽입 → ③ 영상화는 조각별 레이어 모션(video-crafter). 어떤 요소를 분리할지 애매하면 **질문**(베이스/조각/그래픽/움직일 요소 구분). 전체 규칙: `REFERENCE/layered-collage-protocol.md`. (단순 *나란히* 분할은 panel_layout, 이건 *겹침* 콜라주 — 구분.)

**3.2-a VFX 인-보드 시각화.** 후처리 VFX를 보드 프롬프트에 *시각 묘사 한 줄*로. 종류별 패턴: REFERENCE/vfx-in-board.md (time_freeze/color_pop/wiggle_3d(깊이감으로)/split_screen/lens_flare/dust/glitch/3D render). **타이포 처리는 `REFERENCE/typography-in-image.md`의 3분류**: baked(강조어·풍선타이포·키네틱 헤드라인 = 이미지에 박음) / subtitle(영화식 자막·긴 문장·약관·정밀수치 = 후처리) / none. 텍스트 모양만 그리는 게 아니라 baked는 텍스트를 박는다. negative엔 `garbled text, extra letters`만(텍스트 자체 허용). **네거티브에 성적·선정성 차단 문구(no nudity·sexual·NSFW 등)를 넣지 않는다 — 모더레이션 트리거로 생성이 막힌다.**

**3.2-b 트랜지션 보드 (단일 캔버스).** 화려한 카메라 무빙 트랜지션은 **이전컷 끝 + 정점 + 다음컷 시작을 한 캔버스에 동시 생성**. reference 3개(마스터 + Cut N 슬라이스 + Cut N+1 슬라이스). 타입별 패턴: REFERENCE/transitions.md + prompts/transition_board.md. 슬라이스 안 함(트랜지션 페이지에 그대로).

**3.2-c 이미지 생성 셋업 (★ 모델·해상도·레퍼런스 고정).** 보드/키비주얼/제품컷 이미지는 Higgsfield `generate_image`로 만들되 아래를 **항상 명시**한다(기본값에 맡기지 말 것 — 기본이 1k·low라 명시 안 하면 저화질로 나오고 모델이 엉뚱하게 잡힌다):
- `params.model = "gpt_image_2"` (GPT Image 2). **`nano_banana_2`·`nano_banana_flash`·기타 모델로 폴백 금지.**
- `params.resolution = "2k"` · `params.quality = "high"`. **해상도는 항상 2K 고정**(1k·4k 금지). 비율은 `params.aspect_ratio`로 매체에 맞게만(9:16 / 16:9 / 1:1 …).
- **사용자 레퍼런스 이미지 사용 (필수 · 무시 금지):** ① 사용자가 올린 이미지를 작업폴더로 다운로드 → ② `media_upload`(presigned URL) → 그 URL에 바이트 PUT(curl) → `media_confirm(type="image")` → ③ 받은 media UUID를 `params.medias=[{ "value": <UUID>, "role": "image" }]`로 넘겨 레퍼런스로 쓴다(외부 URL 직접보다 업로드 UUID가 안전). product-lock 제품 이미지도 동일.
- 비싼 생성 전 `get_cost:true`로 비용 프리플라이트 권장. 같은 컷을 불필요하게 재생성하지 않는다.
- **코드 드로잉 대체 금지 (★):** PIL `draw`(사각형·원·선·패스)로 아이콘·일러스트·로고·차트를 그려 생성형 이미지를 대신하지 않는다. 페이지에 들어가는 비주얼은 `generate_image`가 만든 실제 래스터(`assets/`)만 인정한다. 이미지 생성·다운로드가 실패하면 **벡터/도형으로 때우지 말고 빌드를 멈추고 사용자에게 알린다.**
- (모델명·해상도·셋업은 내부 정보 — 사용자에게 "모델 확인했습니다" 식으로 노출 금지.)

**3.2-d 생성 이미지 로컬 다운로드 (★ PIL 입력은 반드시 로컬 파일 · URL 직접 사용 금지).** 이미지 생성 도구(Higgsfield 등)가 돌려주는 건 **원격 URL(또는 job)** 이다. 이후 단계(3.3 슬라이스·Phase 4 PIL 합성)는 **URL을 직접 열 수 없다** — `PIL.Image.open(url)`은 실패한다(과거 21바이트·`UnidentifiedImageError`의 원인). 그러니 생성 직후 **반드시 로컬로 내려받아 `assets/`에 저장**하고, 그다음부터는 *로컬 경로만* 쓴다(슬라이스·합성·`hero_stills/`·`확정컷/` 전부). **URL을 경로/`src`로 넘기지 말 것.**
- 저장 후 `PIL.Image.open(path).verify()`로 유효성 확인. 파일이 수백 바이트 이하로 작거나 안 열리면 **다운로드 실패**(대개 컨테이너 네트워크 차단 또는 URL 만료) — 빈 이미지로 빌드하지 말고 재시도하거나 사용자에게 알린다.
- 헬퍼(표준 라이브러리, 추가 설치 불필요):
 ```python
 import os, urllib.request
 from PIL import Image
 def fetch_image(url, dest):
     os.makedirs(os.path.dirname(dest), exist_ok=True)
     req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
     with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
         f.write(r.read())
     with Image.open(dest) as im:        # 깨진/빈 파일 차단
         im.verify()
     if os.path.getsize(dest) < 1024:
         raise ValueError("다운로드 이미지가 비정상적으로 작음 — 환경 네트워킹/URL 확인")
     return dest
 # 예: local = fetch_image(gen_url, f"{proj}/assets/board_{cut}.png")  → 이후 PIL은 local만 사용
 ```
- 도구가 URL 대신 base64/파일 ID를 주면 그것을 디코드·저장해 동일하게 로컬 파일로 만든 뒤 사용한다.
- ⚠ 컨테이너 **네트워킹이 꺼져 있으면 다운로드가 빈 파일로 실패**한다. 환경 networking을 unrestricted(또는 해당 CDN 호스트 허용)로 둬야 한다.

**3.3 슬라이스 (★ 2×2 그리드 → 4컷 분리 · 장표엔 분리본 사용 · 프리셋 폴백).** 2×2 그리드 이미지는 **가로 1회·세로 1회로 4등분**해 컷 4개로 분리한다(흰 갭/중앙선 감지 → 2행×2열 셀 절단 → trim_white). 가로 N패널 보드면 컬럼 흰비율로 N등분(`colw>0.82` 디폴트, 갭 없으면 0.75~0.88 튜닝).
- **그리드 프리셋 폴백 (★ 잘림 대비):** 갭 감지가 실패하거나 감지된 경계가 어긋나면(셀이 옆 셀을 물고 잘리면) 감지값을 버리고 **고정 프리셋 = 정확 4등분**으로 슬라이스한다: `(0,0,W/2,H/2) / (W/2,0,W,H/2) / (0,H/2,W/2,H) / (W/2,H/2,W,H)` + trim_white. 판정은 프로그램으로(감지 경계가 W/2·H/2에서 ±3% 이상 벗어나면 프리셋 채택).
- **셀 내용 자체가 잘려 나온 그리드**(피사체가 셀 경계에 걸려 절단)는 슬라이스로 못 살린다 — 해당 그리드를 3.2 프롬프트(quadrant·no cropping 명시)로 **재생성**한다. 잘린 컷을 그대로 장표·영상에 쓰지 않는다.
- 분리한 컷을 컷 번호로 네이밍해 `확정컷/`·`frames/`에 저장하고 — **장표(Phase 4)·영상에는 반드시 이 분리된 컷별 이미지를 쓴다(2×2 그리드 원본을 장표에 통째로 넣지 않는다).**

**3.3-a 인물 분리 검사 (다중 인물 필수 — A3 학습).** 보드 reference 배치 직후, 각 컷의 `subject_identity`가 맞물리는지 확인: 주인공 컷엔 주인공 시트만, 다른 인물 컷(카페 손님·알바생)엔 그 인물 시트만. 다른 인물 컷에 주인공 마스터시트가 섞이면 빼거나 weight를 낮춘다. (A3: 이 검사 부재로 카페 컷 인물이 주인공으로 변질.)

**3.4 사람의 판정 슬롯 (★ 이미지·PDF Read 금지 · 32MB 페이로드 상한).** 보드/장표 생성되면 멈추고 사용자가 "다시/OK" 결정. **미적 판정은 AI가 하지 않는다.** 생성·다운로드한 이미지나 빌드한 PDF를 `Read`로 컨텍스트에 올려 검수하지 않는다 — 존재·크기·해상도는 PIL/파일로 *프로그램* 확인(`Image.open().verify()`·페이지 수 등), 보고 판단하는 건 사용자다. **이미지·PDF 바이트를 대화/도구 페이로드에 base64로 인라인하는 것도 절대 금지** — 플랫폼 요청 상한이 **32MB 고정**이라 트랜스크립트가 이를 넘으면 요청 자체가 죽는다(`Request exceeds the maximum size` 413). 이미지는 항상 **로컬 파일 경로·업로드 UUID·URL 참조**로만 주고받는다(레퍼런스 전달은 3.2-c media_upload 경로 사용 — 바이트는 presigned URL로 직접 PUT, 대화엔 안 실림).

### Phase 4 — Deck Build (PIL + Korean fonts)

**4.1 빌드 스택.** Python + PIL. 폰트: 제목 Black Han Sans, 본문/캡션 Noto Sans KR(variable). **캔버스 = 4K(3840×2160) 기본** — 좌표·폰트는 논리(1920×1080)로 쓰고 `build_treatment_template`의 `SCALE=2`로 ×2 출력한다(1080p는 빠른 드래프트일 때만). multi-page PDF. **모든 이미지 입력은 로컬 파일만(3.2-d에서 다운로드한 것) — URL을 PIL에 직접 넘기지 말 것.** (다운로드 명령: REFERENCE/deck-build.md.) **저해상도(1080p) 납품 금지** — 코덱스 리디자인 기준이 4K다.

**4.1-에디토리얼 레이아웃 시스템 (★ 코덱스급 기본값 · 평면 텍스트 덤프 금지).** 매 프로젝트 레이아웃을 새로 손짜지 말고 `build_treatment_template`의 **아키타입**을 쓴다. 규칙·토큰: `REFERENCE/editorial-layout.md`.
- `T.set_fonts(title_path, body_path)` 먼저. 테마는 `T.THEME_EDITORIAL`을 **브랜드 팔레트로 덮어쓴다**(bg/surface(크림)/ink/muted/point/line). 크림 surface를 *콘텐츠·카드·보드 면*으로 적극 쓴다(전부 어둡게 두지 않는다 — 리디자인 격차의 핵심).
- 아키타입: `T.cover_split()`(표지 = 텍스트 좌 / **히어로 이미지** 우) · `T.two_col()`(논증 좌 / **크림 PROOF 카드 또는 이미지** 우) · `T.fullbleed_kv()`(풀블리드 키비주얼 + 하단 스크림 텍스트) · `T.cut_board()`(**확정컷 썸네일 그리드** 4열). 좌측정렬 위계(eyebrow→headline→body)가 기본, 중앙정렬은 선언형 1~2줄 슬로건에만.
- **이미지 의무(IMAGE MANDATE):** 표지·키비주얼·컷보드·씬 페이지는 **실제 이미지(hero_stills/·확정컷/)를 합성**한다 — 그라데이션 위 텍스트만 두지 않는다. 빌드 직전 `T.assert_images_present(page_kind, placed_flags)`로 0장이면 보류(Phase 5 ⑩). **코드로 그린 벡터·아이콘·도형은 '이미지'로 치지 않는다 — `generate_image` 래스터만 인정.**
- **컷보드 1장 필수:** 전 컷을 한 페이지 썸네일 그리드로 보여주는 `cut_board` 페이지를 비주얼 언어/콘티 앞에 둔다(리디자인 p12).

**4.1-a 두 페이지 모드 — 광고주용 vs 제작용.** 독자가 둘(광고주 5초 캐치 / 제작팀 풀필드). 같은 데이터를 두 모드로 렌더.
- **광고주 페이지**: 스틸 크게(70%+) + 한 줄 카피("...") + 키워드 1~2개. 큰 폰트, 넓은 여백, 한 페이지 한 메시지.
- **제작 페이지**: 8블록 풀필드(SCENE/COPY/CAMERA/VFX + PROPS/COLOR/TRANSITION). 작은 폰트, 영문 vocabulary 그대로.
빌더 함수 `s_cut_public(d)` / `s_cut_internal(d)`. 광고주 인지 경로 7단계(client_perception_path)는 Phase 1.1 체크리스트로 강제. 자세히: REFERENCE/client-vs-internal.md.

**4.2 슬라이드 구조 (기본 템플릿, 합본) — STRATEGY가 컷보다 먼저.** 표지 → **02~08 STRATEGY(기획 논리: `REFERENCE/deck-logic.md` 7비트를 한 페이지 한 단계, 인사이트 근거 인용 포함)** → 09 기대효과(평가기준/KPI 역산) → 10-12 비주얼 언어(축·기법·팔레트) → 13 키비주얼(마스터시트) → **브리지 1장("앞의 전략을 이렇게 영상으로")** → 14~N 컷별 광고주 페이지 → 트랜지션 페이지 → 페이싱 → 오디오 의도 → 클로징 → 크레딧 → [부록] → 제작 섹션(컷별 8블록 풀필드 + 트랜지션). **컷(실행)은 반드시 STRATEGY 뒤 — 컷이 표지 다음 바로 나오면 안 된다.** 즉 모든 덱 = [표지 → STRATEGY(왜) → 비주얼 언어 → 콘티(어떻게) → 기대효과 → 클로징]. **데이터 드리븐**(s_phrase/s_points/s_palette/s_keyvisual/s_cut/s_transition/s_closing + 전략 비트 렌더 s_strategy). 템플릿: `scripts/build_treatment_template.py`. 스타일이 양반김 아니면 디자인 시그니처만 교체(REFERENCE/deck-styles.md + presentation-rules.md).

**4.2-a 카피 조판 — typeset 시스템 (글자 단위 줄바꿈 금지).** 슬라이드에 찍는 카피는 한 덩어리로 박지 않는다. `REFERENCE/text-setting.md`의 4축으로 *연출*한다: ① **의미 단위 줄바꿈**(쉼표·연결/대조 어미·따옴표 구 — by-char 금지, 대조 구문 "A 아니라 B"는 A/B 줄 분리) ② **포인트 컬러 1강조**(블록당 핵심구 1개만 브랜드색, 나머지 기본색) ③ **역할별 크기 위계**(결론·핵심구 1.0 / 도입 0.62 / 부연 0.38) ④ **정렬 스마트 판단**(선언 1~2줄=center / 설명·논리 3줄+=left, 트랙 톤 가중). 이 4축은 **`scripts/build_treatment_template.py` 모듈로 코드화돼 있다(강제 · _2606031952)** — 매 세션 새로 짜지 말고 `import build_treatment_template as T` 후 `T.typeset(text, base_size, theme, tone)` → `T.draw_block()`으로 렌더한다. 헤드라인은 `T.fit_headline(text, font_path, 컬럼폭, theme)`로 폭에 맞는 최대 크기를 자동 선택. **전략 비트·컨셉 카피·키비주얼 카피·클로징** 등 텍스트가 주인공인 페이지는 반드시 이 함수를 거친다(콘티 자막은 짧아 단순 처리). 모듈이 split_clauses(의미단위)·1강조 예산·역할별 크기(1.0/0.62/0.38)·center/left를 전부 강제하므로, 손으로 박스에 욱여넣는 렌더 금지. planner가 카피에 경량 마크업(`//` 줄바꿈, `*강조*`, `__크게__`)을 부여하면 정확도↑. 예: "데이터 부족은 불편이 아니라 '잠깐 끊기는 단절'" → `데이터 부족은 불편이 아닌,`(52pt 기본색) + `'잠깐 끊기는 단절'`(84pt 포인트 민트), center. ⚠️ 이건 *슬라이드 위 글자* 조판 — *컷 이미지에 텍스트를 박는 것*은 `REFERENCE/typography-in-image.md`(별개).

**4.2-b 문구 휴머나이즈 — AI 티 제거 (★ 조판 전 텍스트 확정 단계 · `REFERENCE/humanize-deck-copy.md`).** 장표에 들어가는 **산문 텍스트**(STRATEGY 비트 문단·컨셉 설명·섹션 리드문·브리지·클로징·발표 스크립트 6.1)는 **쓸 때부터** 휴머나이즈 룰북을 적용해 자연스러운 한국어로 쓴다 — 번역투(A: "~를 통해"·"~에 있어"·"~에 의해"·이중피동), AI 관용구(D: "결론적으로"·"시사하는 바가 크다"·hype 어휘 남발), 명사화 체인(F: "전략적 함의"), hedging(G: "~할 수 있을 것이다" — 장표는 단언), 문두 접속사 남발(H), 형식명사 결말(I: "~인 것이다"), 콜론 부제 헤딩 반복(C-10). 조판(4.2-a typeset) 직전 **자가 스캔으로 S1 패턴 잔존 0건**을 확인하고, 발견 시 그 문구만 재작성한다. **보존 경계(절대 안 건드림):** planner가 확정한 카피 원문(헤드라인·태그라인·CTA — 의도적 대구·반복·리듬은 카피 *기법*이지 AI 티가 아니다), 브랜드명·제품명·수치·가격·법적 고지·직접 인용, 영문 vocabulary 토큰(제작 페이지). 룰 전문 + 장표 프로파일 + 예문: `REFERENCE/humanize-deck-copy.md`.

**4.3 브랜드 컬러 적용.** 1순위 펀치라인·헤드라인, 2~4순위 강조·구분선. hex 그대로(어림짐작 금지). 브랜드 자산 PDF 있으면 열어 정확 hex 추출. (블록당 1강조는 4.2-a typeset이 관장.)

**4.4 Write 24KB 한도 우회.** 빌드 스크립트 24KB 넘으면 bash heredoc로 분할 작성하거나 함수 분리 import. 큰 파일 수정 시 bash python in-place patch.

**4.5 트랜지션 페이지 주의.** 영상 종횡비 유지한 작은 프레임. 9:16이면 패널 9:16(`fh=298; fw=int(fh*9/16)`).

### Phase 5 — QA & 정리

**⓪ 논리 QA (우선 — `REFERENCE/deck-logic.md` §3):** (1) 컷 0장 보고도 "왜 이 광고인지" 한 문장 답 가능? (2) 컨셉이 인사이트에서 도출? (3) 브랜드를 경쟁사로 바꾸면 말 안 되나(정당성)? (4) 평가기준 각 항목에 논리가 닿나? (5) 비트가 "그래서/즉"으로 연결? — 하나라도 실패 시 빌드 보류.

그다음 PDF 출력 전 자동 점검: ① 컷 매칭(전 컷 슬라이드 포함) ② 카피 오타(PDF 텍스트 추출 → plan.md diff) ③ 브랜드 컬러 hex 픽셀 샘플링 ④ 한국어 폰트 깨짐(Tofu ■ 검사) ⑤ 슬라이드 비율 16:9 ⑥ 파일 크기·페이지수. 문제 슬라이드만 재렌더. 통과하면 `treatment.pdf`를 최상단에 두고 `computer://`로 공유.

**⑦ 겹침 게이트 (필수 · 코드 강제):** 텍스트가 패널·이미지를 침범하면 빌드 보류. 각 텍스트 박스 rect와 패널/이미지 rect를 모아 `T.assert_no_overlap(text_rects, blocker_rects)` 호출(`build_treatment_template`) — 통과해야 PDF 출력. 헤드라인은 그 전에 `T.fit_headline()`으로 컬럼폭(=패널 시작 − 여백) 안에 자동 축소해 침범 자체를 차단(§5번 결함 재발 방지).
**⑧ 폰트 하한 (Q6 · 범위 한정):** `T.assert_font_floor(page_type, role, size)` — **광고주/텍스트-주인공 페이지만** 적용(client/text_hero). **제작 8블록 페이지는 면제**(`page_type='production'`, 소폰트 의도적).
**⑨ typeset 경유 확인:** 텍스트-주인공 페이지 카피가 한 덩어리/글자단위 줄바꿈이 아니라 `T.typeset()`을 거쳤는지(줄 수·강조 1개·크기 위계 존재) 확인.
**⑩ 이미지 의무 게이트 (필수 · 코드 강제):** 표지·키비주얼·컷보드·씬 페이지에 `T.assert_images_present(page_kind, placed_flags)` — 실제 합성 이미지 0장(플레이스홀더만)이면 빌드 보류. "그라데이션 위 텍스트만"인 평면 슬라이드 차단.
**⑪ 4K 확인:** 출력 페이지가 3840×2160인가(`SCALE=2`)? 1080p로 떨어지지 않았나.
**⑫ 어두움 과다 점검:** 콘텐츠·보드 페이지가 전부 다크 BG면 크림 surface(카드/보드 면)로 호흡을 준다(리디자인 대비 — 정보 페이지는 크림, 임팩트/표지/KV는 다크/풀블리드).
**⑬ 문구 휴머나이즈 게이트 (4.2-b):** STRATEGY 비트·컨셉 설명·리드문·클로징·발표 스크립트의 산문에서 **S1 패턴 잔존 0건** 스캔 — AI 관용구(D-1~D-7)·"가지고 있다"/이중피동(A-7·A-8)·문두 접속사 5회+(H-1)·"~인 것이다" 결말(I-1)·콜론 부제 헤딩 반복(C-10) 등. 발견 시 해당 문구만 재작성 후 재렌더. **카피 원문·수치·고유명사는 불가침**(`REFERENCE/humanize-deck-copy.md` §1).

### Phase 6 — 광고주 프레젠테이션 패키지

Phase 5 후: **6.1** 1분 발표 스크립트(`treatment_client_pitch.md`, 7단계 시간 마킹 — 입말이므로 4.2-b 휴머나이즈 특히 엄격히). **6.2** 핵심 컷 스틸 패키지(`hero_stills/`, 와우컷+표지+키비주얼+클로징 6~8장). **6.3** PDF 옵션 3종(`treatment.pdf` 합본 / `treatment_client.pdf` / `treatment_internal.pdf`). 광고주엔 보통 client + pitch + hero_stills.

**6.4 산출물 최종 패키지:**
```
{프로젝트명}/
├── treatment.pdf / treatment_client.pdf / treatment_internal.pdf
├── treatment_client_pitch.md
├── plan.md
├── treatment.json
├── hero_stills/
├── assets/ (master_4k.png, board*_*.png, transition_T*_*.png)
├── frames/
├── 확정컷/
├── fonts/ (BlackHanSans.ttf, NotoSansKR.ttf)
└── build_treatment.py
```

### Phase 7 — 영상화 → 별도 스킬 `lsb-video-crafter`로 이관 [선택 · "영상으로 뽑아줘" 요청 시]

확정컷을 모션 영상으로 만드는 단계는 **`lsb-video-crafter` 스킬**이 담당한다(이 스킬이 비대해져 분리). builder는 PDF 장표 본업. 영상화 요청이 오면 `lsb-video-crafter`를 트리거하고 산출물(treatment.json·확정컷·인물별 마스터시트·product-lock 제품 이미지)을 그대로 넘긴다. 거기서 다룬다: 다중 인물·교차편집 클립 분할 / 인물·공간별 reference / 4000단어 프롬프트·CRITICAL 비트 / 한국어 VO·모션타이포 / Seedance 운용·declined_preset 체인 / **ip_detected = 알림→중단→사용자 허용→재개(자동 재시도 금지)** / concat 픽셀포맷 강제 / frame-level QA.

## 데이터셋이 있는 경우 — Cross-pollination로 디자인 톤 끌어오기

데이터셋(`<DATASET>/entries/ADV-*.json`)이 있으면 Phase 1.2(deck style) + 4.1(타이포·컬러) + 4.2(구조)에서 끌어 쓴다.

**실물 우수 트리트먼트 예시:** `<LIBRARY>/003_reference_decks/`(README 색인). 톤 트랙별 1종(서비스·펀=배민클럽 / 시네마틱 세로=KT Y 버퍼링없는사람 / 감성 드라마=Y 무대뒤3초). 새 덱 톤이 정해지면 **가장 가까운 예시의 시그니처(배경·단일 포인트컬러·한글 대형+영문 키커·의미단위 헤드라인·여백)를 학습**하되 픽셀 복제 금지.

**원칙:** 픽셀을 베끼지 않는다. 끌어오는 건 추상화된 시그니처(레이아웃 그리드·타이포 무게·컬러 의도·슬라이드 흐름) + 시각 인벤토리/recreation_prompts(영감으로). **가중치**(§4.3): 동일 0.2 / 인접 0.5 / 원거리 1.0 / 대조 1.2. **와우컷 하드밴.** 판정 맵 단일 출처 = `lsb-ad-planner/schema.md` §3.

**예:** 통신사 트리트먼트면 → 통신(0.2 약) / 은행·보험(0.5) / 패션·뷰티 KV(1.0) / 산업 B2B(1.2 강).

**retrieval 코드 (참고용):**
```python
# ⚠ 주의: 아래 e['meta']['category'] / e['global']['signature_strength']는 구버전 잔재로
# 현재 entry 스키마엔 없다(각각 e['category_primary'], 그리고 signature_strength는 부재).
# 동작에 의존하지 말 것. 카테고리 판정은 e['search_keywords']['industry'](영문 토큰) +
# lsb-ad-planner/schema.md §3 맵 기준으로. (요청에 따라 기존 코드는 삭제하지 않고 보존.)
import json, glob
def cross_pollinate(entries_dir, target_category, top_n=5):
 candidates = []
 for path in glob.glob(f"{entries_dir}/ADV-*.json"):
 e = json.load(open(path, encoding='utf-8'))
 cat = e.get('meta', {}).get('category', 'unknown') # (구버전) → e['category_primary'] 권장
 weight = {target_category: 0.2}.get(cat, 1.0)
 if cat in ADJACENT_MAP.get(target_category, set): weight = 0.5
 if cat in CONTRAST_MAP.get(target_category, set): weight = 1.2
 if e.get('global', {}).get('signature_strength', 0) >= 4: continue # (구버전) 와우컷 하드밴
 candidates.append((weight, e))
 candidates.sort(key=lambda x: -x[0])
 return [c for _, c in candidates[:top_n]]
```
데이터셋이 없으면 §1.2 5개 카탈로그를 메뉴로. 데이터셋이 커지면 카탈로그는 점차 데이터셋 retrieve로 이동.

## 자주 묻는 것 & 자주 망하는 것
- **컷부터 멋지게, 이유는 나중** → 트리트먼트는 설득 문서다. STRATEGY(왜)를 컷보다 먼저(`REFERENCE/deck-logic.md`). 컷이 표지 다음 바로 나오면 실패.
- **카피를 한 덩어리로 박고 글자 단위로 줄바꿈** → "정보는 맞는데 안 예쁜" 슬라이드. 의미 단위로 끊고 핵심구 1개만 색·크기로 띄운다(`REFERENCE/text-setting.md` typeset, Phase 4.2-a).
- **마스터시트를 왜 따로?** 첫 컷은 "그 컷 의미"에 맞춰 변형돼 기준점이 흔들림. 마스터시트는 의미 없는 중립 컷이라 reference로 안정적.
- **27 슬라이드 꼭?** 권장이지 강제 아님. **한 페이지 한 메시지**가 핵심.
- **슬라이서가 패널을 잘못 자름** → "thin white gutter, equal width" 명시 + `colw` 0.75~0.88 튜닝.
- **한국어 두부(■)** → Noto Sans KR variable로 교체, cmap 검증.
- **PPTX 변환 시 폰트 깨짐** → fonts/ 동봉 + 설치 안내.
- **의도와 다른 인물** → 마스터시트 reference 빠짐/충돌. medias 단일화.
- **플래너가 안 만든 컷 필요** → 플래너로 돌아가 보강하거나 사용자에게 "이 컷 추가 가능?" 묻고 plan.md에 박은 뒤 빌드. **이 스킬이 임의로 컷을 늘리지 않는다.**

## 트리거 키워드
"기획안 PDF 만들어줘" / "트리트먼트 짜줘" / "양반김·우리은행 식으로" / "이 컨셉으로 장표" / "캐릭터시트+콘티+장표 한 번에" / "lsb-ad-planner 출력 PDF로". 컨셉을 새로 잡거나 후보 N안 요청이면 이 스킬이 아니다 — `lsb-ad-planner`로.

> **전략 논리의 *원천*은 planner(컨셉·인사이트·strategy_spine)다. builder는 그것을 논리적 발표 구조(STRATEGY 섹션)로 *렌더*할 뿐 새 전략을 지어내지 않는다. 단, 입력에 strategy_spine이 비면 사용자와 함께 채운 뒤 진행(빌드 게이트).**

## 함께 읽어야 할 보조 문서
- `REFERENCE/keyword-vocabulary.md` — 사고법·카피·키워드 분류(§8).
- `REFERENCE/cut-schema.md` — 컷 30+ 필드 + 시각 인벤토리 + recreation_prompts 정의 + 영문 vocabulary.
- `REFERENCE/transitions.md` — 트랜지션 단일 캔버스 원칙·분기 룰.
- `REFERENCE/vfx-in-board.md` — VFX 인-보드 시각화.
- `REFERENCE/client-vs-internal.md` — 광고주 vs 제작 페이지·7단계 인지 경로.
- `REFERENCE/deck-styles.md` — 양반김·우리은행·신세계·KG·G-EYE 디자인 시그니처.
- `REFERENCE/deck-logic.md` — **기획 논리 척추(7비트)·STRATEGY 렌더·논리 QA·안티패턴 (모든 트리트먼트 범용).**
- `REFERENCE/presentation-rules.md` — **34종 역설계: 용도×톤 트랙·공통 문법 12·페이지당 이미지 수 결정표·카피 규칙.**
- `REFERENCE/typography-in-image.md` — **타이포 3분류(none/subtitle/baked)·데이터셋 판정·baked 프롬프트 (Phase 3.2 'no text' 대체).**
- `REFERENCE/editorial-layout.md` — **트리트먼트 기본 디자인 시스템: 4K 캔버스·팔레트 토큰(크림 surface)·레이아웃 아키타입(cover_split/two_col/fullbleed_kv/cut_board)·이미지 의무 (코덱스 리디자인급 기본값). Phase 4.1-에디토리얼.**
- `REFERENCE/text-setting.md` — **덱 카피 조판 typeset 시스템: 의미단위 줄바꿈·포인트컬러 1강조·역할별 크기 위계·center/left 스마트 정렬 (Phase 4 텍스트 렌더 — 글자단위 줄바꿈 대체).**
- `REFERENCE/humanize-deck-copy.md` — **장표 문구 휴머나이즈: 한글 AI-티 패턴(번역투·AI 관용구·명사화·hedging·접속사) 탐지·회피 룰북 + 카피 보존 경계 + 장표 장르 보정 (Phase 4.2-b · 게이트 ⑬ · 6.1 피치 스크립트). 출처: epoko77-ai/im-not-ai v2.0 (MIT).**
- `REFERENCE/scene-boards.md` — 멀티패널 보드 설계·슬라이스.
- `REFERENCE/layered-collage-protocol.md` — **레이어드 콜라주(베이스 위 조각 겹침) 3단 분리: 개별 생성→프리뷰 합성→영상 레이어 모션 (analyzer·video-crafter 공유 단일 출처).**
- `REFERENCE/deck-build.md` — PIL 빌더 폰트·캔버스·24KB 우회.
- `REFERENCE/keyword-vocabulary.md` — 영문 토큰 + KO 별칭(분류 태그 표준).
- `scripts/slice_boards.py` / `build_treatment_template.py` / `cut_template.json` / `treatment_global_template.json` / `transition_template.json`.
- `prompts/master_character.md` / `scene_board.md` / `transition_board.md`.
- (cross-pollination 맵·analyzer→treatment 매핑: `lsb-ad-planner/schema.md` §3·§5. 컷 시작프레임 t2i/i2v: `lsb-ad-analyzer/REFERENCE/frame-recreation-prompts.md`.)

---
*버전: lsb-treatment-builder_2606101200 · 2026-06-10 KST. (_2606101200 = ① **3.3 그리드 프리셋 폴백** — 갭 감지 실패·경계 어긋남(±3%↑) 시 정확 4등분 고정 프리셋 슬라이스, 셀 내용 잘린 그리드는 재생성(3.2 프롬프트에 quadrant·no-cropping 예방 문구) ② **3.4 32MB 페이로드 상한** — 이미지·PDF base64 인라인 절대 금지, 파일 경로·UUID·URL 참조만(플랫폼 요청 32MB 고정).) 이전 _2606101000 = ① **Phase 1.1-b 컷 문법 게이트 재검증**(planner R10 이중 방어 — 같은 피사체·공간 인접 쌍에 사이즈 2단계+/앵글 30도+/피사체·공간·시간 변경 중 1 미충족이면 더블 위반 → seamless 전환 교체 또는 병합 제안, 위반 채로 Phase 3·4 진입 금지) ② **Phase 4.2-b 문구 휴머나이즈**(장표 산문 텍스트에 한글 AI-티 제거 룰 — 번역투·AI 관용구·명사화·hedging·접속사·형식명사, 카피 원문·수치·고유명사 보존) + **Phase 5 게이트 ⑬**(S1 잔존 0) + 6.1 피치 스크립트 적용 + `REFERENCE/humanize-deck-copy.md` 신규(출처 epoko77-ai/im-not-ai v2.0 MIT).) 이전 lsb-treatment-builder_2606081200 · 2026-06-08 KST. (_2606081200 = 컷 생성 기본 2×2 그리드(한 장 4컷·2K)→3.3 슬라이스로 컷 분리, 장표엔 분리본만 사용 / 셀(컷)당 묘사 최소 500단어 강제 / 3.4 생성이미지·PDF Read 검수 금지 — 프로그램·사용자 판정만(413·토큰 방지).) 이전 _2606051640 · 2026-06-05 16:40 KST. (_2606051640 = Phase 3.2-c 이미지 생성 셋업 고정 — model=gpt_image_2 · resolution=2k · quality=high(기본 1k/low 금지, nano_banana 폴백 금지) · 사용자 레퍼런스 media_upload→medias 사용; 다운로드 블록은 3.2-d로 이동.) 이전 _2606051140 = Phase 3.2-d(구 3.2-c) 생성 이미지 로컬 다운로드 강제 — PIL은 URL을 못 여니 assets/로 받은 뒤 로컬 경로만 사용, verify로 빈/깨진 파일 차단; Phase 4.1 'URL 직접 사용 금지' 명시. 동기: 힉스필드 생성 URL을 PDF 빌드(PIL)에 직접 넣어 이미지 삽입 실패.) 변경 내역은 적용방법.md 참조. (_2606041330 = **에디토리얼 레이아웃 시스템(코덱스 리디자인급 기본값)**: build_treatment_template §8 — 4K(3840×2160) 기본 + 아키타입 cover_split/two_col/fullbleed_kv/cut_board + 팔레트 토큰(크림 surface) + 이미지 의무 게이트 assert_images_present + REFERENCE/editorial-layout.md. 동기: 클로드 1차 빌드가 1080p·이미지없는 중앙정렬 텍스트 덤프 → 코덱스 리디자인 불필요하게. 이전 _2606031952 = typeset 코드 강제. _2606032044 = 다중 인물·교차편집(A3): Phase 1.4·2.0·3.2·3.3-a + Phase 7 lsb-video-crafter 분리.)*
