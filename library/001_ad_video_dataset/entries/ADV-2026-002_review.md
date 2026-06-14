# ADV-2026-002 Review

**Video file:** 카카오뱅크2.mp4
**Brand:** 카카오뱅크 (KakaoBank)  **Product:** 모임통장  **Year:** 2026
**Duration:** 81.92s  **FPS:** 23.976  **Resolution:** 1920x1080  **Shots:** 46
**Category:** 01_금융·핀테크 / 디지털뱅킹

## Campaign Summary
세상 모든 모임 (Every group in the world) — KakaoBank 모임통장 ensemble-lifestyle ad featuring 6 distinct friend/family groups: rock band, wakeboarders, car detailing club, baseball supporters, family birthday, wedding couple, and golf club. CG intro with yellow B lettermark, persistent product UI card overlays, slogan rally montage, brand end card.

## Pipeline
- probe.py: duration=81.92s, fps=23.976, 1920x1080, has_audio=true
- allframes: 1963 frames extracted (100%)
- metrics.py: 37 cut candidates detected
- scenedetect adaptive: 46 scenes confirmed
- audio.py: faster_whisper base, ko, speech_coverage=0.769, 10 narration lines
- midframes.py: 46 cutNN_mid.png + contact_sheet.png generated
- validate_entry.py: PASS (46 shots)

## Visual Notes
- wiggle_3d: NOT PRESENT — high metrics shift values from handheld action camera, not stereoscopic parallax (confirmed by visual inspection)
- Shot 19 (0.67s): whip-pan transition device
- Shot 23 (9.97s): longest cut — family restaurant with live balance animation
- Shots 37-44: rapid slogan rally montage (0.5-1.25s per beat)
- Yellow jerseys in baseball vignette intentionally match brand #FFE000
- Teal neon in car wash vignette provides deliberate cool contrast before warm brand yellow outro

## Shot Summary

