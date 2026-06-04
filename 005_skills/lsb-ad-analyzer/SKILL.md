---
name: lsb-ad-analyzer
description: >
  LSB Production 광고 레퍼런스 분석 스킬. 광고 영상 파일(mp4)을 받아 컷 단위로
  분해하고, 컷 내부의 움직임·트랜지션·리듬·레이아웃·타이포모션과 전역 촬영효과(wiggle 등),
  그리고 음성 나레이션(Whisper)까지 판독하여 LSB 광고 메타데이터 스키마(JSON + 표)로
  구조화한다. 반드시 다음 상황에서 사용한다: "이 광고 분석해줘", "레퍼런스 데이터셋 만들어줘",
  "컷별로 분해해줘", "광고 메타데이터 뽑아줘", 광고 mp4 파일을 첨부하며 분석을 요청할 때.
  저작권 안전 추상화(Level 2~3)와 표절 회피 원칙을 강제한다.
---

# lsb-ad-analyzer — LSB 광고 레퍼런스 분석 스킬

광고 영상 한 편을 받아 **LSB 데이터셋 entry 1개**(JSON + 검토용 표)로 만든다.
목적은 "잘 만든 광고가 **어떻게 연출됐는가**(움직임·레이아웃·그리드·타이포모션·촬영효과·나레이션)"를
사람이 베끼지 않고 시스템이 참고할 형태로 구조화하는 것. **영상 자체를 학습/복제하지 않는다.**

## 핵심 원칙 (절대)

0. **'인식'을 하되 '판정'은 하지 않는다.** 프레임을 순서대로 읽으면 시간 구조(컷 리듬·트랜지션·움직임)를
 사람과 동등하게 읽는다. 그 객관적 라벨을 기록하라. "좋은가 나쁜가"의 미적 판정은 사람 몫.
1. **이미지만 보지 말고 '연출'을 본다.** "뭐가 찍혔나"(피사체)가 아니라 **"어떻게 연출됐나"**가 핵심:
 인물 움직임 / 소품 움직임 / 카메라 무빙 / 그리드상 배치 / 타이포 등장·이동 모션 / 인물+자막 공존 레이아웃 /
 전역 촬영효과(wiggle 3D 등). 이게 비면 분석한 의미가 없다.
2. **동적 라벨은 썸네일로 단정 금지 — 개별 프레임 확대 필수.** (교훈: 컨택트시트 썸네일만 보고
 '댄스'로 오독한 적 있음 — 실제론 정적 포즈 + 타이포 색변화였다.) "움직임이 있다"까지는 썸네일로 보되,
 그게 인물 댄스인지/타이포 애니인지/카메라 wiggle인지는 **반드시 개별 프레임을 크게 확대해** 확정한다.
3. **추상화 강제(시각).** 시각 *묘사*는 Level 2~3만. 고유명사는 source_ref/brand/product/model에만. (부록 A §0)
4. **카피는 원문 저장 + 메타태그.** 짧은 슬로건/CTA/캡션 원문 보존. 장문 내레이션·약관은 핵심 라인만(excerpt_only).
5. **숫자·라벨을 지어내지 않는다.** duration·컷수·fps·비율은 manifest에서. 못 본 필드는 비우고 analyst_notes에 표시.

## 데이터셋 저장 경로 (런타임 resolve — 크로스플랫폼, mac/Win 공용)

**경로를 하드코딩하지 않는다.** 데이터셋은 사용자가 연결한 **`LSB_Ad_Datas` 폴더**다(엔진은 누적되는 중앙 라이브러리 하나). 세션마다 그 폴더의 절대경로를 resolve해 `<DATASET>`로 쓴다.

```
<LIBRARY> = 연결된 LSB_Ad_Datas 폴더의 절대경로
<DATASET> = <LIBRARY>/001_ad_video_dataset   (entries/·index/·dataset_view.md는 그 안)
 mac 예: /Users/<id>/Desktop/LSB_Ad_Datas
 win 예: C:\Users\<id>\Desktop\LSB_Ad_Datas
<DATASET>/
 entries/ ADV-YYYY-NNN.json + ADV-YYYY-NNN_review.md (정식 위치)
 index/ by_<10축>.json + master.json
 dataset_view.md
```

- resolve 순서: (1) 연결된 `LSB_Ad_Datas`=`<LIBRARY>`; `<DATASET>`=`<LIBRARY>/001_ad_video_dataset`(entries/+index/ 그 안) → (2) 없으면 `mcp__cowork__request_cowork_directory`로 요청 → (3) 빈 폴더면 dataset_template/를 복사해 시딩.
- 새 entry는 `<DATASET>/entries/`에, 인덱스 갱신은 `<DATASET>/index/`에.
- 워크플로/예시의 상대경로 `entries/`·`index/`는 양 OS 공통(파이썬은 `/` 슬래시를 Windows에서도 허용; 스크립트는 `os.path.join` 사용).
- 작업용 임시 산출물(프레임 캐시 `*_frames/` 등)은 별도 작업폴더에 두고 데이터셋 폴더로 반출하지 않는다.
- 사용자가 다른 경로를 명시하면 그 경로 우선.

## 워크플로 (순서대로)

### STEP 0 — 준비
- 입력: 광고 mp4. 부록 A(entry 스키마) 숙지. `<DATASET>` resolve(위 섹션).
- 의존성: `pip install --break-system-packages scenedetect opencv-python-headless pillow faster-whisper`

### STEP 1 — 프레임 파이프라인 (전 프레임 · **원본 해상도** · 그리드 금지)

> ⛔ **판독은 개별 프레임을 *원본 해상도*로 하나씩 읽는다. 컨택트시트(축소 그리드)·다운스케일 이미지로 분석하지 않는다.** 그리드에 작게 박힌 프레임은 사람도 못 읽고 모델은 더 못 읽는다 — 그건 "분석"이 아니다. 컨택트시트는 *파일 목록 색인*일 때만 허용.

```bash
# 1) 전 프레임을 원본 해상도로 빠짐없이 추출 (다운스케일·샘플링·그리드 전부 금지)
mkdir -p frames/allframes
ffmpeg -i <입력.mp4> -vsync 0 -qscale:v 2 frames/allframes/f%06d.png
# 2) 메타(fps·해상도·rotation):
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_read_frames -count_frames -of json <입력.mp4>
# 3) (선택) 컷 경계 자동검출 — 타임코드만, 이미지 저장 X:
scenedetect -i <입력.mp4> detect-adaptive list-scenes
```
- ad_frames.py를 쓰더라도 **`--max-edge`(다운스케일)·`--contact-cols`(그리드) 옵션은 쓰지 말 것.** 구버전 기본값이 `--max-edge 1024 --contact-cols 6`이라 *축소된 6열 그리드*가 분석에 쓰여 결과가 망가졌다. `allframes/`는 **원본 해상도** 그대로 둔다.
- 산출: `frames/manifest.json`(또는 ffprobe 결과 — fps·width/height·rotation·컷 타임코드) + `frames/allframes/`(전 프레임, 원본 해상도). contact_sheets는 만들지 않거나 만들어도 *파일 네비게이션 색인* 한정 — **판독 금지**.
- **rotation 확인:** ffprobe rotation(또는 manifest)으로 세로/가로 확정. aspect_ratio는 그 기준으로 기록.
- **전수 추출(절대):** 모든 프레임을 native fps·원본 해상도로. STEP 4는 이 `allframes/` 파일들을 **하나씩 열어** 판독한다(미세 텍스트·UI·wiggle은 해당 프레임을 *크롭 확대*해서 확인).

### STEP 1.5 — 음성(나레이션) 추출
```bash
python scripts/ad_audio.py <입력.mp4> --model base --beam 1
```
산출: `<stem>_frames/audio.json`(나레이션 타임코드·텍스트·음성커버리지·BGM추정). CPU에서 base+beam1 권장(small↑는 느림).
- Whisper 원문은 짧은 어휘를 오인식할 수 있으니(예: '우월한'→'우와란') 화면 자막과 대조해 보정한다.

#### STEP 1.5-a — sandbox에서 Whisper가 안 될 때 (폴백 순서 — 절대 멈추지 말 것)

흔한 실패: faster-whisper 설치 실패(CTranslate2 바이너리), 모델 가중치 다운로드 차단(네트워크 allowlist), ffmpeg 부재, OOM/과도한 지연. **아래 순서로 내려가되, 끝까지 안 되면 자막 기반으로라도 채우고 시각 분석은 계속한다.**

1. **ffmpeg·오디오 스트림부터 확인.** `ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 in.mp4` → 출력 없으면 오디오 트랙 없음 → `has_audio:false`로 즉시 종결(전사 불필요). ffmpeg 없으면 `pip install --break-system-packages imageio-ffmpeg`(번들 ffmpeg) 또는 시스템 설치. 오디오 분리: `ffmpeg -i in.mp4 -vn -ac 1 -ar 16000 audio.wav`.
2. **모델 다운로드가 막히면** 더 작은 모델로: `--model tiny`(또는 `base`) — 가중치가 작아 받기 쉽다. HF 캐시(`~/.cache/huggingface`) 재사용, allowlist에 huggingface.co가 있으면 1회 받은 뒤 캐시됨.
3. **faster-whisper 자체가 안 깔리면 대체 ASR:** `pip install --break-system-packages openai-whisper` → `whisper audio.wav --model base --language ko --output_format json` (CTranslate2 불필요, torch 기반). 더 가벼운 대안: whisper.cpp 바이너리 + `ggml-base.bin`.
4. **ASR이 전부 불가하면 — 자막 기반 수동 폴백(entry를 막지 않는다):** 광고는 음성≈화면 자막인 경우가 많다. 화면 자막(`copy_overlay`/`captions`)에서 나레이션을 역으로 채우고 각 line에 `source:"caption_inferred"` 표시. `speech_coverage`/`bgm_likely`는 추정 불가면 `null` + `analyst_notes`에 "오디오 전사 실패(사유: 모델 다운로드 차단 등)" 기록.
5. **어느 경우든 시각 분석(STEP 2~5)은 그대로 진행.** 오디오는 나중에 환경에서 보강 가능.

