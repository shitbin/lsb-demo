# 키워드 vocabulary 표준 — 전 축 영문 토큰 통일 (lsb-treatment-builder_2606021505)

LSB 데이터셋의 모든 분류 라벨링은 이 표준을 따른다. **저장·인덱싱 값은 모두 영문 토큰**이다.
사용자/기획자는 한국어로 발상·검색해도 되며, planner가 한국어 브리프를 아래 **KO 별칭 표**로 영문 토큰에 매핑한다.

## 변경 요약

- 예전 분리룰(카테고리=한국어 / 기술=영어)을 **폐지**. 같은 데이터셋 안에서 ADV-001은 한국어, ADV-002는 영어로 박혀 인덱스가 깨지던 문제를 없앤다.
- 이제 `search_keywords`의 **10축 전부 영문 토큰**으로 저장한다. index 파일 `_meta.language`도 전부 `en`.
- HEX 컬러 코드는 `#값 그대로`(표준).
- 카피 원문·나레이션·`mood`·`category_tags`·`narrative_arc` 등 **서술/콘텐츠 필드는 한국어 유지**(이건 태그가 아니라 내용이다). 영문화 대상은 *인덱싱되는 search_keywords 태그뿐*.

> 키 이름(`industry`, `tone` 등)은 늘 영어(JSON 표준). 이번 버전부터는 **값도** 전부 영어 토큰.

## planner의 한국어 브리프 → 영문 토큰 정규화

- 사용자 브리프 키워드를 아래 표의 **KO 별칭**으로 찾아 영문 토큰으로 바꾼 뒤 인덱스 lookup.
- 예: 브리프 "MZ 사회초년생, 펀치 유머" → `target_demo=[mz, early_career]`, `tone=[punchy_humor]` → `index/by_target_demo.json["mz"]` + `index/by_tone.json["punchy_humor"]`.
- 별칭에 없는 새 표현은 의미상 가장 가까운 토큰에 매핑하고, 신규 토큰이 필요하면 이 표에 추가(영문 토큰 + KO 별칭 1개 이상).

---

## A. search_keywords — 영문 토큰 + KO 별칭 (인덱싱 대상)

### 1. industry (산업)

| 영문 토큰 | KO 별칭 |
|---|---|
| telecom | 통신 |
| finance | 금융 |
| insurance | 보험 |
| fashion | 패션 |
| beauty | 뷰티 |
| fnb | F&B·식음·외식 |
| beverage_alcohol | 주류·음료 |
| automotive | 자동차 |
| home_appliance | 가전·전자 |
| mobility | 모빌리티 |
| public_gov | 공익·정부 |
| education | 교육 |
| film_culture | 영화·문화 |
| conference_expo | 컨퍼런스·전시 |
| industrial_b2b | 산업B2B |
| semiconductor | 반도체 |
| construction_realestate | 건설·부동산 |
| luxury | 럭셔리 |
| healthcare_pharma | 헬스케어·제약 |
| it_saas | IT·SaaS |
| content_ott | 콘텐츠·OTT |
| ecommerce | 이커머스 |
| retail | 유통·리테일 |
| travel_tourism | 관광·여행 |
| sports | 스포츠 |
| sportswear | 스포츠·의류 |

### 2. product_category (제품·서비스 구체)

| 영문 토큰 | KO 별칭 |
|---|---|
| salary_account | 월급통장 |
| savings | 적금 |
| fund_securities | 펀드·증권 |
| card | 카드 |
| mobile_banking | 모바일뱅킹 |
| loan | 대출 |
| insurance_product | 보험상품 |
| data_plan | 요금제 |
| pickup_truck | 픽업트럭 |
| large_suv | 대형SUV |
| hybrid_car | 하이브리드차 |
| ev | EV·전기차 |
| sedan | 세단 |
| luxury_sedan | 럭셔리세단 |
| apartment_presale | 아파트분양 |
| same_day_delivery | 당일배송 서비스 |
| beauty_platform | 뷰티 플랫폼 |
| sportswear | 스포츠웨어 |
| performance_runningwear | 기능성 러닝웨어 |
| cosmetics | 화장품 |
| apparel | 의류 |
| sneakers | 운동화 |

### 3. target_demo (타깃)

| 영문 토큰 | KO 별칭 |
|---|---|
| teens | 10대 |
| 20s | 20대 |
| early_mid_20s | 20대 초·중 |
| late20s_early30s | 20대 후·30대 초 |
| 30s | 30대 |
| late30s_40s | 30대 후·40대 |
| 40s | 40대 |
| 50s_plus | 50대+ |
| senior | 시니어 |
| early_career | 사회초년 |
| office_worker | 직장인 |
| homemaker | 주부·맘 |
| student | 학생 |
| men | 남성 |
| women | 여성 |
| family | 가족 / 패밀리 |
| family_end_users | 가족·실수요 |
| couples | 부부·연인 |
| single_household | 1인가구 |
| mz | MZ |
| leisure_outdoor | 레저·아웃도어 |
| running_fitness | 러닝·피트니스 |
| active_consumers | 액티브 소비자 |
| premium_buyers | 프리미엄 구매층 |
| local_presale_prospects | 지역 분양 관심층 |
| active_senior | 시니어 액티브 |

