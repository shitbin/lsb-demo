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

## STEP 1.5 — 생성 모드: i2v(기본) / t2v(옵션)
기본은 **i2v**(확정컷 스틸을 모션화). 단, 매니저(시스템)가 사용자에게 **t2v 옵션**을 제안해 사용자가 **t2v를 선택하면** 아래로 전환한다:
- 확정컷 스틸을 start/end/image로 깔지 **않고**, **꼭 필요한 브랜드 에셋·캐릭터 레퍼런스만** `medias`에 넣는다(제품 라벨·브랜드 마스코트·주인공 마스터시트 등 IP·정체성 고정에 필수인 것만 — 보통 1~3장).
- `generate_video`를 **t2v로 호출**(start_image 없이 텍스트 프롬프트 주도). 프롬프트는 STEP 4 그대로 **4000자(char) 풀스펙**(스틸이 없으니 공간·동작·인물·레이아웃 묘사를 더 촘촘히).
- 나머지(15초 청크·**seamless 무조건**·**브랜드 모션타이포 필수**·한국어 VO·concat·QA)는 i2v와 동일.
- t2v는 컷 스틸 충실도가 낮으니 STEP 8 QA에서 제품 라벨·인물 정체성 일치를 특히 빡세게 본다(어긋나면 핵심 레퍼런스만 더해 재생성).

## STEP 2 — 클립 분할 (몽타주는 쪼갠다 · 4000자(char) 단일클립 가정 오버라이드)
한 클립에 비트 12개를 다 욱여넣으면 모델이 일부 비트를 통계적으로 누락한다(A3: whip pan·시간정지 누락). 그래서:
- **총 길이 → 15초 최대 청크로 분할 · 생성 횟수 최소화 (★).** Seedance 단일 클립 최대 = **15초**. 사용자가 요청한 총 길이를 15초 덩어리로 나누되 **개수를 최소화**한다: 30초=15+15, 35초=15+15+5, 18초=15+3, 45초=15+15+15, 60초=15×4. **컷마다 따로 생성 금지** — 한 클립(최대 15초)에 그 구간의 여러 컷/비트를 함께 담는다. 자투리만 짧은 클립으로(최소 4초, 4초 미만이면 4초로 만들고 트림).
- **Seamless transition 무조건 적용 (★ 예외 없음 · 모든 길이 15/30/45/60초):** 클립을 이어붙일 때 **선행 클립의 마지막 프레임 = 후행 클립의 시작 프레임**으로 반드시 잇는다(앞 클립 마지막 프레임을 ffmpeg로 추출 → 다음 클립 `start_image`, STEP 3·7). 컷 사이 동작 방향·색감·카메라 무빙이 끊기지 않게 설계. **유일한 예외 = 사용자가 특정 컷을 '하드컷'으로 명시 지시한 그 컷만.** 그 외에는 seamless를 절대 건너뛰지 않는다.
- **`linear_continuous`:** 15초 클립당 4000자(char) 풀 프롬프트(아래 STEP 4) 유지. 30초면 15초×2.
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
- **분량 (★ 하드 최소 4000자(char) · 미달 제출 금지 · 무시하지 말 것):** 모든 i2v/t2v 프롬프트는 **15초 클립 기준 최소 4000자(char)**다. 구성: 원테이크/컷 선언 → 캐릭터 락 → 컬러·그레이드 → 비트별 타임코드 모션·카메라·트랜지션 → 사운드 → 한국어 나레이션 → **브랜드 모션타이포** → 텍스트 규칙 → 네거티브 → 아트디렉션. **제출 직전 프롬프트의 단어 수를 직접 세고, 4000자(char) 미만이면 비트 묘사를 더 채워 4000을 넘긴 뒤에만 제출한다(미달 상태로 절대 제출 금지).** 몽타주로 쪼갠 짧은 세그먼트(4~5초)도 *같은 밀도*로 쓰되 최소 1500자. 한두 문장짜리 빈약한 프롬프트는 컷 누락·저품질의 직접 원인 — 이 규칙을 건너뛰지 않는다.
- **CRITICAL 비트 앞당기기(A3 학습):** 빠지면 컨셉이 깨지는 비트(트랜지션·시간정지·"이 컷은 다른 인물" 등)는 프롬프트 **맨 앞에 따로** 한 번 더 박는다. 예:
 ```
 CRITICAL — DO NOT SKIP:
 - (4-5s) MUST be a whip pan, NEVER a hard cut, hold FULL 1 SECOND
 - this action is performed by a CAFE CUSTOMER, NOT the protagonist
 - (11-13s) the freeze MUST be visible on screen, hold FULL 2 SECONDS
 [그 다음 본문 프롬프트]
 ```