> `audio.transcribed_by`에 실제 사용 경로를 기록한다: `faster_whisper | openai_whisper | whisper_cpp | manual_from_captions | none`. 이게 있어야 나중에 "이 entry의 오디오가 진짜 전사인지 자막 추정인지" 구분된다.

### STEP 2 — 컷 분할 검증 (트랜지션 오탐)
- shot_count·컷길이 확인. **컷 경계는 `allframes/`의 개별 프레임을 원본 해상도로 직접 비교**해 점검한다(컨택트시트 금지 — 경계 프레임의 미세한 변화는 축소 그리드에서 안 보인다):
 - 컷 경계 후보 타임코드 주변의 인접 프레임(f(n-1)·f(n)·f(n+1))을 한 장씩 열어 실제로 장면이 바뀌는지 확인.
 - 한 컷이 둘로 쪼개짐 → threshold 올려 재실행. 두 컷이 하나로 붙음 → 내려 재실행.
 - **동색(blue→blue 등) match-cut/split-screen·디졸브는 자동탐지가 거의 못 잡는다.** threshold를 바꿔도 안 되면
 자동분할 한계로 보고, 전 프레임을 하나씩 보고 **수동으로 실제 컷 경계를 식별**해 shot_count_corrected에 기록.

### STEP 2.5 — 컷별 중간 프레임 + 컨택트시트 보존 (데이터셋에 이미지로 남긴다)

> 왜: entry는 텍스트(JSON)다. 한 프레임 안에 여러 장면이 분할/멀티패널/필름스트립으로 배치된 컷(adv009의 필름스트립·분할 타이포 존 등)은 글 라벨만으로는 다른 세션이 공간 배치를 못 그린다. 그래서 각 컷 duration의 가운데 프레임 이미지를 데이터셋에 함께 저장해, 다른 세션·builder가 실제 그림을 보고 레이아웃을 이해하게 한다.

STEP 2에서 컷 경계를 확정한 직후, allframes에서 각 컷의 중간 시점 프레임을 골라 데이터셋에 복사하고 라벨드 컨택트시트를 만든다(추가 디코딩 없음 — 이미 뽑은 원본 프레임을 복사).

```bash
python3 scripts/ad_midframes.py --allframes frames/allframes --fps <FPS> --cuts "0:1.30,1.30:3.04,3.04:5.20,..." --out "<DATASET>/entries/<ID>_frames" --id <ID> --cols 4
```

- 산출(데이터셋에 영구 보존): `<DATASET>/entries/<ID>_frames/cut01_mid.png …`(컷별 중간 프레임, 원본 해상도) + `contact_sheet.png`(전 컷 한눈에, 컷번호·타임코드 라벨) + `frames_index.json`.
- 이 폴더는 예외적으로 데이터셋 안에 남긴다(allframes 전체 캐시는 여전히 반출 금지 — 컷당 중간 프레임 1장 + 컨택트시트만 보존).
- entry JSON에 경로를 박는다: 최상위 `frames_dir`·`contact_sheet_path`; 각 shot에 `mid_frame_path`. (부록 A §1·§5)
- 분할/멀티패널 컷은 여기서 눈으로 확정하고 STEP 4에서 `panel_layout`으로 구조화한다.

### STEP 3 — 전역 시그니처 식별 (컷별 판독 전에)
컷 몇 개의 개별 프레임을 확대해 **광고 전체에 깔린 효과**를 먼저 잡는다:
- `capture_style`: 실사/3D/AI생성/혼합?
- `camera_signature`: 전 컷에 미세한 좌우 시점 떨림(**wiggle_3d / parallax**)이 있나? handheld 흔들림? locked-off?
 - ★ wiggle은 정적 장면에도 깔려서 썸네일로는 "정지"로 보인다. 개별 프레임 2~3장을 확대해 배경/피사체 가장자리가
 좌우로 미세하게 어긋나는지 확인. (촬영 카메라가 Nishika 같은 다렌즈 3D면 거의 확실히 wiggle.)
 - 카메라 기종이 영상/설명에 언급되면 그 기종의 효과를 웹에서 확인해 signature_note에 적는다.
- `color_grade`, `texture_fx`도 전역으로 기록.
- `global_layout`: 그리드 시스템(rule of thirds/center/split), 인물 주 배치 위치, 인물↔타이포 관계, 여백.

### STEP 4 — 프레임 단위 전수 판독 (every frame, 컷별 종합)

**전 프레임 하나하나 (절대 원칙):** 각 컷의 `allframes/` 프레임을 **첫 프레임부터 끝 프레임까지 순서대로 하나하나** 읽는다. 대표 프레임 한 장이나 컨택트시트 썸네일로 '띄엄띄엄' 보고 넘어가지 않는다. 전 프레임을 순서대로 봐야 (a) 인물·소품·카메라의 *프레임 간 변화*(subject_motion·camera_motion·wiggle·prop_motion)를 정확히 잡고, (b) 1~2프레임짜리 짧은 표정·타이포 변화를 놓치지 않는다. `contact_sheets/`는 *색인*일 뿐 판독 단위가 아니다. 컷이 길면 *건너뛰지 말고* 묶음으로 순차 판독(예: f000–f030, f031–f060 …)하되 전 프레임을 본다.

판독은 **프레임 시퀀스로 보되, 라벨은 컷 단위로 종합**한다. 각 컷마다 아래 **7가지를 모두** 채운다(하나라도 비면 "이미지만 본 것"):
1. **정적**: framing, color_mood, subject_action, copy_overlay (전 프레임 확인 후 컷 대표 상태로)
2. **레이아웃**: layout_grid, subject_position, subject_typo_layout (인물+자막 공존 시 배치)
3. **타이포 모션**: typo_motion — 자막이 *어느 프레임에서 어떻게 등장·이동·소멸*하는지 프레임 추적
4. **카메라 앵글·숏·시선** ★ camera_angle(eye_level/high/low/overhead), camera_facing(정면/¾/측면), shot_scope(얼굴/상반신/전신/환경), gaze(카메라응시/회피/제품).
5. **소품·색·포징** ★ props(소품 목록), prop_semantics(왜 썼나=상징/기능), color_palette(manifest의 dominant HEX), color_intent(보색대비/브랜드컬러 등 의도), pose_description(포즈·제스처가 주는 인상).
6. **동적 (프레임 바이 프레임)**: subject_motion(인접 프레임 비교로 실제 움직임/정지포즈 판별), prop_motion, camera_motion·intensity, camera_effect_local(wiggle은 인접 프레임 좌우 시점차로 확정), motion_blur, intra_cut_rhythm, transition_in/out(경계 프레임에서 확인).
7. **고증**: fact_check_flag.

> `rep_frame`은 *저장용 대표 썸네일*일 뿐 판독 단위가 아니다(판독은 전 프레임). manifest의 shot별 `color_palette`(dominant HEX)는 그대로 쓰고 의도(color_intent)는 사람이 해석한다.

### STEP 4.5 — 시각 풀 인벤토리·질감·조명·색·스타일 프롬프트 (5축)

STEP 4의 7가지가 *연출의 분류*라면, STEP 4.5는 *이미지를 다시 만들기 위해 필요한 정보*다. 후속 builder의 보드 생성에 그대로 들어가는 입력이라 정밀해야 함.

#### 4.5.1 `visible_elements` — 화면 내 모든 시각 요소 (5층 카탈로깅)

`props`는 *집을 수 있는 소품*만. 화면엔 *환경·광원·대기·배경 디테일*도 있다. 컷별로 5층으로 분리해 박는다.

```json
"visible_elements": {
 "foreground": ["주인공·주피사체", "직접 잡히는 소품"],
 "midground": ["배경 인물", "테이블·의자·장비"],
 "background": ["건물 외벽", "산·바다·하늘", "간판·LED"],
 "lighting_env": ["창문 자연광", "스튜디오 키 라이트", "네온 사인"],
 "atmosphere": ["먼지", "안개", "비", "눈", "역광 글로우"]
}
```

각 층 *보이는 것을 다 적는다*. 작은 디테일(예: "배경에 책 한 권") 빠뜨리면 builder가 다시 그릴 때 사라진다.

#### 4.5.2 `texture` — 컷별 표면 질감

전역 `texture_fx`(clean_digital/film_grain 등)는 영상 전체 *렌더 톤*. 컷별 `texture`는 *화면 내 각 표면 질감*. 둘 다 본다. vocabulary는 영어(국제 표준): matte/glossy/metallic/chrome, glass_clear/frosted/tinted, fabric_cotton/silk/denim/velvet/leather, wood_polished/raw, concrete/brick/stone, skin_natural/makeup, plastic_glossy/matte, foliage/fur/hair, paper/cardboard 등.

```json
"texture": { "primary_subject":"fabric_silk", "secondary_objects":["glass_clear","wood_polished"], "background_surface":"concrete", "atmospheric":["dust","atmospheric_haze"] }
```

#### 4.5.3 `lighting` — 광원·콘트라스트·색온도 (이미지 생성 최중요 변수)

```json
"lighting": {
 "key_direction":"front/back/side_left/side_right/top/bottom/45deg_above/45deg_side",
 "key_hardness":"hard/soft/diffused",
 "key_color_temp":"warm_3000K/neutral_5500K/cool_7000K/colored_neon/mixed",
 "fill_strength":"strong/moderate/minimal/none",
 "key_to_fill_ratio":"1:1/2:1/4:1/8:1/silhouette",
 "rim_light":true/false,
 "practical_lights":["창문","네온","촛불"],
 "shadow_presence":"deep/soft/minimal/none",
 "overall_contrast":"low_key/mid_key/hi_key/high_contrast"
}
```
조명 vocabulary는 영어. practical_lights는 한국어 자유 묘사. 실사=그림자/하이라이트로, AI생성=컬러그레이드·음영 모순으로 판별.

