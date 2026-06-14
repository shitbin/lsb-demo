# Cut Schema — 컷별 풀 필드 정의 (lsb-treatment-builder_2606021505)

## 왜 풀 필드인가

영상 한 컷은 "스틸 한 장 + 카피"가 아니다. 컷 하나에 **카메라·인물·소품·타이포·VFX·컬러·트랜지션**의 모든 결정이 들어 있다. "SCENE/COPY/NOTE 3블록"으로만 적으면 후속 제작자(촬영·CG·편집)가 빠진 정보를 추측해 채워야 하고 의도가 흐려진다.

따라서 트리트먼트 컷 데이터는 **`lsb-ad-analyzer` entry의 shots 항목과 동일 스키마**로 적는다. 그래야: (1) 한 페이지에 모든 의사결정 명시, (2) cross-pollination 1:1 매핑, (3) 완성 후 retro-analyzer로 다시 entry 등록 가능, (4) 후속 제작자가 컷 페이지만 봐도 판단 가능.

> analyzer entry와 treatment는 **키 이름이 일부 다르다**(예: total_duration→total_duration_sec). 변환은 `lsb-ad-planner/schema.md` §5 매핑표를 따른다. 아래 컷 필드는 대부분 동일 키다.

## 컷 데이터 풀 스키마 (필수 + 권장 + 선택)

### 식별·길이·기능 (필수)

| 필드 | 타입 | vocabulary / 예시 | 설명 |
|------|------|-------------------|------|
| `index` | int | 1, 2, 3,... | 컷 순서 |
| `no` | string | "C1", "C2A", "C2B" | 표시용 컷 번호 (분기 컷 알파벳 접미) |
| `duration` | float | 1.73 | 컷 길이 (초) |
| `framing` | string | WS / LS / MLS / MS / MCU / CU / ECU / grid / environment | 샷 사이즈 |
| `function` | string | hook / concept / rhythm / benefit / refrain / wow / wrap / payoff / ending / disclaimer | 이 컷의 역할 |

### 인물·동작 (권장)

| 필드 | 타입 | vocabulary / 예시 |
|------|------|-------------------|
| `subject_identity` | string | protagonist_main / cafe_customer_A / cafe_barista / background_crowd / none_environment | **이 컷의 인물 = planner `character_pool`의 id.** 다중 인물 영상 필수 — 빠지면 모델이 전부 주인공으로 간주(A3 카페 결제 사고) |
| `subject_role_in_narrative` | string | main_character / supporting_character / extra_atmosphere | 서사 내 인물 역할 |
| `subject_position` | string | center / left / right / off / varies |
| `subject_action` | string | 자유 한 줄 |
| `subject_motion` | string | 정지포즈 / 미세제스처 / 워킹 / 댄스 / 격동 |
| `pose_description` | string | 자유 한 줄 |
| `gaze` | string | to_camera / off_camera / at_product / at_subject / down / none |
| `eye_contact_effect` | string | 자유 한 줄 |

### 카메라 (권장)

| 필드 | 타입 | vocabulary / 예시 |
|------|------|-------------------|
| `camera_motion` | string | locked_off / slow_dolly / handheld / tracking / push_in / pull_out / pedestal / slide / cut_montage |
| `camera_motion_intensity` | string | none / subtle / moderate / fast / heavy |
| `camera_angle` | string | eye_level / low_angle / high_angle / overhead / dutch / worm_eye |
| `camera_facing` | string | frontal / three_quarter / profile / back / overhead / none |
| `shot_scope` | string | face_only / bust / waist_up / full_body / environment / grid_cell |
| `camera_effect_local` | string | none / wiggle_3d / parallax / vibration / lens_flare / vignette / chromatic_aberration |
| `motion_blur` | string | none / light / moderate / heavy |

### 컷 내부 리듬·트랜지션 (필수)

