---
name: lsb-video-crafter
description: >-
 LSB Production 영상화(i2v) 스킬. lsb-treatment-builder가 만든 트리트먼트(treatment.json +
 확정컷 보드 + 인물별 마스터시트)를 입력으로 받아, Seedance 2.0 등 i2v 모델로 컷을 모션
 영상으로 만들고 클립을 결합해 최종 광고 영상을 뽑는다. 다중 인물·교차편집(컷몽타주) 구조를
 인물/공간 세그먼트별 클립으로 분리해 다루고, 한국어 나레이션 VO·브랜드 모션타이포를 넣되
 화면 자막은 굽지 않으며, IP 모더레이션(ip_detected) 차단 시 사용자 허용 프로토콜로 멈춘다.
 반드시 다음 상황에서 사용한다: "영상으로 뽑아줘", "이 컷 영상화해줘", "i2v 클립 만들어",
 "Seedance로 만들어", "트리트먼트를 영상으로", "30초 광고 영상 결합", 트리트먼트/콘티를
 주며 영상 제작을 요청할 때. 컨셉·기획은 lsb-ad-planner, 장표(PDF)·보드는
 lsb-treatment-builder가 담당하므로 이 스킬은 그걸 다시 하지 않는다.
---

# lsb-video-crafter — LSB 광고 영상화 스킬

확정컷(보드 스틸)을 모션 영상으로 만들고 결합하는 단계. **비싼 단계(크레딧) — 들어가기 전 반드시 컨펌.** 이전엔 lsb-treatment-builder Phase 7이었으나, 장표 스킬이 비대해져 분리했다(builder는 PDF 본업).

## 입력 / 출력
- **입력(builder/planner 산출):** `treatment.json`(global·cuts·transitions, 특히 `narrative_structure`·`character_pool[]`·각 컷 `subject_identity`) + `확정컷/`(보드 스틸) + 인물별 마스터시트 + product-lock 제품 이미지.
- **출력:** `video[_onetake]/`(클립별 mp4) · `{프로젝트명}_길이.mp4`(결합본) · `seedance_prompt*.md`(프롬프트). 결합 후 프레임 추출로 QA.
- 캐릭터(특히 브랜드 마스코트·실제 제품)는 planner R4와 동일: 내가 생성 금지, 사용자 공식 에셋/제공본을 레퍼런스로.

## STEP 1 — 구조·인물 판정 (제일 먼저)
`treatment.json`의 `narrative_structure`와 `character_pool[]`을 읽는다.
- `linear_continuous`(한 공간 연속): 한 클립에 여러 비트 가능.
- `cross_cutting_montage`(같은 시간·다른 공간 교차): **공간/인물 세그먼트별로 클립을 쪼갠다(STEP 2).** 억지로 한 동선으로 잇지 않는다 — A3에서 주인공이 횡단보도→카페로 *걸어 들어가* 직접 결제하는, 트리트먼트 정반대 영상이 나온 직접 원인.
- 각 컷의 `subject_identity`로 *누가 나오는 컷인지* 확인. 주인공 컷 ≠ 다른 인물 컷.

## STEP 2 — 클립 분할 (몽타주는 쪼갠다 · 4000단어 단일클립 가정 오버라이드)
한 클립에 비트 12개를 다 욱여넣으면 모델이 일부 비트를 통계적으로 누락한다(A3: whip pan·시간정지 누락). 그래서:
- **총 길이 → 15초 최대 청크로 분할 · 생성 횟수 최소화 (★).** Seedance 단일 클립 최대 = **15초**. 사용자가 요청한 총 길이를 15초 덩어리로 나누되 **개수를 최소화**한다: 30초=15+15, 35초=15+15+5, 18초=15+3, 45초=15+15+15, 60초=15×4. **컷마다 따로 생성 금지** — 한 클립(최대 15초)에 그 구간의 여러 컷/비트를 함께 담는다. 자투리만 짧은 클립으로(최소 4초, 4초 미만이면 4초로 만들고 트림).
- **Seamless 기본 (별도 지시 없으면 15/30/45/60초 전부):** 클립을 이어붙일 때 **선행 클립의 마지막 프레임 = 후행 클립의 시작 프레임**으로 잇는다(앞 클립 마지막 프레임을 ffmpeg로 추출 → 다음 클립 `start_image`, STEP 3·7). 컷 사이 동작 방향·색감·카메라 무빙이 끊기지 않게 설계. "하드컷으로" 같은 명시 지시가 있을 때만 예외.
- **`linear_continuous`:** 15초 클립당 4000단어 풀 프롬프트(아래 STEP 4) 유지. 30초면 15초×2.
- **`cross_cutting_montage`:** **공간/인물이 바뀔 때마다 별도 클립**으로 분리하고 ffmpeg로 결합. 예(A3): 횡단보도 도입(주인공) / 카페 결제(다른 손님) / 횡단보도 시간정지 / 카페 시간정지(알바생·추출기 액체 넘침) / 주인공 클로즈업→Y덤→펀치라인. 각 클립은 그 공간·인물의 reference만 받는다.
- ⚠️ **클립 최소 길이 = 4초**(Seedance duration 4~15s). 3초짜리는 생성 불가 — 세그먼트가 짧으면 4초로 잡고 후처리에서 트림.
- 의도 충실도가 비교 안 되게 높아지는 대신 크레딧↑ — 사용자에게 분할안·예상 클립 수를 알리고 컨펌.
- **레이어드 콜라주 컷(베이스 위 조각 겹침 — GMA 2018 식)은 i2v로 한 장을 통째로 움직이려 하지 않는다.** 베이스 클립 + 조각 PNG들을 **개별 레이어**로 다뤄 ffmpeg `overlay`(시간차 `enable`·`scale`·`rotate`·`fade`)로 합성하거나 조각별 짧은 모션 후 합성한다. 조각마다 opacity·scale·position·crop·slight rotation·parallax를 따로 제어 → 전체가 하나의 콜라주 프레임으로 읽히되 레이어감·편집 리듬이 산다. 소스(베이스·조각)는 builder가 단계1·2에서 만든 것을 그대로 받는다. 공통 규칙: `lsb-treatment-builder/REFERENCE/layered-collage-protocol.md`(단계 3).

