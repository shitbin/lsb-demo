# Scene Board (multi-panel) — prompt template

> No prior context? See ../../GLOSSARY.md, this skill's SKILL.md (the 7 GATES), and
> REFERENCE/photographic-treatment.md. This template *fills* the prompt; SKILL.md gates G2–G7 are the
> pass/fail on the filled result. G1 (declined_preset) and G6 (moodboard reference UUIDs) live in
> `params`, not the prompt text.

Draw N cuts of the SAME scene on one canvas so that background, lighting, and blocking stay
consistent. The N cuts later sliced out of one board all live inside the same world.

## Core principles

1. **Lay out N panels horizontally, equal width, thin white gutter between them.**
 - The gutter must be clearly visible so the slicer cuts each panel out precisely.
 - GPT (the image model) often fills the space between panels with black or a gradient. Unless you
   explicitly stamp in `"white gutter"`, the slicer loses track of where one panel ends.

2. **Describe each panel separately.**
 - Format: `"Panel 1: ... | Panel 2: ... | Panel 3: ..."`.
 - Write the camera, action, and background out per panel.

3. **Attach the master character sheet AND the moodboard references (GATE G6).**
 - Master sheet = the foundation of character consistency (same person every panel). Omit it and a
   different person shows up each time. (Do not photo-realistically clone a real celebrity's face — the
   master sheet is the studio's own model / talent type.)
 - **Also upload 2–4 representative images from the planner's `moodboard_bucket`** (`media_upload` →
   PUT bytes → `media_confirm`) and pass their UUIDs in `params.medias` alongside the master sheet (and
   the product-lock UUID if any). Citing the bucket in prose is NOT enough — the model must SEE the
   references, or the director's taste never reaches the image. (REFERENCE/moodboard-library.md.)

4. **Absolutely forbid burned-in text and scribbles.**
 - `"ABSOLUTELY NO handwriting, NO labels, NO annotations, NO storyboard markings, NO timecode burn-ins."`
 - When GPT sees the phrase "advertising treatment" it automatically draws storyboard annotations onto
   the image. You have to block this.
 - (Subtitles / copy are a separate matter — see principles 7 and 10. At the board stage on-screen text
   is usually composited in post, but you still preserve the verbatim subtitle text inside the panel
   description and the plan.)

5. **Aspect ratio.**
 - For a 9:16 video the panel itself is 9:16. The whole canvas is 9:16 × N (laid out horizontally).
 - If you hit the image tool's aspect-ratio cap (usually a 16:9 limit), reduce the panel count, or
   receive it at 16:9 and center-crop each panel back to 9:16 at the slice step.

6. **Avoid the visual-metaphor trap.**
 - A metaphor like "people frozen stiff like grey stone" looks like corpses or NPCs when actually
   rendered, and is aesthetically ruined.
 - If you want a time-freeze / frozen moment, keep the colors normal and freeze only the motion —
   `"alive, normal, just paused mid-motion"`.

7. **Describe each panel with a structured set of fields (most important).**
 - A one-line description like `"Panel 1: crosswalk wide shot"` is forbidden. Write it that loosely and
   GPT fills the missing decisions however it likes, so the result differs every time and consistency
   breaks.
 - For each panel, stamp in ALL of: framing / camera_angle / camera_facing / shot_scope / subject_action
   / pose / gaze / props / layout_grid / color_intent / texture / lighting / fg-mg-bg / vfx — using the
   **analyzer vocabulary (English tokens)**, written as dense prose.
 - **Length floor (GATE G2): ≥ ~800 words / ~5,000 characters PER PANEL.** gpt_image_2 high/2k takes
   ~32,000 chars — spend them; a 70-word panel is the bug. Keep the whole prompt ≤ ~30,000 chars; if a
   sheet would exceed, do FEWER panels per sheet (2 instead of 4), never shorter panels.
 - This full-field description must be specific enough that, at the video stage, the shooting team can
   transcribe it directly.

