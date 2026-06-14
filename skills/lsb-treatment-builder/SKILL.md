---
name: lsb-treatment-builder
description: >-
 LSB Production ad treatment-builder skill. Takes the planning markdown produced by
 lsb-ad-planner (concept, copy, cut list) as input and builds it all the way through:
 protagonist character master sheet → per-scene multi-panel boards → cut slices →
 a studio-grade visual treatment PDF. If a dataset is available, it uses
 cross-pollination to pull deck visual tone (layout, typography, color, structure)
 into the design decisions. Always use it for requests like: "make the treatment PDF",
 "build the treatment", "turn this concept into a deck", "character sheet + storyboard
 + deck in one go", "in the cinematic / service deck style", or when someone hands you
 lsb-ad-planner output and asks for the visual build. Coming up with the concept itself
 (cross-pollination, generating N candidate concepts) is lsb-ad-planner's job, so this
 skill does NOT redo that. Bilingual triggers (Korean): "기획안 PDF 만들어줘",
 "트리트먼트 짜줘", "이 컨셉으로 장표 만들어줘", "캐릭터시트 + 콘티 + 장표 한 번에",
 "양반김 식으로", "우리은행 식으로".
---

# lsb-treatment-builder — LSB ad treatment (PDF) builder skill

> No prior context? Read `005_skills/GLOSSARY.md` first — it defines every term used here
> (brief, dataset, cut, hero cut, cross-pollination, KV, i2v/t2v, seamless transition,
> double/jump cut, photographic treatment, the multi-character mixup lesson, the
> redesign-gap post-mortem, wordmark = LSB PRODUCTION, etc.).

## Where this skill fits in

The LSB Production skill ecosystem is a three-way division of labor.

```
 reference ad mp4s brief + dataset planning markdown + brand
 │ │ │
 ▼ ▼ ▼
┌──────────────┐ ┌──────────────┐ ┌─────────────────────┐
│lsb-ad-analyzer│ ───▶ │lsb-ad-planner│ ───▶ │lsb-treatment-builder│
│ (eyes·grasp) │ dataset │ (head·plan) │ plan │ (hands·build) │
└──────────────┘ └──────────────┘ └─────────────────────┘
 │
 ▼
 ┌──────────────────┐
 │ treatment PDF │
 │ + character/cut │
 │ folders │
 └──────────────────┘
```

- **lsb-ad-analyzer**: breaks reference ad videos down into metadata (JSON entries) to build the dataset.
- **lsb-ad-planner**: dataset + brief → cross-pollination → N candidate concepts + copy + cut list (treatment.json).
- **lsb-treatment-builder (this skill)**: takes that plan and builds the visuals, storyboard, and deck pages, bundled into a PDF.

**This skill does not invent a new concept.** Treat the concept as already done by the planner; focus only on visualizing and decking the plan you receive. If the user asks for concept work, send them to lsb-ad-planner.

## How this connects to the project guidelines

- **§3 Wrapper = hands, dataset = muscle**: this skill is the "hands." It turns the direction the user (brain) chose into a deliverable using the dataset (muscle).
- **§4.3 Cross-pollination**: when pulling visual-tone references, the weights use the **same profile as the planner** — currently LOOSE test: 0.5 (same category) / 0.8 (adjacent) / 1.0 (distant) / 1.1 (contrast), hero-cut from same category 0.3 weak-reference (STRICT restore values: 0.2 / 0.5 / 1.0 / 1.2, hero-cut hard-ban). (The single source for the decision map is `lsb-ad-planner/schema.md` §3, keyed on the English industry token. Profile definitions live in the planner SKILL.md cross-pollination section.)
- **§5 Asymmetry of the division of labor**: the AI rapidly emits characters, scene boards, slices, and deck pages; the human makes the aesthetic call and picks cuts. The AI does not trust its own aesthetic judgment.
- **§6 Hit rate**: a slot where you generate many master sheets / scene boards, then the human does a first-pass cull.
- **Copyright safety**: what you pull from the dataset is Level 2–3 abstraction (formula, structure, signature). No tracing pixels. **Subtitle/copy wording is preserved** (short copy verbatim); only a celebrity's *photographic face likeness* and a real *logo mark* are made generic.

## Workflow (Phase 0 → 6)

Stop at the end of each phase, show the user, then move on. Before any expensive step (image generation, PDF build), always get a confirmation.

### Phase 0 — Validate inputs & set up the working folder

When triggered, the user usually hands you these.