- **텍스트 정책 + 브랜드 모션타이포 필수 (★ 자주 누락 — 무시하지 말 것):** 화면 자막·나레이션을 영상에 굽지 않는다. 화면 노출 텍스트는 **브랜드 모션타이포만**(슬로건·로고락업·핵심 숫자). **모든 클립에 브랜드 모션타이포를 최소 1개 이상 프롬프트에 명시한다 — 슬로건·CTA·숫자 비트엔 반드시 넣는다. 모션타이포가 빠진 프롬프트는 제출하지 않는다(매번 체크).** 어떻게 등장/애니메이션되는지(위치·타이밍·인/아웃 모션·서체 무게)까지 적는다. 나레이션은 **한국어 VO 스펙으로 프롬프트에 한글 대사**로 적는다(Seedance가 음성 생성). negative에 "no subtitles/captions/lower-thirds, only intended brand motion-typography". 한글은 한글로 — 로마자 발음표기 금지(R5). **네거티브에 성적·선정성 차단 문구(no nudity·no sexual content·NSFW 등)를 넣지 않는다 — 오히려 모더레이션을 트리거해 생성이 막히는 병목의 원인이다.**
- **동작 정확히 + 사람 동작 구체화 (★ 프리셋 영상 방지):** 비트의 동작을 *정확한 실제 동작*으로 적는다. 예: 카페 결제 = "card tapped on the POS terminal"(추출기 위에 올리는 게 아님 — A3 오류). 트리트먼트의 동작을 임의 해석하지 말 것. **사람이 등장하는 컷은 인물의 움직임을 구체적으로 박는다 — 시작 자세 → 동작(손·발·고개·시선·표정) → 속도·방향·끝 자세까지. 동작을 비워두면 ① 모델이 빈 동작 정보를 학습된 *일반적 기본 모션*(그 장면에서 통계적으로 흔한 움직임)으로 채워 밋밋해지거나, ② 프롬프트가 특정 프리셋과 키워드가 닮아 플랫폼이 유사매칭으로 그 프리셋을 끼얹는다(STEP 5의 declined_preset_id로 강행). 둘 다 모델·플랫폼이 의도를 '이해'해 바꾸는 게 아니라 빈칸·키워드 유사매칭 탓이다 — 그래서 의도와 다른 '프리셋 영상'이 나온다(관측된 문제). 정적인 컷도 "subtle breathing, slight head turn" 등 미세 동작을 명시한다.**
- **트랜지션 방향:** `direction_observer_view`대로 카메라 방향 + 화면 streak 방향을 *둘 다* 박는다(예: "camera rotates right → world streaks LEFT").
- **토큰 위생 (컨텍스트 절감 · 413과는 별개):** 각 프롬프트는 **한 번만 작성해 도구 호출에 넘기고**, 이후 턴에서 전체 프롬프트를 다시 인용·반복하지 않는다(컷ID·완료·파일크기만 보고). 최종 프롬프트는 `seedance_prompt*.md`로 **파일 보관**. (413은 이미지가 원인이지 프롬프트가 아니다 — 이건 순수 토큰·비용 절감용.)

## STEP 5 — 생성·운용 (Seedance 2.0)
- **오디오 생성됨** — 응답 params `generate_audio:true`. 음악·SFX·VO 생성. VO 품질은 들어보고 필요 시 성우 교체.
- **mode = std / fast 둘뿐.** "Fast 말고"="std"(고품질). "pro" 없음.
- **길이** duration 4~15s. 15초×2를 ffmpeg `-f concat`으로 결합(STEP 7).
- **프리셋 가로채기(declined_preset_id):** "이 프롬프트는 프리셋 X 같다" 추천이 뜨면 그 ID를 `declined_preset_id`에 박아 리터럴 강행. **여러 번 연쇄될 수 있다** — 매 추천 ID를 기록하며 declined 체인으로 처리. (관측된 유발 키워드 — *미검증, 하드 블록 금지*: "ONE CONTINUOUS UNBROKEN SINGLE-TAKE", "vertical descent", "world freezes", "dark cafe interior". 가로채기가 잦으면 동의어로 대체 시도.)
- ※ 프리셋 가로채기(추천)와 아래 `ip_detected`(IP 모더레이션 차단)는 **다른 현상**이다. 섞지 말 것.

