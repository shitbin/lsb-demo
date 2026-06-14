# ADV-2026-021 — Review

- **Source file:** 토스 숨은 서비스 5.mp4
- **ID:** ADV-2026-021
- **Duration:** 52.22s @ 29.97fps (1565-frame long-form), 1080x1920 rot 0 → aspect 9:16
- **Brand / product:** 토스 (Toss) / 증명서 발급 (civil & government electronic certificate issuance)
- **Campaign:** 토스 숨은 서비스 — "토스 있으면 주민센터 안 가도 되는 이유" (Curator T)
- **Category:** finance.fintech (civic_service / govtech / document_issuance)
- **One-line summary:** A did-you-know hook (Toss has a community service center inside it) leads into an annotated phone-screen walkthrough of issuing government certificates — bundling a 전세자금대출 (lease-loan) document set, issuing three at once, viewing each and exporting as PDF — closing on a Curator T brand sticker.
- **Dominant technique:** caption-synced presenter-framed screen-recording walkthrough (talking-head + top-down phone UI demo)
- **Shot count:** 12 (shot_count_corrected: true)
- **Hook:** 0.0s · **CTA/endcard:** 50.05s · **wow cut:** 10 (the one-tap multi-issuance flow)
- **Validator:** PASS (12 shots)

## Cut list (start–end s · register · what happens · key caption / VO)

| Cut | Start–End | Register | Content | Caption / VO |
|----|-----------|----------|---------|--------------|
| 01 | 0.00–1.37 | live ECU | woman in lavender shirt, low-angle, warm cafe interior, hook | "토스 안에" / VO "토스 안에 주민센터 있는 거 알고 계셨어요?" |
| 02 | 1.37–3.57 | live ECU | magnifying-glass over her face, optical warp gag | "토스 안에" → "주민센터" |
| 03 | 3.57–6.17 | live MS | presenter at cozy desk counting on fingers | "등본, 초본 / 소득 금액 증명서까지" |
| 04 | 6.17–10.04 | live MS | presenter wider; paper title card slides in (CONTENT / SERVICE 토스주민센터 / 2024 / 공공서비스 / #team_공공프로덕트) | "토스 있으면 주민센터 안 가도 되는 이유" / VO "…발급받을 수 있다는 사실 알고 계셨나요?" |
| 05 | 10.04–14.05 | screen top-down | phone on tan leather, Toss search, typing 증명서, suggestion chips | "'전체 탭'에서" / "'증명서 발급하기'를 선택하면" |
| 06 | 14.05–18.95 | screen fullbleed | 증명서 발급하기 page (정부 전자증명서), 많이 찾는 증명서, long A–Z cert scroll | "이렇게 토스에서 발급받을 수 있는" / "각종 증명서들을 한눈에 볼 수 있는데요" |
| 07 | 18.95–21.99 | live MS | presenter holding black phone, gesturing | "필요한 서류들을 한 번에 묶어서" / "발급받을 수도 있어요" |
| 08 | 21.99–25.23 | screen top-down | 증명서 모아서 받기 bundles, tap 전세자금대출 서류 3종 | "이렇게 '전세자금대출용 서류'를 선택하면" |
| 09 | 25.23–27.66 | screen fullbleed | 전세자금대출에 필요한 서류 detail (1 주민등록등본 2 건강보험자격득실확인서 3 소득금액증명) + 신청하기 | "세 가지 서류를 한 번에 받을 수 있는데요" |
| 10 | 27.66–42.91 | screen top-down | LONG flow: 신청하기 → 주소/발급이유/기간/표시 checkboxes → 동의하고 발급하기 → 발급 진행 → 3개 발급 완료 → 내보내기 | "신청하기를 누르고" / "…정보를 하나씩 입력해주세요" / "이제 발급하기를 누르면" / "한 번에 이루어집니다" / "발급이 끝나면 각 증명서 내역을" |
| 11 | 42.91–50.05 | screen top-down | in-app document viewer (주민등록등본 1/2, red seal) → 어떤 증명서를 내보낼까요? (은행·기관 제출용 / 열람용) → iOS Mail compose w/ PDF (…51.pdf · 182KB) | "직접 확인할 수 있고" / "열람을 위한 PDF 파일로" / "저장할 수도 있어요" |
| 12 | 50.05–52.22 | endcard graphic | white paper field; "Curator T / 토스를 발견하다" blue brush-script sticker peels in & holds | "Curator T — 토스를 발견하다" |

## Notes
- 12 shots after cross-checking scenedetect macro-scenes against per-frame diff spikes + reading 129 native-res staged frames in order. Real hard cuts confirmed at f42, f108, f186, f302, f422, f569, f660, f757, f830, and f1501 (→ endcard, diff 113).
- The scenedetect 8.81s boundary (f265, diff 44) is a sub-gesture spike inside the continuous presenter+title-card take → merged into shot 4 (not a cut).
- The 42.91/43.44s boundaries (f1287/f1303) are the in-app PDF-viewer modal opening within the same flat-phone screen recording (huge white-load brightness change). Kept as the scene-11/12 structural boundary because it marks the distinct issue→view/export phase change; phone framing is identical, so it is not a camera cut.
- VO corrected against on-screen captions + Toss UI labels (등분→등본, 초반→초본, 소류→서류, 전세 작은 대출→전세자금대출, 연람→열람). Both text and text_raw retained per line.
- Image prompts keep logo marks generic; brand name 토스 and UI label text preserved verbatim only as caption text. Personal name on the exported PDF treated as a generic placeholder.

## Dataset paths
- Entry JSON: `01_금융·핀테크/토스/토스 숨은 서비스/ADV-2026-021.json`
- Review: `01_금융·핀테크/토스/토스 숨은 서비스/ADV-2026-021_review.md`
- Frames: `01_금융·핀테크/토스/토스 숨은 서비스/ADV-2026-021_frames/` (cut01_mid–cut12_mid.png + contact_sheet.png + frames_index.json)
