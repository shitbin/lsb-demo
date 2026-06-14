# LSB Skills — Shared Glossary (read this first if you have no prior context)

These five skills (analyzer → planner → image-crafter → treatment-builder → video-crafter) form one
ad-production pipeline. Earlier versions were written in Korean and full of internal code-names from past projects,
so a fresh model session couldn't follow them. This glossary defines every term in plain language.
**All skill docs now reference these definitions instead of insider shorthand.**

## The pipeline in one line
`lsb-ad-analyzer` watches reference ad videos and turns them into structured data → `lsb-ad-planner`
reads that data + the brief and proposes ad concepts + cut lists → `lsb-treatment-builder` turns the
chosen concept into a visual treatment PDF → `lsb-video-crafter` turns the locked frames into video.

## Core terms
- **brief** — the client's request: brand, product, target, length, aspect ratio, tone, must-include / must-avoid.
- **dataset** — the library of analyzed reference ads. Lives at `<LIBRARY>/001_ad_video_dataset/`
  (`entries/` = one JSON per ad, `index/` = search indexes). Built by the analyzer.
- **copy bank** — 4,000+ real Korean ad copy lines for inspiration. `<LIBRARY>/002_ad_copy_bank/`.
- **reference decks** — example treatment PDFs to learn layout from. `<LIBRARY>/003_reference_decks/`.
- **moodboard library** — the director's curated taste images (Pinterest). `<LIBRARY>/004_moodboard_library/`.
- **`<LIBRARY>`** — the folder that **directly contains `001_ad_video_dataset/`**. Resolve by structure:
  first check the connected folder for `001_ad_video_dataset/`; if it isn't there, look one level down in a
  `library/` subfolder and use that as `<LIBRARY>`. This works for every layout: a connected
  `LSB_AD_ENGINE/library`, a GitHub repo with `001…` at its root (old layout), or a repo with a `library/`
  wrapper (new layout). Never hardcode an absolute path.
- **cut** — one shot. **cut list** — the ordered shots of an ad. **frame / still** — one image of a cut.
- **hero cut** (was "wow cut") — the highest-impact 1–2 cuts (hook / key visual / just before the CTA).
- **cross-pollination** — deliberately borrowing the *approach/structure* of an ad from a DISTANT
  category (not the same category) so the result is fresh and not plagiarised. Weighted: same category
  weak, distant/contrast strong.
- **plagiarism gate** — a self-check that the output isn't too similar to any reference (similarity score).
- **KV (key visual)** — the single signature image that represents the whole campaign.
- **i2v / t2v** — image-to-video (animate a locked still) / text-to-video (generate from text + a few
  reference images, no locked still).
- **VO / Na** — voice-over / narration line. **motion typography** — animated on-screen brand text.
- **seamless transition** — the last frame of one clip = the first frame of the next, so cuts flow
  without a hard jump. **hard cut** — an intentional abrupt jump (only when explicitly requested).
- **double / jump cut** — two adjacent cuts of the same subject whose size AND angle barely change, so
  it looks like a glitch rather than a new viewpoint. The cut-grammar gate (planner R10) prevents this.
- **photographic treatment** — concrete shooting specs (film stock, lens, lighting, grain, grade) used
  instead of vague adjectives so generated images don't look AI-made. See treatment-builder
  REFERENCE/photographic-treatment.md.
- **IP moderation block** (status `ip_detected`) — the video tool refused a generation because it
  detected real brand/celebrity likeness. The user must approve it in the tool; the agent cannot bypass
  it by editing the prompt. Stop and tell the user.
- **preset hijack** — the image/video tool suggests replacing your prompt with one of its canned presets
  (and may leak a preset *sample image* — e.g. a stock woman — into the output). You decline it on EVERY
  generate_image AND generate_video (pass the suggested preset id to `declined_preset_id`, as a default —
  not a reaction after you see a leak) and force your literal prompt. A preset/sample/demo is never a
  final deliverable.

## Image-pipeline terms (260614 split)
- **lsb-image-crafter** — the single skill that owns ALL `generate_image` (master sheets, key visual, cut
  stills). Runs after the planner, before the treatment-builder. Enforces 7 gates (declined_preset ·
  full-field cells · composition · foreground/midground/background · baked-copy/no-"no text" · moodboard
  references · model/preset lock). Why it exists: `_meta/IMAGE_PIPELINE_DIAGNOSIS_260614.md`.
- **cut_plan.json** — planner → image-crafter. Per-cut visual fields: composition (1–2 of the 7 laws),
  eye_path, photographic_preset (P1–P6), visible_elements (5 layers), moodboard_bucket, typo_mode, baked_text.
- **stills.json** — image-crafter → treatment-builder + video-crafter. Every produced still with its local
  path, ratio, gen params, declined_preset id, typo_mode, baked_ok. Downstream skills REUSE these (re-send
  = reuse, never regenerate) and never call generate_image themselves.
- **typo_mode** — per frame: `baked` = copy rendered INTO the image; `subtitle` = composited in post
  (long running subtitles / legal only); `none`. NEVER put "no text / no letters / no captions" in a
  negative. **Korean main copy / headline / CTA = ALWAYS baked** (gpt_image_2 renders Korean reliably; no
  attempt/fallback, no romanizing — user-set _260614).
- **wordmark** — the studio name printed on decks/videos. Always **LSB PRODUCTION** (older reference
  files carry a previous studio name — always replace it).
- **E.O.D** — "end of document", the closing page of a treatment deck.

## Past-incident shorthand (translated — these were project names, treat as lessons not jargon)
- "the multi-character mixup" (was "A3") — a past job where, because each cut didn't lock WHO appears in
  it, the video put the protagonist in every cut, contradicting the treatment. Lesson: lock
  `subject_identity` per cut and keep a character roster.
- "the redesign-gap post-mortem" (was "허쉬/Hershey session", "Codex redesign") — a past job whose first
  build was low quality (flat text dumps, no images, wrong ratios) and had to be redone by hand. Lesson:
  the build must hit a high bar on the first pass (real images, correct ratios, no filled text boxes).

## Hard rules that apply pipeline-wide
- Korean copy/narration is written in Korean script, never romanized.
- Never hardcode brand assets (logo/mascot/character) — request the official file or research it.
- Never inline image/video bytes into the conversation (platform request cap is 32MB; it kills the run).
  Pass file paths / job ids / URLs instead.
- Never put sexual/NSFW blocker words in a negative prompt (it triggers moderation and blocks generation).
- Treatment image ratio: preserve the original aspect ratio (no arbitrary cropping). Text never sits on a
  filled cream/tinted box.
