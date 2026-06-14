# ADV-2026-016 — 토스 서비스 2 (Toss 신용등급 무료조회)

- **source file**: `토스 서비스 2.mp4`
- **brand / campaign**: Toss (Viva Republica) — 신용등급 무료조회 (credit rating free check)
- **category**: finance.credit_score · **duration**: 15.07s · **fps**: 29.97 · **aspect**: 16:9 (1920×1080)
- **shots**: 4 (scenedetect found 3; metrics caught the slide boundary at 8.21s → corrected to 4)
- **signature**: motion-graphics + app-UI demo, locked-off, no wiggle; brand-blue dominant, clean digital
- **hook**: 0.0s (3D credit speedometer) / verbal question at 6.07s · **CTA**: 8.21s (신용등급 무료조회)
- **audio**: faster_whisper (ko), 4 VO lines, coverage 0.54

## Cut-by-cut
1. **0–6.07s** — 3D semicircular credit gauge (red→blue); chrome needle sweeps between 2등급/4% and 9등급/10%, numerals incrementing — demonstrates credit grade → loan rate. Fineprint: "2019년 5월 전국은행연합회 자료 기준". Hard cut out.
2. **6.07–8.21s** — full-screen Toss-blue card, white text "당신의 신용등급은 ?" (hook question). Slides out as a phone enters from the left.
3. **8.21–13.51s** — split composite (panel_layout): left brand+copy zone (logo · "신용등급 무료조회" · "조회, 진단, 관리까지 한번에" · legal fineprint) | right phone app credit screen (신용관리 · 2등급 · 상위 13.0% ▲8% · 930/1000점 ▲32점). Key visual / CTA. Dissolve out.
4. **13.51–15.07s** — centered Toss logo end card on light field; narration "토스".

## Copy (verbatim)
- Headline: **신용등급 무료조회** · Sub: **조회, 진단, 관리까지 한번에**
- Hook: **당신의 신용등급은 ?**
- Gauge labels: 신용등급 2등급 / 대출금리 4 % → 9등급 / 10%
- VO: "당신의 신용등급은 / 토스 신용등급 무료조회 / 조회 진단 관리까지 한 번에 / 토스"

## Notes
No human subjects (pure motion graphics + UI). Year 2019 inferred from on-screen data citation. Whisper raw "무려조해" corrected to "무료조회" against captions. validate_entry.py → PASS (4 shots).
