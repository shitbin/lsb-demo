# ADV-2026-012 — So Win (Nike) — 검토표

| 항목 | 값 |
|---|---|
| 브랜드/제품 | Nike (브랜드 / 여성 스포츠) |
| 캠페인 | "So Win" — 2025 Super Bowl |
| 길이 / fps / 비율 | 60.1s · 23.976fps · 16:9 시네마틱 와이드 |
| 컷 수 | scenedetect 27 → **보정 60컷** (전 프레임 판독; 경계 누락컷 f1297 추가) |
| 카테고리 | apparel.sportswear |
| 촬영/그레이드 | live_action · **고대비 흑백(monochrome)** · 스튜디오 하드라이트 포트레이트 ↔ 실제 방송 footage 교차 · 헤비 슬로모 · 필름그레인 |
| 핵심 디바이스 | 카피를 끝까지 감추다 **도발→반전 2비트 타이포**: `YOU CAN'T WIN.` → `SO WIN.` (여성 선수의 no-win 이중잣대를 '그러니 이겨라'로 전복) |
| 오디오 | has_audio=true / **여성 매니페스토 VO 전사 완료**(faster-whisper base.en; model.bin을 HTTP range 청크로 우회 다운로드). speech_coverage 0.81, transcribed_by=faster_whisper |
| 판독 | **1441/1441 전 프레임** 원본 1080p 개별 판독 (30 세그먼트 + 2 경계보강 리포트) |

## 핵심 카피
### 음성 VO — 매니페스토 (faster-whisper 전사, verbatim)
> "You can't be demanding. You can't be relentless. You can't put yourself first. **So put yourself first.** You can't be confident. **So be confident.** You can't challenge. **So challenge.** You can't dominate. **So dominate.** You can't flex. **So flex.** You can't feel[=fill] a stadium. **So feel[=fill] that stadium.** You can't be emotional. **So be emotional.** You can't take credit. You can't speak up. You can't break records. You can't have any fun. You can't make demands. You can't keep scoring. You can't stand out. **Whatever you do, you can't win. So win.**"
- 구조: `You can't [X]` 도발 나열 → 각각 `So [X]` 명령으로 반전(애너포라/콜앤리스폰스) → `Whatever you do, you can't win. So win.`로 수렴.

### 화면 텍스트카드 (음성 climax만 노출)
- 도발 카드(f1339~): `YOU CAN'T WIN.`
- 반전/캠페인 라인(f1370~, 'SO WIN.' 2배 스케일): `YOU CAN'T WIN. SO WIN.`
- 엔드카드(f1420~): 흰색 Nike 스우시 (워드마크·태그라인 없음)

## 구조 (60컷 요약)
- **f1–263 도입 스튜디오 히어로**: 체조선수형 도발적 정면 응시(바 위 전방 리닝) → NIKE PRO/ELITE 트레이닝·농구 포트레이트.
- **f264–1338 교차 몽타주(본문)**: 스튜디오 하드라이트 포트레이트 ↔ 실제 방송 footage 고속 교차 — 육상(RICHARDSON·BUDAPEST), WNBA/대학농구(FEVER 22·CLARK·IOWA·Southern Cal·BARCLAYS·Las Vegas ACES·NEW YORK LIBERTY), 체조(CHILES 235), 축구(NIKE.COM/SOCCER·백색 의상 발레풍 히어로), 테니스(호주오픈·WILSON), 세계육상(ASICS). 헤비 슬로모 + 하드컷 리듬.
- **f1339–1390 타이포 페이오프**: `YOU CAN'T WIN.` → `SO WIN.` 풀스크린 화이트/블랙 정지 카드(하드컷 스톱).
- **f1391–1419 최종 히어로**: 흑백 슬로모 체조/무용 공중 스플릿(라이브액션).
- **f1420–1441 엔드카드**: 흰 스우시 on 블랙, 마지막까지 홀드.

## cross-pollination 메모
- 공식: **색 제거 + 슬로모 무게감 + 실제 방송footage 신뢰성 + 카피 withhold 후 2비트 타이포 반전(도발→명령)**.
- 화려한 컬러/3D/VFX형 광고(우리은행·배민·KREAM류)와 **강한 대조 신호** → contrast/distant 입력으로 가치 높음. 동일 카테고리(sportswear)는 와우컷 하드밴 유의.
- 데이터셋 내 자산: `ADV-2026-012_frames/`(컷별 중간프레임 60장 + contact_sheet.png + frames_index.json).
- ⚠️ 표절회피: 시각은 '여성 엘리트선수 유형'으로 추상화·선수 초상복제 금지, 스우시 generic. 방송 그래픽 원문은 보존(실제 신원 단서이나 묘사엔 미사용).
