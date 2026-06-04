# 씬 보드 (멀티패널) 프롬프트 템플릿

같은 씬의 N개 컷을 한 캔버스에 그려서 배경·조명·동선 일관성을 확보한다.
같은 보드에서 슬라이스된 N개 컷은 서로 같은 세계관 안에 있다.

## 핵심 원칙

1. **N개 패널을 가로로 배치, 같은 폭, 얇은 흰 갭.**
 - 갭이 명확해야 슬라이서가 정확히 자른다.
 - GPT는 종종 패널 사이를 까만색이나 그라데이션으로 채우는데, 명시적으로 "white gutter"를 박지 않으면 슬라이서가 헤맨다.

2. **패널마다 별도 묘사.**
 - "Panel 1: ... | Panel 2: ... | Panel 3: ..." 형식.
 - 패널마다 카메라·동작·배경을 따로 적는다.

3. **마스터 캐릭터시트를 reference로 건다.**
 - 인물 일관성의 근간. 빼면 매번 다른 사람이 나온다. (실존 셀럽 얼굴을 사진수준으로 복제하지 않는다 — 마스터시트는 스튜디오 자체 모델/탤런트 유형.)

4. **절대 금지 텍스트·낙서.**
 - "ABSOLUTELY NO handwriting, NO labels, NO annotations, NO storyboard markings, NO timecode burn-ins."
 - GPT는 "advertising treatment"를 보면 자동으로 스토리보드 주석을 그려넣는다. 막아야 한다.
 - (자막/카피는 별개 — 7·10번 참조. 보드 단계에선 보통 텍스트를 후처리로 얹지만, 패널 묘사·plan엔 자막 원문을 보존한다.)

5. **종횡비.**
 - 9:16 영상이면 패널 자체가 9:16. 전체 캔버스는 9:16 × N (가로).
 - Higgsfield 종횡비 캡(보통 16:9 한계)에 걸리면 패널 수를 줄이거나 16:9로 받고 슬라이스 단계에서 9:16으로 center-crop.

6. **시각적 비유 함정 회피.**
 - "회색 돌처럼 굳은 사람들" 같은 비유는 실제로 그려보면 시체·NPC처럼 보여 미적으로 망한다.
 - 시간정지·동결을 원하면 색은 정상, 동작만 멈춘 모습 — "alive, normal, just paused mid-motion".

7. **패널 묘사는 구조화된 풀필드로 (가장 중요).**
 - "Panel 1: 횡단보도 와이드샷" 같은 한 줄 묘사 금지. 그렇게 적으면 GPT가 빠진 결정을 자기 마음대로 채워 매번 다른 결과가 나오고 일관성이 깨진다.
 - 패널마다 framing / camera_angle / camera_facing / shot_scope / subject_action / pose / gaze / props / layout_grid / color_intent / vfx 필드를 모두 박는다 — **analyzer vocabulary(영문 토큰)** 사용.
 - 이 풀필드 묘사는 영상화 시 촬영팀이 그대로 받아쓸 수 있어야 한다.

8. **VFX도 보드 단계에서 시각화 (광고주가 5초로 이해하게).**
 - 후처리 VFX(time_freeze, color_pop, lens_flare, dust, glitch 등)는 보드 프롬프트에 *시각 묘사 한 줄*로. "post-production에서 추가" 같은 추상 표현 금지.
 - 시간 의존 효과(wiggle_3d 등)는 단일 이미지로 직접 표현 불가 — 깊이감·패럴랙스 의도로 시각화. 자세히: REFERENCE/vfx-in-board.md.
 - 텍스트·숫자가 들어가는 VFX(3D 풍선 타이포 등)는 보드에 *모양만* 그리고 텍스트는 후처리(원문은 plan에 보존).

9. **트랜지션은 별도 — 단일 캔버스 보드.**
 - 화려한 카메라 무빙(whip_pan, morph, push_in/pull_out 강한 것, 360_spin, match_action, dolly_through) 트랜지션은 **씬보드와 다른 별도 보드**.
 - 이전컷 끝 + 트랜지션 정점 + 다음컷 시작을 하나의 캔버스에 동시 생성.
 - 자세히: prompts/transition_board.md + REFERENCE/transitions.md.

10. **컷의 시각 입력을 패널 묘사에 결합 (신규 — 일관성의 핵심).**
 - 컷에 `recreation_prompts.t2i_start_frame`(또는 `style_prompt`)이 있으면 그 프롬프트를 **패널 묘사의 베이스**로 쓴다. 단 셀럽 *얼굴 사진복제*·실제 로고 마크는 제외(유형으로), **자막·카피 원문은 보존**.
 - `lighting`(key_direction/hardness/color_temp/ratio) → 패널 조명, `texture`(표면 질감) → 패널 질감, `visible_elements`(foreground/midground/background/lighting_env/atmosphere) → 패널 요소, `color_analysis`(palette·accent) → 패널 색을 각 패널 필드로 풀어 넣는다.
 - 이게 빠지면 같은 컨셉이어도 보드마다 톤·질감·조명이 달라진다.
 - 영상화(i2v) 단계에선 `recreation_prompts.i2v_motion` + `i2v_params`로 슬라이스 스틸을 컷 모션으로 움직인다(보드 생성과 별개 단계).

## 프롬프트 골격