#### 4.5.4 `color_analysis` — 색 정밀 분석

기존 `color_palette`(dominant HEX)에 *관계·전략*을 더한다.

```json
"color_analysis": {
 "palette_hex":["#6ab3cb","#29282d","#dfcac2","#667b76"],
 "palette_role":{"#6ab3cb":"background_dominant","#29282d":"subject_dark_anchor","#dfcac2":"skin_or_warm_accent","#667b76":"midtone_bridge"},
 "color_relationship":"complementary/analogous/triadic/split_complementary/monochrome/brand_dominant",
 "temperature_balance":"warm_dominant/cool_dominant/balanced/split_warm_cool",
 "saturation_strategy":"vivid/muted/desaturated_with_pop/monochrome",
 "contrast_type":"luminance_high/luminance_low/hue_complementary/temperature_split",
 "accent_color":"#dfcac2", "accent_ratio":"5_percent/15_percent/30_percent",
 "brand_color_match":["브랜드 블루 #0046AA 근사 매칭"]
}
```

#### 4.5.5 `style_prompt` — AI 이미지 생성용 한 줄 프롬프트 (핵심 컷)

키비주얼·와우컷·hook·cta 등 *다시 만들 가능성 높은 컷*에 한 줄 영어 프롬프트(200~350자). 구조: [subject+pose]→[outfit/material]→[location]→[lighting]→[framing+angle]→[palette+mood]→[texture+atmosphere]→[post look]→[style anchor]. 국적·문화 명시, 브랜드 컬러 HEX. **셀럽 *얼굴 사진복제*·실제 로고 마크는 만들지 않는다(유형으로). 자막·카피 원문은 보존(아래 4.5.6과 동일 규칙).**

#### 4.5.6 `recreation_prompts` — 컷 시작프레임 t2i + i2v 모션 (전 컷 보존) ★

**모든 컷**에 *시작 프레임을 재현하는 긴 t2i 프롬프트(**한 컷당 ≥500단어**, 목표 500–650)* + *그 스틸을 원본 컷 모션으로 영상화하는 i2v 프롬프트*를 만들어 `recreation_prompts`에 보존한다. (300단어면 디테일이 날아가 나중에 구현 불가 — 그래서 500단어 하한.) **분할/멀티패널 컷이면 패널별 위치·크기비율·내용·디바이더를 t2i에 모두 풀어쓴다(부록 B §2 Part 13).** 4.5.1~4.5.4(시각 인벤토리)를 한 문단으로 직조하고, 동적 필드(subject_motion·camera_motion·camera_effect_local·prop_motion·typo_motion·intra_cut_rhythm·duration·transition·motion_blur)로 i2v를 합성. **다중 인물 컷이면 t2i/i2v에 *그 컷의 인물 ID*를 명시**(예: "the protagonist, character ID protagonist_main" / "a different person — cafe customer, NOT the protagonist"). builder가 어느 마스터시트를 넣을지 명확해진다.

```json
"recreation_prompts": {
 "t2i_start_frame": "<12(+분할시 13)파트 구조 ≥500단어>",
 "t2i_negative": "<네거티브>",
 "i2v_motion": "<원본 컷 모션 i2v>",
 "i2v_params": {"clip_duration_sec":<duration>,"camera_move":"...","subject_motion_level":"...","signature_effect":"wiggle_3d/none","pacing":"...","loopable":<bool>},
 "fidelity_note": "craft-faithful; on-screen copy preserved verbatim (per copywriting); celeb face-likeness & logo mark generic"
}
```

작성 규칙·12파트 t2i 구조·i2v 모션 매핑·t2i→i2v 체인·워크드 예시·경계는 **이 문서 하단 부록 B** 참조.

> **경계(요약):** 자막·카피 원문은 **보존**(짧은 카피·수치 verbatim, 장문 고지만 excerpt — copywriting과 동일). 단 셀럽 *얼굴 사진수준 복제*와 실제 *로고 마크*는 generic(초상·상표). 카피 텍스트 속 브랜드명·모델명은 자막이라 그대로 둔다. craft(구도·렌즈·조명·색·모션)는 충실히 — "원본 느낌"은 거기서 나온다. 결과는 cross-pollination(새 오리지널) 입력.

### STEP 5 — 상위 구조 + 카피 + 오디오 종합
- narrative_arc, pacing_curve, hook/cta_position, wow_cut_index, creative_device.
- copywriting: 화면 카피 원문 + 각 line의 `source`(voice/caption/both)를 audio.json과 대조해 채움.
- audio: narration_lines(보정본+원문), voice_vs_caption, bgm_likely.
- typography(typo_motion_dominant 포함), vfx.

### STEP 5.5 — 사고법 역추정·검색 키워드·브리프 역추정

광고의 *원인*을 역추정해 entry 하단에 박는다. 모든 추정 필드는 `confidence: "inferred"` 라벨.

**5.5.1 사고법 역추정 (7단계)** — `inferred_creative_thinking`: insight/persona/moment/product_role/punchline/differentiator/brand_fit_one_liner (treatment-builder REFERENCE/client-vs-internal.md와 동일 스키마).

**5.5.2 검색 키워드 (10축)** — `search_keywords`. planner가 브리프 매칭에 쓰는 인덱스. 각 축 1~5개.

```json
"search_keywords": {
 "industry": ["finance"],
 "product_category": ["salary_account"],
 "target_demo": ["late20s_early30s","early_career","office_worker","mz"],
 "media_format": ["shortform_landscape_30s"],
 "tone": ["punchy_humor","friendly"],
 "pacing": ["front_loaded","ramp_up"],
 "technique": ["celeb_hook","balloon_typo_3d","filmstrip_collage"],
 "vfx_keywords": ["wiggle_3d","color_pop","3d_render","split_screen"],
 "copy_strategy_keywords": ["product_name_pun","refrain_repetition","model_name_drop"],
 "concept_derivation_pattern": ["celeb_fashionfilm"]
}
```

**언어 룰 (반드시 준수): search_keywords 10축 전부 영문 토큰.**
카테고리/제품/타깃/매체/톤/기법/카피전략/사고법까지 *모두 영문 토큰*으로 박는다(예전 한국어 축 폐지). 한국어로 떠오른 값은 `lsb-treatment-builder/REFERENCE/keyword-vocabulary.md`의 KO 별칭표로 영문 토큰을 찾아 박는다. 표에 없으면 가장 가까운 토큰, 신규면 표에 `영문 토큰 + KO 별칭` 추가.

**왜 영문 통일인가:** KO/EN 혼용이면 같은 데이터셋에서 "통신" 검색이 "telecom" entry를 못 잡아 인덱스가 깨진다. 전 축 영문 토큰 + KO 별칭표로 통일한다.

**5.5.3 브리프 역추정** — `inferred_brief`: 광고주가 줬을 브리프를 한 문장으로(planner의 brief 매칭 직접 비교용).

**5.5.4 Cross-pollination 태그** — `cross_pollination_tags`: adjacent/distant/contrast. **영문 토큰**으로(예: `"adjacent":["insurance","telecom","subscription_membership"]`). planner 가중치 보조 신호.

**5.5.5 컨셉 도출 패턴** — `concept_derivation_pattern`: 영문 토큰(handbook 12패턴, keyword-vocabulary §8).

**5.5.6 신뢰도 라벨** — `confidence`: inferred / human_verified / partial. 신규는 inferred, 사람 검수 후 human_verified 승격.

### STEP 5.6 — 카테고리 인덱스 자동 갱신

신규 entry를 `<DATASET>/entries/`에 저장 직후 인덱스를 갱신한다(빠지면 planner가 새 entry를 못 찾음).

별도 `index_helper.py` 파일이 필요 없다 — 아래 **인라인 스니펫**으로 갱신한다(자기완결). `<DATASET>`은 연결된 LSB_Ad_Datas 절대경로, `<ENTRY>`는 방금 저장한 entry 경로. 산출(by_*.json·master.json)은 **전부 strict JSON**이다. (Windows에서 heredoc이 안 되면 아래 본문을 **작업 스크래치 폴더**에 `idx_update.py`로 저장해 `python idx_update.py "<DATASET>" "<ENTRY>"` 실행 — 단 그 `.py`는 스크래치에만 두고 `<DATASET>`엔 두지 않는다.)

```bash
python3 - "<DATASET>" "<DATASET>/entries/ADV-YYYY-NNN.json" <<'PYEOF'
import json, os, sys, datetime
D, ep = sys.argv[1], sys.argv[2]
AX = ["industry","product_category","target_demo","media_format","tone",
      "pacing","technique","vfx_keywords","copy_strategy_keywords","concept_derivation_pattern"]
e = json.load(open(ep, encoding="utf-8")); eid = e["id"]; sk = e.get("search_keywords", {})
os.makedirs(os.path.join(D, "index"), exist_ok=True); today = str(datetime.date.today())
for ax in AX:
    vals = sk.get(ax, []); vals = [vals] if isinstance(vals, str) else vals
    if not vals: continue
    p = os.path.join(D, "index", "by_%s.json" % ax)
    idx = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {"_meta": {}}
    for v in vals:
        v = str(v).strip()
        if not v: continue
        idx.setdefault(v, [])
        if eid not in idx[v]: idx[v].append(eid)
    ids = {i for k, val in idx.items() if k != "_meta" for i in val}
    idx["_meta"] = {"axis": ax, "language": "en", "updated": today, "entry_count": len(ids)}
    json.dump(idx, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
mp = os.path.join(D, "index", "master.json")
m = json.load(open(mp, encoding="utf-8")) if os.path.exists(mp) else {}
sr = e.get("source_ref", {})
m[eid] = {"path": "entries/%s.json" % eid, "category_primary": e.get("category_primary"),
          "brand": sr.get("brand"), "title": sr.get("title_or_campaign"), "year": sr.get("year"),
          "search_keywords": sk, "confidence": e.get("inferred_creative_thinking", {}).get("confidence", "inferred")}
json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("OK index updated:", eid)
PYEOF
```

