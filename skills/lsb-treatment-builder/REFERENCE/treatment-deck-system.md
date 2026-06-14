# Treatment Deck System — the single source of truth for building LSB treatment PDFs

> Reverse-engineered from 35 real studio decks in the reference folder (Yangban Kim, Woori
> Bank, Air Force, KT outdoor, KT G-EYE, LG, KG, Ministry of Health, Shinsegae, NEXO, DMZ,
> INSTEROID, Baemin, KT-Y, etc.). The code that renders all of this is `scripts/treatment_deck.py`.
> If anything here and the code disagree, fix the code to match this doc.

This document assumes you have **no prior conversation context**. Everything you need to build
a good treatment deck is here. Read it top to bottom before writing any build script.

## 0. Proposal vs Treatment vs PPM (know which one you are making)
A "deck" can be one of three things. They look different and contain different things:
- **Proposal (기획안):** sells the strategy, concept, logline, mood, color direction. Stills are
  rough "to be refined" examples. Text/copy heavy.
- **Treatment (트리트먼트):** sells *how the film will actually look* — locked cinematic frames,
  cut numbers, narration, sometimes the generation prompt. The cuts are the star. **This is what
  this skill builds.**
- **PPM (pre-production meeting):** logistics — location, casting, art, schedule, budget. Tables. Separate.

The more it is a proposal, the more copy/text and the more stills are just examples. The more it is
a treatment, the more locked cuts, cut numbers, and narration dominate the pages.

## 1. Two base modes (pick one by brand/genre)
- **Cinematic dark:** background near-black `#000` or charcoal `#1C1C1E–#212121`. The cut is the
  star; text sits directly on the background. (Yangban, Air Force, NEXO, DMZ, Maekyung, KG)
- **Editorial light:** background white `#FFF`. Strategy and white space are the star. (LG, Ministry
  of Health, KBS, Shinsegae storyboard, KT body pages)
- Both modes: **never put a filled panel behind text.** Dark mode = text on background; light mode =
  text on white. A tinted/cream card behind copy is an anti-pattern (this was a repeated director
  complaint — see also REFERENCE/humanize-deck-copy.md and the "no text box" rule).

## 2. ★ IMAGE RATIO LAW (the most-broken rule — absolute)
This is the #1 thing past builds got wrong: they cropped every image to a uniform 16:9 and destroyed
the original framing. Rules:
1. **Reference / external photos = preserve original ratio 100% (`contain`, letterbox/pillarbox).**
   Never crop or distort someone else's photo.
2. **Your own storyboard cells = set the CELL ratio to the cut's own ratio, then `cover`.** If the
   campaign is 9:16, the cells are 9:16; if 16:9, cells are 16:9. **Never force an image of one ratio
   into a cell of a different ratio with `cover`** — that is the ratio destruction to avoid.
3. **Single cinematic hero / standalone cut = `contain` letterbox** (a frame floating on the dark page).
4. **Code default = `place_image(mode="auto")`:** if the image ratio ≈ cell ratio (within ±8%) it
   uses `cover`; otherwise it falls back to `contain` (letterbox). This makes accidental cropping
   impossible unless you explicitly force `mode="cover"` (only the full-bleed key visual should).
5. Gutters thin (hairline ~3%). In dark mode the gutter shows the black background and separates frames.
6. Collage layouts (Woori-style) may use variable-ratio cells (big main + small supporting) instead of
   a rigid N×M grid — still each cell keeps its image's ratio.

## 3. ★ POINT COLOR — three layers (how to derive it)
1. **Background = mood** (dark or light, section 1).
2. **Point = exactly ONE color derived from the brand/content** — never hardcoded. Examples:
   Yangban deep-red `#9A130F` / Woori electric-blue (orange only on the EOD) / KT purple `#5B4BE0`
   + red period / Air Force near-monochrome (almost no accent) / DMZ blood-red `#BB0102`.
   Use `theme_from_brand(brand_hex, tone)` — it lifts the brand color for contrast against the base.
   If there is no brand color, or the scene mood overrides it, use a genre-emotion color instead.
3. **Wordmark = constant: LSB PRODUCTION** (the reference decks still carry an old studio name —
   always replace it with LSB PRODUCTION).
- Usage: one keyword in the point color / a period at the end of a headline / a section-divider color
  field / a giant letter (A. B. C.) / a label. **Never fill the area behind text with the color.**
- Per-concept named palettes (KT-style color chips) are allowed; you do not have to force a fixed brand color.

## 4. Page archetypes (the library — all in treatment_deck.py)
1. **cover_film** — full-bleed key still + bottom-center title lockup (KO title / EN subtitle / date).
   **cover_type** — giant diagonal wordmark on a brand-color full background.
2. **section_divider** — brand-color (or dark) full bleed, centered label (± underline) or a giant
   letter A./B./C. No decorative lines.
3. **concept_headline** — brand-color/cream full bleed + small serif-italic `Concept.` eyebrow + huge KO
   headline (use `//` to split lines) + small parenthetical subtitle.
