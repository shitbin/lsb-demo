# ADV-2026-011 — Dish with ChatGPT (OpenAI · ChatGPT) — 검토표

| 항목 | 값 |
|---|---|
| 브랜드/제품 | OpenAI — ChatGPT (consumer AI assistant) |
| 캠페인 | "Dish with ChatGPT" (2025) |
| 길이 / fps / 비율 | 30.03s · 23.976fps · 16:9 컨테이너에 2.39:1 레터박스 |
| 컷 수 | scenedetect 1 → **보정 7컷** (하드컷 0건; 전부 심리스 모핑/매치) |
| 카테고리 | IT.ai_product |
| 촬영/그레이드 | live_action · 따뜻한 로우키 필름 그레이드 · 핸드헬드 푸시인/연속 풀아웃 · 필름그레인 |
| 핵심 디바이스 | 무언의 감정 몽타주를 **타이핑된 ChatGPT 프롬프트 한 줄**이 사후 재맥락화 → 감성·위트 있는 레시피 응답이 스크롤되며 창밖 브릭 외관으로 연속 풀아웃 → ChatGPT 로고 엔드카드 |
| 오디오 | has_audio=true / faster-whisper 전사 완료 → **음악 베드 + faint 대사 몇 마디('Good?/Yeah?/Very good.')뿐, 구조적 VO 없음** 확인. 카피=화면 ChatGPT 대화 verbatim, transcribed_by=faster_whisper |
| 판독 | **720/720 전 프레임** 원본 1080p 개별 판독 (13개 세그먼트 리포트) |

## 핵심 카피 (verbatim, 화면 타이핑 대화)
- 프롬프트: `I need a recipe that says, "I like you, but want to play it cool."`
- 응답 헤드라인: `Here's the move: Lemon-Garlic Butter Pasta with Cherry Tomatoes.`
- 사인오프: `Above all, don't sweat it. You got this.`
- 엔드카드: ChatGPT 로고 마크 + `ChatGPT` 워드마크 (태그라인·URL 없음)

## 컷별 한 줄
1. **f1–144 (0–6.0s)** ECU→CU, 여성이 첫 한 입을 음미 — 무언의 친밀, 느린 푸시인 / 모핑아웃.
2. **f145–216 (6.0–9.0s)** 식탁, 파트너와 함께 — 손을 얼굴로, 눈물 참는 감정 비트(모핑).
3. **f217–277 (9.0–11.5s)** 식탁, 활기찬 대화·웃음, 남성이 좌측으로 진입 — 관계의 온기.
4. **f278–360 (11.6–15.0s)** 주방서 함께 요리, 화분 건네기 — **ChatGPT 프롬프트 자막 등장**(영상 전체 재맥락화), 응답 시작. ★hinge.
5. **f361–445 (15.0–18.6s)** 연속 풀백 시작, 응답(Why This Works·The Flow) 라인별 타이핑.
6. **f446–613 (18.6–25.6s)** 창밖으로 빠져나와 브릭 외관, 응답 전문 스크롤 + 브랜드 락업 페이드인. ★wow.
7. **f614–720 (25.6–30.0s)** ChatGPT 로고+워드마크 엔드카드, 마지막 프레임까지 홀드.

## cross-pollination 메모
- 공식: **감정 먼저 / 기능 안 보임 + 심리스 모핑 + 카피=화면대화**. 기능 직설형(우리은행·배민류)과 **정반대 대비 신호** → distant/contrast 입력으로 가치 높음.
- 데이터셋 내 자산: `ADV-2026-011_frames/`(컷별 중간프레임 7장 + contact_sheet.png + frames_index.json).