8. **Visualize VFX at the board stage too (so the client gets it in 5 seconds).**
 - Post-production VFX (time_freeze, color_pop, lens_flare, dust, glitch, etc.) goes into the board
   prompt as a *single line of visual description*. No abstract wording like "added in post-production".
 - Time-dependent effects (wiggle_3d, etc.) cannot be shown directly in a single image — visualize them
   as the intended sense of depth / parallax. Details: REFERENCE/vfx-in-board.md.
 - For VFX that contains text or numbers (3D balloon typography, etc.), draw only the *shape* in the
   board and leave the text to post (preserve the verbatim text in the plan).

9. **Transitions are separate — a single-canvas board.**
 - Flashy camera-movement transitions (whip_pan, morph, strong push_in/pull_out, 360_spin,
   match_action, dolly_through) get their **own board, separate from the scene board**.
 - Generate the end of the previous cut + the peak of the transition + the start of the next cut all on
   one canvas.
 - Details: prompts/transition_board.md + REFERENCE/transitions.md.

10. **Fold the cut's visual inputs into the panel description (key to consistency).**
 - If a cut has `recreation_prompts.t2i_start_frame` (or `style_prompt`), use that prompt as the **base
   of the panel description**. Exclude only celebrity *face cloning* and real logo marks (handle them by
   type), and **preserve the verbatim subtitle / copy text**.
 - `lighting` (key_direction/hardness/color_temp/ratio) → panel lighting; `texture` (surface texture) →
   panel texture; `visible_elements` (foreground/midground/background/lighting_env/atmosphere) → panel
   elements; `color_analysis` (palette / accent) → panel color — unpack each into the per-panel fields.
 - Skip this and even the same concept comes out with a different tone, texture, and lighting from board
   to board.
 - At the video (i2v) stage, `recreation_prompts.i2v_motion` + `i2v_params` animate the sliced still into
   cut motion (a separate stage from board generation).

## Prompt skeleton

```
A horizontal storyboard panel sequence for an advertising treatment.
{N} panels of equal width, separated by thin white gutters (4-8 pixels between panels).

Setting / location:
[LOCATION — time of day, weather, ambience].

Style — {the P1–P6 snippet mapped from the cut's tone, from REFERENCE/photographic-treatment.md}:
- Brand accent: {brand color} is the ONLY saturated color in frame.
- Light: {preset lighting} reinforced by the cut's own lighting (key direction / hardness / color temp).
- Texture: render the cut's surfaces as real (keep pores, fabric weave, surface imperfections).
- Composition: {1–2 of the cut's `comp_bias` laws from REFERENCE/composition-principles.md, e.g.
  "rule_of_thirds, leading_lines" — subject off-center on a third/intersection, lines converging on it}.
  Do not center the subject unless authority/frontality is intended.

Anti-AI (avoid): waxy plastic skin, over-smoothing, HDR clarity, perfect symmetry, everything-in-focus,
dead glassy eyes, over-saturation, centered stock-photo framing, airbrushed perfection.

Panel 1:
 Framing: [WS / LS / MS / MCU / CU / ECU].
 Camera angle: [eye_level / low_angle / high_angle / overhead / dutch].
 Camera facing: [frontal / three_quarter / profile / back].
 Shot scope: [face_only / bust / waist_up / full_body].
 Subject action: [what the protagonist does — one line].
 Pose: [specific pose — foot stance / hand position / center of gravity].
 Gaze: [to_camera / off_camera / at_product / down].
 Props: [props present + how they are handled].
 Layout grid: [rule_of_thirds_center / left / right / split / overhead].
 Color intent: [based on cut.color_analysis — palette / accent color].
 Texture: [cut.texture — surface texture].
 VFX in shot: [specific visual description — REFERENCE/vfx-in-board.md].

Panel 2: (same structure)
Panel 3: (same structure)

Continuity:
- Same location / time of day / protagonist (master sheet) / lighting direction across all panels.

ABSOLUTELY NO handwriting, NO labels, NO annotations, NO storyboard markings, NO grid overlays, NO timecode burn-ins.

Aspect: each panel 9:16 (vertical). Whole canvas: 27:16 horizontal (3 panels × 9:16).
```

