# editorial-layout.md — 트리트먼트 기본 디자인 시스템 (4K · 코덱스 리디자인급)

> 목적: lsb-treatment-builder의 **기본 출력 품질**을 "그라데이션 위 텍스트 중앙정렬"(저품질)에서
> **에디토리얼 키노트**(코덱스 리디자인급)로 끌어올린다. 코드는 `scripts/build_treatment_template.py` §8.
> 이 문서는 *무엇을 어떤 규칙으로* 배치하는지의 단일 출처. (양반김·우리은행 등 톤 시그니처는 `deck-styles.md`,
> 이 문서는 그 위에 깔리는 **공통 레이아웃·해상도·이미지 규율**.)

## 0. 왜 이 문서가 생겼나 (격차 진단)

클로드 1차 빌드 vs 코덱스 리디자인(허쉬 맥세이프) 대조 결론:

| 축 | 저품질(피해야 할 것) | 목표(리디자인) |
|---|---|---|
| 해상도 | 1920×1080 | **3840×2160 (4K)** |
| 이미지 | 표지·전략에 이미지 0장, 텍스트만 | 표지 히어로·컷보드 썸네일·풀블리드 KV **이미지 합성** |
| 레이아웃 | 전부 중앙정렬 텍스트 덤프 | **좌측정렬 위계 + 2단(텍스트+이미지/직접 조판)** |
| 팔레트 면 | (구) 크림 카드 강제 → **폐기** | **텍스트 박스 금지** — 다크 베이스 위 직접 조판, 호흡은 여백·명도 리듬·헤어라인 (★ 디렉터 확정 지시 _2606110030) |
| 컷 개관 | 이미지 1장 + 여백 | **컷보드 = 썸네일 그리드 1장** |

이 5축이 이 시스템의 강제 항목이다. (구버전 _2606041330의 "크림 surface 적극 사용"은 디렉터 지시로 **폐기** — 크림/미색 채운 텍스트 박스를 어떤 페이지에도 쓰지 않는다.)

## 1. 캔버스 · 그리드 · 해상도

- **논리 좌표 1920×1080, 출력 ×SCALE(=2) → 3840×2160.** 코드에서 좌표·폰트는 논리값으로, `S()`/`Ft()`가 ×2.
- 마진 `MARGIN=96`, 거터 `GUTTER=48`, 라운드 `RADIUS=28`(논리px).
- 2단 분할 기준선: 텍스트 컬럼 ≈ 좌측 0~52%, 이미지/카드 ≈ 54~(100−마진). 표지는 텍스트 0~52% / 히어로 54~100%.
- 푸터(좌: 스튜디오/우: AD TREATMENT)·eyebrow(섹션 키커)는 전 페이지 일관.

## 2. 팔레트 토큰 (THEME_EDITORIAL, 브랜드별 덮어쓰기)

```
bg          페이지 다크 배경 (예 #2A0A12)
surface     bg보다 살짝 밝은 동계열 다크 면 (예 #3A1C23) — 이미지 플레이스홀더 등 비(非)텍스트 면 전용
surface_ink surface 위 잉크 (밝은 색 — ink와 동일 계열)
ink         다크 위 본문/제목 (예 #F5EEE7)
muted       보조 텍스트
point       포인트 1강조색 (예 #C9882F) — 블록당 1곳
line        구분선·디바이더·헤어라인
```
- **브랜드 가이드가 있으면 hex 그대로 덮어쓴다**(Phase 4.3). point는 브랜드 1순위색.
- **★ 텍스트 박스 금지(디렉터 확정 지시):** 텍스트 뒤에 채운 면(크림·미색·라이트 카드)을 깔지 않는다. `surface`를 텍스트 배경으로 쓰지 말 것 — 텍스트는 항상 bg 위 직접.
- 페이지 리듬은 면 교대가 아니라 **밀도 교대**로: 텍스트 페이지(여백 크게·위계 강하게) → 풀블리드 KV(임팩트) → 컷보드(그리드 밀집) → … 단조로우면 여백·명도 리듬·헤어라인·이미지 배치로 푼다.

## 3. 타입 스케일 · 위계 (좌측정렬 기본)