1. entry의 `search_keywords` 10축(영문 토큰)을 읽어 → 2. `index/by_<axis>.json` 각각에 entry ID 추가(중복 허용) → 3. master.json 갱신. 인덱스 `_meta.language`는 전부 `en`.

인덱스 파일 예 `index/by_industry.json`:
```json
{ "_meta": {"axis":"industry","language":"en","updated":"2026-06-02","entry_count":6},
 "finance": ["ADV-2026-001"], "automotive": ["ADV-2026-002","ADV-2026-003"] }
```

### STEP 6 — 자가검사 (출력 전 필수)
- ★전수 판독: 각 컷을 `allframes/` **전 프레임 순서대로** 봤나? 대표 프레임·컨택트시트로 띄엄띄엄 보지 않았나? subject_motion·camera wiggle 등 동적 라벨을 인접 프레임 비교로 확정했나?
- 추상화: 시각 *묘사*에 고유명사 누출 0(고유명은 source_ref/copywriting 한정) → abstraction_checked.
- 연출 완전성: 각 shot에 subject_motion·layout_grid·typo_motion(해당 시) 채움. "정적 포즈인데 효과만 움직임" 구분.
- 전역 시그니처(wiggle 등) 누락 없나.
- ★ 각 컷 camera_angle/facing/shot_scope/gaze, props/prop_semantics, color_palette/intent, pose_description 채움.
- ★STEP 5.5: inferred_creative_thinking 7단계·search_keywords 10축·inferred_brief·cross_pollination_tags·concept_derivation_pattern·confidence 채움. 추정값에 `confidence: "inferred"` 박힘.
- ★vocabulary: search_keywords 10축 + cross_pollination_tags가 **전부 영문 토큰**인가? 한국어 값이 남지 않았나? (keyword-vocabulary.md 기준)
- ★STEP 5.6: 인덱스 갱신 스크립트 실행됐나? `index/`의 10개 파일 + master.json에 새 ID 추가됐나? `_meta.language=="en"`?
- ★STEP 4.5 5축: 각 컷 `visible_elements`(5층)·`texture`·`lighting`(9서브)·`color_analysis`(9서브) 채움.
- ★STEP 2.5: `<DATASET>/entries/<ID>_frames/`에 컷별 `cutNN_mid.png` + `contact_sheet.png` 저장됐나? entry에 `frames_dir`·`contact_sheet_path`·각 shot `mid_frame_path` 박혔나?
- ★분할/멀티패널 컷: 해당 컷에 `panel_layout`(패널 위치·비율·내용·divider) 채웠나? (글로만 두지 않았나)
- ★STEP 4.5.6: 각 컷 `recreation_prompts`(t2i_start_frame·i2v_motion·i2v_params) 채움. **t2i_start_frame이 컷당 ≥500단어인가?** 분할 컷은 Part 13(패널 분해)을 t2i에 풀어썼나? **셀럽 얼굴 사진복제·실제 로고 마크 누출 0? 자막은 copywriting 원문대로(장문 고지만 excerpt)?**
- ★저장 경로: 산출물이 `<DATASET>`(entries/·index/·dataset_view.md)에 저장됐나?

### STEP 7 — 출력 (2종)
1. `<DATASET>/entries/ADV-YYYY-NNN.json` — 부록 A 스키마 구조 그대로. **반드시 strict JSON 파일로 저장**(아래 ⚠️).
2. 검토용 `<DATASET>/entries/ADV-YYYY-NNN_review.md` (상위 메타 + 컷별 한 줄). `<DATASET>/dataset_view.md` 갱신.
- 데이터셋 폴더와 프레임 캐시(`*_frames/`)는 분리 보관. 프레임 캐시는 외부 반출 금지.

> ⚠️ **엔트리의 최종 산출물은 `.json` — `.py`가 아니다.** entry는 `Write` 툴로 `entries/ADV-YYYY-NNN.json`에 **strict JSON**(키는 쌍따옴표, `true`/`false`/`null`, 트레일링 콤마·주석 없음)으로 직접 쓴다. 파이썬 dict로 조립하고 싶으면 그 **조립 스크립트는 작업 스크래치(outputs)에서만** 돌리고 `json.dump(obj, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=2)`로 *json만* `<DATASET>`에 내보낸다 — **조립용 `.py`를 `<DATASET>`에 남기지 않는다.** 저장 직후 `python3 -c "import json;json.load(open('<ENTRY>',encoding='utf-8'))"`로 파싱 검증한다. 실패하면 파이썬 리터럴이 섞인 것(`True`/`False`/`None`·홑따옴표·주석) — 전부 JSON으로 고친다. (데이터셋엔 `.json`·`_review.md`·`dataset_view.md`만 존재해야 한다.)

## 하지 말 것
- 이미지만 분석(연출 누락) 금지. 썸네일만으로 동적 라벨 단정 금지.
- 전역 효과(wiggle 등) 누락 금지. rotation 무시 금지.
- 영상 안 보고 추측, Level 0~1 시각 *묘사* 저장 금지.
- **데이터셋을 `<DATASET>`(연결된 LSB_Ad_Datas) 밖에 저장 금지.** (사용자가 다른 경로 명시 시만 예외)
- **`<DATASET>`에 `.py`·스크립트·파이썬 dict 리터럴 저장 금지.** entry·index는 전부 strict JSON(`.json`). 조립용 파이썬은 스크래치에서만 돌리고 데이터셋엔 `.json`만 남긴다.
- search_keywords·cross_pollination_tags에 **한국어 값** 박기 금지(전부 영문 토큰).
- 한 세션에 다 못 끝내면 부분 저장 후 이어받기.
- **STEP 5.5 추정 필드를 *사실*처럼 적지 않는다.** confidence: "inferred" 필수. 비울 거면 `null`로 명시.
- recreation_prompts에 **셀럽 얼굴 사진복제·실제 로고 마크** 넣지 않는다. 자막·카피 원문은 *보존*이 정상.
- **t2i 복제 프롬프트를 컷당 500단어 미만으로 줄이지 않는다**(디테일 소실 → 구현 불가). 분할/멀티패널 컷을 글 한 줄로 뭉뚱그리지 말고 패널별로 분해한다(panel_layout + Part 13).
- **컷 중간프레임/컨택트시트 저장을 건너뛰지 않는다**(STEP 2.5). 텍스트만 저장하면 다른 세션이 분할 레이아웃을 못 그린다.

---
*버전: lsb-ad-analyzer_2606041200 · 2026-06-04 12:00 KST. 변경 내역은 적용방법.md 참조. (_2606041200 = **컷별 중간프레임+컨택트시트 데이터셋 보존(STEP 2.5, scripts/ad_midframes.py)** + entry `frames_dir`·`contact_sheet_path`·shot `mid_frame_path` · **분할/멀티패널 `panel_layout`** 스키마(§5/§10) · **t2i 복제 프롬프트 컷당 ≥500단어**로 상향 + 부록 B Part 13 패널 분해 규칙. 동기: 텍스트만으론 한 프레임 분할 레이아웃[adv009 필름스트립]을 다른 세션이 이해 못 함.)*


---

# 부록 A — entry 출력 스키마 (구 schema.md 통합)

> 버전: lsb-ad-analyzer_2606041200 · 2026-06-04 12:00 KST. 누적 변경(연출 심층·전역 시그니처·음성·카메라/소품/색·역추정 10축·시각 인벤토리·프레임 복제·전 프레임 원본해상도 판독/그리드 금지·엔트리 JSON-first/데이터셋 .py 금지·shots 인물식별/narrative_structure 메타[A3]·라이브러리 재구성 DATASET=001_ad_video_dataset·**컷 중간프레임/컨택트시트 보존+panel_layout+t2i≥500단어[2606041200]**)은 SKILL.md 참조.
> "이미지에 뭐가 찍혔나"가 아니라 "어떻게 연출됐나"를 데이터화한다.

---

## 0. 추상화 규칙 (절대 원칙)

- **시각 *묘사*** → Level 2~3만. Level 0(원본 묘사)·Level 1(고유명 포함 묘사) 금지.
- **카피(슬로건·태그라인·CTA·캡션·짧은 한 줄)** → 원문 그대로 저장 + 분류 메타태그. 출력이 원문과 "단어만 바꾼 수준"으로 닮는 것만 금지(표절검사).
- **장문 텍스트(긴 내레이션·약관)** → 통째 저장 금지, 핵심 라인만(`narration_handling: excerpt_only`).
- **고유명사(브랜드·모델·제품 정식명)** → `source_ref`/`brand`/`product`/`model` + 카피 원문(copywriting) 한정. 시각 *묘사* 본문엔 금지.

---

## 1. 최상위 필드 — 구조·서사