## STEP 5.5 — 산출물 진본 검증 (★ 프리셋/샘플/데모 영상을 결과물로 쓰지 않는다)

Higgsfield가 돌려주는 영상이 **내 job의 신규 생성물임을 확인하기 전엔** 어떤 클립도 결과물로 취급하지 않는다. **preset·sample·demo·template·gallery·example·preview 성격의 영상은 어떤 경우에도 최종 결과물이 아니다** — 플랫폼이 프리셋 유사매칭(STEP 5) 과정에서 기존 프리셋 미리보기/샘플 영상을 산출처럼 노출할 수 있다(가로채기와 동전의 양면).

1. **reference 없는 생성 금지.** 모든 `generate_video` 요청에는 **사용자가 승인한 실제 입력**이 reference로 들어가야 한다 — i2v = 확정컷 스틸의 실제 파일/업로드 UUID/URL(start_image·medias), t2v = 승인된 브랜드/캐릭터 레퍼런스(STEP 1.5). reference가 빈 요청은 보내지 않는다(승인 안 된 이미지로도 생성하지 않는다).
2. **수신 시 3종 대조.** 클립을 받으면 ① **job id** — 내가 생성 요청해 기록해 둔 job인가 ② **output video url** — 그 job id를 조회한 응답의 url과 일치하는가 ③ **reference 사용 여부** — 요청에 넣은 medias/start_image·duration·aspect_ratio가 job 응답 params에 그대로 박혀 있는가. 셋 중 하나라도 안 맞으면 그 url은 쓰지 않는다.
3. **URL·길이 성격 검사.** output url의 경로·파일명에 `preset`/`sample`/`demo`/`template`/`gallery`/`example`/`preview` 류 토큰이 보이거나, ffprobe duration이 요청 길이와 동떨어지면 프리셋 샘플로 의심 — 그 url 폐기, job id로 재조회, 진본이 없으면 **재생성**.
4. **최종 전달(video_ready) = 내 job의 신규 생성 output url만.** preset preview·tool preview·example url을 결합(STEP 7)이나 전달에 절대 쓰지 않는다.

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

## STEP 8 — 전달 전 점검 (★ 이미지/프레임 Read 금지 · 프로그램 + 사용자 판정)
**생성한 영상·프레임·이미지를 `Read`로 컨텍스트에 올리지 않는다.** 이미지/프레임 base64가 요청을 수십 MB로 불려 **`Request exceeds the maximum size`(413)**의 주원인이 된다. 자동 시각검수는 폐지하고, 전달 전 점검은 **프로그램으로만**:
- `ffprobe`로 각 클립·결합본의 duration·pix_fmt·코덱 확인(결합 후 재생 깨짐 방지 — STEP 7).
- 결합본 **파일이 실제로 존재 + 크기 정상**인지 확인(0바이트·수 KB면 실패).
- **진본 확인(STEP 5.5):** 결합에 쓴 **모든 클립**이 내 job id의 신규 생성 output인지 — preset/sample/demo/template/gallery/example/preview url **0건**, reference input 사용 확인.
- 제품 라벨·CRITICAL 비트·브랜드 모션타이포·한국어 VO를 **프롬프트 텍스트에** 다 넣었는지 프롬프트로 자가 점검(이미지로 열어보지 말 것).
**미적·내용 판정(라벨이 잘 보이나·인물이 맞나·모션타이포가 떴나)은 사용자가 영상을 직접 보고** 한다 — 에이전트가 프레임을 읽어 판정하지 않는다. 사용자가 "이 클립 다시"라고 하면 그 클립만 재생성.
(트레이드오프: 자동 시각검수를 빼는 대신 프롬프트를 정확히 써서 품질을 확보 — 검수로 잡던 품질차는 작고, 413·토큰 폭증을 막는 이득이 크다.)

