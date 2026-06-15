# LSB ad-planner input/output schema (planner-only · lsb-ad-planner_2606021645)

> Version: lsb-ad-planner_2606021645 · 2026-06-02 16:45 KST. Defines only what the planner owns: the brief input · the cross-pollination map · the treatment.json output · the analyzer→treatment mapping table. For detailed entry/shots fields, see lsb-ad-analyzer/schema.md (not duplicated here).

---

## 0. Dataset-resolve contract (cross-platform — shared mac/Win)

The planner **resolves the dataset folder at runtime** at session start (STEP 0). No hardcoded absolute paths.

- `<LIBRARY>` = the folder that **directly contains `001_ad_video_dataset/`** (resolve by structure, never by name): take the connected folder; if it directly contains `001_ad_video_dataset/` that IS `<LIBRARY>`, else drop into its `library/` subfolder and use that. The same rule maps **both deploy environments**: **(API — console Managed Agent)** the connected `shitbin/lsb-demo` repo keeps `001…` under `library/`, so `<LIBRARY>` = the repo's **`library/`**; **(Local — Mac Cowork)** the connected `LSB_AD_ENGINE` folder keeps `001…` under `library/`, so `<LIBRARY>` = **`/Users/soobin/Desktop/LSB_AD_ENGINE/library`** (or that `library/` connected directly). **`<DATASET>` = `<LIBRARY>/001_ad_video_dataset`** — inside it: `entries/`, `index/`, `dataset_view.md`. (Copy bank `<LIBRARY>/002_ad_copy_bank/`, reference decks `<LIBRARY>/003_reference_decks/`, moodboard `<LIBRARY>/004_moodboard_library/`.)
- **Copy-bank contract (`<LIBRARY>/002_ad_copy_bank/` · the input for STEP 3 (E)):** `copy_bank.json` = `{_meta, index_by_industry(counts), entries[]}` — each entry: `industry` (English token) · `category_kr` · `brand` · `copy` (Korean original verbatim) · `date` · `url` · `src`. `index_by_industry.json` = `{industry: [array of integer indices]}` — **use those integers to access `entries[i]`** (for fast extraction). `copy_bank.csv` is for human reading (the skill doesn't read it). It's ~1MB — don't Read it whole; pick via the index and extract with code only (SKILL.md STEP 3 (E) code). The 16 industry tokens and their Korean mapping are in `002_ad_copy_bank/README.md`.
 - Local (Mac Cowork) example: `/Users/soobin/Desktop/LSB_AD_ENGINE/library` · Win example: `C:\Users\<id>\Desktop\LSB_AD_ENGINE\library` · API: the connected `shitbin/lsb-demo` repo's `library/`
- Resolve order: (1) take the connected folder — **API:** the `shitbin/lsb-demo` repo root; **Local:** `LSB_AD_ENGINE`. If it directly contains `001_ad_video_dataset/` it IS `<LIBRARY>`; else drop into its `library/` subfolder. `<DATASET>` = `<LIBRARY>/001_ad_video_dataset` (entries/ + index/ inside it) → (2) if absent, request it with `request_cowork_directory` → (3) if the folder is empty, seed by copying the skill's `dataset_template/`.
- The **absolute path obtained this way = `DATASET`**. All paths thereafter are treated as relative to `DATASET` (`entries/`, `index/`).
- For Python path joins use `os.path.join` (safer than hardcoding slashes). The `entries/` · `index/` in docs/examples are notations common to both OSes.
- This one folder is the **central library** (not recreated per project). It's an accumulating asset, so the same folder is connected every session.

---

## 1. Brief input schema (the STEP 0 form result)

Normalize the `AskUserQuestion` form responses into the following dict. Values are **English tokens** (keyword-vocabulary.md); Korean responses are mapped via the KO-alias table.

```python
brief = {
 "brand": str, # free text (proper noun OK)
 "product": str,
 "industry": str, # 1 English token (e.g.: "finance")
 "product_category": [str], # English token
 "target_demo": [str], # English token (e.g.: ["mz","early_career"])
 "media_format": str, # English token (e.g.: "shortform_landscape_30s")
 "tone": [str], # English token (e.g.: ["punchy_humor","friendly"])
 "must_include": str, # free
 "must_avoid": str, # free
 "visual_ref_attached": bool,
 "raw_text": str # user free description (Korean allowed)
}
```

**Normalization:** Korean brief → substitute English tokens via the KO aliases in `keyword-vocabulary.md`.
E.g.: "MZ 사회초년생" → `target_demo=["mz","early_career"]`, "재밌고 가볍게" → `tone=["punchy_humor","friendly"]`.

---

## 2. Search contract — read the index directly (no index_helper import)

The index (`index/by_<axis>.json`) is plain JSON, so the planner **reads it directly** and matches. (Don't import the analyzer's `index_helper.py` — that file is for analyzer writes only.)

```python
import json, os
AXES = ["industry","product_category","target_demo","media_format","tone",
 "pacing","technique","vfx_keywords","copy_strategy_keywords","concept_derivation_pattern"]

def search(DATASET, **brief_axes):
 """English-token multi-axis match. return [(entry_id, score, hits)] score=# of matched axes."""
 matches = {}
 for axis, values in brief_axes.items:
 if axis not in AXES: continue
 if isinstance(values, str): values = [values]
 p = os.path.join(DATASET, "index", "by_%s.json" % axis)
 if not os.path.exists(p): continue
 idx = json.load(open(p, encoding="utf-8"))
 for v in values:
 for eid in idx.get(v, []):
 m = matches.setdefault(eid, {"score":0,"hits":{}})
 m["score"] += 1; m["hits"].setdefault(axis,[]).append(v)
 out = [(e,m["score"],m["hits"]) for e,m in matches.items]
 out.sort(key=lambda x:-x[1]); return out
```

If you need an entry's body, `json.load` `os.path.join(DATASET,"entries","%s.json"%eid)`. `master.json` allows a fast lookup of brand/title/category_primary.

---

## 3. Cross-pollination category map (keyed on the English industry)

Match weights: **same 0.2 / adjacent 0.5 / distant 1.0 / contrast 1.2**. For hero cuts, same category = **0 (HARD BAN)**.
The judgment basis is the entry's `search_keywords.industry` (English token). Any industry not listed below defaults to `1.0` (distant) + uses the entry's `cross_pollination_tags` as a secondary signal.

| industry (X) | adjacent (0.5) | contrast (1.2) |
|---|---|---|
| finance | insurance, telecom, it_saas | sportswear, fnb, public_gov |
| automotive | mobility, luxury, construction_realestate | beauty, fnb, public_gov |
| construction_realestate | finance, luxury, home_appliance | sportswear, fnb, content_ott |
| retail | ecommerce, fnb, beauty | industrial_b2b, automotive, finance |
| sportswear | sports, fashion, beauty | finance, construction_realestate, public_gov |
| telecom | it_saas, content_ott, finance | luxury, construction_realestate, fnb |
| fashion | beauty, luxury, content_ott | industrial_b2b, automotive, finance |
| fnb | beverage_alcohol, retail | luxury, automotive, industrial_b2b |
| beauty | fashion, retail, healthcare_pharma | industrial_b2b, automotive, sports |
| public_gov | healthcare_pharma, education | luxury, fashion, automotive |

> All other combinations are `1.0` (distant). As the dataset grows, each entry's `cross_pollination_tags` (adjacent/distant/contrast) reinforces/replaces this table.
> Each entry's `cross_pollination_tags` are recommended to be English tokens from this version on (current data may still carry Korean descriptions — use as a secondary signal only).

---

## 4. treatment.json output contract (the builder's Phase 0 input)

The planner's STEP 6 single-detailed output is the following JSON. The builder receives it **without edits**.

```json
{ "global": { /* §4.1 */ }, "cuts": [ /* §4.2 */ ], "transitions": [ /* §4.3 */ ] }
```

- §4.1 global = 1:1 with the keys of `lsb-treatment-builder/scripts/treatment_global_template.json`.
- §4.2 cuts[] = 1:1 with the keys of `lsb-treatment-builder/scripts/cut_template.json` (**includes the 5 visual-inventory axes** — see the §5 mapping table).
- §4.3 transitions[] = 1:1 with the keys of `lsb-treatment-builder/scripts/transition_template.json`.

Required completeness (missing → output forbidden): global's `client_perception_path` (7 items) + **`strategy_spine` 6 fields (brief · insight + evidence[] · strategy · concept_rationale · brand_right · payoff)**, `brand/product/target_demo/total_duration_sec/aspect_ratio/narrative_arc/pacing_curve`; each cut's `index/no/duration/framing/function/intra_cut_rhythm/transition_in/out`. (`strategy_spine` is rendered by the builder as the STRATEGY section — `lsb-treatment-builder/REFERENCE/deck-logic.md` §1.)

---

## 5. analyzer entry → treatment field-mapping table (core — prevents drift)

The analyzer entry (analysis schema) and the treatment (production schema) have **different key names.** The planner is the translator.
(Entry field definitions: `lsb-ad-analyzer/schema.md`. Treatment fields: the builder's template jsons.)

### 5.1 Global

| analyzer entry | → treatment global | Note |
|---|---|---|
| `total_duration` | `total_duration_sec` | `_sec` suffix |
| `hook_position` | `hook_position_sec` | |
| `cta_position` | `cta_position_sec` | |
| `shot_count_corrected` (if present) / `shot_count` | `shot_count` | corrected value preferred |
| `fps`,`aspect_ratio`,`narrative_arc`,`pacing_curve`,`music_tempo_curve`,`wow_cut_index`,`creative_device` | same | as-is |
| `production_signature.*`,`global_layout.*`,`recurring_motifs` | same | as-is |
| `typography` | `typography_global` | `typography.animation_style` → `typography_global.animation_style_default` |
| `vfx` | `vfx_global` | key name only differs (subfields same) |
| `copywriting.*` | `copywriting.*` | same |
| `inferred_creative_thinking` (7 one-liners) | `client_perception_path` | same 7 keys. `confidence` excluded (analyzer estimate label) |
| `inferred_creative_thinking` + `inferred_brief` (grounds) | `strategy_spine` (brief · insight + evidence · strategy · concept_rationale · brand_right · payoff) | **the planner expands it into an argument** — one-liner → a logical paragraph with grounds & derivation attached. Mapping: deck-logic §1 |
| `audio` (Whisper observation) | `audio_intent` (production intent) | **not a direct mapping.** analyzer.audio = what was heard, treatment.audio_intent = what to make. The planner writes it fresh |

### 5.2 Cut (analyzer `shots[i]` → treatment cut)

Most are **same key = same meaning.** Only the differences:

| Situation | Handling |
|---|---|
| analyzer has no `no` | the planner assigns it (C1, C2A…) |
| analyzer has no per-cut `wow_cut` | derive from global `wow_cut_index` |
| `typo_color_strategy` (cut) | if absent, inherit from `typography_global.color_strategy` or write it |
| `source_refs`,`still_path`, per-cut `audio_intent`,`vfx_in_board_prompts` | written by the planner/builder (not in the analysis entry) |
| **the 5 axes** `visible_elements`,`texture`,`lighting`,`color_analysis`,`style_prompt` | **carry through as-is.** Pull these fields from the cross-pollination reference entry as *inspiration* and write fresh for the new cut (no pixel cloning). The builder uses them in the board prompts |

> Key point: when you pull a reference entry via cross-pollination, read it with analyzer keys and write the output with treatment keys. This table is that conversion rule.

---

## 6. References
- Detailed entry/shots fields & vocabulary: `lsb-ad-analyzer/schema.md` + `lsb-treatment-builder/REFERENCE/cut-schema.md`
- English tokens & KO aliases: `lsb-treatment-builder/REFERENCE/keyword-vocabulary.md`
- Thinking methods & page patterns: `lsb-treatment-builder/REFERENCE/keyword-vocabulary.md` (§8)
- The plan-logic spine (strategy_spine framework · QA): `lsb-treatment-builder/REFERENCE/deck-logic.md`
- Deck design · use×tone tracks · image-count decision table: `lsb-treatment-builder/REFERENCE/presentation-rules.md`