4. **narration_still** — dark, center-aligned one to three lines, one beat per page, **only the keyword
   in the point color** (simulates the film's narration). Minimal elements.
5. **mood_board** — image grid + per-cell caption + a bottom `>> one-line tone`. **References use
   `contain` (original ratio).** This is also where the Pinterest moodboard library plugs in
   (REFERENCE/moodboard-library.md).
6. **scene_hero** — page number + section title (keyword in point color) + one-line description +
   **single hero still (`contain` letterbox)** + small italic caption at the bottom.
7. **scene_cluster** — one big main still + 1–2 supporting stills (stacked). Same scene, multiple angles.
8. **storyboard_grid (core)** — section label + cell grid. Each cell = `[#number header bar] / [image
   (cell ratio = cut ratio so cover never crops)] / [timecode line (film only)] / [one-line action]`.
   A dialogue/lyric strip can span the full width below several cells. Fixed columns, fill as many cuts
   as there are, leave blanks. Optional `REF` badge (reference juxtaposition) and camera-move arrow.
   **★ The grid is CENTERED — horizontally (each row by its own item count) and vertically balanced in
   the band. Never left-pinned (the height-clamp shrinks the cells, so without re-centering the right
   side goes dead — a fixed defect).** Caption type scale: action ≥16, timecode ≥16, cut-number ≥18.
8b. **cut_board** — detailed per-cut board, **up to 2 cuts per page**. Each card's width is derived from
   the image's own ratio at a fixed height (image fills the card with NO crop), the cards are centered
   as a group, and a READABLE caption block pins to each card's left edge: scene name (point color, ~30)
   / `장면 · …` (≥20) / `V.O · …` (≥20). Use this for full-still per-cut pages — **never hand-roll a
   2-up with tiny 13–16px captions and a top-heavy layout (a fixed defect).**
9. **option_ab** — two heroes side by side + a recommended label.
10. **back matter** — SCENE BREAKDOWN (dark-header table: No./scene·cut/description/dialogue) and
    SCHEDULE (weekly calendar). Skip for a pure-visual treatment.
11. **closing** — "E.O.D" + **LSB PRODUCTION**.

## 5. Timecode policy (by medium)
- **Film/video:** timecodes required (`00:00-00:03`, cumulative). (Air Force, Maekyung)
- **OOH/viral/mood:** no timecodes — `#number` order or "stage N" text. (KT)

## 6. Layout & furniture (shared)
- **Vertical text on both edges:** left = domain/handle, right = © copyright + date. (Use the LSB version.)
- Title top-left, wordmark top-right, page number bottom-right (or none).
- Section dividers, narration, cover title = center-aligned. Storyboard and spec pages = left-aligned.
- Dual header: small-caps English (wide tracking) on top, bold Korean below.
- Generous margins; white space is a design element.

## 7. Typography
- Display = heavy sans (Black Han Sans class) or condensed serif (covers). Korean body = sans.
- Accent = serif italic (`Concept.` `*Ref.` `Summary.` meta labels).
- Weight sets the tone: commercial = bold (LG) / public·gov = light (Ministry of Health) / cinema =
  bold + huge glyphs (KG).
- Emphasis = color (one point color) + size. Underline/box/shadow almost never used.

## 7.5 Composition (which archetype, where the eye goes)
The archetypes already encode composition (left-aligned hierarchy; center only for 1–2-line slogans;
full-bleed KV; letterbox single hero). Use the seven composition laws to *justify* the archetype choice
and the eye-path, not to override the archetype. Center alignment is only for authority / static
stability / frontality — never the default. Full rules: **REFERENCE/composition-principles.md**.

## 8. Photographic look of the images themselves
The stills that go INTO these pages must not look AI-generated. Use the photographic-treatment presets
(film stock / lens / lighting / grain / color grade / imperfection) instead of empty adjectives like
"cinematic, 4K, beautiful". See **REFERENCE/photographic-treatment.md** — the planner maps each cut's
tone to one of six presets and injects the spec into the image prompt.

## 9. DO / DON'T
- **DO:** pick one mode (dark/light); obey the ratio law (refs = contain, own grid = cut-ratio cover,
  single hero = letterbox); one point color (keyword/period/divider); giant section letters/labels;
  edge vertical furniture; the four storyboard-cell elements; minimal cover/EOD; wordmark = LSB.
- **DON'T:** ★ crop an image of one ratio into a cell of another ratio (ratio destruction) / put a filled
  panel behind text (cream/tinted box) / overuse the point color / overcrowd / leave an old studio name /
  use infographic badges or two-column proof cards (that is a proposal, not a treatment).

## 10. Code module rules (treatment_deck.py)
- `place_image(mode=auto|contain|cover)` is ratio-aware; `auto` is the default and letterboxes on
  mismatch — this prevents arbitrary cropping.
- Theme tokens: bg / point / accent2 / ink / muted / wordmark(=LSB). Build with `theme_from_brand()`.
- Archetype functions = section 4. EOD = LSB. No cream/filled-box function exists.
- 16:9 4K (3840×2160). 9:16 cuts → cells set to 9:16 (cell ratio matches cut ratio).
- `assert_images_present(placed_flags, kind)` halts the build if a key page has zero real images
  (do not fill with vectors or cream).

---
*Reverse-engineered from 35 studio decks. Supersedes the earlier Korean structure notes. The old
infographic module (build_treatment_template) is retired.*