## STEP 3 — 인물·공간별 reference 그룹 (medias ≤ 9슬롯)
각 클립의 reference 슬롯에 **그 클립의 인물·공간만** 넣는다.
- 다중 인물: 주인공 클립엔 주인공 마스터시트만, 카페 클립엔 카페 인물 시트만. 다른 인물 컷에 주인공 시트를 섞지 않는다(A3 변질 방지).
- 구성: `start_image`(첫 컷) + `end_image`(끝 컷) + `image`(중간 핵심 컷 몇) + 컨택트시트(영문 라벨). **seamless가 기본이므로 앞 클립의 실제 마지막 프레임을 ffmpeg로 추출해 다음 클립 start_image로** 쓴다(정적 hinge 이미지 금지 — 어긋남).
- **레퍼런스 9장 한도 — 4장 이상이 안정. 너무 많으면(욕심내 9개 꽉) 생성 실패하기도 하니 핵심부터.** 값은 컷 job_id / media_upload UUID / https URL.
- **제품 충실도(product-lock):** 실제 제품·라벨은 사용자 공식 이미지를 reference로 고정 + 프롬프트에 "실제 라벨 항상 정확히 노출" + negative "무라벨/빈 병/라벨 없는 제품 금지"(builder Phase 3.2와 동일 규칙).

## STEP 4 — 프롬프트 작성
- **분량:** `linear_continuous`는 15초당 4000단어(원테이크/컷 선언 → 캐릭터 락 → 컬러·그레이드 → 비트별 타임코드 모션·카메라·트랜지션 → 사운드 → 한국어 나레이션 → 텍스트 규칙 → 네거티브 → 아트디렉션). 몽타주 쪼갠 짧은 클립은 그 세그먼트만 *집중* 서술(짧아도 됨). **⚠ 실제로는 짧게 쓰지 말 것** — 비트별 타임코드·카메라·모션·트랜지션·사운드·한국어 나레이션·네거티브를 모두 채우면 자연히 수천 자가 된다. 한두 문장짜리 빈약한 프롬프트는 컷 누락·저품질의 직접 원인이다.
- **CRITICAL 비트 앞당기기(A3 학습):** 빠지면 컨셉이 깨지는 비트(트랜지션·시간정지·"이 컷은 다른 인물" 등)는 프롬프트 **맨 앞에 따로** 한 번 더 박는다. 예:
 ```
 CRITICAL — DO NOT SKIP:
 - (4-5s) MUST be a whip pan, NEVER a hard cut, hold FULL 1 SECOND
 - this action is performed by a CAFE CUSTOMER, NOT the protagonist
 - (11-13s) the freeze MUST be visible on screen, hold FULL 2 SECONDS
 [그 다음 본문 프롬프트]
 ```