| 필드 | 타입 | 설명 | 출처 |
|---|---|---|---|
| `id` | string | `ADV-YYYY-NNN` | 부여 |
| `source_ref` | object | `{platform, title_or_campaign, brand, product, model, year, production_note, url}` | 메타 |
| `category_primary` | string | 주 카테고리 1개 (§6, `<도메인>.<세부>`) | 판정 |
| `category_tags` | array | 보조 태그(서술, 한국어 허용 — 인덱싱 안 함) | 판정 |
| `mood` | array | 분위기 태그(서술) | 판정 |
| `target_demo` | string | 타깃 인구(서술) | 판정 |
| `total_duration` | number | 총 길이(초) | manifest |
| `shot_count` / `shot_count_corrected` | number | 검출/보정 컷 수 | manifest/판정 |
| `fps` | number | 프레임레이트 | manifest |
| `aspect_ratio` | string | **표시 기준** 비율(rotation 반영) | manifest |
| `hook_position` / `cta_position` | number | 후크·CTA 시각(초) | 판정 |
| `narrative_arc` | string | 서사 구조 요약(Level 3) | 판정 |
| `narrative_structure` | string | linear_continuous / cross_cutting_montage / parallel_narrative / nested_flashback | 서사 구조 enum(같은 구조 광고 retrieve용 — planner와 동일 enum) |
| `pacing_curve` | enum | slow_build/steady/accelerating/front_loaded/staccato | 판정 |
| `music_tempo_curve` | enum | steady/ramp_up/drop/fluctuate | 판정 |
| `wow_cut_index` | array | 와우컷 인덱스 | 판정 |
| `creative_device` | string | 핵심 디바이스 | 판정 |
| `production_signature` | object | 전역 촬영/효과 시그니처 (§1.1) | 판정 |
| `global_layout` | object | 그리드·인물배치 경향 (§1.2) | 판정 |
| `recurring_motifs` | array | 반복 시각 모티프 | 판정 |
| `copywriting` | object | 카피 메타 (§2) — **원문 보존** | 판정 |
| `typography` | object | 타이포 메타 (§3) | 판정 |
| `vfx` | object | VFX 메타 (§4) | 판정 |
| `audio` | object | 음성 분석 (§4.5) | Whisper+판정 |
| `frames_dir` | string | 컷 중간프레임 폴더명 `"<ID>_frames"` (STEP 2.5, 데이터셋 내 보존) | 메타 |
| `contact_sheet_path` | string | `"<ID>_frames/contact_sheet.png"` — 전 컷 한눈에(분할 레이아웃 확인용) | 메타 |
| `shots` | array | 컷별 상세 (§5) + 시각 인벤토리/recreation (§10) | manifest+판정 |
| `search_keywords` | object | 검색 인덱스 10축 — **영문 토큰** (§9) | 판정 |
| `inferred_creative_thinking` / `inferred_brief` / `cross_pollination_tags` / `concept_derivation_pattern` / `confidence` | — | 역추정 (SKILL STEP 5.5) | 판정 |
| `analyst_notes` | string | 분석자 코멘트·정정 | 판정 |
| `verification` | object | `{frames_reviewed, audio_analyzed, hitrate_na, abstraction_checked}` | 메타 |

### 1.1 `production_signature`
`capture_style`(live_action/3d_cg/ai_generated/mixed/stop_motion) · `camera_signature[]`(wiggle_3d/parallax/handheld_shake/locked_off/dolly_heavy) · `signature_note` · `color_grade`(high_key/brand_color_dominant/desat/warm/cool) · `texture_fx`(film_grain/halation/glow/clean_digital).
> ★ wiggle_3d 같은 전역 미세 시점 떨림은 썸네일로 "정지"로 오판하기 쉽다. 개별 프레임 확대로 좌우 시점 이동 확인 → 여기 + 각 shot `camera_effect_local`.

### 1.2 `global_layout`
`grid_system`(rule_of_thirds/center/golden_ratio/split_screen/dynamic_symmetry) · `subject_placement_dominant`(center/left_third/right_third/varies) · `subject_typo_relation`(typo_opposite_subject/typo_over_subject/typo_separate_zone/alternating) · `negative_space_use`(minimal/generous/asymmetric) · `layout_note`.

## 2. `copywriting` — 원문 보존
`tagline_text`(원문) · `tagline_structure` · `tagline_length_syllables` · `tagline_position_sec` · `cta_text`/`cta_text_structure`/`cta_position_sec` · `copy_tone[]` · `copy_strategy` · `copy_lines_count` · `lines[]`(`{position_sec,text(원문),function,tone,source}` — source: voice/caption/both) · `captions[]`(`{position_sec,text(원문),function}`) · `narration_handling`(excerpt_only/summary_only/none).

## 3. `typography`
`primary_font_class`/`secondary_font_class` · `animation_style[]`(fade_in/typewriter/kinetic/static/pop/slide/blur_in/bounce/scale_in/track_in) · `subtitle_position_dominant`(lower_third/center/full_screen/top/floating) · `tagline_position` · `color_strategy` · `appearance_count` · `key_typography_moments_sec[]` · `typo_motion_dominant`.

## 4. `vfx`
`primary_effects[]`(light_leak/particle/lens_flare/color_pop/glitch/morph/ui_motion/3d_render/data_viz/split_screen) · `effect_intensity`(subtle/moderate/heavy/extreme) · `transition_style_dominant`(cut/fade/light_wipe/match_cut/morph/whip_pan/camera_push_through) · `vfx_event_count` · `vfx_timing_array_sec[]` · `wow_vfx_index[]`.

## 4.5 `audio` (Whisper)
`has_audio` · `language` · `speech_coverage`(0~1) · `bgm_likely`(true/false/null) · `narration_lines[]`(`{start,end,text(보정),text_raw(원문),kind,source}` — source에 `caption_inferred` 가능) · `voice_vs_caption` · `narration_handling` · `transcribed_by`(faster_whisper/openai_whisper/whisper_cpp/manual_from_captions/none) · `audio_note`.
> Whisper가 sandbox에서 실패하면 SKILL.md STEP 1.5-a 폴백(ffmpeg 확인 → 작은 모델 → openai-whisper/whisper.cpp → 자막 기반 수동). 전사 못 해도 시각 분석은 진행하고 `transcribed_by`에 경로 기록.

## 5. `shots[]` — 컷별 상세

각 shot과 `index`로 정렬. 판독은 **`allframes/`의 개별 프레임을 원본 해상도로 하나씩** 본다 — 정적 정보든 동적/연출이든 컨택트시트(축소 그리드)로 판독하지 않는다.

- **정적**: `index` · `duration` · `framing`(ECU/CU/MCU/MS/MLS/LS/WS/EWS/grid/environment) · `function` · `color_mood` · `subject_action` · `copy_overlay`(원문).
- **인물 식별 (다중 인물 광고)**: `subject_identity`(이 컷의 인물 분류 — 예 protagonist_main · supporting_A · cafe_barista · background_crowd · none_environment) · `subject_relationship_to_protagonist`(main_character / supporting_character / extra_atmosphere). 컷몽타주·다중 인물 구조를 데이터셋에서 retrieve 가능하게(planner character_pool과 같은 개념).
- **프레임 이미지**: `mid_frame_path`("<ID>_frames/cutNN_mid.png") — 이 컷 중간 프레임(STEP 2.5). 다른 세션이 실제 그림을 보는 핸들.
- **레이아웃**: `layout_grid` · `subject_position` · `subject_typo_layout` · `typo_motion`.
- **분할/멀티패널 레이아웃 (★ 한 프레임에 여러 장면)**: 화면이 분할/멀티패널/필름스트립/그리드/PIP/콜라주면 `panel_layout`을 채운다(아니면 생략/`null`). 글로만 두면 다른 세션이 패널 배치를 못 그린다.
  ```json
  "panel_layout": {
    "is_multi_panel": true,
    "type": "filmstrip | split_vertical | split_horizontal | grid | picture_in_picture | collage | layered_collage | typo_zone_split",
    "panel_count": 6,
    "divider": "thin black gutter | white line | none | overlap",
    "orientation": "row | column | grid_RxC",
    "panels": [
      {"id":1, "rect":"x 0-16%, y 0-100%", "size_ratio":"~1/6 width", "content":"<Level2~3 묘사>", "text_in_panel":"<있으면 원문>"},
      {"id":2, "rect":"x 16-33%, y 0-100%", "size_ratio":"~1/6 width", "content":"..."}
    ],
    "layout_note":"패널 순서·반복 여부·시선 흐름 등"
  }
  ```
  각 panel의 `rect`는 프레임 대비 백분율(좌상단 기준), `size_ratio`는 대략 비율, `content`는 추상화 묘사, `text_in_panel`은 자막 원문 보존. 이 구조 + `mid_frame_path` 이미지를 함께 보면 builder가 분할 레이아웃을 그대로 재현한다.
  - **`layered_collage`(베이스 위 조각 겹침 — GMA 2018 식)**: 단순 *나란히* 분할이 아니라 *겹침* 콜라주면 `type:"layered_collage"` + `base`(베이스 이미지 묘사) + `panels[]`를 조각으로 쓰되 각 조각에 `z`(레이어 순서)·`rotation_deg`·겹침 여부를 적는다. 이 경우 builder/video-crafter는 **한 장 생성 금지 · 개별 소스→프리뷰 합성→영상 레이어 모션**의 3단 분리로 처리한다(공통 규칙: `lsb-treatment-builder/REFERENCE/layered-collage-protocol.md`).
- **카메라 앵글·숏·시선 **: `camera_angle`(eye_level/low_angle/high_angle/overhead/dutch/worm_eye) · `camera_facing`(frontal/three_quarter/profile/back) · `shot_scope`(face_only/bust/waist_up/full_body/environment) · `gaze`(to_camera/off_camera/at_product/down/none) · `eye_contact_effect`.
- **소품·색·포징 **: `props[]` · `prop_semantics` · `color_palette[]`(dominant HEX) · `color_intent` · `pose_description`.
- **동적**: `subject_motion` · `prop_motion` · `camera_motion` · `camera_motion_intensity` · `camera_effect_local`(없으면 none) · `motion_blur` · `intra_cut_rhythm`(static/steady/accelerating/chaotic) · `transition_in`/`transition_out` · `vfx_in_shot[]` · `vfx_intensity_local` · `fact_check_flag` · `notes`.
- **시각 인벤토리 + 프레임 복제 **: §10.

> 모든 vocabulary(영문 토큰)와 treatment 키 매핑은 `lsb-treatment-builder/REFERENCE/cut-schema.md` + `lsb-ad-planner/schema.md` §5.

---

## 6. `category_primary` 값 체계 (개방 확장)

형식: **`<도메인>.<세부>`**. IT 외 도메인도 허용한다(데이터에 이미 `auto.*`, `realestate.*`, `retail.*`, `apparel.*` 사용 중).

```
IT.smartphone / IT.wearable / IT.app_b2c / IT.app_b2b_saas / IT.ai_product
IT.laptop_pc / IT.smart_home / IT.fintech / IT.gaming_hardware / IT.platform
auto.sedan / auto.suv_hybrid / auto.pickup_truck / auto.ev / auto.luxury
finance.bank / finance.card / finance.insurance / finance.securities
realestate.apartment_presale / retail.beauty_platform / retail.commerce
apparel.sportswear / apparel.fashion / fnb.* / beauty.* / public.*...
```

