# ADV-2026-039 — 검토용 리뷰

- **영상 파일:** `현대카드 2.mp4`
- **브랜드 / 캠페인:** 현대카드 / 현대카드 슈퍼콘서트 22 — 콜드플레이 (A Head Full of Dreams Tour) 내한 발표 필름
- **category_primary:** finance.card
- **총 길이:** 15.26s | **fps:** 29.97 | **해상도:** 1920x1080 (16:9, rotation 0) | **프레임:** 451
- **shot_count(검출/보정):** 0 (자동) → **4 (육안 보정)**
- **hook:** 0.0s (사운드 파형 인트로) | **CTA:** 14.02s (Hyundai Card 브랜드 로고)
- **오디오:** has_audio=true / faster_whisper(base) 전사 0 segments, speech_coverage=0.0 → **음성 나레이션 없음**(BGM 음악만) / narration_handling=none
- **capture_style:** 3d_cg (모션그래픽·키네틱 타이포, 실사/인물 없음) | **color_grade:** high_key | **texture_fx:** clean_digital
- **wow_cut:** 1 (무지개 사운드 파형 → COLDPLAY 워드마크 응집)
- **creative_device:** audio_waveform_to_wordmark_morph + emotional_apology_copy_hook
- **concept_derivation_pattern:** detail_to_whole_reveal

## 컷별 요약

| # | 프레임 | 시각(s) | dur | 기능 | 레이아웃 | 핵심 내용 (화면 카피 원문 보존) | 모션/트랜지션 |
|---|---|---|---|---|---|---|---|
| 1 | f1–f280 | 0.00–9.34 | 9.34 | brand_hook / artist_reveal | center, typo_only | 순백 배경 중앙 수평축에 무지개 스펙트럼 도트 **사운드 파형**이 음악 반응하듯 진폭 변조 → 컬러 입자가 응집해 **COLDPLAY** / **A HEAD FULL OF DREAMS TOUR** 무지개 워드마크로 정착(~7.9s) 후 페이드 | particle_assemble + morph, locked_off, accelerating / in:fade out:cut |
| 2 | f281–f337 | 9.34–11.25 | 1.90 | empathy_hook | center, typo_only | 블랙 한 줄 카피 **너무 늦어서 미안** (bold geometric sans, on white) | 정지(하드컷 in f281, diff 1.21) / cut–cut |
| 3 | f338–f420 | 11.25–14.02 | 2.77 | event_announcement | center, typo_only | **콜드플레이 / 현대카드 슈퍼콘서트 22** + **2017. 4. 15 (토) 오후 7시 잠실종합운동장 주경기장** + (캡션) **만 7세 이상 관람가** | 정지(하드컷 in f338, diff 3.33) / cut–cut |
| 4 | f421–f451 | 14.02–15.26 | 1.25 | brand_cta | center, typo_only | **Hyundai Card** 워드마크 + 라운드 사각 브래킷(카드형 로고 락업), on white | 정지(하드컷 in f421, diff 4.03) / cut–cut |

## 분석 노트 (요약)
- **자동 컷검출 0개**(scenedetect 1 scene, metrics cut_candidates 0): 순백 배경 위 작은 그래픽이라 diff가 미검출 수준. **전 프레임 육안 판독**으로 하드컷 4개 확정 — diff 스파이크 f281/f338/f421이 컷 경계와 정확히 일치. shot_count_corrected=4.
- **wiggle 수치**(mean_abs_shift_x=0.3657, sign_flips_ratio=0.424)는 cut1 무지개 사운드 파형의 도트 진폭 변조에 기인. 순수 카메라 wiggle_3d 아님(배경 정지, locked_off).
- **브랜드/콘텐츠**: manifest 브랜드는 '현대카드'이고 실제 콘텐츠는 현대카드 컬처마케팅(슈퍼콘서트 22, 콜드플레이 내한) 발표 필름. 화면 카피는 원문 보존, source_ref 브랜드=현대카드 유지.
- **제작연도 2017** 확정(화면 고지 '2017. 4. 15').
- **추상화**: 실사·인물 0, 로고 마크는 type-in-bracket 락업으로 generic 처리, 카피 원문 보존(짧은 카피·일시 verbatim).

## 산출물
- 엔트리: `ADV-2026-039.json` (validate **PASS**, 4 shots)
- 프레임: `ADV-2026-039_frames/` (cut01–04_mid.png + contact_sheet.png + frames_index.json)
