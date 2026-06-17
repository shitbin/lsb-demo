---
name: lsb-image-crafter
description: >-
  LSB image generation skill — the SINGLE owner of every Higgsfield `generate_image` call
  (character master sheets, key visuals, storyboard cut stills). Takes the planner's per-cut
  plan (`cut_plan.json`) and produces verified local still images + a `stills.json` manifest
  that the treatment-builder (deck) and video-crafter (i2v) consume. Use it whenever images
  must be generated for an ad: "generate the cuts", "make the key visual", "character sheet",
  "storyboard stills", "이미지 뽑아줘", "컷 이미지 생성". It does NOT lay out the PDF (that is
  treatment-builder) and does NOT make video (that is video-crafter).
---

# lsb-image-crafter — generate the ad's still images (the one owner)

> New session, no prior context? Read `../GLOSSARY.md` first, then this file top to bottom.
> Pipeline position: **lsb-ad-planner → lsb-image-crafter (this) → lsb-treatment-builder / lsb-video-crafter.**

## 0. Why this skill exists (read this once)

Image generation used to live as a sub-phase inside the treatment-builder (whose real job is the
PDF deck). Because it was a *means to an end*, the agent generated images shallowly and skipped the
rules that actually make them good — they were buried in on-demand docs and never enforced at the
`generate_image` call. Seven concrete failures recurred (see `_meta/IMAGE_PIPELINE_DIAGNOSIS_260614.md`):
preset leak, shallow per-cell prompts, no composition, no foreground/midground/background, copy not
baked in, moodboard never used as a reference, and (the meta-cause) no single owner.

**This skill is that owner.** Image generation is its *primary deliverable*, and the seven rules below
are **hard gates** checked at every call — not suggestions. Generating without passing them is the bug.

## 1. Inputs and outputs (the data contract)

**Input — `cut_plan.json`** from the planner (schema: `REFERENCE/data-contract.md`). Per cut it carries:
`composition` (1–2 comp_bias laws), `eye_path`, `typo_mode` (none/subtitle/baked), `baked_text` (verbatim
copy to bake), `photographic_preset` (P1–P6), `visible_elements` (foreground/midground/background/
lighting_env/atmosphere), `moodboard_bucket`, plus brand color, product-lock asset, aspect ratio.
If the planner output is missing a field, **stop and ask / fill it** — do not generate from a hole.

**Output** — `assets/` (verified local stills) + **`stills.json`** manifest: every produced image with
`{cut_no, role, path, ratio, gen_params, declined_preset_id, typo_mode, baked_text}`. The deck and the
video skill read **only** `stills.json` (they never call `generate_image`).

## 2. Generation order (consistency first)

1. **Character master sheet** (one per character). The consistency anchor. Generate first, confirm with
   the user, keep its media UUID.
2. **Key visual (KV)** — the hero frame for the cover/title. References the master sheet.
3. **Cut stills** — default **2×2 storyboard grid (4 cuts / image, 2K)**; slice into per-cut stills.
   5+ cuts → several sheets (6 = 4+2, 9 = 4+4+1). References the master sheet + moodboard refs.
Each step ends at the **human judgment slot** (§6).

## 3. THE SEVEN GATES (must pass before every `generate_image`)

Run this checklist for each call. If any item fails, fix the prompt/params first — do not call.

**G1 — Preset declined (fixes the "leaked preset woman" bug).** Higgsfield injects a default preset
sample unless you decline it — and it leaks on the VERY FIRST call, so you must learn the id BEFORE
generating, not after seeing a leak.
- **Before the first `generate_image`, learn the preset id(s):** call **`presets_show`** (and/or
  `models_explore` for `gpt_image_2`) to read the active/default preset id(s). Seed
  `params.declined_preset_id` with them on call #1. If `presets_show` returns nothing, seed with the
  known default id the way the video skill does (lsb-video-crafter STEP 5 seeds the known
  "IN THE DARK" preset) — never call #1 with an empty decline.
- On every subsequent call, carry the accumulated declined id(s); if a new "this prompt looks like preset
  X" recommendation appears, add that id too and resend. **Never** call `generate_image` (or
  `generate_video`) without `declined_preset_id`. This is a *default*, not a reaction after a leak.

**G2 — Per-cell full-field prompt, HEAVY length floor (fixes shallow/short cells).** Every panel/cell is
described with the FULL field set (framing / camera_angle / camera_facing / shot_scope / subject_action
/ pose / gaze / props / layout_grid / color_intent / texture / vfx / lighting / fg-mg-bg) using analyzer
English tokens (`REFERENCE/cut-schema.md`), written out as dense prose — not a token list.
- **Floor: ≥ ~800 words / ~5,000 characters PER CELL.** (gpt_image_2 high/2k accepts ~32,000 characters,
  so spend them — 70-word cells were the bug.) A single KV / master sheet / transition apex ≥ ~5,000
  chars too. A one-line cell ("crosswalk wide shot") is forbidden — the model fills the gaps randomly and
  consistency breaks.
