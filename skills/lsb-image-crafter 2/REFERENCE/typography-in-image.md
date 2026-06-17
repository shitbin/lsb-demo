# typography-in-image — 컷 이미지에 타이포를 박아 생성하는 규칙
*버전: lsb-treatment-builder_2606021645 · 2026-06-02 16:45 KST. 범용.*
> **현 스킬 Phase 3.2 / 3.2-a의 "보드엔 텍스트 절대 금지(텍스트는 후처리)" 전면 규칙을 대체**한다.

## 0. 원칙 전환 (왜)
기존 규칙은 "보드/컷 이미지엔 `ABSOLUTELY NO text`, 텍스트 VFX는 모양만, 텍스트는 후처리"였다. 이유는 ① 구형 모델의 글자 깨짐 ② 스토리보드 자동 주석 방지였다.

그러나 광고에서 **타이포는 후처리 잉여가 아니라 핵심 비주얼 시그니처**다 — 우리은행 풍선타이포 "3.1%", ANTA 형광 키네틱 헤드라인, 올리브영 키네틱 카피, KT "다되G". 이런 컷은 *타이포까지 보여줘야* 연출 의도가 전달된다. 또 최신 모델(nano_banana_pro·gpt_image_2)은 **짧은 한/영 텍스트 렌더가 가능**(긴 문장·약관·정밀 숫자는 여전히 불안).

**새 원칙:** 영화식 자막(나레이션/대사 lower-third)만 후처리로 빼고, **강조 단어·헤드라인·키네틱/모션 타이포·타이포 키비주얼은 이미지 생성 프롬프트에 박아서 생성**한다. 단, **모든 컷이 아니라 강조·텍스트모션이 필요한 컷에만.**

## 1. 컷별 타이포 모드 — 3분류
각 컷에 `typo_mode` 부여:

| mode | 무엇 | 이미지 처리 |
|---|---|---|
| **none** | 텍스트 없는 순수 서사·무드 컷 (대부분) | 텍스트 없음 |
| **subtitle** (post) | 영화식 자막/나레이션, 긴 문장, 법적 고지, 정밀 수치 | 깨끗한 plate로 생성 → **텍스트는 후처리(편집)** |
| **baked** (in-image) | 강조 단어/슬로건/헤드라인 락업/키네틱·모션 타이포/타이포 키비주얼 | **이미지 프롬프트에 텍스트+스타일+배치+모션감 명시해 박아 생성** |

## 2. 판정은 데이터셋(analyzer)으로 — 결정 규칙 ★
"이 컷에 타이포를 박을지"는 감이 아니라 **cross-pollination으로 같은 유형·톤 레퍼런스가 어떻게 했는지 보고** 정한다. analyzer entry의 아래 필드를 읽는다:

- **`typography.typo_motion_dominant` / `typography.animation_style[]`** (pop·kinetic·bounce·풍선등장·track_in·scale_in…) → 모션타이포가 강한 레퍼런스면, 해당 기능 컷(후크/펀치/베네핏 수치/후렴/CTA)에 **baked**.
- **`copywriting.lines[].source`** = `caption` 또는 `both` → 화면 자막으로 나온 카피 = 타이포 대상. `voice`-only → none/subtitle.
- **`typography.key_typography_moments_sec`** + **`vfx.primary_effects`** 에 `3d_render`(풍선타이포)·`color_pop`·`glitch`·`ui_motion` → 타이포가 *비주얼 이벤트*인 컷 = **baked**.
- **`recurring_motifs[]`** 에 타이포 모티프(예 "우월 컬러박스 타이포", "옐로 키네틱 헤드라인", "브랜드 그린 키네틱 카피") → 그 유형은 타이포를 화면 시그니처로 씀 → baked 적극.
- **`typography.subtitle_position_dominant`** = floating/center/그리드 → 키네틱/플로팅이면 baked, lower_third 위주면 subtitle.
- 컷의 **`function`**: hook·펀치·후렴·베네핏(수치)·CTA·엔딩 → baked 후보 / general 서사·무드 → none·subtitle.