| 필드 | 타입 | vocabulary / 예시 |
|------|------|-------------------|
| `intra_cut_rhythm` | string | static / steady / accelerating / decelerating |
| `transition_in` | string | cut / match_cut / fade / dissolve / whip_pan / morph / wipe |
| `transition_out` | string | (위와 동일) |

### 소품·세트 (권장)

| 필드 | 타입 | vocabulary / 예시 |
|------|------|-------------------|
| `props` | string[] | ["스마트폰", "커피잔", "튤립 꽃병"] |
| `prop_motion` | string | none / 들어올림 / 회전 / 떨어뜨림 / 이동 |
| `prop_semantics` | string | 자유 한 줄 |

### 컬러 (권장)

| 필드 | 타입 | vocabulary / 예시 |
|------|------|-------------------|
| `color_mood` | string | warm_on_blue / cool_blue / bright_blue / desat_cool / golden / neon |
| `color_palette` | string[] | ["#6ab3cb", "#29282d", "#dfcac2"] (HEX 4~6색) |
| `color_intent` | string | 자유 한 줄 |

### 타이포·자막 (권장 — 자막 컷만)

| 필드 | 타입 | vocabulary / 예시 |
|------|------|-------------------|
| `copy_overlay` | string\|null | "원영이처럼 우월한 월급통장" / null (화면 카피 **원문 보존**) |
| `layout_grid` | string | rule_of_thirds_center / _left / _right / center / split / split_3x3 |
| `subject_typo_layout` | string\|null | 자유 (예: "인물 중앙, 타이포 우측 1/3 컬러박스") |
| `typo_motion` | string\|null | pop / scale_in / slide_in / fade_in / kinetic / bounce / balloon_pop / fade_scale_out / glitch_in / static |
| `typo_color_strategy` | string\|null | 자유 (예: "브랜드 블루+화이트, 핵심어 옐로 컬러박스") |

### VFX (선택 — 있는 경우만)

| 필드 | 타입 | vocabulary / 예시 |
|------|------|-------------------|
| `vfx_in_shot` | string[] | ["wiggle_3d", "color_pop", "3d_render", "split_screen", "ui_motion"] |
| `vfx_intensity_local` | string | none / subtle / moderate / heavy |
| `vfx_in_board_prompts` | object | 보드 생성 시 패널 묘사에 결합할 VFX 텍스트 |

### 시각 인벤토리 (이미지/보드 생성 입력)

analyzer가 채워 두는 값. builder는 Phase 3 보드 프롬프트에 결합해 톤·질감·조명·색을 고정한다. cross-pollination 참조 entry의 같은 필드는 *영감*으로(픽셀 복제 금지).

| 필드 | 타입 | 설명 |
|------|------|------|
| `visible_elements` | object | 5층: foreground / midground / background / lighting_env / atmosphere — 화면 내 모든 요소 |
| `texture` | object | primary_subject / secondary_objects[] / background_surface / atmospheric[] — 표면 질감 (영문 vocab: matte/glossy/glass_*/fabric_*/wood_*/concrete/skin_*/plastic_* 등) |
| `lighting` | object | key_direction / key_hardness / key_color_temp / fill_strength / key_to_fill_ratio / rim_light / practical_lights[] / shadow_presence / overall_contrast |
| `color_analysis` | object | palette_hex[] / palette_role{} / color_relationship / temperature_balance / saturation_strategy / contrast_type / accent_color / accent_ratio / brand_color_match[] |
| `style_prompt` | string\|null | 핵심 컷(hook/cta/key_visual/brand_endcard/wow)용 한 줄 영어 프롬프트. 셀럽 *얼굴 사진복제*·실제 로고 마크 제외(자막·카피 원문은 보존) |

### 프레임 복제 (컷 시작프레임 t2i + i2v 모션)

모든 컷에 보존. 정의·12파트 t2i 구조·i2v 매핑·예시·경계는 `lsb-ad-analyzer/REFERENCE/frame-recreation-prompts.md`.