신규 도메인·세부는 자유 확장. 단 `search_keywords.industry`(영문 토큰, §9)와 일관되게(예: category_primary `auto.pickup_truck` ↔ industry `automotive`).

## 7. Cross-Pollination 카테고리 매핑 — (구버전 참고용)

> ★ **가중치 맵의 단일 출처는 이제 `lsb-ad-planner/schema.md` §3 (영문 industry 기준).** 맵 2개가 분기하면 안 되므로 planner 쪽을 정본으로 쓴다. 아래 IT 표는 *구버전 참고용*으로만 남긴다.

| 클라이언트 X | 인접(0.5) | 원거리(1.0) | 대조(1.2) |
|---|---|---|---|
| IT.fintech | app_b2c, platform | 럭셔리, 자동차 | 게임, 스트리트패션 |
| IT.smartphone | wearable, laptop_pc | 자동차, 패션 | 농산물, 전통주 |

> 동일(X=X)=0.2(참고만), 와우컷=동일 카테고리 0개(하드밴).

---

## 8. 채워진 예시
실제 예시는 `<DATASET>/entries/ADV-2026-001.json`(금융, 우월한 월급통장) 참조. production_signature(wiggle 3D)·global_layout·audio·shots[]의 연출 심층 + 시각 인벤토리 + search_keywords(영문 토큰)가 채워진 레퍼런스다.

---

## 9. `search_keywords` (10축) — 전 축 영문 토큰

planner가 브리프 매칭에 쓰는 인덱스 입력. **10축 전부 영문 토큰**(예전 한국어 축 폐지). 한국어로 떠오른 값은 `lsb-treatment-builder/REFERENCE/keyword-vocabulary.md`의 KO 별칭표로 영문 토큰을 찾아 박는다.

축: `industry` · `product_category` · `target_demo` · `media_format` · `tone` · `pacing` · `technique` · `vfx_keywords` · `copy_strategy_keywords` · `concept_derivation_pattern`.

```json
"search_keywords": {
 "industry": ["finance"], "product_category": ["salary_account"],
 "target_demo": ["late20s_early30s","early_career","office_worker","mz"],
 "media_format": ["shortform_landscape_30s"], "tone": ["punchy_humor","friendly"],
 "pacing": ["front_loaded","ramp_up"], "technique": ["celeb_hook","balloon_typo_3d","filmstrip_collage"],
 "vfx_keywords": ["wiggle_3d","color_pop","3d_render","split_screen"],
 "copy_strategy_keywords": ["product_name_pun","refrain_repetition","model_name_drop"],
 "concept_derivation_pattern": ["celeb_fashionfilm"]
}
```

- `cross_pollination_tags`(adjacent/distant/contrast)도 **영문 토큰**으로.
- 인덱스 갱신: **STEP 5.6의 인라인 파이썬 스니펫** 사용(별도 `index_helper.py` 파일 불필요; 대량 rebuild만 선택). 인덱스 `_meta.language`는 전부 `en`.
- **혼용 금지**: 한국어 값을 search_keywords에 박으면 인덱스 매칭이 깨진다("통신" vs "telecom").

## 10. 시각 인벤토리 + 프레임 복제 — shots[] 확장

핵심 컷(또는 전 컷)에 *이미지/영상 재생성 입력*을 박는다. builder 보드 생성에 그대로 들어간다.

- `mid_frame_path`: 이 컷 중간 프레임 이미지(STEP 2.5). `panel_layout`: 분할/멀티패널이면 패널별 위치·비율·내용(§5).
- `visible_elements`: foreground/midground/background/lighting_env/atmosphere (5층).
- `texture`: primary_subject/secondary_objects[]/background_surface/atmospheric[] (영문 vocab).
- `lighting`: key_direction/key_hardness/key_color_temp/fill_strength/key_to_fill_ratio/rim_light/practical_lights[]/shadow_presence/overall_contrast.
- `color_analysis`: palette_hex[]/palette_role{}/color_relationship/temperature_balance/saturation_strategy/contrast_type/accent_color/accent_ratio/brand_color_match[].
- `style_prompt`: 핵심 컷 한 줄 영어 프롬프트.
- `recreation_prompts`: `t2i_start_frame`(**≥500단어**) · `t2i_negative` · `i2v_motion` · `i2v_params` · `fidelity_note`. 분할/멀티패널 컷이면 t2i에 패널별 위치·비율·내용을 모두 기술(부록 B §2 Part 13).

상세 작성법·예시·경계는 STEP 4.5 / STEP 4.5.6 + **아래 부록 B**(이 문서 내).

> **경계:** 자막·카피 원문은 **보존**(짧은 카피·수치 verbatim, 장문 고지만 excerpt). 셀럽 *얼굴 사진수준 복제*·실제 *로고 마크*만 generic(초상·상표). craft(구도·렌즈·조명·색·모션)는 충실히.


---

# 부록 B — 컷 프레임 복제 t2i/i2v 사양 (구 frame-recreation-prompts.md 통합)

각 컷의 **시작 프레임**을 다시 만들 수 있는 긴 t2i 프롬프트와, 그 스틸을 **원본 컷의 모션 느낌**으로 영상화하는 i2v 프롬프트를 컷마다 보존한다. STEP 4.5의 시각 인벤토리(visible_elements·texture·lighting·color_analysis)를 *한 줄 프롬프트로 직조*하는 단계다.

## 0. 목적과 경계 (반드시 먼저 읽기)

- **목적:** 잘 만든 컷의 *연출 craft* — 구도·렌즈·조명·색·질감·모션 — 를 **재사용 가능한 생성 레시피**로 보존한다. 스튜디오가 이 craft를 학습하고, planner의 cross-pollination으로 **새 오리지널 광고**를 만드는 입력으로 쓴다.
- **경계 (craft·자막 보존 + 정확도):**
 - 이 프롬프트는 스튜디오 *내부 레퍼런스/재현*용 craft 레시피이며 cross-pollination(새 오리지널 생성)의 입력으로 쓴다.
 - **자막·카피는 원문 그대로 보존 (추상화·placeholder 금지).** 화면 텍스트는 entry `copywriting`에 기록된 **실제 원문**을 그 위치·타이포·색박스 트리트먼트와 함께 프롬프트에 넣는다. 짧은 슬로건·캡션·수치는 verbatim, **장문 고지·약관만** excerpt(기존 copy 규칙과 동일). (이미지 모델이 한국어 텍스트를 깔끔히 못 그릴 수 있어 실제 자막은 후처리로 얹는 게 보통이지만, 프롬프트엔 원문을 보존한다.)
 - **인물 신원:** 특정 실존인·셀럽의 *사진수준 얼굴 복제*는 만들지 않는다(초상·퍼블리시티). 대신 유형으로("a Korean woman in her mid-20s, calm confident"). 톤·조명·연출이 같으면 느낌은 재현된다 — 스튜디오 자체 모델/탤런트로 촬영·생성하는 전제. (자막 원문에 인물 이름이 들어가는 건 카피라서 그대로 둔다.)
 - **브랜드 로고 마크(시각 심볼):** 실제 로고 *이미지*는 generic으로(상표). *카피 텍스트 속 브랜드명*은 자막 원문이므로 그대로 둔다.
- **왜 그래도 "원본 느낌"이 나는가:** 광고 컷의 "느낌"은 셀럽 신원이 아니라 **조명 방향·경도·색온도, 렌즈·화각, 구도, 컬러그레이드, 모션 다이내믹**에서 나온다. 이것들을 정밀하게 보존하면 추상화된 주체로도 동일한 톤·무드·리듬이 재현된다.

## 1. 필드 구조 (컷마다)

```json
"recreation_prompts": {
 "t2i_start_frame": "<시작 프레임 재현 t2i 프롬프트 — 영어, 컷당 ≥500 단어(목표 500–650). 분할/멀티패널이면 패널별로 다 기술>",
 "t2i_negative": "<네거티브 프롬프트 — 모델 무관 공통 + 컷 특이>",
 "i2v_motion": "<그 스틸을 원본 컷 모션으로 움직이는 i2v 프롬프트 — 영어>",
 "i2v_params": {
 "clip_duration_sec": <컷 duration>,
 "camera_move": "<locked_off / push_in / pan_L...>",
 "subject_motion_level": "<still / micro / walk / dynamic>",
 "signature_effect": "<wiggle_3d / none...>",
 "pacing": "<static / steady / accelerating...>",
 "loopable": <bool>
 },
 "fidelity_note": "craft-faithful; identity/brand/on-screen-text abstracted (copyright-safe)"
}
```

- **모든 컷**에 t2i_start_frame + i2v_motion을 박는 것이 목표(전부 보존). 단 핵심 컷(hook/cta/wow/key_visual)일수록 더 정밀하게.
- 값은 이미 채운 STEP 4.5 필드에서 *합성*한다(아래 §2 매핑). 새로 관찰하지 않고도 조립 가능하도록 STEP 4.5를 먼저 채운다.

## 2. t2i 시작프레임 프롬프트 — 12파트(+분할 시 13) 구조 (컷당 ≥500단어)

STEP 4.5/4 필드를 아래 순서로 한 문단에 직조한다. 각 파트는 *그 컷에 실제로 채워진 값*에서 가져온다(지어내지 않는다). **분량은 한 컷당 최소 500단어(목표 500–650).** 300단어로는 디테일이 날아가 나중에 구현이 안 된다 — 각 파트를 *구체 수치·방향·재질·비율·색 HEX*로 충분히 풀어 쓴다.

