# LSB Production — Skill Set (read this first)

Five skills form one ad-production pipeline. Written for a fresh Claude Opus 4.8 session with **no
prior context** — start with `GLOSSARY.md`, then the skill you need.

```
lsb-ad-analyzer → lsb-ad-planner → lsb-image-crafter → lsb-treatment-builder → lsb-video-crafter
   (analyze        (brief + data      (★ generate ALL        (lay out the deck       (locked frames
    reference       → concepts +        images: master        PDF from stills.json    → video)
    ad videos)      cut lists +         sheets · KV · cut     — no image gen here)
                    cut_plan.json)      stills → stills.json)
```
**260614 split:** image generation was pulled out of treatment-builder into its own owner,
`lsb-image-crafter`, with 7 hard gates (declined_preset · full-field cells · composition · fg/mg/bg ·
baked-copy/no-"no text" · moodboard refs · model/preset lock). Why + the 9 fixed defects:
`../_meta/IMAGE_PIPELINE_DIAGNOSIS_260614.md`. Data contract: `lsb-image-crafter/REFERENCE/data-contract.md`.

## Read order
1. **GLOSSARY.md** — every shared term in plain English (dataset, cut, hero cut, cross-pollination,
   i2v/t2v, seamless transition, double/jump cut, photographic treatment, IP moderation block, etc.)
   and the pipeline-wide hard rules. The skills replaced all insider code-names with these definitions.
2. The skill's own `SKILL.md`.
3. That skill's `REFERENCE/` docs, on demand.

## The library (data the skills read at runtime)
`<LIBRARY>` = the folder that **directly contains `001_ad_video_dataset/`**. Resolve by structure: check the
connected folder; if `001_ad_video_dataset/` isn't there, drop into a `library/` subfolder and use that.
Works for `LSB_AD_ENGINE/library`, a repo with `001…` at root, or a repo with a `library/` wrapper. Never hardcode a path.
- `001_ad_video_dataset/` — analyzed reference ads (analyzer writes, planner reads).
- `002_ad_copy_bank/` — 4,000+ real Korean ad copy lines (planner reads).
- `003_reference_decks/` — example treatment PDFs (builder learns layout from).
- `004_moodboard_library/` — the director's Pinterest taste library (planner + builder read; contract in
  `lsb-treatment-builder/REFERENCE/moodboard-library.md`).

## Current versions (all `_2606140000` = English rewrite + de-jargon)
- `lsb-ad-analyzer` — reference-ad → dataset entry.
- `lsb-ad-planner` — brief + dataset + copy bank + moodboard → 5 candidate concepts (A–E + regenerate),
  each with a cut list; cross-pollination; cut-grammar (anti "double"/jump-cut) gate; plagiarism gate.
- `lsb-treatment-builder` — concept → cinematic treatment PDF via `scripts/treatment_deck.py`
  (11 archetypes). Canonical design rules: `REFERENCE/treatment-deck-system.md` (image-ratio law,
  point-color law, no text box), `REFERENCE/photographic-treatment.md` (anti-AI image presets),
  `REFERENCE/moodboard-library.md`.
- `lsb-video-crafter` — locked frames → video (Seedance i2v/t2v), seamless transitions, brand
  motion-typography, anti-preset authenticity checks, IP-moderation protocol.

## Three rules that caused the most rework (now enforced everywhere)
1. **Image ratio:** keep the original aspect ratio — never crop/squeeze. (treatment-deck-system §2)
2. **No text box:** copy sits on the page or on an image scrim, never on a filled cream/tinted card.
3. **No AI look:** generated stills use shooting specs (film stock/lens/light/grain), not adjectives.

## How to apply changes (production)
1. Sync `005_skills/` → GitHub `shitbin/lsb-demo` `005_skills/`.
2. Re-upload the skills in the console Managed Agent; keep `agent_config.yaml`.
3. Changes take effect from the next session.

## Notes
- `적용방법.md` is the legacy Korean change-log (kept for history).
- Still Korean (next translation batch — secondary, loaded on demand): some `REFERENCE/` docs
  (cut-schema, keyword-vocabulary, presentation-rules, editorial-layout, text-setting,
  typography-in-image, layered-collage-protocol, deck-logic). The SKILL.md entry points are English.
- `build_treatment_template.py` is the retired infographic module (treatment_deck.py replaces it).