### 4. media_format (매체·길이)

| 영문 토큰 | KO 별칭 |
|---|---|
| tvc_15s | TVC 15초 |
| tvc_30s | TVC 30초 |
| tvc_60s | TVC 60초 |
| shortform_vertical_30s | 숏폼 세로 30초 이하 |
| shortform_landscape_30s | 숏폼 가로 30초 이하 |
| shortform_vertical_30s_plus | 세로 숏폼 30초+ |
| digital_30s | 디지털 30초 |
| youtube_60s_plus | 유튜브 60초+ |
| sns_viral | SNS 바이럴 |
| ooh_led | OOH·옥외 LED |
| product_hero_film | 제품 히어로 필름 |
| presale_lifestyle_film | 분양 라이프스타일 필름 |
| cinemascope_lifestyle | 시네마스코프 라이프스타일 |
| feature_demo_film | 기능소구 필름 |
| pt_video | PT·키노트 영상 |

### 5. tone (톤·분위기)

| 영문 토큰 | KO 별칭 |
|---|---|
| cinematic | 시네마틱 |
| cinematic_serious | 시네마틱 시리어스 |
| cinematic_luxury | 시네마틱 럭셔리 |
| punchy_humor | 펀치·유머 |
| friendly | 친근 |
| warm_emotional | 감성·따뜻함 / 따뜻·감성 |
| emotional_lyrical | 감성·서정 |
| premium | 프리미엄 |
| luxury_minimal | 럭셔리·미니멀 |
| luxury_highend | 럭셔리·하이엔드 |
| serious_classic | 시리어스·정통 |
| serious_documentary | 시리어스·다큐 |
| kitsch | 키치 |
| retro | 레트로 |
| calm_refined | 차분·정제 |
| confident | 당당·자신감 |
| relaxed_healing | 여유·힐링 |
| family | 가족 |
| empathetic_comforting | 공감·위로 |
| upbeat | 경쾌 |
| clean_minimal | 깔끔·미니멀 |
| dynamic_powerful | 역동·파워 |
| refreshing | 청량·상쾌 |
| determined_focused | 결연·집중 |
| mystery_teaser | 미스터리·티저 |

### 6. technique (기법)

| 영문 토큰 | KO 별칭 |
|---|---|
| celeb_hook | 셀럽 후크 |
| anthropomorphism_character | 의인화·캐릭터화 |
| time_freeze | 시간정지·동결 |
| transformation | 변신·트랜스포메이션 |
| omnibus_series | 옴니버스·시리즈 |
| oner_walking_shot | 1테이크·워킹 샷 |
| splitscreen | 분할화면·split |
| teaser_mystery | 티저·미스터리 |
| mirroring_contrast_edit | 미러링·대비편집 |
| world_builder | 세계관 빌더 |
| call_and_response | 콜앤리스폰스 |
| balloon_typo_3d | 풍선타이포·3D |
| filmstrip_collage | 필름스트립·콜라주 |
| color_shift | 색 변환·color shift |
| bw_color_shift | 흑백↔컬러 톤전환 |
| glitch_crt | 글리치·CRT |
| facade_ooh_meta | 파사드·OOH 메타 |
| morph | 모핑·morph |
| landscape_travelling | 풍경 트래블링 |
| overhead | 부감·overhead |
| kinetic_typo | 키네틱 타이포 |
| silhouette_teaser | 실루엣 티저 |
| dark_to_light_reveal | 어둠에서 빛 리빌 |
| detail_closeup | 디테일 클로즈업 |
| signature_lamp_ignition | 시그니처 램프 점등 |
| product_solo_hero | 제품 단독 히어로 |
| anaphora_copy | 애너포라 카피 |
| lifestyle_cg_intercut | 라이프스타일+CG단지 교차 |
| nature_intro | 자연 인트로 |
| low_angle_tiltup | 로우앵글 틸트업 |
| location_map_graphic | 위치맵 그래픽 |
| empathy_copy_hook | 공감 카피 후크 |
| product_app_cutout_float | 제품·앱 컷아웃 부유 |
| dissolve_montage | 디졸브 몽타주 |
| direct_cta | 직접 CTA |
| slowmo_explosion_start | 슬로모 폭발 스타트 |
| fabric_macro_proof | 원단 매크로 기능증명 |
| product_solo_feature_demo | 제품 단독 기능소구 |

### 7. copy_strategy_keywords (카피 전략)