| Cut | TC_in | Duration | Function | Copy |
|-----|-------|----------|----------|------|
| 01 | 00:00:00.000 | 4.004s | cg_intro |  |
| 02 | 00:00:04.004 | 1.877s | lifestyle_vignette |  |
| 03 | 00:00:05.881 | 2.002s | lifestyle_vignette | RocknGir.../0원 |
| 04 | 00:00:07.883 | 0.500s | lifestyle_vignette | RocknGirls 통장 / 3,147,000원 / 합주실 대여료 -120,000원 |
| 05 | 00:00:08.383 | 0.584s | lifestyle_vignette | 2,467,000원 / 공연장 대여료 -680,000원 |
| 06 | 00:00:08.967 | 0.584s | lifestyle_vignette | 2,467,000원 / 공연장 대여료 -680,000원 |
| 07 | 00:00:09.551 | 1.919s | lifestyle_vignette |  |
| 08 | 00:00:11.470 | 0.667s | lifestyle_vignette |  |
| 09 | 00:00:12.137 | 2.169s | product_feature_demo | 보드타러가자 |
| 10 | 00:00:14.306 | 1.460s | product_ui_demo | 모임통장 신청 완료 |
| 11 | 00:00:15.766 | 2.502s | lifestyle_vignette |  |
| 12 | 00:00:18.268 | 1.043s | lifestyle_vignette | 보드타러가자 / 300,000원 |
| 13 | 00:00:19.311 | 3.795s | wow_cut |  |
| 14 | 00:00:23.106 | 1.877s | product_feature_demo | 워시스턴트 transaction_list |
| 15 | 00:00:24.983 | 1.376s | lifestyle_vignette |  |
| 16 | 00:00:26.360 | 1.084s | lifestyle_vignette |  |
| 17 | 00:00:27.444 | 0.792s | lifestyle_vignette | 워시스턴트 / 824,000원 |
| 18 | 00:00:28.237 | 2.252s | lifestyle_vignette |  |
| 19 | 00:00:30.489 | 0.667s | transition_device |  |
| 20 | 00:00:31.156 | 1.877s | lifestyle_vignette | 옐로배트 서포터즈 통장 / 1,630,000원 / +30,000원 |
| 21 | 00:00:33.033 | 2.961s | lifestyle_vignette |  |
| 22 | 00:00:35.994 | 1.627s | lifestyle_vignette |  |
| 23 | 00:00:37.621 | 9.968s | lifestyle_vignette | 박남매 가족 통장 / 256,200원 → 406,200원 |
| 24 | 00:00:47.589 | 1.627s | product_feature_demo | 박남매 가족 통장 full transaction list |
| 25 | 00:00:49.216 | 1.251s | lifestyle_vignette |  |
| 26 | 00:00:50.467 | 1.585s | lifestyle_vignette |  |
| 27 | 00:00:52.052 | 0.584s | lifestyle_vignette |  |
| 28 | 00:00:52.636 | 1.001s | transition_device |  |
| 29 | 00:00:53.637 | 1.376s | lifestyle_vignette |  |
| 30 | 00:00:55.013 | 5.005s | lifestyle_vignette | 낭만골프클럽 / 2,070,000원 |
| 31 | 00:01:00.018 | 2.252s | wow_cut |  |
| 32 | 00:01:02.271 | 3.045s | wow_cut |  |
| 33 | 00:01:05.315 | 1.710s | product_ui_demo | B♡H 결혼준비 통장 / 17,290,000원 |
| 34 | 00:01:07.025 | 2.294s | lifestyle_vignette | wedding expense list on phone screen |
| 35 | 00:01:09.319 | 1.210s | lifestyle_vignette | member invite screen |
| 36 | 00:01:10.529 | 0.667s | lifestyle_vignette | yellow moim account action menu |
| 37 | 00:01:11.196 | 0.626s | slogan_rally_montage | 세상 모든 모임 |
| 38 | 00:01:11.822 | 0.500s | slogan_rally_montage | 세상 모든 모임 |
| 39 | 00:01:12.322 | 0.626s | slogan_rally_montage | 세상 모든 모임 / 모임통장으로 모여라 |
| 40 | 00:01:12.948 | 0.876s | slogan_rally_montage | 세상 모든 모임 / 모임통장으로 모여라 |
| 41 | 00:01:13.824 | 0.667s | slogan_rally_montage | 세상 모든 모임 / 모임통장으로 모여라 |
| 42 | 00:01:14.491 | 0.709s | slogan_rally_montage | 세상 모든 모임 / 모임통장으로 모여라 |
| 43 | 00:01:15.200 | 0.709s | slogan_rally_montage | 카카오뱅크 모임통장 |
| 44 | 00:01:15.909 | 1.251s | slogan_rally_montage | 카카오뱅크 모임통장 |
| 45 | 00:01:17.160 | 1.710s | product_ui_demo | 카카오뱅크 wordmark + legal fine print |
| 46 | 00:01:18.870 | 3.003s | product_ui_demo | 카카오뱅크 wordmark + full legal disclaimer text (excer |

## Search Keywords
- **industry**: ['finance', 'digital_banking']
- **product_category**: ['group_account', 'shared_account', 'fintech_app']
- **target_demo**: ['mz', 'late20s_early30s', 'hobby_community', 'young_adult']
- **media_format**: ['longform_landscape_82s', 'ensemble_vignette']
- **tone**: ['energetic_fun', 'friendly', 'community_warmth']
- **pacing**: ['fast_cut_montage', 'vignette_episodic']
- **technique**: ['product_card_overlay', 'ensemble_cast', 'kinetic_cta', 'cg_intro']
- **vfx_keywords**: ['ui_overlay_animation', 'whip_pan', 'lens_flare', '3d_cg_intro']
- **copy_strategy_keywords**: ['slogan_repetition', 'product_name_cta', 'use_case_demonstration']
- **concept_derivation_pattern**: ['slice_of_life_ensemble', 'product_demonstration_lifestyle']

**Validated:** 2026-06-13T06:05:10
**Analyst:** claude-sonnet-4-6 (automated)