| 필드 | 타입 | 설명 |
|------|------|------|
| `recreation_prompts` | object | `t2i_start_frame`(~300단어) · `t2i_negative` · `i2v_motion` · `i2v_params`(clip_duration_sec/camera_move/subject_motion_level/signature_effect/pacing/loopable) · `fidelity_note` |

> **경계:** 자막·카피 원문 **보존**(짧은 카피·수치 verbatim, 장문 고지만 excerpt). 셀럽 *얼굴 사진수준 복제*·실제 *로고 마크*만 generic(초상·상표). craft(구도·렌즈·조명·색·모션)는 충실히.

### 메타 (선택)

| 필드 | 타입 | vocabulary / 예시 |
|------|------|-------------------|
| `wow_cut` | bool | true / false |
| `fact_check_flag` | bool | true / false |
| `notes` | string | 자유 |
| `source_refs` | string[] | ["ADV-2026-001#shot5"] (cross-pollination 참조 추적) |
| `still_path` | string | PDF 빌드 스틸 경로 |

## 컷 데이터 JSON 예시 (한 컷, 발췌)

```json
{
 "index": 5, "no": "C5A", "duration": 1.5, "framing": "MS", "function": "wow",
 "subject_position": "center", "subject_action": "주인공이 멈춘 횡단보도에서 카메라 응시",
 "subject_motion": "정지포즈", "pose_description": "한 발 든 자세 그대로 정지", "gaze": "to_camera",
 "camera_motion": "slow_dolly", "camera_motion_intensity": "subtle", "camera_angle": "eye_level",
 "camera_facing": "frontal", "shot_scope": "waist_up", "camera_effect_local": "none", "motion_blur": "none",
 "intra_cut_rhythm": "static", "transition_in": "match_cut", "transition_out": "match_cut",
 "props": ["스마트폰"], "prop_motion": "none", "prop_semantics": "데이터 바닥난 폰",
 "color_mood": "cool_overcast", "color_palette": ["#1a3a52", "#11E6D8", "#f0f0f0", "#2a2a2a"],
 "color_intent": "시간정지 쿨톤 + 카고팬츠 민트가 유일한 채도 포인트",
 "copy_overlay": null, "layout_grid": "rule_of_thirds_center", "typo_motion": null,
 "vfx_in_shot": ["time_freeze"], "vfx_intensity_local": "moderate",
 "visible_elements": {"foreground": ["주인공"], "midground": ["정지한 행인"], "background": ["횡단보도·신호등"], "lighting_env": ["흐린 자연광"], "atmosphere": ["아침 습기"]},
 "texture": {"primary_subject": "fabric_cotton", "secondary_objects": ["concrete"], "background_surface": "concrete", "atmospheric": ["atmospheric_haze"]},
 "lighting": {"key_direction": "top", "key_hardness": "soft", "key_color_temp": "cool_7000K", "fill_strength": "moderate", "key_to_fill_ratio": "2:1", "rim_light": false, "practical_lights": [], "shadow_presence": "soft", "overall_contrast": "mid_key"},
 "color_analysis": {"palette_hex": ["#1a3a52", "#11E6D8", "#f0f0f0", "#2a2a2a"], "palette_role": {"#11E6D8": "accent_brand_mint"}, "color_relationship": "monochrome_with_pop", "temperature_balance": "cool_dominant", "saturation_strategy": "desaturated_with_pop", "contrast_type": "luminance_mid", "accent_color": "#11E6D8", "accent_ratio": "5_percent", "brand_color_match": ["mint #11E6D8"]},
 "recreation_prompts": {
 "t2i_start_frame": "<~300단어, frame-recreation-prompts.md 12파트 구조>",
 "t2i_negative": "real brand logos/marks, second person, deformed face, grain, watermark",
 "i2v_motion": "<원본 컷 모션 — 주변 정지, 주인공만 alive, slow dolly, ~1.5s>",
 "i2v_params": {"clip_duration_sec": 1.5, "camera_move": "slow_dolly", "subject_motion_level": "still", "signature_effect": "none", "pacing": "static", "loopable": false},
 "fidelity_note": "craft-faithful; on-screen copy preserved verbatim; celeb face-likeness & logo mark generic"
 },
 "wow_cut": true, "fact_check_flag": false, "notes": "C5B와 같은 순간 다른 카메라 — 같은 보드 생성.",
 "source_refs": [], "still_path": "/{프로젝트}/확정컷/06_C5A_시간정지-와이드.png"
}
```