## 하지 말 것
- 몽타주를 한 클립에 욱여넣기. 공간/인물 바뀌면 클립을 쪼갠다.
- `ip_detected`에서 사용자에게 안 알리고 혼자 재시도. 멈추고 알린다.
- 모더레이션을 톤 우회로 뚫기. (약관·근거 없음.)
- 긴 자막·약관을 영상에 굽기. 나레이션은 VO, 화면 자막 금지.
- 모든 컷을 주인공으로 가정. `subject_identity`를 따른다.
- 프리셋·샘플·데모·갤러리·example 영상을 결과물로 전달. 최종은 항상 **내 job id의 신규 생성 url**만(STEP 5.5). reference 없는 생성 요청도 금지.
- ffprobe·파일 존재 점검 없이 "완성" 전달. **단, 이미지/프레임을 `Read`로 열어보지 않는다(413 방지) — 시각 판정은 사용자.**

## 트리거 키워드
"영상으로 뽑아줘" · "영상화" · "i2v" · "Seedance" · "클립 생성/결합" · "30초 광고 영상" · 트리트먼트를 주며 영상 제작 요청.

## 함께 읽을 문서
- 입력 구조·인물 필드: `lsb-ad-planner` STEP 4(character_pool·narrative_structure·subject_identity) · `lsb-treatment-builder/REFERENCE/cut-schema.md`.
- 보드·product-lock·마스터시트: `lsb-treatment-builder` Phase 2·3.
- 타이포 처리: `lsb-treatment-builder/REFERENCE/typography-in-image.md`.

---
*버전: lsb-video-crafter_2606101000 · 2026-06-10 KST. (_2606101000 = **STEP 5.5 산출물 진본 검증** — preset/sample/demo/template/gallery/example/preview 영상을 최종 결과물로 사용 금지, 사용자 승인 이미지·컷의 실제 파일/URL을 reference input으로 필수 포함(reference 없는 생성 금지), 수신 시 job id·output url·reference 사용 여부 3종 대조, url/길이 성격 검사(프리셋 의심 시 폐기·재조회·재생성), video_ready 최종 전달은 신규 생성 output url만 + STEP 8 진본 확인·하지 말 것 연동.) 이전 lsb-video-crafter_2606081200 · 2026-06-08 KST. (_2606081200 = ① 4000자(char) 하드 최소·미달 제출 금지(제출 전 자가 카운트) ② 브랜드 모션타이포 모든 클립 필수 + QA 체크 ③ seamless transition 무조건(사용자가 하드컷 명시한 컷만 예외) ④ STEP 1.5 t2v 옵션 모드 — 사용자 선택 시 확정컷 스틸 대신 꼭 필요한 브랜드/캐릭터 레퍼런스만으로 t2v. ⑤ STEP 8 자동 이미지/프레임 Read 검수 폐지 → ffprobe·파일존재·프롬프트 자가점검 + 사용자 시각판정(요청 413·토큰 폭증 방지) · 프롬프트 재인용 금지·파일보관. ⑥ 영상 프롬프트 단위 4000자(char) 정정(구 4000단어) · 네거티브 성적·선정성 차단 문구 금지(모더레이션 트리거) · 사람 등장 컷 인물 동작 구체화(프리셋 영상 방지).) 이전 _2606051640 · 2026-06-05 16:40 KST. (_2606051640 = 총 길이 15초 최대 청크 분할·생성횟수 최소화(30=15/15, 35=15/15/5, 18=15/3) + '압축 마스터 영상' 금지·단일 concat 최종본 파일저장 + 프롬프트 빈약 금지(수천 자). 이전 _2606051100 = seamless transition 기본화 — 15/30/45/60초 전부 선행 클립 마지막 프레임=후행 클립 시작 프레임, STEP2·3 갱신.) 이전 _2606041430 = 렌더 대기 프로토콜 — 도구 호출 루프 치명결함 수정: sleep 900 1회·짧은 폴링 금지·예고 텍스트 금지·클립 일괄 대기. 허쉬 세션 A14.) 이전 _2606032044 = 신규 스킬, builder Phase 7 분리, A3 학습(다중 인물·교차편집·concat 코덱·ip_detected·preset 체인).*