```
A horizontal storyboard panel sequence for an advertising treatment.
{N} panels of equal width, separated by thin white gutters (4-8 pixels between panels).

Setting / location:
[LOCATION — time of day, weather, ambience].

Style:
- Cinematic photographic look, 4K quality.
- {brand color descriptor — e.g., "Y Mint #11E6D8 accents on protagonist's pants"}.
- {lighting — from cut.lighting: direction / hardness / color temp}.
- {tone — e.g., "energetic", "wistful", "calm"}.

Panel 1:
 Framing: [WS / LS / MS / MCU / CU / ECU].
 Camera angle: [eye_level / low_angle / high_angle / overhead / dutch].
 Camera facing: [frontal / three_quarter / profile / back].
 Shot scope: [face_only / bust / waist_up / full_body].
 Subject action: [protagonist 무엇을 — 한 줄].
 Pose: [구체적 포즈 — 발 자세·손 위치·무게중심].
 Gaze: [to_camera / off_camera / at_product / down].
 Props: [등장 소품 + 다루는 방식].
 Layout grid: [rule_of_thirds_center / left / right / split / overhead].
 Color intent: [cut.color_analysis 기반 — 팔레트·강조색].
 Texture: [cut.texture — 표면 질감].
 VFX in shot: [구체적 시각 묘사 — REFERENCE/vfx-in-board.md].

Panel 2: (동일 구조)
Panel 3: (동일 구조)

Continuity:
- Same location / time of day / protagonist (master sheet) / lighting direction across all panels.

ABSOLUTELY NO handwriting, NO labels, NO annotations, NO storyboard markings, NO grid overlays, NO timecode burn-ins.

Aspect: each panel 9:16 (vertical). Whole canvas: 27:16 horizontal (3 panels × 9:16).
```

> 컷에 `recreation_prompts.t2i_start_frame`이 있으면 위 패널 블록을 그 프롬프트(셀럽 얼굴복제·로고 마크 제외)로 채우고, lighting/texture/visible_elements/color_analysis로 보강한다.

## 예시 (KT Y board1_intro — 횡단보도 와이드 + 데이터 잔량 클로즈업)

```
A horizontal storyboard panel sequence for an advertising treatment.
3 panels of equal width, separated by thin white gutters (6 pixels).

Setting / location:
Morning Shibuya scramble crosswalk. Tokyo. Office-going crowd. Bright overcast daylight. Slight morning haze.

Style:
- Cinematic photographic look, 4K.
- Y Mint #11E6D8 accents on protagonist's cargo pants.
- Soft overcast morning light (key: top, soft, cool ~7000K), no harsh shadows.
- Energetic, slightly tense.

Panel 1:
 Framing: WS. Camera angle: low_angle (hip height, slight tilt up). Camera facing: frontal.
 Shot scope: full_body + environment.
 Subject action: 주인공이 횡단보도 한가운데로 정면으로 걸어 들어옴.
 Pose: 오른발 한 걸음 내딛는 중, 양손 자연스럽게 옆.
 Gaze: forward (slightly down). Props: none on protagonist; office workers as crowd.
 Color intent: cool overcast + Y Mint single-color pop. Texture: fabric_cotton, concrete.
 VFX: none.

Panel 2:
 Framing: CU. Camera angle: eye_level. Camera facing: three_quarter. Shot scope: hands + phone.
 Subject action: 주인공이 폰을 가슴 높이에서 들고 화면을 본다.
 Pose: 양손으로 폰을 잡고 약간 앞으로 숙임. Gaze: at the phone (off_camera).
 Props: smartphone with a stylized red low-data indicator on screen (graphic shape only).
 Color intent: shallow DOF, mint pop. VFX: shallow depth of field on phone.

Panel 3:
 Framing: MCU. Camera angle: eye_level. Camera facing: frontal. Shot scope: face + shoulders.
 Subject action: 주인공이 폰에서 시선을 떼고 정면을 본다 (살짝 걱정).
 Pose: 고개 약간 기울임. Gaze: down→up to_camera.
 Props: smartphone (lowered partway). VFX: none.

Continuity:
- Same Shibuya crosswalk / morning overcast / protagonist (master sheet) / light from upper-left.

ABSOLUTELY NO handwriting, NO labels, NO storyboard markings, NO grid overlays.
(On-screen captions per plan are added in post; the phone shows only a graphic indicator shape.)

Aspect: each panel 9:16. Whole canvas: 27:16 horizontal.
```

## 자주 망하는 패턴 & 교정
- **패널이 까만 갭으로 분리** → "thin WHITE gutter, 6 pixels" 강조.
- **갭 없이 한 그림처럼 합쳐짐** → "clearly separated panels, like a storyboard".
- **패널마다 다른 인물** → reference 빠짐(medias 확인).
- **패널마다 다른 시간대** → "same time of day" + 빛 방향 명시.
- **GPT가 스토리보드 주석 그림** → "no annotations, no labels" 강조 + 4번 반복.
- **회색 돌처럼 사람들(시체·NPC)** → "alive, normal everyday people, just paused mid-motion. NOT statues, NOT grey, NOT pale, NOT dead-looking".
- **9:16인데 패널이 가로로 길게** → "each panel 9:16 vertical" 명시.
- **보드마다 톤·질감이 다름** → 컷의 lighting/texture/color_analysis를 패널 필드에 안 넣은 것(10번).

## 사람의 판정 슬롯
보드가 생성되면 멈추고 사용자에게: "이 보드 그대로 슬라이스해도 돼?" / "다시 그릴 패널 있어?" / "톤·구도 OK?". 판정은 사람이. AI는 기술 점검(얼굴 깨짐, 손가락 6개, 안 시킨 주석 누설)만.

---
*버전: lsb-treatment-builder_2606021505 · 2026-06-02 15:05 KST.*
