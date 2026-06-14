# ADV-2026-023 — Review

- **Video file:** 토스 숨은 서비스 7.mp4
- **ID:** ADV-2026-023
- **Duration:** 31.70s
- **FPS:** 29.97
- **Aspect:** 9:16 (1080x1920)
- **Shot count:** 5
- **Brand / Product:** 토스 (Toss) — 토스 앱 / 숨은 서비스 (따릉이 타기, Seoul public-bike rental hidden service)
- **Campaign:** 토스 숨은 서비스 7 — "토스로 쉽게 따릉이 타기" (creator series: Curator T / 토스를 발견하다)
- **Category:** finance.fintech
- **One-line summary:** A vertical creator-style how-to that demonstrates renting a Seoul Ttareungi public bike entirely inside the Toss super-app — opening at a real bike station, running the full in-app flow as one continuous phone screen recording, scanning the bike's QR to unlock, and paying off with the presenter walking the freed bike down a sunny winter street.
- **Dominant technique:** Continuous in-hand screen-UI walkthrough (tutorial demo) with step-by-step voiceover mirrored by lower-center subtitle pills, bookended by live-action and a QR-unlock macro.

## Structure
- 4 confirmed hard cuts (scenedetect + metric diff spikes at 4.404 / 22.289 / 26.193 / 29.396) → 5 shots.
- The 4.40–22.29 block is ONE continuous phone screen recording (Toss UI changes through the flow but framing never cuts) → single shot per spec.
- Whisper `text_raw` mis-hears 따릉이 as 다른/다른 길 and 대여 as 대화; corrected against on-screen subtitles which mirror the VO.

## Corrected VO / caption lines (Korean)
1. 토스로 따릉이 빌릴 수 있대요. 제가 바로 빌려볼게요.
2. 전체 탭에서 따릉이를 선택해 주세요.
3. 지도를 통해 따릉이 대여소 위치를 확인할 수 있는데요.
4. 이제 대여하기를 눌러줍니다.
5. 내게 맞는 이용권을 선택하고
6. 토스에 등록된 결제 수단으로 결제까지 진행하면
7. 대여 준비가 모두 끝났어요.
8. 안장 뒤에 있는 QR 코드를 인식하면
9. 잠금이 풀리면서 따릉이를 이용하실 수 있어요.
- End card: **Curator T / 토스를 발견하다** (creator signature sticker, not an official Toss logo lockup)

## Cuts (one line each)
| # | Time (s) | Framing | Function | What happens |
|---|----------|---------|----------|--------------|
| 1 | 0.00–4.40 | MS | hook / presenter intro | Woman in black puffer at a Ttareungi station holds a phone; printed CONTENT title card ("토스로 쉽게 따릉이 타기") slides up. VO: "토스로 따릉이 빌릴 수 있대요." |
| 2 | 4.40–22.29 | ECU | core screen-UI walkthrough | One continuous in-hand Toss screen recording: 전체 tab → 따릉이 mode → station map (15대) → 대여하기 → 이용권 (1일 1,000원…) → 토스뱅크 체크카드 결제 → "1일권을 구매했어요". Subtitles step through the flow. |
| 3 | 22.29–26.19 | ECU | product detail / QR unlock | Macro of the bike lock (white QR sticker "57322", green release lever); phone enters and scans, Toss scanner reads "QR코드는 안장 밑에 있어요 / 문자 코드 입력하기". Subtitle: "인식하면". |
| 4 | 26.19–29.40 | MS | real-world payoff | Presenter walks the unlocked mint-green 따릉이 (basket reads 따릉이) toward a backward-tracking camera down a sunny tree-lined sidewalk past the kiosk. Subtitle: "따릉이를 이용하실 수 있어요". |
| 5 | 29.40–31.70 | ECU | creator signature end card | Hand-stamped paper sticker peels and settles: blue "Curator T" with "토스를 발견하다" beneath on off-white paper. |

## Validator
- `validate_entry.py` → **PASS (5 shots)**, no warnings.
- All 5 t2i_start_frame prompts 507–647 words (≥500 required).