| # | 파트 | 출처 필드 |
|---|------|-----------|
| 1 | Subject & pose (추상화) | `subject_action`,`pose_description`,`shot_scope`,`gaze` (신원 제거) |
| 2 | Wardrobe / material | `texture.primary_subject`, 의상 묘사(브랜드 제거) |
| 3 | Location / set & background | `visible_elements.background/midground` |
| 4 | Foreground & props | `props`,`visible_elements.foreground`,`prop_semantics`(기능만) |
| 5 | Lighting setup | `lighting.*` (direction/hardness/color_temp/ratio/rim/shadow/contrast) |
| 6 | Lens / framing / camera angle | `framing`,`camera_angle`,`camera_facing`,`shot_scope` (+ 추정 화각) |
| 7 | Composition / grid | `layout_grid`,`subject_position`,`subject_typo_layout`(존 표시만) |
| 8 | Color palette & strategy | `color_analysis.palette_hex/role/relationship/accent`,`color_intent` |
| 9 | Texture & surfaces | `texture.*`,`visible_elements` 표면 |
| 10 | Atmosphere | `visible_elements.atmosphere`,`lighting.practical_lights` |
| 11 | Post / signature look | `production_signature`(capture_style·color_grade·texture_fx),`camera_effect_local`(예: wiggle 깊이감) |
| 12 | Style anchor | 사진/렌더 장르 한 줄(예: "clean 4K commercial, hi-key studio") + 국적·문화 명시 |
| 13 | **Layout decomposition (분할/멀티패널 컷만)** | `panel_layout` — 프레임이 split/multi-panel/filmstrip/grid/PIP/collage면, 패널을 하나씩: 위치(좌상단 기준 %), 크기 비율, 각 패널 내용(추상화), 패널 간 divider(거터/라인/없음), 배열 방향(row/column/grid RxC), 패널 내 자막 원문. "한 프레임 = 여러 장면"을 모델이 그릴 수 있게 풀어 쓴다. |

**작성 규칙**
- 한 문단(분할 컷은 패널 절을 길게), 세미콜론·콤마로 절 구분, **컷당 ≥500단어(목표 500–650)**.
- **분할/멀티패널 컷(Part 13)**: 예) "a horizontal filmstrip of six equal panels separated by thin black gutters; panel 1 (leftmost, ~1/6 width, full height) shows …; panel 2 (next, ~1/6 width) shows …; … panel 6 (rightmost) shows …; the six panels read left-to-right as a rapid montage of …". 각 패널의 위치·비율·내용·자막을 빠짐없이.
- 화면 텍스트가 있으면 entry `copywriting`의 **실제 원문**을 위치·타이포·색박스 트리트먼트와 함께 넣는다(짧은 카피·수치 verbatim; 장문 고지만 excerpt). 추상화·placeholder 금지.
- 브랜드 컬러는 HEX로(예: "brand-blue #2da1e7 dominant"). 색·카피는 보존하되 *로고 마크(시각 심볼)*만 generic.
- 시간 의존 효과(wiggle_3d)는 스틸로 직접 못 그리니 *깊이감/패럴랙스 의도*로(11파트).

## 3. i2v 모션 프롬프트 — 시작프레임을 원본 컷처럼 움직이기

t2i 결과 스틸을 **첫 프레임**으로 넣고, 아래 모션을 입힌다. 컷의 동적 필드에서 합성.

| 모션 축 | 출처 필드 | i2v 표현 |
|---|---|---|
| 인물 모션 | `subject_motion` | "near-static / micro-gesture / walking forward /..." (정지포즈면 "hold pose, breathing-level only") |
| 카메라 무브 | `camera_motion`,`camera_motion_intensity` | "locked-off / slow push-in / handheld drift..." |
| 시그니처 효과 | `camera_effect_local`,`production_signature.camera_signature` | wiggle_3d → "subtle left-right viewpoint oscillation / lenticular parallax on edges, ~1–2px feel" |
| 소품 모션 | `prop_motion` | "prop lifts / rotates / floats in..." |
| 타이포/그래픽 모션 | `typo_motion`,`vfx_in_shot` | "headline pops in from right (placeholder text), 3D numeral inflates & color-shifts..." |
| 리듬·길이 | `intra_cut_rhythm`,`duration` | "steady, ~2.0s, no cut" / "accelerating montage feel" |
| 모션블러·전환 | `motion_blur`,`transition_out` | "light motion blur; ends on match-cut handoff to next shot" |

**규칙:** 컷 1개 = i2v 클립 1개(컷 길이). 카메라+인물+효과+그래픽 모션을 *동시에* 한 프롬프트에. 다음 컷으로의 `transition_out`이 화려하면(whip_pan/match_cut 등) 끝 부분에 그 핸드오프를 명시(트랜지션 보드와 연결).

## 4. t2i → i2v 체인 (원본 비디오 느낌 복원)

1. `t2i_start_frame`로 시작 프레임 스틸 생성(이미지 모델).
2. 그 스틸을 i2v 모델 첫 프레임으로 + `i2v_motion`(+`i2v_params`) 입력 → 컷 길이만큼 클립.
3. 컷들을 `transition_in/out`(필요시 트랜지션 보드, builder가 단일 캔버스로 생성)으로 이어 붙이면 원본 *리듬·톤·모션*이 재현된다.
4. 이 결과는 planner cross-pollination의 입력 비주얼 톤으로도 쓰인다(새 오리지널로 변형).

## 5. 워크드 예시 (추상화 — 실명·로고·verbatim 없음)

### 예시 A — 금융 숏폼 hook 컷 (정물 옆 인물, 정면 응시, wiggle 3D)

