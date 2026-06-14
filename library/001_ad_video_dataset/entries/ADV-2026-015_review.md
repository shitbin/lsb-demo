# ADV-2026-015 — Review

**Source file:** `토스 서비스 1.mp4`
**Folder:** `01_금융·핀테크/토스/토스 서비스`
**Entry:** `ADV-2026-015.json` · **Review:** `ADV-2026-015_review.md`

## Top meta
- **Brand / product:** Toss (Viva Republica) — Toss app / 종합 금융 서비스 (all-in-one financial life)
- **Type:** Flagship **brand film**, flat 2D motion-graphics (illustrated lifestyle vignettes + app-UI demo). No live-action; all people are generic stylised illustrations.
- **Duration:** 66.78s · **fps:** 25 · **1920×1080** · **16:9** · **16 cuts**
- **category_primary:** `finance.fintech_platform`
- **Narrative arc:** Empathy → reframe → everyday vignettes → doubt/turn → "송금 = texting since Toss" → app-UI proof (한 눈에 보이는 금융) → transformation → brand promise.
- **Hook:** "금융. 멀고 어렵게 느껴지는 단어입니다." (finance feels distant/hard)
- **CTA / sign-off:** "나에게 금융이 필요한 순간, 토스" (tagline 60.56s → logo 64.04s)
- **Camera signature:** locked_off + simulated dolly/pan + top_down (2D motion-graphics). Metrics mean_abs_shift_x 1.225 / sign_flips 0.23 = lifestyle edit & scroll movement, **NOT 3D wiggle**.
- **Audio:** ko voiceover, coverage 0.948, bgm_likely true, transcribed_by faster_whisper. On-screen credit: 나레이션 토스팀 안지영. Protagonist named 지영.

## 16 cuts (one-liner each)
1. **0–4.48** — Royal-blue won (₩) coin bobs on pale grey financial slider rails; word "금융"; vertical-wipe out.
2. **4.48–9.0** — Overhead woven grid of streaming ₩ coins (one bright hero) = money flows through everyday life.
3. **9.0–11.24** — Protagonist (black hair, mustard coat, coffee) walks in profile inside a thin dotted orbit ring.
4. **11.24–24.92** — Long continuous overhead/side montage of 5 life moments: splitting a bill (calc 8,580) / first salary passbook / moving house (passbook 1,870,000) / buying a car / planning a vacation.
5. **24.92–28.12** — Tropical beach payoff (sunglasses, flower, orange cocktail); dissolving booking card "하와이 자유여행 1,359,000원~ · 예약하기".
6. **28.12–28.64** — Doubt onset: faded financial UI panels invade the carefree beach.
7. **28.64–32.88** — Worried face among financial UI incl. a red-X error window; "확신없고 막막할 때".
8. **32.88–33.8** — Abstract peach face-dot + scattered fragments on brand-blue = pivot into the transfer world.
9. **33.8–41.4** — 송금 = texting: ₩ token, then a contacts-avatar grid with 3 highlighted people; a finger taps a contact.
10. **41.4–44.64** — App greeting card "지영님 안녕하세요." with the user's circular avatar.
11. **44.64–47.0** — Spending card "이번 달의 지출 내역입니다." with a multi-colour donut + legend (카드대금/이체/기타/쇼핑/그 외 7개 카테고).
12. **47.0–49.2** — Savings card "자유 적금을 시작해보는 건 어떨까요?" with a colourful capsule bar row.
13. **49.2–53.6** — Full-screen app dashboard/timeline scroll (balances, 3월 타임라인 transactions) = 한 눈에 보이는 금융.
14. **53.6–60.56** — Scrolling 3-row icon recap of every money moment, blooming into spinning brand-palette colour arcs.
15. **60.56–64.04** — Overhead desk: a phone whose screen shows orbital colour rings around the glowing Toss logo core.
16. **64.04–66.78** — Centered cobalt speech-bubble + lowercase "toss" logo end card on a pale field; VO "토스".

## Voiceover transcript (corrected, ko)
1. 1.1–3.1 "금융."
2. 3.1–6.1 "멀고 어렵게 느껴지는 단어입니다."
3. 6.1–10.1 "하지만 돌이켜보면 우리는 늘 금융과 함께하고 있습니다."
4. 10.1–14.4 "친구들과 밥값 나눌 때"
5. 14.4–17.4 "처음 월급 통장을 만들 때"
6. 17.4–19.4 "이사를 갈 때"
7. 19.4–21.4 "차를 살 때" (raw "차를 사이 때")
8. 21.4–24.4 "근사한 휴가 계획 짤 때에도요" (raw "금사한 휴가게 애교 짤 때에도요")
9. 24.4–30.3 "그런데 내가 현명한 금융 생활을 하고 있는지"
10. 30.3–33.3 "확신 없고 막막할 때가 있지 않나요?"
11. 34.3–37.3 "어느 순간부터 많은 사람들에게 송금은" (raw "성금은")
12. 37.3–40.3 "문자를 보내는 것만큼 간편한 일이 됐습니다." (raw "문짜를")
13. 40.3–43.3 "토스와 함께했을 때부터 말이죠."
14. 43.3–46.3 "이제 토스는 모든 금융 생활을"
15. 46.3–49.3 "더 쉽고 간편하게 만들어 갑니다."
16. 49.3–55.4 "한 눈에 보이는 금융"
17. 55.4–60.4 "자신 없고 어렵기만 하던 나의 금융이 달라집니다."
18. 60.4–63.4 "나에게 금융이 필요한 순간"
19. 63.4–65.4 "토스"

## Validation
`validate_entry.py` → **PASS (16 shots)**, no warnings. All 27 required top keys, all 28 per-shot keys, t2i ≥500 words/cut, English search tokens, frame artifacts present.

## Abstraction notes
- All people are generic stylised flat-illustration characters (no real-person likeness).
- Brand logo rendered generically; merchant/bank names abstracted in UI (ㅁㅁ카드, ㅇㅇ카드, △△은행, ㅁㅇ은행, 가나다커피, AB레코드, 마마북스).
- On-screen Korean copy, narration and app/prop numerals preserved verbatim in the entry; visual descriptions abstracted to Level 2–3.