> **Style block — pick the preset by the cut's tone.** Replace the old vague
> `Style: cinematic photographic look, 4K quality` with the matching P1–P6 snippet from
> REFERENCE/photographic-treatment.md (decisions, not adjectives — a real photographer's choices make an
> image look real instead of AI-made). Tone → preset map:
> - **P1 · Film documentary (warm, human)** — warm_emotional / friendly / family.
> - **P2 · Cinestill night (moody urban / neon)** — cinematic / mystery_teaser / dynamic_powerful.
> - **P3 · Faded editorial (airy, fashion)** — clean_minimal / premium / calm_refined.
> - **P4 · High-contrast B&W (graphic, resolute)** — serious_classic / determined_focused / confident.
> - **P5 · Golden-hour anamorphic (premium cinematic)** — cinematic_luxury / emotional_lyrical.
> - **P6 · Product hero (real studio — no render)** — product cuts.
>
> Drop the WHOLE preset snippet into the Style block, then add the brand-accent / light / texture lines
> and the Anti-AI negative line shown above. ⚠️ **Never** put sexual / NSFW blocker words
> (no nudity / sexual / NSFW) in the negative prompt — they trigger moderation and block generation.
> Anti-AI negatives like "waxy plastic skin" are fine and encouraged.

> If a cut has `recreation_prompts.t2i_start_frame`, fill the panel block above from that prompt
> (excluding celebrity face cloning and logo marks) and reinforce it with
> lighting / texture / visible_elements / color_analysis.

## On-screen typography — baked vs subtitle  (GATE G5)

> **★ NEVER write `no text`, `no letters`, `no captions`, `no words` in the negative prompt.** That is the
> exact bug that suppressed all copy on the Carrot run. The only allowed text negatives are
> `no handwriting, no storyboard annotations, no labels, no scribbles, garbled text, extra letters`
> (they block AI auto-annotation, not real copy).

On-screen text that is **baked** = headline / emphasis / kinetic typography / end-card logo lockup / CTA
goes INTO the image (`typo_mode=baked`): write the **verbatim `baked_text` into the prompt** as on-image
typography. Only **subtitles** (long sentences, legal terms, precise figures) are added in post
(`typo_mode=subtitle`) — keep their verbatim text in the plan. `typo_mode=none` → no text.

**Korean baking policy (user-set _260614 = ALWAYS BAKED, no fallback):** gpt_image_2 renders Korean
reliably — bake the Korean `baked_text` directly into the frame. Do NOT route Korean to post pre-emptively,
do NOT add fallback hedging, do NOT shorten/romanize to play safe. Main copy / headline / CTA / emphasis
is baked, Korean included. `subtitle` is reserved for long running subtitle lines / legal fine print only.
(REFERENCE/typography-in-image.md.)

## Example (KT Y board1_intro — crosswalk wide + low-data close-up)