## 글로벌 메타 (treatment 전체 한 번만)

`scripts/treatment_global_template.json` 키와 1:1. analyzer 글로벌과의 키 변환은 `lsb-ad-planner/schema.md` §5 (예: total_duration→total_duration_sec, typography→typography_global, vfx→vfx_global, inferred_creative_thinking→client_perception_path).

## Vocabulary 상세 — 헷갈리기 쉬운 것

### framing
ECU(눈·입) / CU(얼굴) / MCU(얼굴+가슴) / MS(허리 위) / MLS(무릎 위) / LS(전신 포함) / WS(인물+배경) / EWS(풍경 우위) / grid(분할화면) / environment(인물 없는 환경·제품).

### camera_angle
eye_level(중립) / low_angle(위엄·우월) / high_angle(취약·왜소) / overhead(탑다운·객관) / dutch(불안·위트) / worm_eye(영웅·과장).

### typo_motion
pop(작게→크게 펑) / scale_in(크게→정상) / slide_in / fade_in / kinetic(글자 하나씩·회전) / bounce / balloon_pop(3D 풍선) / fade_scale_out(슬로건 마무리 회수) / glitch_in / static.

### vfx_in_shot
wiggle_3d(좌우 미세 시점 떨림) / parallax / color_pop / 3d_render / ui_motion / split_screen / time_freeze / morph / whip_pan / lens_flare / dust_simulation / glitch / atmospheric_haze / rim_light / light_reveal / data_viz / speed_ramp.

### transition (in/out)
cut / match_cut / match_action / fade / dissolve / whip_pan / morph / wipe / push_in / pull_out / 360_spin / dolly_through.

## 컷 데이터 작성 순서 (실무)
1. 5필수(index·no·duration·framing·function). 2. 인물·소품(subject_action·pose·props·prop_semantics → 보드 가능). 3. 카메라(angle·facing·scope·gaze·motion → 촬영 셋업). 4. 트랜지션·리듬(편집 흐름). 5. 컬러·타이포(디자이너). 6. VFX·시각 인벤토리(visible_elements·texture·lighting·color_analysis → CG·이미지 생성). 7. recreation_prompts(t2i/i2v). 8. 메타.
빠진 필드는 추측 말고 사용자에게. 특히 카메라·전환·타이포 모션은 비워두면 안 된다.

## analyzer entry와의 매핑
`lsb-ad-analyzer` entry의 `shots[i]`와 트리트먼트 컷은 **대부분 동일 키 = 동일 의미**(차이·변환은 planner/schema.md §5). 시각 인벤토리 5축 + `recreation_prompts`도 동일 키로 carry-through된다. 그래서 cross-pollination으로 참조 entry의 해당 필드를 영감으로 끌어와 새 컷을 디자인하기 쉽고, 제작 후 retro-analyzer로 의도 vs 실현을 같은 스키마로 비교할 수 있다.

## 컷 페이지(PDF) 8블록 레이아웃
좌측 ⅔ 스틸 + 우측 ⅓ 4블록(SCENE·COPY·CAMERA·VFX) + 하단 가로 3등분(PROPS·COLOR·TRANSITION). 한 페이지 = 한 컷 = 한 의사결정 묶음. 후속 제작자가 자기 영역 블록만 빠르게 읽는다.