`t2i_start_frame`:
> A confident Korean woman in her mid-20s seen from the waist up, resting her chin lightly on her right hand with a calm, self-assured to-camera gaze; she wears a structured navy silk-blend blazer (matte silk sheen), minimal styling, no visible logos; she is seated at a clean white table beside a single vibrant orange tulip arrangement in a glossy ceramic vase placed mid-ground to her side; plain teal-to-sky blue gradient studio wall behind (no signage); soft hi-key lighting with a large diffused key from 45° upper-left, gentle fill (key-to-fill ~2:1), no rim, soft short shadows, neutral 5500K; medium shot at eye level, frontal, ~50mm-equivalent look, shallow-to-moderate depth; rule-of-thirds with the subject centered-left and the recorded on-screen headline copy “원영이처럼 우월한 월급통장” set in a bold rounded sans-serif inside a brand-blue color box on the right third (white with emphasis lettering; typically finalized in post but preserved here for fidelity); muted high-contrast brand-blue-dominant palette (#6ab3cb background dominant, #29282d dark anchor, warm orange accent ~15% of frame for complementary pop); textures read as smooth silk fabric, glossy ceramic, matte gradient wall, natural lightly-retouched skin; calm, quiet, clean atmosphere with subtle ambient glow and no haze or grain; subtle retro-tech wiggle-3D parallax depth between the subject and the foreground vase (slight viewpoint offset suggesting lenticular dimensionality); clean digital 4K commercial production look, hi-key, polished but natural. Korean studio commercial aesthetic.

`t2i_negative`: "second person, extra hands, distorted fingers, real brand logos/marks, watermark, harsh shadows, low-key, grain, blur, deformed face" (텍스트는 negative에서 빼서 자막이 살도록)

`i2v_motion`:
> Hold the opening pose with breathing-level stillness — the subject does not gesture, only the faintest natural micro-motion; camera locked-off; apply a subtle continuous left-right viewpoint oscillation (wiggle / lenticular 3D parallax) so the foreground vase and the subject's edges shift a hair against the background, giving retro-tech dimensionality; lighting and color steady; ~2.0s, steady rhythm, no cut; toward the end, the headline copy “원영이처럼 우월한 월급통장” settles into the right-third color box (finalized in post). Light, clean, no large motion.

`i2v_params`: `{ "clip_duration_sec": 2.07, "camera_move": "locked_off", "subject_motion_level": "still", "signature_effect": "wiggle_3d", "pacing": "static", "loopable": true }`

### 예시 B — 금융 숏폼 wow 컷 (3D 풍선 수치 타이포 reveal, 색전환)

`t2i_start_frame`:
> A Korean woman in her mid-20s in a static, centered pose with a calm subtle smile, framed from the chest up, partly behind a large 3D inflatable balloon-style numeral reading “3.1%” (the recorded on-screen figure) floating at chest height in the foreground (a glossy puffed form); the balloon form carries a gradient that shifts from deep purple (#161761) at the top to bright brand-blue (#2da1e7) at the base, with soft reflective highlights; vivid solid brand-blue studio background, no signage; soft even frontal key light, minimal fill, almost no shadows, neutral 5500K, hi-key; medium shot, eye-level, frontal, ~35–50mm-equivalent, the 3D numeral occupying the upper-center foreground (~30% of frame); vivid saturated palette, brand-blue dominant with a purple-to-blue color-shifting accent on the balloon, white highlight glow; textures read as glossy inflated plastic/3D-render surface with reflective specular, smooth fabric on the subject, natural skin; clean, playful, retro-tech mood, no haze, no grain; subtle wiggle-3D parallax depth on the background behind the floating numeral; clean digital 3D-render-composited 4K commercial look, hi-key, glossy. Korean studio commercial aesthetic.

`t2i_negative`: "real brand logos/marks, second person, extra fingers, dark/low-key, grain, watermark, distorted balloon"

`i2v_motion`:
> The 3D balloon-style numeral inflates/scales in from chest level and settles, its gradient color-shifting from purple to brand-blue with glossy highlight travel; the subject holds a static pose behind it (breathing-level only); camera locked-off with subtle wiggle-3D parallax on the background; the side headline copy “우월~ 좋은데?” pops in briefly (recorded copy; finalized in post); ~1.7s, steady, no cut, ending on a clean cut handoff. Glossy, playful, hi-key.

`i2v_params`: `{ "clip_duration_sec": 1.73, "camera_move": "locked_off", "subject_motion_level": "still", "signature_effect": "wiggle_3d", "pacing": "steady", "loopable": false }`

## 6. 자가검사
- t2i_start_frame이 **컷당 ≥500단어**인가? 12파트(+분할 시 Part 13)를 *그 컷의 실제 값*으로 채웠나(지어내기 0)?
- 분할/멀티패널 컷은 Part 13(패널 위치·비율·내용·divider)을 t2i에 풀어쓰고 `panel_layout`도 채웠나? `mid_frame_path` 이미지가 데이터셋에 있나?
- 셀럽 *얼굴 사진복제*·실제 로고 마크가 들어가지 않았나? (자막·카피 원문 보존은 정상)
- 화면 텍스트가 copywriting 원문과 일치하나? (짧은 카피·수치 verbatim, 장문 고지만 excerpt)
- i2v_motion이 컷의 subject_motion·camera·effect·typo_motion·duration을 모두 반영했나?
- wiggle_3d 등 시간효과를 i2v로 옮겼나(스틸엔 깊이감으로만)?
- 길이/카메라무브/시그니처효과가 i2v_params와 일치하나?


---

# 부록 C — search_keywords 영문 토큰 vocab (핵심, KO→EN)

planner가 한국어 브리프를 매칭하도록 KO 별칭을 함께 둔다. **저장값은 영문 토큰.** (기술축 framing/camera_*/vfx/transition/pacing/typo_motion은 이미 영문 — REFERENCE/cut-schema.md.)

### industry
`telecom`←통신 · `finance`←금융 · `insurance`←보험 · `fashion`←패션 · `beauty`←뷰티 · `fnb`←F&B·식음 · `beverage_alcohol`←주류·음료 · `automotive`←자동차 · `home_appliance`←가전 · `mobility`←모빌리티 · `public_gov`←공익·정부 · `education`←교육 · `film_culture`←영화·문화 · `industrial_b2b`←산업B2B · `semiconductor`←반도체 · `construction_realestate`←건설·부동산 · `luxury`←럭셔리 · `healthcare_pharma`←헬스케어·제약 · `it_saas`←IT·SaaS · `content_ott`←콘텐츠·OTT · `retail`←유통·리테일 · `travel_tourism`←관광·여행 · `sports`←스포츠 · `sportswear`←스포츠·의류

### product_category
`salary_account`←월급통장 · `savings`←적금 · `card`←카드 · `mobile_banking`←모바일뱅킹 · `loan`←대출 · `insurance_product`←보험상품 · `data_plan`←요금제 · `pickup_truck`←픽업트럭 · `large_suv`←대형SUV · `hybrid_car`←하이브리드차 · `ev`←전기차 · `sedan`←세단 · `luxury_sedan`←럭셔리세단 · `apartment_presale`←아파트분양 · `same_day_delivery`←당일배송 · `beauty_platform`←뷰티 플랫폼 · `sportswear`←스포츠웨어 · `performance_runningwear`←기능성 러닝웨어 · `cosmetics`←화장품 · `apparel`←의류 · `sneakers`←운동화

### target_demo
`teens`←10대 · `20s`←20대 · `early_mid_20s`←20대 초·중 · `late20s_early30s`←20대 후·30대 초 · `30s`←30대 · `late30s_40s`←30대 후·40대 · `40s`←40대 · `50s_plus`←50대+ · `senior`←시니어 · `early_career`←사회초년 · `office_worker`←직장인 · `homemaker`←주부·맘 · `student`←학생 · `men`←남성 · `women`←여성 · `family`←가족·패밀리 · `family_end_users`←가족·실수요 · `couples`←부부·연인 · `single_household`←1인가구 · `mz`←MZ · `leisure_outdoor`←레저·아웃도어 · `running_fitness`←러닝·피트니스 · `active_consumers`←액티브 소비자 · `premium_buyers`←프리미엄 구매층 · `local_presale_prospects`←지역 분양 관심층 · `active_senior`←시니어 액티브

### media_format
`tvc_15s`←TVC 15초 · `tvc_30s`←TVC 30초 · `tvc_60s`←TVC 60초 · `shortform_vertical_30s`←숏폼 세로 30초이하 · `shortform_landscape_30s`←숏폼 가로 30초이하 · `shortform_vertical_30s_plus`←세로 숏폼 30초+ · `digital_30s`←디지털 30초 · `youtube_60s_plus`←유튜브 60초+ · `sns_viral`←SNS 바이럴 · `ooh_led`←OOH·옥외LED · `product_hero_film`←제품 히어로 필름 · `presale_lifestyle_film`←분양 라이프스타일 필름 · `cinemascope_lifestyle`←시네마스코프 라이프스타일 · `feature_demo_film`←기능소구 필름 · `pt_video`←PT·키노트 영상

### tone
`cinematic`←시네마틱 · `cinematic_serious`←시네마틱 시리어스 · `cinematic_luxury`←시네마틱 럭셔리 · `punchy_humor`←펀치·유머 · `friendly`←친근 · `warm_emotional`←감성·따뜻함 · `emotional_lyrical`←감성·서정 · `premium`←프리미엄 · `luxury_minimal`←럭셔리·미니멀 · `luxury_highend`←럭셔리·하이엔드 · `serious_classic`←시리어스·정통 · `serious_documentary`←시리어스·다큐 · `kitsch`←키치 · `retro`←레트로 · `calm_refined`←차분·정제 · `confident`←당당·자신감 · `relaxed_healing`←여유·힐링 · `family`←가족 · `empathetic_comforting`←공감·위로 · `upbeat`←경쾌 · `clean_minimal`←깔끔·미니멀 · `dynamic_powerful`←역동·파워 · `refreshing`←청량·상쾌 · `determined_focused`←결연·집중 · `mystery_teaser`←미스터리·티저

### technique
`celeb_hook`←셀럽 후크 · `anthropomorphism_character`←의인화·캐릭터화 · `time_freeze`←시간정지·동결 · `transformation`←변신 · `omnibus_series`←옴니버스·시리즈 · `oner_walking_shot`←1테이크·워킹샷 · `splitscreen`←분할화면·split · `teaser_mystery`←티저·미스터리 · `mirroring_contrast_edit`←미러링·대비편집 · `world_builder`←세계관 빌더 · `call_and_response`←콜앤리스폰스 · `balloon_typo_3d`←풍선타이포·3D · `filmstrip_collage`←필름스트립·콜라주 · `color_shift`←색 변환 · `bw_color_shift`←흑백↔컬러 톤전환 · `glitch_crt`←글리치·CRT · `facade_ooh_meta`←파사드·OOH 메타 · `morph`←모핑 · `landscape_travelling`←풍경 트래블링 · `overhead`←부감 · `kinetic_typo`←키네틱 타이포 · `silhouette_teaser`←실루엣 티저 · `dark_to_light_reveal`←어둠에서 빛 리빌 · `detail_closeup`←디테일 클로즈업 · `signature_lamp_ignition`←시그니처 램프 점등 · `product_solo_hero`←제품 단독 히어로 · `anaphora_copy`←애너포라 카피 · `lifestyle_cg_intercut`←라이프스타일+CG 교차 · `nature_intro`←자연 인트로 · `low_angle_tiltup`←로우앵글 틸트업 · `location_map_graphic`←위치맵 그래픽 · `empathy_copy_hook`←공감 카피 후크 · `product_app_cutout_float`←제품·앱 컷아웃 부유 · `dissolve_montage`←디졸브 몽타주 · `direct_cta`←직접 CTA · `slowmo_explosion_start`←슬로모 폭발 스타트 · `fabric_macro_proof`←원단 매크로 기능증명 · `product_solo_feature_demo`←제품 단독 기능소구

### copy_strategy_keywords
`product_name_pun`←제품명 펀 · `brand_name_pun`←브랜드명 펀 · `refrain_repetition`←후렴 반복 · `call_and_response`←콜앤리스폰스 · `neologism_slogan`←신조어 슬로건 · `question_hook`←의문형 후크 · `imperative_slogan`←명령형 슬로건 · `model_name_drop`←모델 이름 박기 · `place_city_drop`←지명·도시 박기 · `bilingual_subtitle`←영문+한국어 자막 · `number_emphasis`←숫자·수치 강조 · `building_climax`←점층 클라이맥스 · `caption_led`←캡션 주도 · `voice_caption_sync`←음성·자막 동기화 · `leadership_declaration`←리더십 선언 · `spec_caption_split`←스펙 자막 분리 · `new_model_naming`←신차 네이밍 고지 · `double_wordplay`←더블 워드플레이 · `facility_subcopy_match`←시설 서브카피 매칭 · `location_equation`←입지 등식 · `empathy_to_solution`←공감→솔루션 전환 · `immediacy_emphasis`←즉시성 강조 · `brand_green_keyword`←브랜드 그린 키워드 · `superiority_declaration`←우위 선언 · `feature_benefit_direct`←기능 베네핏 직설 · `visual_copy_proof`←비주얼로 카피 증명

### concept_derivation_pattern (handbook 12 + 확장)
`celeb_fashionfilm`←셀럽+패션필름st · `time_bridge_metaphor_device`←시간 잇는 메타포 장치 · `call_and_response_copy`←콜앤리스폰스 카피 · `giant_character_world_builder`←거대 캐릭터·세계관 · `metaphor_visual_sequence`←메타포 비주얼 시퀀스 · `teaser_mystery_concept`←티저·미스터리 컨셉 · `teaser_mystery_payoff`←티저·미스터리 회수 · `highend_fantasy_fusion`←하이엔드 판타지 결합 · `series_omnibus`←시리즈 옴니버스 · `three_part_time_flow`←3파트 시간 흐름 · `breaking_fourth_wall`←제4의 벽 넘기 · `space_structure_illustration`←공간·구조 일러스트 · `symbol_character_fusion_3d`←심볼+캐릭터 융합 3D · `everyday_problem_metaphor_product_release`←일상 문제→비유→제품 해방 · `dark_to_light_reveal_structure`←어둠→빛 리빌 구조 · `detail_to_whole_reveal`←디테일→전체 공개

> 표에 없는 값은 가장 가까운 토큰으로, 신규면 여기에 `영문 토큰 ← 한국어` 추가. 전체·기술축 vocab은 `lsb-treatment-builder/REFERENCE/keyword-vocabulary.md`(있을 때).