| 영문 토큰 | KO 별칭 |
|---|---|
| product_name_pun | 제품명 펀 |
| brand_name_pun | 브랜드명 펀 |
| refrain_repetition | 후렴 반복 |
| call_and_response | 콜앤리스폰스 |
| neologism_slogan | 신조어 슬로건 |
| question_hook | 의문형 후크 |
| imperative_slogan | 명령형 슬로건 |
| model_name_drop | 모델 이름 박기 |
| place_city_drop | 지명·도시 박기 |
| bilingual_subtitle | 영문+한국어 자막 |
| number_emphasis | 숫자·수치 강조 |
| building_climax | 점층 클라이맥스 |
| caption_led | 캡션 주도 |
| voice_caption_sync | 음성·자막 동기화 |
| leadership_declaration | 리더십 선언 |
| spec_caption_split | 스펙 자막 분리 |
| new_model_naming | 신차 네이밍 고지 |
| double_wordplay | 더블 워드플레이 |
| facility_subcopy_match | 시설 서브카피 매칭 |
| location_equation | 입지 등식 |
| empathy_to_solution | 공감→솔루션 전환 |
| immediacy_emphasis | 즉시성 강조 |
| brand_green_keyword | 브랜드 그린 키워드 강조 |
| superiority_declaration | 우위 선언 |
| feature_benefit_direct | 기능 베네핏 직설 |
| visual_copy_proof | 비주얼로 카피 증명 |

### 8. concept_derivation_pattern (사고법 분류 — freewillusion-handbook.md 12패턴 + 확장)

| 영문 토큰 | KO 별칭 |
|---|---|
| celeb_fashionfilm | 셀럽+패션필름st |
| time_bridge_metaphor_device | 시간 잇는 메타포 장치 |
| call_and_response_copy | 콜앤리스폰스 카피 |
| giant_character_world_builder | 거대 캐릭터·세계관 빌더 |
| metaphor_visual_sequence | 메타포 비주얼 시퀀스 |
| teaser_mystery_concept | 티저·미스터리 컨셉 |
| teaser_mystery_payoff | 티저·미스터리 회수 |
| highend_fantasy_fusion | 하이엔드 판타지 결합 |
| series_omnibus | 시리즈 옴니버스 |
| three_part_time_flow | 3파트 시간 흐름 |
| breaking_fourth_wall | 제4의 벽 넘기·메타 |
| space_structure_illustration | 공간·구조 일러스트레이션 |
| symbol_character_fusion_3d | 심볼+캐릭터 융합 3D |
| everyday_problem_metaphor_product_release | 일상 문제→비유 변환→제품 해방 |
| dark_to_light_reveal_structure | 어둠→빛 리빌 구조 |
| detail_to_whole_reveal | 디테일→전체 공개 |

> 신규 패턴은 자유 추가하되, 추가 시 freewillusion-handbook.md에 정의를 같이 적는다.

---

## B. 기술 vocabulary — 원래 영문 (그대로 유지)

촬영·편집 국제 표준이라 의역하지 않는다. 값 영문 유지.

### framing
`ECU / CU / MCU / MS / MLS / LS / WS / EWS / grid / environment`
(이전 표기 `그리드`→`grid`, `환경`→`environment`로 영문 통일)

### camera_angle
`eye_level / low_angle / high_angle / overhead / dutch / worm_eye`

### camera_motion
`locked_off / slow_dolly / push_in / pull_out / tracking / pan / tilt / handheld / crane / slide / cut_montage`
(이전 `정지`→`locked_off`, `컷몽타주`→`cut_montage`)

### camera_facing
`frontal / three_quarter / profile / back / overhead / none`

### vfx_keywords / vfx_in_shot
`wiggle_3d / parallax / color_pop / 3d_render / ui_motion / split_screen / time_freeze / morph / whip_pan / lens_flare / dust_simulation / glitch / atmospheric_haze / rim_light / light_reveal / data_viz / speed_ramp`

### transition_in / transition_out
`cut / match_cut / match_action / fade / dissolve / whip_pan / morph / wipe / push_in / pull_out / 360_spin / dolly_through`

### pacing
`front_loaded / slow_build / ramp_up / steady / ping_pong / back_loaded / accelerating`

### music_tempo_curve
`ramp_up / steady / ramp_down / ping_pong / build_drop`

### typo_motion
`pop / scale_in / slide_in / fade_in / kinetic / bounce / balloon_pop / fade_scale_out / glitch_in / static`

### intra_cut_rhythm
`static / steady / accelerating / decelerating / slow_build`

---

## 신규 등록 룰
- vocabulary에 없는 값을 박아야 하면: (1) 가장 가까운 기존 영문 토큰으로 매핑 시도 → (2) 정말 새 토큰이면 이 표에 `영문 토큰 + KO 별칭`으로 추가 → (3) entry 하단 `analyst_notes`에 신규 토큰 명시 → (4) `index_helper.py update`로 인덱스 갱신.
- vocabulary가 자라는 것은 정상. 단 통제 없는 자율 확장은 인덱스를 망가뜨린다.