1. **The plan (treatment.json or markdown)** — lsb-ad-planner output. If missing, request it or guide the user to write one.
2. **Brand guidelines** — color palette (hex), logo, fonts, tone. If missing, find the official brand assets and organize them (down to the hex values).
3. **Dataset (optional)** — `entries/` + `index/` inside `001_ad_video_dataset/` (= `<DATASET>`) inside `<LIBRARY>` = the folder that **directly contains `001_ad_video_dataset/`** (resolve by structure: check the connected folder; if `001_ad_video_dataset/` isn't there, drop into a `library/` subfolder and use that — works for `LSB_AD_ENGINE/library`, a repo with `001…` at root, or a repo with a `library/` wrapper). **Do not hardcode paths** — resolve at runtime (works on both mac `/Users/...` and win `C:\Users\...`). If present, use it for cross-pollination; if absent, pick directly from the catalog.
4. **Output folder** — the Cowork working folder. If none, call `mcp__cowork__request_cowork_directory`.

**Strategy input (required — do this first).** Lock the *planning logic* before cuts and visuals: the assignment (the brand's homework) / target insight + evidence / strategy (the one move) / why this concept was derived / brand justification (product truth) / expected effect + evaluation criteria. **If this input is empty, do not build** — expand the planner's `strategy_spine` (or `client_perception_path`) into logical paragraphs and receive it, or send it back to the planner, or derive it together with the user before proceeding. (Spine framework: `REFERENCE/deck-logic.md` §1.)

Then the **execution checklist** (ask the user about anything missing): concept name · hashtag · one-line summary / video copy (distinguish subtitle / Na / O.V) / cut list / protagonist + characters / setting + location / tone & manner / medium + spec (9:16 / 16:9, length) / brand must-haves (logo · primary color first · subtitle disclaimers).

Working-folder structure:
```
{output_folder}/{project_name}/
├── assets/ # character sheet / scene board originals (full multi-panel images)
├── frames/ # sliced per-cut frames
├── 확정컷/ # human-curated final cuts
├── fonts/ # build fonts
├── plan.md # copy of the input plan
├── treatment.json # full-field data (global + cuts + transitions)
├── build_treatment.py # reproducible build script
└── treatment.pdf # final deliverable
```

### Phase 1 — Decompose the plan + decide the deck style

**1.1 Decompose the plan — global meta + full per-cut fields.**

Core principle: **write the treatment cut data in the SAME schema as the `shots[]` of an `lsb-ad-analyzer` entry (30+ fields).** Do not collapse it to "SCENE/COPY/NOTE 3 blocks" — if the downstream builder fills in guesses, intent blurs and the cross-pollination format breaks. For the analyzer→treatment key conversion, follow the mapping table in `lsb-ad-planner/schema.md` §5 (e.g. total_duration→total_duration_sec, typography→typography_global).

**(A) Global meta (once for the whole treatment)**

| Group | Fields |
|------|------|
| Identity | `id`, `schema_version`, `source_plan_ref`, `brand`, `product`, `target_demo` |
| Length·structure | `total_duration_sec`, `shot_count`, `fps`, `aspect_ratio`, `hook_position_sec`, `cta_position_sec` |
| Narrative | `narrative_arc`, `pacing_curve`, `music_tempo_curve`, `wow_cut_index[]`, `creative_device` |
| Shooting signature | `production_signature.capture_style/.camera_signature[]/.color_grade/.texture_fx` |
| Global layout | `global_layout.grid_system/.subject_placement_dominant/.subject_typo_relation/.negative_space_use` |
| Motifs | `recurring_motifs[]` |
| Typography global | `typography_global.primary_font_class/.secondary_font_class/.animation_style_default[]/.subtitle_position_dominant/.color_strategy` |
| VFX global | `vfx_global.primary_effects[]/.effect_intensity/.transition_style_dominant` |
| Copy global | `copywriting.tagline_text/.cta_text/.copy_tone[]` |
| Perception path | `client_perception_path` (7 stages, emotional path) |
| Planning logic | `strategy_spine.brief / .insight(+evidence[]) / .strategy / .concept_rationale / .brand_right / .payoff` — the business argument (planner output). The builder renders it as the STRATEGY section. If empty, derive it with the user. Mapping/framework = `REFERENCE/deck-logic.md` §1 |

**(B) Full per-cut fields (every cut)**

| Group | Fields |
|------|------|
| Identity (required) | `index`, `no`, `duration`, `framing`, `function` |
| Subject·action | `subject_position`, `subject_action`, `subject_motion`, `pose_description`, `gaze`, `eye_contact_effect` |
| Camera | `camera_motion`, `camera_motion_intensity`, `camera_angle`, `camera_facing`, `shot_scope`, `camera_effect_local`, `motion_blur` |
| Rhythm·transition (required) | `intra_cut_rhythm`, `transition_in`, `transition_out` |
| Props·set | `props[]`, `prop_motion`, `prop_semantics` |
| Color | `color_mood`, `color_palette[]` (HEX 4–6 colors), `color_intent` |
| Typography·subtitle (subtitled cuts only) | `copy_overlay`, `layout_grid`, `subject_typo_layout`, `typo_motion`, `typo_color_strategy` |
| VFX (cuts that have it) | `vfx_in_shot[]`, `vfx_intensity_local`, `vfx_in_board_prompts` |
| Visual inventory | `visible_elements`, `texture`, `lighting`, `color_analysis`, `style_prompt` |
| Frame recreation | `recreation_prompts` (`t2i_start_frame`·`t2i_negative`·`i2v_motion`·`i2v_params`·`fidelity_note`) |
| Meta | `wow_cut`, `fact_check_flag`, `notes`, `source_refs[]`, `still_path` |

The vocabulary (framing / camera_angle / typo_motion etc.) and field definitions live in `REFERENCE/cut-schema.md`. You **must** pick values from within that vocabulary (English tokens), or cross-pollination matching breaks.

The visual inventory and `recreation_prompts` are *image/video generation inputs* the analyzer made for key cuts. Pull them as *inspiration* from a cross-pollination reference entry (no pixel copying) or author them for this cut, and combine them into the Phase 3 board prompts.

Do not guess at missing fields. Especially **camera (angle · facing · motion) · transition · typo motion** must not be left blank. Writing order: ① the 5 required → ② subject·props → ③ camera → ④ transition·rhythm → ⑤ color·typography → ⑥ VFX·visual inventory → ⑦ recreation_prompts → ⑧ meta.

**1.1-b Re-verify the cut-grammar gate (double-prevention — planner R10 second line of defense).** Right after decomposing the plan, re-verify **every adjacent pair** of cuts in the cut list against the planner R10 criterion: if it's the same subject (`subject_identity`) and same space, but ① the `framing` size changes by fewer than 2 steps (7-step ladder `ECU→CU→MCU→MS→MLS→FS/LS→ELS`) ② `camera_angle`/`camera_facing` changes by less than 30 degrees ③ subject/space/time are identical — if **all three** hold, it's a **double (jump-cut) violation**: that boundary isn't a cut. Fix it: ⓐ replace `transition_in/out` with a seamless type (`push_in`/`pull_out`/`dolly_through`/`morph`/`match_action`) and absorb it into a single-canvas transition board at the 3.0 branch (default), or ⓑ propose merging the cuts to the user (the builder does not arbitrarily add or delete cuts — merging happens only after confirmation). Exceptions: punch-in (same angle, size change **2+ steps**), match-cut, and any cut whose `notes` says "intentional jump cut". **Do not enter board generation (Phase 3) or build (Phase 4) with a violation still present.**

**1.2 Decide the deck style.** Deck style is not a single tone.

| Style | When | Characteristics |
|--------|------|------|
| Cinematic deck (was "양반김") | video-led, premium, character drama | black BG, building the copy one phrase at a time as a "train of thought" + full-still per-cut storyboard |
| Service deck (was "우리은행") | celebrity/model-led, punchy copy | white BG, centered copy, person-photo modules |
| Luxury/fashion deck (was "신세계 럭셔리") | luxury, fashion | large negative space, serif, minimal grid |
| Object/product KV deck (was "KG INSTEROID") | product KV film | object close-up grid, short captions |
| Worldview/character deck (was "G-EYE") | character/worldview viral | illustration-style consistent character, comic-style cut division |

If you have a dataset, use cross-pollination to pull similar-tone entries with weights 0.2–1.2, sort the candidates, and present them to the user. If not, pick from the 5 above. See `REFERENCE/deck-styles.md` (design signatures). **Pick a track by purpose (plan/treatment/PPM) × tone (cinematic / service·fun / luxury / worldview / public-service / conference / B2B / education)** — `REFERENCE/presentation-rules.md` §0·§5. The 5 are just seeds; the track matrix maps *any* domain deck.

**1.3 Confirm the style.** Ask "is this the right style?" once and move on. This is the last cheap decision point before the expensive steps.

**1.4 Narrative structure / character determination (multi-character & cross-cutting — the multi-character mixup lesson).** Read the plan's `narrative_structure` and `character_pool[]` and branch on the handling.
- `linear_continuous`: a continuous spatial flow as before.
- `cross_cutting_montage` (same time, different spaces, intercut): **do not force-splice spaces together.** Separate each space into its own reference group, mark the cuts of different spaces at the same moment with the *same time state* (e.g. time-frozen), and label the transitions as *space jumps*. The video stage splits this into per-space / per-character segment clips (video skill).
- if `character_pool[]` has 2+ people: check each cut's `subject_identity` → **place only the protagonist sheet on protagonist cuts / only that person's sheet on other-character cuts** (Phase 2·3). Otherwise you get the multi-character mixup: a video where *the protagonist appears in every cut*.

### Phase 2 — Master character sheet

The backbone of visual consistency. (REFERENCE/scene-boards.md + prompts/master_character.md)

**2.0 Decide how many characters (multi-character — the multi-character mixup lesson).** Look at the plan's `requires_character_sheets[]`. Make a master sheet for **each** person who appears *clearly on screen* (protagonist, key supporting cast) — one for the protagonist, one for the cafe customer, one for the part-timer, etc. Crowds / extras (`background_crowd`) are handled without a sheet as "anonymous other people." Each sheet is used as a reference only on the cuts where that person appears.

**2.1 Prompt principles.** Single person, single outfit (per sheet), front + 1–2 side views in one canvas. Brand color in the outfit (state the hex). Minimal accessories. Calm/neutral expression. Plain background. 4K, GPT Image 2 high. **Do not reproduce a real celebrity's face at photographic fidelity** — define by type (age range, styling, pose) and assume the studio's own model/talent.

**2.2 Post-generation handling.** Confirm the result with the user → save the job id → use it as a reference for all subsequent scene boards (Higgsfield `medias`). Only one master sheet in the reference slot.

**2.3 Common failures & fixes.** Face differs every time → reference dropped (check medias). Outfit color off → hex + "exactly this color". Two people → "single subject" + negative "no second person". Unrequested accessory → state it in negative.

### Phase 3 — Scene boards (multi-panel) + transition boards (single canvas) + VFX in-board + slicing

The stage that produces all the visual assets for the video. Build three board types, deciding which via a *branching judgment*.

**3.0 Board-type branch (automatic judgment).**

| Board type | When | Single/split |
|----------|------|-----------|
| Scene board | 2+ cuts share the same background | split multi-panel |
| Transition board | transition_in/out is whip_pan/morph/match_action/push_in/pull_out/360_spin/dolly_through | single canvas |
| Standalone cut | a punchline/ending that doesn't group with other cuts | single 1-panel |

When you get the plan, scan every cut's transition_in/out, decide the branching, show the user, and confirm. Detailed rules: REFERENCE/transitions.md.

**3.1 Cut grouping.** Regroup by same-background / same-viewpoint clusters (3 cuts inside the cafe → a 3-panel row / the final punchline → standalone). Why multi-panel: background consistency, credit savings, intuitive review.
**Images per page = decision table in `REFERENCE/presentation-rules.md` §3** (apply the same at the Phase 4.2 render): divider / strategy text / slogan / narration subtitle = **0 images** / key visual · product hero · cinematic narrative = **1 image** (full-bleed/letterbox) / comparison · option-A-vs-B · past-vs-present = **2 images** / mood · variation · character = **3 images** / storyboard grid = **5 columns (plan) · 3 columns (treatment)** / large tone-and-mood = **6–16 grid** / whole flow = **1 contact sheet**. Principle: more images = mood/summary, 1 image = narrative/impact. Alternate information-dense ↔ impact to control the breathing rhythm.

**3.2 Board generation prompt principles.**
- **Default cut generation = 2×2 grid (★ 4 cuts in one image · 2K · do not ignore).** Don't generate cut images one cut at a time; generate them grouped into a **2×2 grid (2 rows × 2 columns, 4 cuts in one image)** — like a storyboard. Fewer generations, higher tone/character consistency across the 4 cuts. If there are 5+ cuts, do several sheets of 4 (6 cuts = 4+2, 9 cuts = 4+4+1). State in the prompt: `"2x2 storyboard grid, 4 equal quadrants, 2 rows by 2 columns, symmetric centered thin white gutters, no overlap, each cell's subject fully inside its cell with margin, nothing cropped at cell edges"` (prevents cell-edge cropping — paired with the 3.3 preset slice). Resolution is 2K (3.2-c). (For decks/video, slice and use the cuts separately — 3.3.)
- **A separate description per cell (cut) + 500+ words per cut (★ do not ignore):** `"Cell 1 (top-left): … | Cell 2 (top-right): … | Cell 3 (bottom-left): … | Cell 4 (bottom-right): …"`. **Each cell (cut) description must be at least 500 words** (word count of English words, not character count) — covering subject, action, expression, camera (angle, lens, distance), lighting (direction/hardness/color temperature), foreground, background elements, texture, palette, mood, VFX, and typography without omission. A thin one- or two-line cell description is a direct cause of quality loss, so if it's under 500 words, fill it out more before generating.
- (Only for the special case where a simple horizontal storyboard fits better: "horizontal storyboard, N panels, equal width, thin white gutter" — the default is the 2×2 grid.)
- **Forbid (annotations/scribbles only)**: "no handwriting, no annotations, no labels, no storyboard markings, no timecode" — to prevent GPT auto-annotation. **But this is NOT a blanket "no text on the image" ban** — emphasis words, slogans, and kinetic/motion typography are *baked into* the generated image. Per-cut typo mode (none/subtitle/baked), baked prompts, and dataset determination: `REFERENCE/typography-in-image.md`.
- Use the master character sheet as the reference. **Character consistency — enforce the master sheet (the multi-character mixup lesson):** when generating boards (final cuts), bake the master-sheet constraints (e.g. no necklace, short hair, plain jacket) straight into the prompt and negative so *the board doesn't drift from the master* (prevention first). If an already-made final cut conflicts (necklace, hair length, etc.), make a cleaned-up version with that detail removed, or drop the conflicting cut from references and use only the master + contact sheet (fallback). Seedance follows a rich final cut more strongly than the master, so without enforcement the negative gets ignored.
- Aspect ratio: for a 9:16 video, panels are 9:16, the whole row is N× wide. If the Higgsfield cap forces it, receive at 16:9 and trim on slice.
- **Beware the visual-metaphor trap**: comparing a person to an object (a grey stone, a mannequin) usually fails aesthetically. Time-freeze is "alive, normal, just paused mid-motion".
- **Product fidelity (label · package) — product-lock:** for campaigns where the real product must appear exactly, fix the user's official product image as a **product-lock reference** (planner R4: don't generate brand IP yourself, prefer the user's asset) and state in every board prompt that "the real label/package is shown accurately and always" + **negative "no unlabeled / empty bottle / label-less product"**. Don't assume the product image isn't in `uploads/` — fall back to the conversation transcript (.jsonl) base64 then confirm with the user (Phase 0). Baking the main copy is **a default only for the KV/title/CTA frames** (not every frame); don't bake Korean — composite it in post. (At the video stage, the same product-lock reference applies to labels/VO in the video skill.)
- **Combine each cut's visual input into the panel description (key):**
 - if a cut has `recreation_prompts.t2i_start_frame` (or `style_prompt`), use that prompt as the **base of the panel description** (excluding celebrity face photo-replication and real logo marks; preserve subtitle/copy wording).
 - unpack `lighting` (direction/hardness/color temperature) · `texture` (surface texture) · `visible_elements` (foreground/midground/background/atmosphere) · `color_analysis` (palette · accent color) into each panel field. Without these, the same concept ends up with different tone/texture board to board.
 - at the video (i2v) stage, move the still into cut motion with `recreation_prompts.i2v_motion` + `i2v_params`.
- Detailed template: `prompts/scene_board.md`.

**3.1-b Layered-collage branch (★ fragments overlapping on a base — do not generate as one image).** If a cut / key visual has a structure where *several image fragments collage-overlap on top of an original* (the GMA-2018 style), do NOT tell the generation model to "make one collage image." **Split into 3 stages**: ① generate each fragment (base, eyes, hair, clothing, texture, graphic) as a separate t2i → ② composite an irregular collage preview with Pillow/OpenCV (different sizes, positions, z-order, slight rotations, so it doesn't look like a grid) → insert into the treatment → ③ the video stage does per-fragment layer motion (video-crafter). If which elements to separate is ambiguous, **ask** (distinguish base / fragments / graphics / elements that move). Full rules: `REFERENCE/layered-collage-protocol.md`. (A simple *side-by-side* split is panel_layout; this is an *overlapping* collage — keep them distinct.)

**3.2-a VFX in-board visualization.** Put post-production VFX into the board prompt as *one line of visual description*. Per-type patterns: REFERENCE/vfx-in-board.md (time_freeze/color_pop/wiggle_3d (via depth)/split_screen/lens_flare/dust/glitch/3D render). **Typography handling = the 3 categories in `REFERENCE/typography-in-image.md`**: baked (emphasis word, balloon typo, kinetic headline = baked into the image) / subtitle (cinema-style subtitle, long sentences, legal terms, precise figures = post) / none. It's not about merely drawing text shapes — baked actually bakes the text in. In the negative, only `garbled text, extra letters` (the text itself is allowed). **Do not put sexual/explicit blocker phrases (no nudity / sexual / NSFW, etc.) in the negative — it triggers moderation and blocks generation.**

**3.2-b Transition board (single canvas).** A flashy camera-movement transition is generated as **the end of the previous cut + the apex + the start of the next cut, all in one canvas**. 3 references (master + Cut N slice + Cut N+1 slice). Per-type patterns: REFERENCE/transitions.md + prompts/transition_board.md. No slicing (it stays on the transition page as-is).

**3.2-c Image-generation setup (★ lock the model · resolution · references).** Generate board/key-visual/product-cut images with Higgsfield `generate_image`, but **always state** the following (don't leave it to defaults — the default is 1k/low, so without stating it you get low quality and the model gets picked wrong):
- `params.model = "gpt_image_2"` (GPT Image 2). **Do not fall back to `nano_banana_2` / `nano_banana_flash` / any other model.**
- `params.resolution = "2k"` · `params.quality = "high"`. **Always lock the resolution at 2K** (no 1k/4k). Set the ratio with `params.aspect_ratio` to match the medium only (9:16 / 16:9 / 1:1 …).
- **Use the user's reference image (required · do not ignore):** ① download the user's uploaded image to the working folder → ② `media_upload` (presigned URL) → PUT the bytes to that URL (curl) → `media_confirm(type="image")` → ③ pass the returned media UUID as `params.medias=[{ "value": <UUID>, "role": "image" }]` to use as a reference (an uploaded UUID is safer than a direct external URL). Same for the product-lock product image.
- Recommend a cost preflight with `get_cost:true` before an expensive generation. Don't needlessly regenerate the same cut.
- **No code-drawing substitution (★):** do not use PIL `draw` (rectangles, circles, lines, paths) to draw icons/illustrations/logos/charts in place of a generative image. The only visual that goes on a page is a real raster made by `generate_image` (in `assets/`). If image generation/download fails, **do not patch it with vectors/shapes — stop the build and tell the user.**
- (Model name, resolution, and setup are internal info — do not expose to the user like "I confirmed the model.")

**3.2-d Local download of generated images (★ PIL input must be a local file · no direct URL use).** What the image-generation tool (Higgsfield etc.) returns is a **remote URL (or job)**. Later steps (3.3 slice, Phase 4 PIL compositing) **cannot open a URL directly** — `PIL.Image.open(url)` fails (the past cause of 21-byte files and `UnidentifiedImageError`). So right after generation, **always download locally and save to `assets/`**, then from there on use *only local paths* (slicing, compositing, `hero_stills/`, `확정컷/`, everything). **Do not pass a URL as a path/`src`.**
- After saving, validate with `PIL.Image.open(path).verify()`. If the file is a few hundred bytes or smaller, or won't open, that's a **download failure** (usually container network blocked or the URL expired) — don't build with an empty image; retry or tell the user.
- Helper (standard library, no extra install needed):
 ```python
 import os, urllib.request
 from PIL import Image
 def fetch_image(url, dest):
     os.makedirs(os.path.dirname(dest), exist_ok=True)
     req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
     with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
         f.write(r.read())
     with Image.open(dest) as im:        # block broken/empty files
         im.verify()
     if os.path.getsize(dest) < 1024:
         raise ValueError("downloaded image is abnormally small — check env networking/URL")
     return dest
 # e.g. local = fetch_image(gen_url, f"{proj}/assets/board_{cut}.png")  → from here on PIL uses local only
 ```
- If the tool returns base64 / a file id instead of a URL, decode and save it to make a local file the same way, then use that.
- ⚠ If the container's **networking is off, the download fails into an empty file.** The environment networking must be unrestricted (or the relevant CDN host allowed).

**3.3 Slicing (★ 2×2 grid → 4 cuts separated · decks use the separated cuts · preset fallback).** Split a 2×2 grid image into 4 cuts by **one horizontal and one vertical cut into quarters** (detect the white gutter / center line → cut into 2-row × 2-column cells → trim_white). For a horizontal N-panel board, split into N by column white-ratio (`colw>0.82` default; if there's no gutter, tune 0.75–0.88).
- **Grid preset fallback (★ guard against cropping):** if gutter detection fails or the detected boundary is off (a cell bites into and crops its neighbor), discard the detected value and slice with the **fixed preset = exact quartering**: `(0,0,W/2,H/2) / (W/2,0,W,H/2) / (0,H/2,W/2,H) / (W/2,H/2,W,H)` + trim_white. Decide programmatically (if a detected boundary deviates ≥3% from W/2·H/2, adopt the preset).
- A grid where **the cell content itself came out cropped** (the subject is cut off at the cell boundary) can't be saved by slicing — **regenerate** that grid with the 3.2 prompt (state quadrant · no cropping). Don't use a cropped cut in the deck/video as-is.
- Name the separated cuts by cut number and save into `확정컷/` · `frames/` — and **the deck (Phase 4) and video must use these separated per-cut images (never drop the whole 2×2 grid original into the deck).**

**3.3-a Character-separation check (required for multi-character — the multi-character mixup lesson).** Right after placing board references, confirm that each cut's `subject_identity` lines up: protagonist cuts get only the protagonist sheet; other-character cuts (cafe customer, part-timer) get only that person's sheet. If a protagonist master sheet is mixed into an other-character cut, drop it or lower its weight. (The multi-character mixup: with this check absent, a cafe-cut character degraded into the protagonist.)

**3.4 The human judgment slot (★ no Read of images/PDFs · 32MB payload cap).** Once boards/deck pages are generated, stop and let the user decide "redo / OK." **The AI does not make the aesthetic call.** Do not load a generated/downloaded image or a built PDF into context with `Read` to inspect it — existence, size, and resolution are checked *programmatically* with PIL/files (`Image.open().verify()`, page count, etc.); judging by looking is the user's job. **Inlining image/PDF bytes as base64 into the conversation/tool payload is also absolutely forbidden** — the platform request cap is **a fixed 32MB**, and if the transcript exceeds it the request itself dies (`Request exceeds the maximum size` 413). Always pass images only as a **local file path · upload UUID · URL reference** (deliver references via the 3.2-c media_upload path — bytes go via a direct PUT to the presigned URL and are never loaded into the conversation).

### Phase 4 — Deck Build (PIL + Korean fonts)

**4.1 Build stack.** Python + PIL. Fonts: title Black Han Sans (fallback Noto Sans CJK KR Bold), body/caption Noto Sans KR, English label Noto Serif CJK. **Canvas = 4K (3840×2160)** — write coordinates/fonts in logical 1920×1080 and output ×2 with `SCALE=2` (1080p is draft only). Multi-page PDF. **Every image input is a local file only — never pass a URL straight to PIL.**

**4.1 ★ Cinematic treatment module = `scripts/treatment_deck.py` (canonical · reverse-engineered from the ddasd 35-deck set _2606110130).** Single source of rules: **`REFERENCE/treatment-deck-system.md`**. The old `build_treatment_template` (editorial 2-column / infographic) is retired / a draft fallback only — build treatments with this module.

- `import treatment_deck as T` → `T.set_fonts(display, body, serif)` → **`th = T.theme_from_brand(brand_hex, tone)`** (don't hand-build the theme; derive it from the brand color).
- **★ THE IMAGE LAW (the #1 sin a prior gen broke · absolute):** `T.place_image`'s **default mode='fit' (preserve original ratio · dark letterbox)**. Scenes, mood, storyboard cuts, supporting cuts — all **in their original ratio**, no cropping / distortion / arbitrary stretching. `mode='fill'` (fill the frame) is allowed **only for cover/closing KV, and only when the source ratio is within ±8% of the page's 16:9** as a real crop (otherwise it auto-falls back to fit). **Do not crop a vertical (9:16) source horizontally** — stand it up as a vertical card. Rounded corners / shadows / borders default to 0 (a card exception applies only to the luxury tone).
- **★ THE COLOR LAW (the #2 sin a prior gen broke):** the base is by mood (cinematic/premium = near-black / service·public-service = white), and **the one point color is derived by `theme_from_brand` from the brand's primary color** (if absent, the genre's emotional color). The point color goes **only on section labels · headline keywords · cut numbers · divider lines · the tagline's text color / thin lines** — never as a filled box. The 5 tone presets (cinematic/service/luxury/public/brand_immersive) are in `treatment-deck-system.md` §3.
- Archetypes (§4, 11 types): `cover_film`·`cover_type`·`section_divider`·`concept_headline`·`narration_still`·`mood_board`·`scene_hero`·`scene_cluster`·`storyboard_grid`·`option_ab`·`closing`. Cut meta `{no,tc,scene,caption,na,note}`.
- **Moodboard grounding (★ Pinterest library connection):** the `mood_board` page and the image-generation tone are pulled from the `<MOODBOARD>` buckets in `REFERENCE/moodboard-library.md` (load it like a dataset — reflect the director's taste, no generic defaults). Reference images use `contain` (original ratio).
- **De-AI the images (★ required):** for generated images (KV, character, cut), bake the shooting-spec presets (P1–P6, tone-mapped) from `REFERENCE/photographic-treatment.md` into the Style block — no evaluative adjectives like "cinematic, 4K". No sexual/NSFW blocker words in the negative (moderation trigger).
- **★ No text box (cream/off-white card) — director's confirmed directive (_2606110030, invariant).** Text sits directly on the dark background, or on a scrim over a full-bleed image (a gradient, not a box). No filled surfaces.
- **IMAGE MANDATE:** cover, KV, cut-board, and scene pages composite real generated images (hero_stills/ · 확정컷/). Use `T.assert_images_present(placed_flags, page_kind)` — if 0 images, hold (Phase 5 ⑩). **Code-drawn vectors/shapes do not count as images — only `generate_image` rasters.**
- **One cut-board page required:** all cuts' timecodes go on a single `storyboard_grid` page (before the storyboard).

**4.1-a Two page modes — for the client vs for production.** There are two readers (the client catches it in 5 seconds / the production team needs the full fields). Render the same data in two modes.
- **Client page**: large still (70%+) + a one-line copy ("...") + 1–2 keywords. Large font, wide margins, one message per page.
- **Production page**: 8-block full fields (SCENE/COPY/CAMERA/VFX + PROPS/COLOR/TRANSITION). Small font, English vocabulary verbatim.
Builder functions `s_cut_public(d)` / `s_cut_internal(d)`. The client's 7-stage perception path (client_perception_path) is enforced by the Phase 1.1 checklist. Details: REFERENCE/client-vs-internal.md.

**4.2 Slide structure (default template, combined) — STRATEGY before cuts.** Cover → **02–08 STRATEGY (planning logic: the 7 beats of `REFERENCE/deck-logic.md`, one stage per page, with insight evidence cited)** → 09 expected effect (evaluation criteria / KPI worked backwards) → 10–12 visual language (axis · technique · palette) → 13 key visual (master sheet) → **a 1-page bridge ("here's how the strategy becomes video")** → 14~N per-cut client pages → transition pages → pacing → audio intent → closing → credits → [appendix] → production section (per-cut 8-block full fields + transitions). **Cuts (execution) must come after STRATEGY — cuts must not appear right after the cover.** That is, every deck = [cover → STRATEGY (why) → visual language → storyboard (how) → expected effect → closing]. **Data-driven** (s_phrase/s_points/s_palette/s_keyvisual/s_cut/s_transition/s_closing + the strategy-beat renderer s_strategy). Template: `scripts/build_treatment_template.py`. If the style isn't the cinematic deck, swap only the design signature (REFERENCE/deck-styles.md + presentation-rules.md).

**4.2-a Copy typesetting — the typeset system (no by-character line breaks).** Copy printed on a slide is not stamped as one block. *Direct* it with the 4 axes of `REFERENCE/text-setting.md`: ① **meaning-unit line breaks** (commas · connective/contrastive endings · quoted phrases — no by-char; a contrastive construction "A 아니라 B / not A but B" splits A and B onto separate lines) ② **one point-color emphasis** (only one key phrase per block in the brand color, the rest in the base color) ③ **role-based size hierarchy** (conclusion/key phrase 1.0 / lead-in 0.62 / supporting 0.38) ④ **smart alignment** (declarative 1–2 lines = center / explanatory·logical 3+ lines = left, weighted by track tone). These 4 axes are **coded into the `scripts/build_treatment_template.py` module (enforced · _2606031952)** — don't re-author each session; `import build_treatment_template as T` then `T.typeset(text, base_size, theme, tone)` → render with `T.draw_block()`. For a headline, `T.fit_headline(text, font_path, column_width, theme)` auto-picks the largest size that fits the width. **Strategy beats · concept copy · key-visual copy · closing** and other pages where text is the protagonist must go through these functions (storyboard subtitles are short, so simple handling). The module enforces split_clauses (meaning units) · the 1-emphasis budget · role-based sizes (1.0/0.62/0.38) · center/left, so no rendering that hand-jams text into a box. If the planner gave the copy lightweight markup (`//` line break, `*emphasis*`, `__big__`), accuracy goes up. Example: "데이터 부족은 불편이 아니라 '잠깐 끊기는 단절'" → `데이터 부족은 불편이 아닌,` (52pt base color) + `'잠깐 끊기는 단절'` (84pt point mint), center. ⚠️ This is typesetting *text on a slide* — *baking text into a cut image* is `REFERENCE/typography-in-image.md` (separate).

**4.2-b Copy humanization — strip the AI tell (★ a text-finalization step before typesetting · `REFERENCE/humanize-deck-copy.md`).** The **prose text** that goes into the deck (STRATEGY beat paragraphs · concept explanation · section lead-ins · bridge · closing · pitch script 6.1) is written naturally in Korean by applying the humanization rulebook **from the moment you write it** — translationese (A: "~를 통해" · "~에 있어" · "~에 의해" · double passives), AI clichés (D: "결론적으로" · "시사하는 바가 크다" · overuse of hype words), nominalization chains (F: "전략적 함의"), hedging (G: "~할 수 있을 것이다" — a deck asserts), sentence-initial conjunction overuse (H), formal-noun endings (I: "~인 것이다"), and repeated colon-subtitle headings (C-10). Right before typesetting (4.2-a typeset), confirm **0 remaining S1 patterns** via a self-scan, and rewrite only the offending phrases. **Preservation boundary (never touch):** the copy wording the planner finalized (headline · tagline · CTA — deliberate parallelism / repetition / rhythm is copy *craft*, not an AI tell), brand/product names, figures, prices, legal disclaimers, direct quotes, and English vocabulary tokens (production page). Full rules + deck profile + examples: `REFERENCE/humanize-deck-copy.md`.

**4.3 Apply brand color.** Primary on punchlines/headlines, 2nd–4th on emphasis/dividers. Use the hex verbatim (no eyeballing). If a brand-asset PDF exists, open it and extract the exact hex. (The one-emphasis-per-block is governed by 4.2-a typeset.)

**4.4 Work around the Write 24KB limit.** If the build script exceeds 24KB, write it in parts via bash heredoc, or split into functions and import. For editing large files, do an in-place patch via bash python.

**4.5 Transition-page note.** Small frames that keep the video aspect ratio. For 9:16, panels are 9:16 (`fh=298; fw=int(fh*9/16)`).

### Phase 5 — QA & cleanup

**⓪ Logic QA (first — `REFERENCE/deck-logic.md` §3):** (1) Even with 0 cuts shown, can you answer "why this ad" in one sentence? (2) Is the concept derived from the insight? (3) If you swap the brand for a competitor, does it stop making sense (justification)? (4) Does logic reach each item of the evaluation criteria? (5) Do the beats connect with "so / that is"? — if any one fails, hold the build.

Then, before PDF output, the automatic checks: ① cut matching (every cut's slide is included) ② copy typos (extract PDF text → diff against plan.md) ③ brand-color hex pixel sampling ④ Korean font breakage (Tofu ■ check) ⑤ slide ratio 16:9 ⑥ file size · page count. Re-render only the problem slides. On pass, put `treatment.pdf` at the top and share via `computer://`.

**⑦ Overlap gate (required · code-enforced):** if text encroaches on a panel/image, hold the build. Gather each text box rect and the panel/image rects and call `T.assert_no_overlap(text_rects, blocker_rects)` (`build_treatment_template`) — must pass to output the PDF. Before that, the headline is auto-shrunk into the column width (= panel start − margin) via `T.fit_headline()` so the encroachment is blocked at the source (prevents the §5 defect from recurring).
**⑧ Font floor (Q6 · scoped):** `T.assert_font_floor(page_type, role, size)` — applied **only to client / text-protagonist pages** (client/text_hero). **The production 8-block pages are exempt** (`page_type='production'`, small font is intentional).
**⑨ Confirm typeset routing:** confirm that the copy on text-protagonist pages went through `T.typeset()` (line count · 1 emphasis · size hierarchy present) rather than being one block / by-character line breaks.
**⑩ Image mandate gate (required · code-enforced):** on cover, key-visual, cut-board, and scene pages call `T.assert_images_present(placed_flags, page_kind)` — if 0 real composited images (placeholders only), hold the build. Blocks a flat slide that's "just text on a gradient."
**⑩-b Image-ratio preservation gate (★ THE IMAGE LAW):** did scene/mood/storyboard cuts go in at their original ratio (`fit`)? 0 cases of arbitrary crop / distortion / forced horizontal crop of a vertical source? `fill` only for cover/closing KV + ratio-near (±8%). On violation, re-place and re-render.
**⑪ 4K check:** is the output page 3840×2160 (`SCALE=2`)? It didn't drop to 1080p?
**⑫ No-text-box gate (★ director's confirmed directive):** if there's a filled surface behind text (cream / off-white / light card or any box), **hold the build** — replace with text typeset directly on the dark background and re-render. If a page feels monotonous, solve it with **negative space · brightness rhythm · hairlines · image placement**, not a box (no reverting to a cream surface). No exceptions: PROOF · strategy card · quote box all included. (Only a legibility scrim gradient over a full-bleed image is allowed.)
**⑬ Copy-humanization gate (4.2-b):** scan the prose in STRATEGY beats · concept explanations · lead-ins · closing · pitch script for **0 remaining S1 patterns** — AI clichés (D-1~D-7) · "가지고 있다"/double passives (A-7·A-8) · 5+ sentence-initial conjunctions (H-1) · "~인 것이다" endings (I-1) · repeated colon-subtitle headings (C-10), etc. On a hit, rewrite only that phrase and re-render. **Copy wording · figures · proper nouns are inviolable** (`REFERENCE/humanize-deck-copy.md` §1).

### Phase 6 — Client presentation package

After Phase 5: **6.1** a 1-minute pitch script (`treatment_client_pitch.md`, 7 stages with time markers — it's spoken, so apply the 4.2-b humanization especially strictly). **6.2** a key-cut still package (`hero_stills/`, hero cut + cover + key visual + closing, 6–8 images). **6.3** three PDF options (`treatment.pdf` combined / `treatment_client.pdf` / `treatment_internal.pdf`). For the client, usually client + pitch + hero_stills.

**6.4 Final deliverable package:**
```
{project_name}/
├── treatment.pdf / treatment_client.pdf / treatment_internal.pdf
├── treatment_client_pitch.md
├── plan.md
├── treatment.json
├── hero_stills/
├── assets/ (master_4k.png, board*_*.png, transition_T*_*.png)
├── frames/
├── 확정컷/
├── fonts/ (BlackHanSans.ttf, NotoSansKR.ttf)
└── build_treatment.py
```

### Phase 7 — Video production → handed off to the separate `lsb-video-crafter` skill [optional · on a "turn it into video" request]

The stage that turns final cuts into motion video is handled by the **`lsb-video-crafter` skill** (split out because this skill was getting bloated). The builder's core job is the PDF deck. When a video request comes in, trigger `lsb-video-crafter` and hand it the deliverables (treatment.json · final cuts · per-character master sheets · product-lock product image) as-is. That skill covers: multi-character / cross-cutting clip splitting / per-character · per-space references / 4000-word prompts · CRITICAL beats / Korean VO · motion typography / Seedance operation · declined_preset chain / **ip_detected = notify → stop → user approval → resume (no auto-retry)** / concat pixel-format enforcement / frame-level QA.

## When a dataset exists — pulling design tone via cross-pollination

If a dataset (`<DATASET>/entries/ADV-*.json`) exists, draw on it in Phase 1.2 (deck style) + 4.1 (typography·color) + 4.2 (structure).

**Real excellent-treatment examples:** `<LIBRARY>/003_reference_decks/` (README index). One per tone track (service·fun = Baemin Club / cinematic vertical = KT Y "the no-buffering person" / emotional drama = Y "3 seconds backstage"). Once the new deck's tone is set, **learn the signature of the nearest example** (background · single point color · large Korean + English kicker · meaning-unit headline · negative space) — no pixel copying.

**Principle:** don't copy pixels. What you pull is the abstracted signature (layout grid · type weight · color intent · slide flow) + the visual inventory / recreation_prompts (as inspiration). **Weights** (§4.3, same profile as the planner — currently LOOSE): same 0.5 / adjacent 0.8 / distant 1.0 / contrast 1.1 · hero-cut same 0.3 (STRICT restore values: 0.2/0.5/1.0/1.2 · hard-ban). The single source for the decision map is `lsb-ad-planner/schema.md` §3.

**Example (LOOSE basis):** for a telecom treatment → telecom (0.5) / bank·insurance (0.8) / fashion·beauty KV (1.0) / industrial B2B (1.1).

**Retrieval code (for reference):**
```python
# ⚠ Note: e['meta']['category'] / e['global']['signature_strength'] below are old-version leftovers
# and are NOT in the current entry schema (they are e['category_primary'] respectively, and
# signature_strength is absent). Do not depend on this running. Determine category by
# e['search_keywords']['industry'] (English token) + the lsb-ad-planner/schema.md §3 map.
# (Per request, the existing code is preserved rather than deleted.)
import json, glob
def cross_pollinate(entries_dir, target_category, top_n=5):
 candidates = []
 for path in glob.glob(f"{entries_dir}/ADV-*.json"):
 e = json.load(open(path, encoding='utf-8'))
 cat = e.get('meta', {}).get('category', 'unknown') # (old-version) → prefer e['category_primary']
 weight = {target_category: 0.2}.get(cat, 1.0)
 if cat in ADJACENT_MAP.get(target_category, set): weight = 0.5
 if cat in CONTRAST_MAP.get(target_category, set): weight = 1.2
 if e.get('global', {}).get('signature_strength', 0) >= 4: continue # (old-version) hero-cut hard-ban
 candidates.append((weight, e))
 candidates.sort(key=lambda x: -x[0])
 return [c for _, c in candidates[:top_n]]
```
If there's no dataset, use the §1.2 5-item catalog as a menu. As the dataset grows, the catalog gradually moves to dataset retrieval.

## FAQ & common failures
- **Make the cuts pretty first, reasons later** → a treatment is a persuasion document. STRATEGY (why) comes before cuts (`REFERENCE/deck-logic.md`). If cuts come right after the cover, it fails.
- **Stamp copy as one block and line-break by character** → an "information's right but it's not pretty" slide. Break by meaning unit and lift only one key phrase by color/size (`REFERENCE/text-setting.md` typeset, Phase 4.2-a).
- **Why a separate master sheet?** The first cut gets warped to fit "that cut's meaning," so the reference point wobbles. The master sheet is a meaning-free neutral cut, so it's stable as a reference.
- **Must it be 27 slides?** A recommendation, not a requirement. **One message per page** is the core.
- **The slicer cuts panels wrong** → state "thin white gutter, equal width" + tune `colw` 0.75–0.88.
- **Korean tofu (■)** → swap to Noto Sans KR variable, verify cmap.
- **Font breaks on PPTX conversion** → bundle fonts/ + install instructions.
- **The wrong character appears** → master-sheet reference dropped/conflicting. Unify medias.
- **A cut the planner didn't make is needed** → go back to the planner to reinforce, or ask the user "can I add this cut?" and stamp it into plan.md before building. **This skill does not add cuts on its own.**

## Trigger keywords
"make the treatment PDF" / "build the treatment" / "in the cinematic·service deck style" / "deck this concept" / "character sheet + storyboard + deck in one go" / "lsb-ad-planner output to PDF". Bilingual (Korean): "기획안 PDF 만들어줘" / "트리트먼트 짜줘" / "양반김·우리은행 식으로" / "이 컨셉으로 장표" / "캐릭터시트+콘티+장표 한 번에" / "lsb-ad-planner 출력 PDF로". If it's a new concept or a request for N candidates, this is not the skill — go to `lsb-ad-planner`.

> **The *source* of the strategic logic is the planner (concept · insight · strategy_spine). The builder merely *renders* it into a logical presentation structure (the STRATEGY section); it does not invent new strategy. But if the input's strategy_spine is empty, fill it with the user before proceeding (build gate).**

## Companion docs to read alongside
- `REFERENCE/keyword-vocabulary.md` — thinking method · copy · keyword taxonomy (§8).
- `REFERENCE/cut-schema.md` — the 30+ cut fields + visual inventory + recreation_prompts definitions + English vocabulary.
- `REFERENCE/transitions.md` — transition single-canvas principle · branching rules.
- `REFERENCE/vfx-in-board.md` — VFX in-board visualization.
- `REFERENCE/client-vs-internal.md` — client vs production pages · 7-stage perception path.
- `REFERENCE/deck-styles.md` — design signatures of the cinematic / service / luxury / object-KV / worldview decks.
- `REFERENCE/deck-logic.md` — **planning-logic spine (7 beats) · STRATEGY render · logic QA · anti-patterns (universal to all treatments).**
- `REFERENCE/presentation-rules.md` — **34-type reverse engineering: purpose × tone tracks · 12 common grammars · images-per-page decision table · copy rules.**
- `REFERENCE/typography-in-image.md` — **the 3 typo categories (none/subtitle/baked) · dataset determination · baked prompts (replaces the Phase 3.2 'no text').**
- `REFERENCE/treatment-deck-system.md` — **★ canonical design system (English): ddasd 35-deck reverse engineering. plan/treatment/PPM distinction · 2 modes · THE IMAGE RATIO LAW · POINT COLOR 3 layers · 11 archetypes · timecode · furniture · typography · do/don't. The single standard for `treatment_deck.py`.**
- `REFERENCE/photographic-treatment.md` — **★ de-AI the images (English): the 8 photographic_treatment fields + 6 per-tone presets (P1–P6). Enforced into the image-generation Style block.**
- `REFERENCE/moodboard-library.md` — **★ the Pinterest moodboard library contract (English): `<MOODBOARD>` path · buckets · how to load the manifest · planner/treatment/image-generation wiring.**
- `REFERENCE/composition-principles.md` — **★ the 7 composition laws (English): rule-of-thirds / golden-ratio / leading-lines / framing / symmetry / depth / fg-mg-bg. Wired to comp_bias, scene_board Style, the planner cut `composition` field, and archetype selection. 1–2 per frame; don't default to center.**
- `REFERENCE/editorial-layout.md` — (old) editorial module doc. Treatments use the deck-system above as canonical; this is a fallback reference.
- `REFERENCE/text-setting.md` — **deck-copy typeset system: meaning-unit line breaks · one point-color emphasis · role-based size hierarchy · center/left smart alignment (Phase 4 text render — replaces by-character line breaks).**
- `REFERENCE/humanize-deck-copy.md` — **deck-copy humanization: detect/avoid Korean AI-tell patterns (translationese · AI clichés · nominalization · hedging · conjunctions) rulebook + copy-preservation boundary + deck-genre adjustment (Phase 4.2-b · gate ⑬ · 6.1 pitch script). Source: epoko77-ai/im-not-ai v2.0 (MIT).**
- `REFERENCE/scene-boards.md` — multi-panel board design · slicing.
- `REFERENCE/layered-collage-protocol.md` — **layered collage (fragments overlapping on a base) 3-stage split: generate individually → composite preview → video layer motion (single source shared with analyzer · video-crafter).**
- `REFERENCE/deck-build.md` — PIL builder fonts · canvas · 24KB workaround.
- `REFERENCE/keyword-vocabulary.md` — English tokens + KO aliases (taxonomy-tag standard).
- `scripts/slice_boards.py` / `build_treatment_template.py` / `cut_template.json` / `treatment_global_template.json` / `transition_template.json`.
- `prompts/master_character.md` / `scene_board.md` / `transition_board.md`.
- (Cross-pollination map · analyzer→treatment mapping: `lsb-ad-planner/schema.md` §3·§5. Cut start-frame t2i/i2v: `lsb-ad-analyzer/REFERENCE/frame-recreation-prompts.md`.)

---
*Version: lsb-treatment-builder_260614_v11 · 2026-06-14 KST. (version scheme = YYMMDD_vN; earlier inline _2606xxxx codes are legacy timestamps. v11 = **7 composition laws wired in** — new REFERENCE/composition-principles.md (rule-of-thirds/golden-ratio/leading-lines/framing/symmetry/depth/fg-mg-bg); extended photographic-treatment comp_bias tokens; scene_board Style block gets a composition line; planner adds a per-cut `composition`+`eye_path`; treatment-deck-system §7.5 ties archetype choice to the laws. 1–2 per frame, no center-by-default.) Previous _2606140000 = **Phase 1 asset consolidation** — merged a prior gen's v3 module (11 archetypes · section_divider · concept_headline · option_ab · vertical furniture) with the IMAGE/COLOR LAW → made `treatment_deck.py` canonical (theme_from_brand derivation + legibility correction + tone presets, place_image auto ratio law). 3 new canonical English docs: treatment-deck-system.md (35-deck reverse engineering consolidated · English) · photographic-treatment.md (anti-AI presets P1–P6 · English) · moodboard-library.md (Pinterest library contract · English). Wired the moodboard · photographic-treatment into mood_board · image generation.) Previous _2606110130 = **ddasd 35-deck visual reverse engineering → made the cinematic treatment module `treatment_deck.py` canonical + new `REFERENCE/treatment-deck-system.md` (single standard).** Corrected the prior gen treatment_deck.py's two sins: ① **THE IMAGE LAW** — place_image default mode='fit' (preserve original ratio · letterbox), fill only for cover/closing KV + ratio-near (±8%), no forced horizontal crop of a vertical source, rounded/shadow default 0 → Phase 5 gate ⑩-b ② **THE COLOR LAW** — derive the one point color via theme_from_brand(brand_hex, tone) (no hardcoding) · text/lines only · 5 tones. 4-way subagent analysis original outputs/_deck_analysis. No-cream-box rule (_2606110030) kept invariant.) Previous _2606110030 = **★ Total ban on text boxes (cream/off-white card) — reflecting the director's confirmed directive**: THEME_EDITORIAL surface cream (#FBF7EF) → dark same-family (#3A1C23, for non-text surfaces only), two_col PROOF filled card → hairline + direct-on-background typesetting, 4.1-editorial rewrite (text directly on dark background · breathing via negative space/brightness/hairlines), **gate ⑫ = flipped from 'breathe with cream' to a '0 text boxes' check**, editorial-layout.md synced. The cream mandate was a wrong default from _2606041330 — no recurrence.) Previous _2606101300 = synced cross-pollination weights to the **LOOSE test profile** (paired with planner _2606101300) — same 0.5/adjacent 0.8/distant 1.0/contrast 1.1 · hero-cut same 0.3, STRICT restore values noted.) Previous _2606101200 = ① **3.3 grid preset fallback** — on gutter-detection failure / boundary off (±3%+), slice with the fixed exact-quartering preset; regenerate a grid with cropped cell content (3.2 prompt with quadrant · no-cropping prevention wording) ② **3.4 32MB payload cap** — never inline image/PDF base64, file path/UUID/URL reference only (platform request fixed at 32MB).) Previous _2606101000 = ① **Phase 1.1-b cut-grammar gate re-verification** (planner R10 second defense — for same-subject·same-space adjacent pairs, if one of size 2+ steps / angle 30°+ / subject·space·time change is unmet it's a double violation → replace with a seamless transition or propose merge, no entering Phase 3·4 with a violation present) ② **Phase 4.2-b copy humanization** (strip Korean AI-tell from deck prose — translationese · AI clichés · nominalization · hedging · conjunctions · formal nouns, preserve copy wording · figures · proper nouns) + **Phase 5 gate ⑬** (0 remaining S1) + 6.1 pitch script application + new `REFERENCE/humanize-deck-copy.md` (source epoko77-ai/im-not-ai v2.0 MIT).) Previous lsb-treatment-builder_2606081200 · 2026-06-08 KST. (_2606081200 = default cut generation 2×2 grid (4 cuts in one image · 2K) → separate into cuts via 3.3 slice, decks use separated cuts only / each cell (cut) description forced to a 500-word minimum / 3.4 no Read-inspection of generated images · PDFs — programmatic / user judgment only (prevents 413 · token blow-up).) Previous _2606051640 · 2026-06-05 16:40 KST. (_2606051640 = Phase 3.2-c image-generation setup locked — model=gpt_image_2 · resolution=2k · quality=high (no default 1k/low, no nano_banana fallback) · user reference via media_upload→medias; download block moved to 3.2-d.) Previous _2606051140 = Phase 3.2-d (old 3.2-c) forced local download of generated images — PIL can't open a URL, so receive into assets/ then use local paths only, verify to block empty/broken files; Phase 4.1 'no direct URL use' stated. Motive: a Higgsfield generation URL passed straight to the PDF build (PIL) caused image-insert failure.) Change history: see 적용방법.md. (_2606041330 = **editorial layout system (redesign-gap-grade default)**: build_treatment_template §8 — 4K (3840×2160) default + archetypes cover_split/two_col/fullbleed_kv/cut_board + palette tokens (cream surface) + image-mandate gate assert_images_present + REFERENCE/editorial-layout.md. Motive: a first build was 1080p · centered text dump with no images → an unnecessary redesign. Previous _2606031952 = typeset code enforcement. _2606032044 = multi-character & cross-cutting (the multi-character mixup lesson): Phase 1.4·2.0·3.2·3.3-a + Phase 7 lsb-video-crafter split-off.) _2606140000 = English rewrite + de-jargon (faithful, no content dropped).*