**가중치(§4.3 동일):** 동일·인접 유형이 강조컷에 타이포를 박으면 우리도 박되, **와우컷은 동일 카테고리의 타이포 시그니처를 직접 복제 금지**(형태·배치·모션 원리만 추상화, 카피는 우리 것). 데이터셋이 없으면 핸드북 카테고리 기본값(서비스/펀=baked 많음, 시네마틱 드라마=baked 적고 subtitle/none 위주).

**산출:** 각 컷에 `typo_mode` + (baked면) `baked_typo` 스펙을 plan(treatment.json)에 박는다. 컷 스키마의 기존 `copy_overlay·typo_motion·typo_color_strategy·layout_grid`를 그대로 활용해 채운다.

## 3. BAKED 타이포 프롬프트 패턴 (이미지 생성에 결합)
컷의 `copy_overlay`(원문, 짧게) + `typo_motion` + `typo_color_strategy` + `layout_grid`를 영어 이미지 프롬프트 한 구로 변환. 요소:
- **텍스트 원문**(짧은 강조어/슬로건만) + **언어**(KO/EN)
- **폰트 느낌**: heavy rounded sans / condensed / serif italic / handwritten…
- **컬러**: 브랜드 hex
- **배치**: upper-right third / center / opposite the subject / on a color box / over negative space
- **크기·통합**: integrated into the scene lighting & perspective (스티커처럼 붕 뜨지 않게)
- **모션의 한 순간 포착**(정지 이미지지만 모션타이포를 암시): "mid-pop bounce", "speed-streak trailing", "3D balloon inflating", "kinetic slide-in blur"

예시:
- (서비스/펀) `bold rounded Korean headline "데이터, 프리덤" in lime #E0FF53 on a small mint color-box, upper-right third, mid-pop bounce with slight 3D extrusion, integrated into scene light. Crisp, no garbled letters.`
- (수치 강조) `large 3D balloon-style number "2X" in mint #11E6D8, center, inflating mid-motion, glossy. Short, crisp text only.`
- (시네마틱) 대개 none/subtitle. 굳이 baked면 절제된 세리프 소형 락업.

**가드:** 긴 *러닝 자막*·약관·정밀 수치 표만 subtitle(후처리). **메인 카피·헤드라인·CTA·강조는 한국어라도 무조건 baked** (gpt_image_2 한글 재현 신뢰 — _260614 사용자 확정: baking 시도/폴백 없음, 짧게/영문화 우회 금지). negative엔 `garbled text, extra letters, misspelled`만(텍스트 자체는 허용 — 전면 "no text" 금지 해제). 한국어를 후처리로 미리 빼지 말 것.

## 4. 영상화(i2v) 연결
- **baked** 컷은 모션타이포가 핵심 → `recreation_prompts.i2v_motion`에 타이포 애니 명시(pop-in, kinetic slide, balloon inflate, speed streak).
- **subtitle** 컷은 plate만 움직이고 자막은 편집에서.
- **트랜지션 보드**에 타이포가 가로지르면 단일 캔버스에 함께 그린다.

## 5. 자가검사
1. **누락**: 후크/펀치/수치 베네핏/CTA/엔딩 컷인데 타이포가 비었나? → 데이터셋 확인 후 baked 검토.
2. **과잉**: 서사·무드 컷까지 타이포를 박았나? → 강조 컷에만. 나머지는 none.
3. **오배치**: 긴 문장·법적고지를 이미지에 박았나? → subtitle로 내려 후처리.
4. **재생성 규칙**: baked 한국어는 무조건 baked로 간다(가정상 깨지지 않음 — gpt_image_2 한글 신뢰). 만약 특정 1컷에서 글리프가 실제로 깨지면 *영문화/생략이 아니라* 같은 한국어로 재생성한다(짧게·영문 우회 금지). 긴 러닝자막·약관·정밀 수치 표만 subtitle(후처리).
5. **표절**: 와우컷 타이포가 특정 광고 시그니처를 그대로 베꼈나? → 원리만, 카피·색·배치 새로.

## 6. 한 줄 요약
**타이포는 후처리 자막이 아니라 연출이다. 강조·모션 타이포 컷은 이미지에 박아 생성하고, 어느 컷이 그런 컷인지는 애널라이저 데이터셋이 같은 유형 레퍼런스에서 타이포를 어떻게 썼는지로 판정한다. 단, 강조 컷에만 — 서사 컷은 비운다.**