- **텍스트 정책:** 화면 자막·나레이션을 영상에 굽지 않는다. 화면 노출 텍스트는 **브랜드 모션타이포만**(슬로건·로고락업·숫자). 나레이션은 **한국어 VO 스펙으로 프롬프트에 한글 대사**로 적는다(Seedance가 음성 생성). negative에 "no subtitles/captions/lower-thirds, only intended brand motion-typography". 한글은 한글로 — 로마자 발음표기 금지(R5).
- **동작 정확히:** 비트의 동작을 *정확한 실제 동작*으로 적는다. 예: 카페 결제 = "card tapped on the POS terminal"(추출기 위에 올리는 게 아님 — A3 오류). 트리트먼트의 동작을 임의 해석하지 말 것.
- **트랜지션 방향:** `direction_observer_view`대로 카메라 방향 + 화면 streak 방향을 *둘 다* 박는다(예: "camera rotates right → world streaks LEFT").

## STEP 5 — 생성·운용 (Seedance 2.0)
- **오디오 생성됨** — 응답 params `generate_audio:true`. 음악·SFX·VO 생성. VO 품질은 들어보고 필요 시 성우 교체.
- **mode = std / fast 둘뿐.** "Fast 말고"="std"(고품질). "pro" 없음.
- **길이** duration 4~15s. 15초×2를 ffmpeg `-f concat`으로 결합(STEP 7).
- **프리셋 가로채기(declined_preset_id):** "이 프롬프트는 프리셋 X 같다" 추천이 뜨면 그 ID를 `declined_preset_id`에 박아 리터럴 강행. **여러 번 연쇄될 수 있다** — 매 추천 ID를 기록하며 declined 체인으로 처리. (관측된 유발 키워드 — *미검증, 하드 블록 금지*: "ONE CONTINUOUS UNBROKEN SINGLE-TAKE", "vertical descent", "world freezes", "dark cafe interior". 가로채기가 잦으면 동의어로 대체 시도.)
- ※ 프리셋 가로채기(추천)와 아래 `ip_detected`(IP 모더레이션 차단)는 **다른 현상**이다. 섞지 말 것.

## STEP 6 — ip_detected 프로토콜 (★ 자동 재시도 금지)
job 조회 응답의 `status`가 문자열 **`"ip_detected"`** 면, 그 생성은 *내가 프롬프트를 바꿔서 풀 수 있는 게 아니다* — 사용자가 Higgsfield(힉스필드)에서 그 건을 직접 '허용(allow)'해야 풀린다. 따라서:
1. **즉시 멈춘다.** 추가 재시도·우회를 먼저 시도하지 않는다. (A3: 모르고 4번 재시도 → 크레딧·시간 낭비.)
2. **사용자에게 알린다** — 어떤 생성 건이 ip_detected인지 함께.
3. 사용자가 힉스필드에서 해당 건을 **허용** 처리한다.
4. 사용자가 "허용했다/다시 진행해" 신호를 주면 그때 재시도·진행.

> **금지:** 톤을 밝게 바꿔 필터를 우회하는 식의 시도(근거 없는 추정이고 약관상 부적절). 유력 트리거는 실제 브랜드·실인물 유사성이지 톤이 아니다.
> **영상 작업 상태 분류:** 대기 / 진행중 / **사용자개입대기(ip_detected)** / 완료 / 실패. ip_detected는 '영구 차단'도 'AI가 풀 상태'도 아닌 *사용자 조치 대기* 상태다.

### 렌더 대기 프로토콜 (★ 도구 호출 루프 금지 — 2606041430 치명결함 수정)

긴 렌더(1080p 15초 ≈ 15~20분)를 **짧은 sleep으로 쪼개 폴링하지 않는다.** 30~60초 sleep을 수십 번 반복하면 폴링이 40~60회로 폭발하고, "이제 확인하겠다"는 예고 텍스트만 반복하는 자기강화 루프에 빠진다(실제 사고). 아래를 **그대로** 지킨다.

1. **한 번에 길게 잔다.** 1080p 15초 = `sleep 900`(15분) **1회**. 30·60초 단위 반복 폴링 금지. (대기 작업과 다음 작업을 잘게 분리하지 말 것 — 불가피한 대기는 길게 한 번.)
2. 깬 뒤 **상태 1회 확인**. 아직 `in_progress`면 남은 예상시간만큼(예: `sleep 300`) **한 번 더** 자고 재확인. **같은 상태를 2회 확인했는데 여전히 진행중이면, 더 짧게 재확인하지 말고 더 긴 sleep 1회로 대기.** 짧은 재확인 반복 절대 금지.
3. **예고 텍스트 금지.** 도구를 호출할 거면 "이제 ~하겠다 / 호출합니다 / 잠시만요" 같은 예고 없이 **바로 호출**한다. 호출 전 설명은 1문장 이내. 예고만 하고 호출이 안 나가는 패턴이 루프의 씨앗이다.
4. 사용자에겐 시작 시 1번 "렌더 ~분 소요, 기다립니다"만 알린다(매 폴링마다 중계 금지).
5. `job_display`가 간헐 오류·상태 전이 지연이 있으니 job id로 재조회해 복구. 여러 클립이면 **모두 큐에 넣고 한 번에 길게 대기**한 뒤 일괄 수거(클립당 따로 폴링 금지).