- eyebrow(키커): 22px, 레터스페이스, point색, (번호 있으면 Black 굵게).
- headline: `fit_headline()`이 컬럼폭에 맞춰 56~132px 자동. **좌측정렬**(슬로건 1~2줄만 center).
- body: 20~24px, muted, leading 1.5, 의미단위 줄바꿈.
- caption/label: 15~18px.
- 1강조: `typeset`의 `*..*` 마크업으로 블록당 1구만 point색(나머지 기본색).

## 4. 레이아웃 아키타입 (코드 = template §8)

| 함수 | 용도 | 구성 |
|---|---|---|
| `cover_split(im,d,theme,title,sub,tags,hero)` | 표지 | 좌: eyebrow→대형 headline(+1강조)→sub→태그칩 / 우: **히어로 이미지**(라운드) |
| `two_col(im,d,theme,headline,body,eyebrow_num,eyebrow_txt,proof_points=...,side_img=...)` | 전략·논증·비교 | 좌: eyebrow(번호)→headline→body / 우: **PROOF 직접 조판**(세로 헤어라인 구분 + point 불릿, 박스 없음) 또는 이미지. 겹침 게이트 내장 |
| `fullbleed_kv(im,d,theme,hero,lines)` | 키비주얼·임팩트 | 풀블리드 이미지 + 하단 스크림 + 좌하단 텍스트 |
| `cut_board(im,d,theme,title,thumbs,labels,cols=4)` | 컷 개관 | 제목 + **썸네일 그리드**(라벨), 행 넘치면 자동 축소 |

- 단독 컷/콘티 디테일 페이지는 기존 `s_cut_public/s_cut_internal`(4.1-a) 유지하되 이미지 존을 크게.
- 모든 아키타입은 `rounded_img()`로 이미지를 **cover-fit + 라운드** 합성; 이미지 없으면 다크 surface 플레이스홀더(실빌드에선 금지 → ⑩ 게이트).

## 5. 이미지 규율 (IMAGE MANDATE)

- **표지·키비주얼·컷보드·씬 페이지 = 이미지 필수.** 소스: `hero_stills/`(와우컷·KV·표지·클로징), `확정컷/`(컷별), 마스터시트.
- product-lock 캠페인은 실제 제품 이미지를 그대로 합성(생성 라벨 금지 — Phase 3.2 product-lock).
- `assert_images_present(page_kind, placed_flags)`로 0장 보류. placed_flags는 `rounded_img()`가 반환하는 `has`를 모은 것.
- 한국어 카피는 이미지에 굽지 말고 PIL 텍스트로 위에 합성(두부·깨짐 방지).

## 6. 빌드 골격 (권장 순서)

```python
import build_treatment_template as T
T.set_fonts(TITLE_TTF, BODY_TTF)
TH = dict(T.THEME_EDITORIAL); TH.update(brand_palette)   # 브랜드 hex 덮어쓰기
pages=[]; flags=[]
im,d = T.new_canvas(TH); T.cover_split(im,d,TH,title,sub,tags,hero=hero_cover); pages.append(im)
im,d = T.new_canvas(TH); T.two_col(im,d,TH,h,body,eyebrow_num="05.",proof_points=[...]); pages.append(im)
im,d = T.new_canvas(TH); T.cut_board(im,d,TH,"30초 컷보드", thumbs=확정컷목록); pages.append(im)
...
T.save_pdf(pages, OUT_PDF, dpi=150)
```
- 텍스트-주인공 페이지는 `typeset()/fit_headline()/draw_block()` 경유(4.2-a), 빌드 직전 `assert_no_overlap`·`assert_font_floor`·`assert_images_present` 게이트.

## 7. 자가검사 (Phase 5 연동)
- [ ] 출력 3840×2160? (⑪)
- [ ] 표지/KV/컷보드/씬에 실제 이미지 합성? (⑩)
- [ ] 텍스트 뒤 채운 박스(크림·미색·라이트 카드) 0개? 텍스트 전부 배경 위 직접? (⑫)
- [ ] 좌측정렬 위계(중앙정렬은 슬로건만)? eyebrow·footer 일관?
- [ ] 컷보드 1장 존재?
- [ ] 텍스트↔패널/이미지 겹침 0(assert_no_overlap)?