- **Total-prompt cap: ≤ ~30,000 characters** (safety margin under the model's ~32,000 limit). A 2×2 grid
  of ~5,000-char cells ≈ 20,000 chars — fine. **If a sheet's cells would push past ~30,000, put FEWER
  cells per sheet** (e.g. 2 cells/sheet) rather than shortening the cells. Detail wins over batching.
- Build each cell from the cut's `recreation_prompt` / `recreation_prompts.t2i_start_frame` when present
  and expand it to the floor (`prompts/scene_board.md` principle 10).

**G3 — Composition injected (fixes ignored golden-ratio / rule-of-thirds).** Put the cut's 1–2
`composition` laws into the Style block, in words: e.g. rule_of_thirds → "subject off-center on a
left-third intersection"; golden_ratio → "subject at the phi focal point, ~62% across"; leading_lines
→ "street lines converge on the subject". **Do not center the subject** unless authority/frontality is
intended. Source: `REFERENCE/composition-principles.md`. If `cut_plan` has no `composition`, ask the
planner / fill it — never emit a frame with zero composition language.

**G4 — Foreground / midground / background built (fixes flat layout).** Every cell prompt has the five
explicit layers from `visible_elements`: `foreground:` … `midground:` … `background:` … `lighting_env:`
… `atmosphere:` …. This is what gives depth; a frame that only names the subject reads flat.

**G5 — On-screen copy BAKED into the image (fixes "no text" everywhere).**
- **NEVER put `no text`, `no letters`, `no captions`, `no words` in the negative.** The only allowed
  text negatives are: `no handwriting, no storyboard annotations, no labels, no scribbles, garbled text,
  extra letters`. (These block AI auto-annotation, NOT real copy.)
- For each frame use `typo_mode`: `baked` → write the **verbatim `baked_text` into the prompt** as
  on-image typography (headline / emphasis / kinetic / end-card logo lockup / CTA), with its placement
  and treatment (size, weight, position, color box); `subtitle` → only for genuinely long running
  subtitle lines / legal fine print, composited in post; `none` → no text.
- **Korean baking policy (user-set _260614 = ALWAYS BAKED, no fallback).** gpt_image_2 renders Korean
  reliably — **bake the Korean `baked_text` directly into the frame.** Do NOT pre-emptively route Korean
  to post, do NOT add fallback hedging, do NOT shorten or romanize the copy to "play safe." The main
  copy / headline / CTA / emphasis is baked, Korean included. (`subtitle` stays reserved for long running
  subtitle text only.) `stills.json.baked_ok` is informational; default `true`. Details + the 3
  categories: `REFERENCE/typography-in-image.md`.

**G6 — Moodboard images uploaded as references (fixes "Pinterest ignored").** The planner picked a
`moodboard_bucket`. **`media_upload` 2–4 representative images from that bucket** (presigned URL → PUT
bytes → `media_confirm`) and pass their UUIDs in `params.medias` (role `image`) **together with** the
master-sheet UUID (and the product-lock UUID if any). Citing the bucket only in prose is not enough —
the model must SEE the references. Library contract: `REFERENCE/moodboard-library.md`.

**G7 — Model / resolution / quality / anti-AI locked.** `params.model="gpt_image_2"` (never fall back
to `nano_banana_*`), `resolution="2k"`, `quality="high"` (the defaults are 1k/low). Drop the matching
**P1–P6 photographic preset** (real film-stock / lens / lighting decisions, not adjectives like
"cinematic, 4K") into the Style block + the Anti-AI negative (waxy plastic skin, over-smoothing, HDR
clarity, dead glassy eyes, centered stock-photo framing). **Never** put sexual/NSFW blocker words in the
negative — they trip moderation and block generation. Source: `REFERENCE/photographic-treatment.md`.

> Build the actual prompt with `prompts/scene_board.md` (it already encodes G2–G5/G7). The skeleton there
> is the template; these gates are the pass/fail check on the filled result.

## 4. The Higgsfield call (mechanics)

- `generate_image(params={ model, prompt, aspect_ratio, resolution:"2k", quality:"high", count,
  declined_preset_id, medias:[{role:"image", value:<UUID>} …] })`.
- **References via uploaded UUID, not raw external URLs:** download asset locally → `media_upload`
  (returns a presigned URL) → `curl -X PUT` the bytes → `media_confirm(type="image")` → use the UUID.
- Cost preflight (`get_cost:true`) before an expensive batch; don't regenerate an unchanged cut.
- **No code-drawn substitutes.** Never replace a generative image with PIL rectangles/icons. If
  generation or download fails, **stop and tell the user** — do not patch with vectors.

## 4-a. Render-wait — batch-wait, don't idle-spin (★)

`generate_image` is async (submit → job → poll → download). **Submit every image job first** (master
sheet · KV · all cut grids) as one batch, then wait on the batch — never one image at a time, and **never a
tight `sleep; echo` idle loop** doing nothing.
- **Wait once, long.** After submitting, `sleep` once for the render estimate, then poll `job_display` for
  the **whole batch** and download the finished results to `assets/`; recover flaky status by re-querying
  the job id. Don't separate the wait into dozens of short idle echoes.
- **The wait is overlapped, not wasted.** The manager runs the deck *skeleton* build (lsb-treatment-builder
  Phase 4.0 Pass A — layout · typeset copy · ratio-sized image slots) **while** these images render, so the
  wall-clock isn't burned on idle sleeps.
- **Hand off only a COMPLETE `stills.json`.** It's complete only when every cut / KV / master-sheet image
  is downloaded **and** verified (§7). **Never let the pipeline report the deck "done" while any image is
  still generating** — the deck is finalized only after all stills land (the builder's Pass B).

## 5. Download, slice, verify (local files only)

- Higgsfield returns a remote URL/job. PIL cannot open a URL. **Download every result to `assets/`**
  immediately, then use local paths only. Validate `PIL.Image.open(path).verify()`; a few-hundred-byte
  file = a failed download (network/expired URL) — retry or tell the user, never build with an empty image.
- **Slice the 2×2 grid into 4 cuts** (detect white gutter / center line → quarter → trim white). A cell
  whose content came out cropped at the boundary can't be saved by slicing — **regenerate** that grid.
- Name per-cut stills by cut number into `assets/확정컷/`. Write each into `stills.json`.

## 6. Human judgment slot (the AI does not make the aesthetic call)

After the master sheet / KV / each grid, **stop and ask** the user: "OK to slice / use as is?" / "Any
frame to redraw?" / "Tone & composition OK?". The AI only does technical checks (broken faces, six
fingers, leaked annotations, wrong aspect ratio, garbled baked text). **Do not `Read` a generated image
or built PDF into context to judge it** — check existence/size/ratio programmatically (PIL). **Never
inline image/PDF bytes as base64** (the 32MB request cap kills the call). Pass images only as a local
path / upload UUID / URL reference.

## 7. Post-generation self-check (before handing off)

For every still in `stills.json`: aspect ratio matches the plan; no leaked annotations/labels; faces/
hands sane; baked Korean is present and clean (Korean is always baked per G5 — if one frame's glyphs
actually garble, regenerate that frame in Korean; do NOT romanize/shorten/drop it); the master-sheet face
is consistent across cuts. Then hand `stills.json` + `assets/` to treatment-builder (deck) and/or video-crafter (i2v).

## 8. Special branches

- **Transition frames** — a flashy camera-move transition (whip_pan/morph/strong push/360/match_action)
  is its own board: end of cut N + apex + start of cut N+1 on one canvas (`prompts/transition_board.md`).
  Not sliced into the storyboard.
- **Layered collage** (fragments overlapping on a base, GMA-2018 style) — do NOT generate as one image:
  generate each fragment → composite a preview (Pillow) → video stage animates layers.
  `REFERENCE/layered-collage-protocol.md`.

## 9. Do-not list
- Do not `generate_image` without `declined_preset_id` (once known), full-field cells (G2), composition
  (G3), fg/mg/bg (G4), or moodboard refs (G6).
- Do not put `no text / no letters / no captions` in any negative. Bake copy where `typo_mode=baked`.
- Do not lay out the PDF or make video here. Output `stills.json` + `assets/` and hand off.
- Do not photo-realistically clone a real celebrity face or draw a real logo mark; use the studio's own
  master-sheet talent type and a generic mark (copy text in the plan is preserved as written).

---
*Version: lsb-image-crafter_260615_v2 · 2026-06-15 KST. (version scheme = YYMMDD_vN.) v2 = **§4-a render-wait**
— submit all image jobs as ONE batch, then a single longer `sleep` + batched `job_display` poll instead of an
idle `sleep; echo` loop; the wait is overlapped with the treatment deck-skeleton build (builder Phase 4.0
Pass A); hand off only a COMPLETE verified `stills.json` and never report the deck "done" mid-generation.
v1 = NEW SKILL split out of lsb-treatment-builder Phase 3 to be the single owner of all `generate_image`, with the
seven hard gates (declined_preset · full-field cells · composition · fg/mg/bg · baked-copy/no-"no text" ·
moodboard refs · model/preset lock) and the cut_plan.json → stills.json data contract. Resolves the seven
image-generation defects in _meta/IMAGE_PIPELINE_DIAGNOSIS_260614.md. User decisions _260614: per-cell
floor ~5,000 chars (≤30k total), Korean main copy ALWAYS baked (no fallback), split adopted.*