```
A horizontal storyboard panel sequence for an advertising treatment.
3 panels of equal width, separated by thin white gutters (6 pixels).

Setting / location:
Morning Shibuya scramble crosswalk. Tokyo. Office-going crowd. Bright overcast daylight. Slight morning haze.

Style — P2 · Cinestill night → swapped to overcast-morning variant (tone: dynamic, slightly tense):
Shot on Fuji Pro 400H, 35mm f1.8, soft overcast morning daylight (key: top, soft, cool ~7000K), no harsh shadows.
Fine film grain, subtle halation. Muted editorial grade, real skin with visible pores, off-center candid framing.
- Brand accent: Y Mint #11E6D8 is the ONLY saturated color in frame (on protagonist's cargo pants).
- Light: soft overcast morning light reinforced by the cut's own key (top, soft, cool ~7000K).
- Texture: render fabric weave and concrete as real (keep pores, micro-texture, surface imperfections).

Anti-AI (avoid): waxy plastic skin, over-smoothing, HDR clarity, perfect symmetry, everything-in-focus,
dead glassy eyes, over-saturation, centered stock-photo framing, airbrushed perfection.

Panel 1:
 Framing: WS. Camera angle: low_angle (hip height, slight tilt up). Camera facing: frontal.
 Shot scope: full_body + environment.
 Subject action: 주인공이 횡단보도 한가운데로 정면으로 걸어 들어옴.
 Pose: 오른발 한 걸음 내딛는 중, 양손 자연스럽게 옆.
 Gaze: forward (slightly down). Props: none on protagonist; office workers as crowd.
 Color intent: cool overcast + Y Mint single-color pop. Texture: fabric_cotton, concrete.
 VFX: none.

Panel 2:
 Framing: CU. Camera angle: eye_level. Camera facing: three_quarter. Shot scope: hands + phone.
 Subject action: 주인공이 폰을 가슴 높이에서 들고 화면을 본다.
 Pose: 양손으로 폰을 잡고 약간 앞으로 숙임. Gaze: at the phone (off_camera).
 Props: smartphone with a stylized red low-data indicator on screen (graphic shape only).
 Color intent: shallow DOF, mint pop. VFX: shallow depth of field on phone.

Panel 3:
 Framing: MCU. Camera angle: eye_level. Camera facing: frontal. Shot scope: face + shoulders.
 Subject action: 주인공이 폰에서 시선을 떼고 정면을 본다 (살짝 걱정).
 Pose: 고개 약간 기울임. Gaze: down→up to_camera.
 Props: smartphone (lowered partway). VFX: none.

Continuity:
- Same Shibuya crosswalk / morning overcast / protagonist (master sheet) / light from upper-left.

ABSOLUTELY NO handwriting, NO labels, NO storyboard markings, NO grid overlays.
(On-screen captions per plan are added in post; the phone shows only a graphic indicator shape.)

Aspect: each panel 9:16. Whole canvas: 27:16 horizontal.
```

## Common failure patterns & fixes
- **Panels separated by a black gap** → emphasize `"thin WHITE gutter, 6 pixels"`.
- **Merged into one picture with no gaps** → `"clearly separated panels, like a storyboard"`.
- **A different person in each panel** → reference missing (check medias).
- **A different time of day per panel** → `"same time of day"` + state the light direction.
- **GPT draws storyboard annotations** → emphasize `"no annotations, no labels"` + repeat principle 4.
- **People like grey stone (corpses / NPCs)** → `"alive, normal everyday people, just paused mid-motion.
  NOT statues, NOT grey, NOT pale, NOT dead-looking"`.
- **9:16 requested but panels come out wide** → state `"each panel 9:16 vertical"`.
- **Tone / texture differs board to board** → the cut's lighting/texture/color_analysis wasn't put into
  the panel fields (principle 10).
- **Stills look AI-made (waxy skin, flat light, dead-center, render look)** → the Style block still used
  vague adjectives instead of a P1–P6 photographic preset (see REFERENCE/photographic-treatment.md).

## Human judgment slot
When the board is generated, stop and ask the user: "OK to slice this board as is?" / "Any panel to
redraw?" / "Tone and composition OK?". The human makes the call. The AI only does technical checks
(broken faces, six fingers, leaked annotations it wasn't asked for).

The default board grid is **2×2 (one sheet, 4 cuts)** — 2K generation, then slice the cuts apart; only
the sliced cuts go into the deck.

---
*Version: lsb-image-crafter_260614_v1 · 2026-06-14 KST. (moved here from lsb-treatment-builder when image
generation split into its own owner skill.) v1 = GATE G6 (moodboard refs uploaded as `medias`) added to
principle 3; GATE G5 hardened — explicit ban on `no text/no letters/no captions` negatives + Korean
baking attempt→fallback policy. Prior (under treatment-builder): English rewrite + photographic-treatment
presets wired into the Style block.*