> 요지: **"길게 한 번 자고, 도구는 예고 없이 바로." sleep 900 > sleep 30 × 30.**

## STEP 7 — 결합 (concat · 픽셀 포맷 강제)
**별도의 '압축 마스터 영상'·'요약본'을 만들지 않는다.** STEP 2에서 나눈 청크(예: 15초+5초)를 **ffmpeg로 하나로 이어 최종본 1개**만 만들어 작업폴더에 **파일로 저장**한다(저장해야 사용자에게 전달됨 · 영상을 실제로 만들지 않고 '완료'라고 하지 않는다).

클립을 이어붙이기 *전에* 두 클립의 포맷이 같은지 확인한다. 다르면 깨진다(A3: 15초 이후 재생 불가 — 앞 yuv420p / 뒤 yuv444p).
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt,profile,has_b_frames -of default=noprint_wrappers=1 clip1.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt,profile,has_b_frames -of default=noprint_wrappers=1 clip2.mp4
# 동일하면 무손실 결합:
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4
# 다르면 둘째 클립을 첫째 포맷으로 재인코딩 후 결합:
ffmpeg -i clip2.mp4 -c:v libx264 -pix_fmt yuv420p -profile:v high -level 4.0 -preset fast -crf 18 -c:a copy clip2_fixed.mp4
```
**후처리(overlay·drawtext 등) 할 때는 항상 `-pix_fmt yuv420p -profile:v high` 명시.** PNG의 RGBA를 그냥 두면 ffmpeg가 yuv444p로 빠져 concat이 깨진다.

## STEP 8 — frame-level QA (전달 전 필수)
"프롬프트 잘 박았으니 됐다" 단정 금지. ffmpeg로 **비트별 핵심 시점 프레임을 추출해 Read로 직접 본다.** 체크:
- 제품 라벨이 보이나? 카피·나레이션이 들어갔나?
- 각 컷 인물이 `subject_identity`와 맞나(주인공 컷에 주인공, 다른 인물 컷에 다른 사람)?
- CRITICAL 비트(트랜지션·시간정지)가 실제로 화면에 있나?
- 인물 디테일이 마스터시트와 일치하나(목걸이·머리길이 등 어긋나면 그 reference 빼고 재제출)?
- 결합 후 15초 이후 재생되나(코덱)?
어긋나면 해당 클립만 재생성·정정 후 다시 QA.

## 하지 말 것
- 몽타주를 한 클립에 욱여넣기. 공간/인물 바뀌면 클립을 쪼갠다.
- `ip_detected`에서 사용자에게 안 알리고 혼자 재시도. 멈추고 알린다.
- 모더레이션을 톤 우회로 뚫기. (약관·근거 없음.)
- 긴 자막·약관을 영상에 굽기. 나레이션은 VO, 화면 자막 금지.
- 모든 컷을 주인공으로 가정. `subject_identity`를 따른다.
- 검수 없이 "완성" 전달. STEP 8 프레임 확인 필수.

## 트리거 키워드
"영상으로 뽑아줘" · "영상화" · "i2v" · "Seedance" · "클립 생성/결합" · "30초 광고 영상" · 트리트먼트를 주며 영상 제작 요청.

## 함께 읽을 문서
- 입력 구조·인물 필드: `lsb-ad-planner` STEP 4(character_pool·narrative_structure·subject_identity) · `lsb-treatment-builder/REFERENCE/cut-schema.md`.
- 보드·product-lock·마스터시트: `lsb-treatment-builder` Phase 2·3.
- 타이포 처리: `lsb-treatment-builder/REFERENCE/typography-in-image.md`.

---
*버전: lsb-video-crafter_2606051640 · 2026-06-05 16:40 KST. (_2606051640 = 총 길이 15초 최대 청크 분할·생성횟수 최소화(30=15/15, 35=15/15/5, 18=15/3) + '압축 마스터 영상' 금지·단일 concat 최종본 파일저장 + 프롬프트 빈약 금지(수천 자). 이전 _2606051100 = seamless transition 기본화 — 15/30/45/60초 전부 선행 클립 마지막 프레임=후행 클립 시작 프레임, STEP2·3 갱신.) 이전 _2606041430 = 렌더 대기 프로토콜 — 도구 호출 루프 치명결함 수정: sleep 900 1회·짧은 폴링 금지·예고 텍스트 금지·클립 일괄 대기. 허쉬 세션 A14.) 이전 _2606032044 = 신규 스킬, builder Phase 7 분리, A3 학습(다중 인물·교차편집·concat 코덱·ip_detected·preset 체인).*
