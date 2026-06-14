---
name: lsb-ad-planner
description: >
 LSB Production ad-planning skill. It takes the analyzed ad dataset (the JSON entries
 produced by lsb-ad-analyzer) plus the client brief, and uses a cross-category-reference
 (cross-pollination) rule set to generate fresh, plagiarism-safe ad concepts
 (concept, storyboard, cut list, copy, typography, VFX direction). Use it whenever the
 user asks things like: "plan an ad from this brief" / "이 브리프로 기획안 짜줘",
 "come up with ad concepts" / "광고 컨셉 뽑아줘", "plan it using the dataset" /
 "데이터셋 기반으로 기획해줘", "give me N candidate concepts" / "후보 컨셉 N개 만들어줘",
 or any time a client brief + dataset is handed over for planning. It follows a division of
 labor in which the AI mass-produces candidates and the human (director) judges them.
---

# lsb-ad-planner — LSB ad-planning skill

This skill takes a client brief + the dataset and produces **candidate ad concepts**.
Core philosophy: **the AI quickly mass-produces candidates that it claims are "good," and the
human (director) only judges those candidates.** So the output of this skill is NOT a "finished
plan" — it is "candidates for a human to pick from." The goal is to spend the human's time only
on judging, not on producing.

> No prior context? Read `005_skills/GLOSSARY.md` first — it defines every shared term (brief, dataset, cross-pollination, hero cut, moodboard library, etc.).

## Inputs
1. **Client brief**: brand, product, category, target, length (seconds), budget, requested tone, must-include elements.
2. **Dataset**: inside the connected **`LSB_Ad_Datas`** folder (= `<LIBRARY>`), the `entries/` + `index/` folders under **`001_ad_video_dataset/`** (= `<DATASET>`). These are the entries built by lsb-ad-analyzer.
 - The dataset is an asset that grows over time (it accumulates "layered muscle"). When there are many entries, **do NOT read them all in** — use STEP 2's index search + ranking to pick only the top N that fit (this stays constant no matter the dataset size).

## Schema / contract reference
- This skill's input/output contracts (the brief dict, the cross-pollination map, the treatment.json output, and the **analyzer→treatment field-mapping table**) live in `schema.md`.
- For the detailed entry/shots fields, see `lsb-ad-analyzer/schema.md`; for the English tokens and their Korean (KO) aliases, see `lsb-treatment-builder/REFERENCE/keyword-vocabulary.md`.

## Absolute rule — Cross-Pollination

When the client's category is X, pull reference candidates from the dataset with the following weights. (Cross-pollination = deliberately borrowing the *approach/structure* of an ad from a DISTANT category — not the same category — so the result is fresh and not plagiarized. Same category is weighted weak; distant/contrast is weighted strong.)

**★ Currently active = LOOSE test profile (_2606101300).** This is a relaxed version that allows more same-category referencing. Before real client delivery or contest submission, restoring the STRICT values listed alongside is recommended.

| Match | LOOSE (active) | STRICT (original / restore value) | Meaning |
|---|---|---|---|
| Same category (X=X) | **0.5** | 0.2 | wider referencing allowance |
| Adjacent (similar emotion/target) | **0.8** | 0.5 | |
| Distant | 1.0 | 1.0 | default source of inspiration |
| Contrast (deliberate clash) | **1.1** | 1.2 | |

**Hero cuts** (the highest-impact 1–2 cuts — the hook / key visual / the cut just before the CTA): under LOOSE, **same-category weak referencing at 0.3 is allowed** (under STRICT = 0, fully banned). Either way, the output must still pass the STEP 5 (A) plagiarism gate.

The **single source of truth for adjacent/distant/contrast judgments is `schema.md` §3 (the cross-pollination map keyed on the English `industry` token)**. Any industry not listed there defaults to 1.0 (distant), with the entry's `cross_pollination_tags` (English) as a secondary signal.

## Absolute rule — Concept quality & brand assets (lessons learned, prevents the director's anger points)

These are the spots where this skill repeatedly got criticized. Violating any of them means: do not output / rewrite.

### R1. No safe-bets — the sharpness gate (enforced in STEP 3 & 5)
"Averaging the references together" is not a concept. Each candidate concept must have all three:
- ⓐ **One ownable reframe** — a single move that twists a product truth (a *shift in viewpoint*, not a list of benefits).
- ⓑ **One sticky line** — a slogan/punchline (something that *imprints*, not something that just conveys info).
- ⓒ **A fresh-but-restrained visual device** — one hit of *a detail everyone knows but no one has shown*. No spectacle, no cliché.

**Auto-reject signals:** a "bland average" that safely blends multiple references; copy that lists benefits; accountant-style copy like "you break even / you save / amount saved"; a candidate where neither the copy nor the visual lands; or a device that uses the exact category cliché you said you'd avoid (e.g., "a number ticking down to ₩0"). → In STEP 5, self-judge whether the one-line slogan is *a reframe or just an info summary*; if it's an info summary, rewrite.

### R2. Careful interpretation of vibe words — "팝하게/힙하게/감각적/세련되게" (poppy / hip / sensual / refined)
Do not assume an abstract tone word means *a specific art style* (e.g., "팝하게" / "poppy" ≠ pop art). First split the meaning: is it "mainstream, snappy energy" or "a specific art style"? **Default interpretation = amplify the energy using the brand's own assets (color, typeface, character, tone).** If ambiguous, ask once with AskUserQuestion.

### R3. Research-and-lock brand assets first (part of STEP 0.6's proactive web research)
When you receive the brief, secure the brand assets and pin them into the plan **before** concepting: brand color (exact hex), proprietary typeface, mascot/character, tone. Confirm via web search, and attach a **"verify against the official guide" recommendation** (values may have changed due to a rebrand). Beyond assets, this also covers the product's reality, the brand tone, and competitor clichés = the whole of STEP 0.6.

### R4. Do not generate brand IP myself — user assets first
Do not fill in a real brand's **character, logo, or mascot** by *drawing* a placeholder. Instead: ⓐ ask the user for the official asset (PNG/JPG), or ⓑ confirm the appearance/source via research. If a draft mock is unavoidable, mark it "placeholder — replace with the final official asset." Request attachments **as PNG/JPG** (SVG/vector can export the wrong layers and break).

> **★ An explicit user exception takes priority (the "use-the-real-logo" override).** If the user **explicitly and repeatedly allows** something like "this is a performance test this time, so it's fine to use the real logo/wordmark," then for that session only, **prioritize the user's instruction** over GENERIC placeholders (don't slap in a GENERIC placeholder citing R4 — re-running it again is itself a known mistake). Still keep the "not an official asset / for draft use" note; if ambiguous, ask once to confirm. R5 (Korean script) is the same — even for an absolute rule, an explicit user exception takes priority for that session.

### R5. Korean copy & narration in Korean script only
All Korean — taglines, CTAs, narration, etc. — is written **in Korean (Hangul) script**. **Never romanize the pronunciation** (e.g., "baedalbi" is forbidden).

### R6. Don't assert capabilities — verify the model/tool first
Before declaring "that model/feature doesn't exist," **query the full list and verify** (don't decide based on one failed search). If a skill or the user specifies a particular model (e.g., GPT Image 2), first confirm it actually exists and prefer using it. Also confirm a model's capability (e.g., whether it generates audio) against actual parameters/responses before speaking.

### R7. Multi-character & multi-location starts with the roster
If the video has two or more people, or the locations cross-cut (cross-cutting montage), define `character_pool[]` (who is in which cut) and `narrative_structure` *before* you build the cut list. Otherwise it collapses into "the protagonist does every cut" — that was the cause of the multi-character mixup, where the protagonist walked into the cafe and paid in person, the *exact opposite* of the treatment, because each cut hadn't locked WHO appears in it. Pin the person per cut with `subject_identity`, and give any clearly-visible person their own master sheet (`requires_character_sheets`).

### R8. Spell out each deliverable's downstream use in one line (the redesign-gap lesson)
Before making each deliverable (product sheet, key visual, cut, copy), **state in one line "how this will be used in the next step."** Skip it and you pin in the wrong thing (e.g., one past job baked spec text onto the product reference sheet so it couldn't be used as an i2v reference; another baked the main copy of a Korean ad in English).
- **A product reference sheet = a *pure visual* with no text, no dimensions, no spec table** (because it's used as the video i2v reference). Specs go in the plan text only, never baked into the image.
- **On-screen main copy = Korean (R5).** English only for proper nouns / logos / brand wordmarks. Don't rationalize it as "an English campaign copy."

### R9. Confirm before expensive steps · do not pre-announce a tool call (common execution discipline)
- **Before an expensive step (image/video generation, PDF build), get confirmation on aspect ratio, tone, and the key specs** (don't decide by inference — ask the aspect ratio explicitly, don't assume). Stopping at a cheap decision point is cheaper than redoing 14 cuts.
- **If you're going to call a tool, just call it — no pre-announcement text like "now I'll do ~."** (Announcing without the execution following is the seed of a loop — this is the tool-call-loop / no-announce-text lesson.) For long waits, don't poll in short slices; wait once in a long block (for video renders, follow video-crafter STEP 6's wait protocol).

### R10. Prevent the "double" (jump cut) — the cut-grammar gate (★ enforced when writing the cut list)

A "double" = two adjacent cuts of the same subject where **both the size AND the angle barely change**, so instead of looking like a new viewpoint it looks like the same picture slightly offset and shown twice (Korean set slang; the textbook name = jump cut / a violation of the 30-degree rule). A cut is a declaration of "new viewpoint / new information." If the change is ambiguous, the viewer reads it not as a new viewpoint but as *the camera teleporting by mistake*. **Once you've cut, it must be obvious at a glance that the viewpoint has clearly changed — a cut boundary with no justification is not a cut.**

**Shot-scale ladder (7 steps):** `ECU → CU → MCU(bust) → MS → MLS → FS/LS → ELS`. The `framing` value counts steps on this ladder.

**Adjacent-cut validity condition — for the same subject in the same space, at least one must hold:**
1. **Shot size jumps 2+ steps** — CU→MS ○ / CU→MCU ✗ (one step is a double).
2. **Camera angle changes 30°+** — `camera_angle`/`camera_facing` is a clearly different value (front→side, eye-level→low, etc.).
3. **Subject / space / time change** — `subject_identity` swap, location jump, time jump. (Inserts, reactions, and scene changes automatically satisfy this condition.)

**If none of the three hold, that boundary may NOT be a hard cut — handle it one of two ways:**
- **Seamless transition (default):** connect the two cuts into one flow and express the distance/angle change with an in-cut camera move — set `transition_in/out` to a seamless-family value like `push_in` · `pull_out` · `dolly_through` · `morph` · `match_action`. (When the change is small but you want to change the frame = the situation calls for a *move*, not a cut.)
- **Merge the cuts:** if the information overlaps, merge into one cut and sum the durations.

**Exceptions (intentional devices that are allowed):** ⓐ **punch-in / axial cut** — same angle, size jumps **2+ steps** (a one-step punch-in is just a double); ⓑ **match cut (match_action)** — the action linkage masks the change; ⓒ **deliberate jump-cut staging** (time-lapse montage, etc.) — only if `notes` explicitly says "intentional jump cut."

Where it applies: STEP 4 (B) cut-list writing checks every adjacent pair + STEP 5 (A-3) self-check. The builder also re-verifies with the same criteria in its Phase 1.1-b (double defense).

## Workflow

### STEP 0.0 — Resolve the dataset (immediately at session start, cross-platform)

When the planner triggers, **first of all** resolve the dataset folder at runtime. Never hardcode the path (mac `/Users/...`, win `C:\Users\...` — both).

1. `<LIBRARY>` = the folder that **directly contains `001_ad_video_dataset/`** (resolve by structure, not by name): check the connected folder; if `001_ad_video_dataset/` isn't there, drop into a `library/` subfolder and use that. (Works for `LSB_AD_ENGINE/library`, a repo with `001…` at root, or a repo with a `library/` wrapper.) **`<DATASET>` = `<LIBRARY>/001_ad_video_dataset`** (containing `entries/` · `index/` · `dataset_view.md`). Other library resources: copy bank `<LIBRARY>/002_ad_copy_bank/`, reference decks `<LIBRARY>/003_reference_decks/`, moodboard `<LIBRARY>/004_moodboard_library/`.
2. If absent, request the folder with `mcp__cowork__request_cowork_directory`. If the folder is empty, seed it by copying the analyzer's `dataset_template/`.
3. Thereafter, `entries/` · `index/` are relative paths based on `<DATASET>`. Detailed contract: `schema.md` §0.

### STEP 0 — First exchange: brief-collection form (AskUserQuestion interactive)

**So the user doesn't have to write out a long brief as free text every time — collect the essentials quickly in *form* style.** Use Cowork's `AskUserQuestion`.

**0.1 First question batch (5 at once):** brand / product & service category / tone & mood (multiple) / medium & length / whether a visual reference is attached.
**0.2 Second batch (3):** target (multiple) / must-include elements / must-avoid elements.

> **★ Aspect ratio must be an explicit question (ask it explicitly, don't assume).** Don't decide by inference like "it's short-form so 9:16." Put the **aspect ratio (9:16 / 16:9 / 1:1) as a separate option** in the medium & length question and collect it. **Confirm it before** any expensive image/video generation (prevents the mistake of building 14 cuts then scrapping them). Pin `aspect_ratio` into the plan.
> **★ product_spec_lock (lock the product's fixed spec).** For a campaign that shows a real product, define the product's *invariant form spec* (grid count, ratio, embossing, material — e.g. "exactly 3 rows × 4 cols = 12 blocks, embossed 'HERSHEY'S', portrait ratio") once in the plan (`product_spec_lock`), and **insert it verbatim into every image prompt** (the builder copies it in as-is). If you don't, the model arbitrarily mutates it (e.g. into 4×4) — that was a known incident.

(Show the question options in Korean, but normalize the responses to English tokens in 0.3 below.)

**0.3 Responses → assemble the brief dict (values are English tokens):**

```python
brief = {
 "brand": "<response>", # proper noun OK
 "product": "<response>",
 "industry": "<English token>", # e.g.: "finance"
 "product_category": ["<English token>"],
 "tone": ["<English token>"], # e.g.: ["punchy_humor","friendly"]
 "media_format": "<English token>", # e.g.: "shortform_landscape_30s"
 "target_demo": ["<English token>"], # e.g.: ["mz","early_career"]
 "must_include": "<response>",
 "must_avoid": "<response>",
 "visual_ref_attached": True/False,
 "raw_text": "<free text (Korean allowed)>"
}
```

**0.4 Ask follow-ups for missing info:** up to 2–3 rounds. Beyond that, take it as free text.

**0.45 Brief internal-contradiction check (LSB-014 family — catch conflicts before producing).** Before
locking the brief, scan it for self-contradictions and **ask one confirming question** for each found:
- aspect ratio vs format wording (e.g. "16:9 / landscape" but also "short-form / Reels / 세로") — which one?
- length vs cut/pacing implications (e.g. "15s" but a cut list that needs 30s; "30초" with "빠른 다컷 20컷+").
- medium vs deliverable (e.g. "OOH/print" but "narration/VO"; "TVC" but "9:16 SNS").
- must-include vs must-avoid clashes (e.g. "use the real logo" + "no brand IP").
Do not silently pick one side — surface the conflict and confirm. (This prevents the "16:9 brief came out
all 9:16" class of failure downstream.)

### STEP 0.5 — Visual reference analysis (optional)

Proceed if question 5 was "yes" + an image is attached. Extract only the *visual signature* (an abstraction level that captures the look without copying pixels — never pixel-copy): color_palette / color_mood / lighting / composition / subject_type / subject_pose / texture_fx / tone_keywords / anti_referenced. Use it only as *inspiration* for the downstream concept, never quote it directly into the cut list. Confirm the extraction result with the user.

> **★ Read the *physical basis of the mood*, not just surface tokens (prevents swinging between extremes).** Do not understand a reference (or a dataset entry) by its **result labels (technique/vfx) alone** — like "film UI, kinetic typo, magazine." Read *why* the look reads that way — its physical basis — and pin that into the look direction:
> - `color_analysis` (exact palette_hex, saturation_strategy, contrast_type) · `lighting` (key_direction / hardness / key_to_fill_ratio / color_temp / overall_contrast) · `texture` · `style_prompt`.
> - **Quote the adjectives of `style_prompt` verbatim**: "clean digital with **light** film-grain" / "warm low-key" / "desaturated with pop". **Do not turn "light grain" into "heavy sepia," or "warm" into "dark low-key"** (that was the cause of the three-way extreme swing — heavy sepia ↔ darkness ↔ brightness).
> - Even when a dataset entry exists, **confirm the tone with one moodboard image with the user** (matching tone with words alone misses twice).

### STEP 0.55 — Moodboard library grounding (★ reflect the director's Pinterest taste)

Load the director's taste moodboard **exactly like** the dataset (001) and copy bank (002) — i.e., treat it as a dataset you load. Path & loading method: `lsb-treatment-builder/REFERENCE/moodboard-library.md`. `<MOODBOARD> = <LIBRARY>/004_moodboard_library/` (with `_분석/manifest.json` · `index_map.json` · 9 buckets). If absent, skip it and state so in the output (do not invent a taste arbitrarily).

Pick 1–2 buckets that fit the brief's tone (e.g., a typography-led concept → `01_타이포_CJK포스터` / `02_타이포_영문포스터`; a film mood → `05_필름그레인_인물무드`) and **cite that aesthetic as the concept's visual reference** — so the concept inherits the director's taste (typography-led editorial + film grain + collage + wit) rather than a generic default. This becomes the basis for STEP 4 global's `moodboard_refs` (bucket + representative file paths) and each cut's `photographic_treatment` (tone → presets P1–P6, see `photographic-treatment.md`) choices.

### STEP 0.6 — Proactive brand & product web research (required · includes R3)

Once the brand + product are set (STEP 0), **before generating concepts or searching the dataset (STEP 2~3)**, **web-search that brand & product first**. Do this proactively without asking permission (searching is the default behavior). If you plan without knowing, the product truth (`brand_right`) and differentiators stay empty and the concept floats untethered. The user usually just throws "an ad for some brand's some product," so take that one line and research it immediately.

**What to find:**
- **The product/service reality** — exactly what it is, the core features/benefits/price/differentiators (= the things you can sell). Numbers, benefits, and prices can change → add a `fact_check_flag` + verify the terms at execution time.
- **The brand** — positioning, brand DNA, tone, existing ads/campaigns, slogan, key messages (the "on-brand" tone).
- **Brand assets (R3)** — color (exact hex), proprietary typeface, logo, mascot/character. Recommend verifying against the official guide (rebrand drift).
- **Market / competitors / clichés** — competitors, category conventions (clichés to avoid) → reinforce `must_avoid`.
- **Recency** — currently-running campaigns, new products, events. These may be after the knowledge cutoff, so **be sure to search**.

**Handling the results:** merge into the brief dict — `product_facts` (benefits, features, price + sources) / `brand_assets` (color hex, font, character) / `brand_voice` (tone, slogan DNA) / `category_cliches` → `must_avoid`. Record sources. This result becomes the **basis for `brand_right` · `insight`** in STEP 3's `strategy_spine`.

**Principles:** search results are only *grounds/inspiration*. Don't take a competitor's or an existing slogan and just swap words (plagiarism · R1). Brand IP (character, logo) must not be generated — use user assets (R4). Korean copy & narration in Korean script (R5). Don't assert model/tool capability before verifying (R6).

### STEP 1 — Normalize the brief (Korean → English tokens)

Tokenize STEP 0's dict to English tokens via the KO-alias table in `keyword-vocabulary.md`.

- "20대 사회 초년생" → `target_demo = ["late20s_early30s", "early_career"]`
- "재밌고 가볍게" → `tone = ["punchy_humor", "friendly"]`
- "기존 시중은행 광고 같지 않게" → `must_avoid = "bank_cliche"`

If a term isn't in the alias table, use the closest token; if it's genuinely new, add it to the table. **Because the index is in English, the brief must be matched to English tokens to hit.**

### STEP 2 — Reference selection = direct index search + ranking (cross-pollination)

The dataset is an accumulating asset, so **don't read it whole.** From the index files (`<DATASET>/index/by_*.json`), pull candidates by keyword match, apply weights, and fetch only the top N. This works identically whether there are 2 entries or 300 (constant regardless of scale).

**Do not import index_helper.** The index is plain JSON, so the planner reads it directly with `json.load` (removing the coupling). Only index *writing* is the analyzer's index_helper's job.

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

def load_entry(eid, DATASET):
 return json.load(open(os.path.join(DATASET,"entries","%s.json"%eid), encoding="utf-8"))

def retrieve_references(brief, shot_type, DATASET, n=5):
 hits = search(DATASET, industry=brief["industry"], product_category=brief["product_category"],
 target_demo=brief["target_demo"], tone=brief["tone"],
 technique=brief.get("technique",[])) # add axes as needed
 ranked = []
 for eid, idx_score, hits_detail in hits:
 e = load_entry(eid, DATASET)
 cat = (e.get("search_keywords",{}).get("industry") or [None])[0] # English token
 # ★ LOOSE test profile active (STRICT restore values: hero_cut same=0 / same 0.2 / adjacent 0.5 / contrast 1.2)
 if shot_type == "wow_cut" and cat == brief["industry"]:
 weight = 0.3 # LOOSE: weak referencing allowed (STRICT: 0 HARD BAN)
 elif cat == brief["industry"]:
 weight = 0.5 # LOOSE (STRICT: 0.2)
 elif cat in adjacent_to(brief["industry"]): # schema.md §3 map
 weight = 0.8 # LOOSE (STRICT: 0.5)
 elif cat in contrast_to(brief["industry"]):
 weight = 1.1 # LOOSE (STRICT: 1.2)
 else:
 weight = 1.0
 brief_match = semantic_match(e.get("inferred_brief",""), brief["raw_text"])
 final = idx_score * weight * (0.7 + 0.3*brief_match)
 ranked.append((eid, final, hits_detail, weight))
 ranked.sort(key=lambda x:-x[1])
 return ranked[:n]
```

(Note: `shot_type == "wow_cut"` is the internal token for a hero cut.)

**Strengths of index search (English-token normalization):**
- Brief "MZ early-career, punchy humor" → normalized `target_demo=["mz","early_career"]`, `tone=["punchy_humor"]`.
- lookup: `by_target_demo.json["mz"]` + `by_tone.json["punchy_humor"]` → ADV-2026-001 (score 2).
- weight: brief industry=finance, entry=finance → 0.2 (a reference, since it's not a HARD BAN). final 2×0.2=0.4.
- Even if the user only wrote "20대 (twenties)," normalization maps it to the standard token → the same hit. **Robust to keyword variation.**

- **State what you picked and why** (e.g.: "fintech brief, but I pulled the cut rhythm from a streetwear ad — contrast 1.2, score 0.9").
- The bigger the dataset, the higher the chance of getting a well-fitting distant/contrast card (dataset = muscle).
- (Infrastructure: at larger scale, move to a Postgres + pgvector RAG. For now it's direct index reading — keep the "pick and fetch," not "read everything," behavior.)

### STEP 2.5 — Using the data

**Production/global fields:** pull production_signature · global_layout · typo_motion · audio in as cross-pollination targets to propose new staging. Reference the rhythm/refrain structure of the narration copy, but don't take the original and just swap words.

**Inference fields (analyzer STEP 5.5):**
- `inferred_creative_thinking` (7 steps) — read directly *how* the reference was derived (a stronger retrieval signal than one that only has the result).
- `search_keywords` (10 axes, English) — direct brief matching.
- `inferred_brief` — semantic match of the brief vs. the entry's inferred brief.
- `cross_pollination_tags` (English adjacent/distant/contrast) — the entry's own labels. Secondary to the weight.
- `concept_derivation_pattern` (English) — the classification name of the thinking method.

**Visual fields:** use the reference entry's `visible_elements · texture · lighting · color_analysis · style_prompt` and `recreation_prompts` (t2i/i2v) as visual-tone *inspiration* (no pixel cloning). Carry these through to the builder (STEP 4 B).

**confidence:** if `inferred`, use it knowing it's an estimate (no direct quoting, inspiration only). If `human_verified`, trust it more.

**Thinking-method catalog (`lsb-treatment-builder/REFERENCE/keyword-vocabulary.md`):** use the 12-method catalog as a seed when the dataset is thin / for reinforcement. Once 50+ entries accumulate, prefer cross-pollination.

### STEP 3 — Generate 5 candidate concepts (A~E)

Five **qualitatively different** concepts (A · B · C · D · E). For each concept, output *all* of:

**(A)** One-line concept + creative_device + concept_derivation_pattern (English token — match one of the handbook's 12, or new).
**(B) 7-step cognition path + the strategic spine of the plan (required)**
- `client_perception_path` (emotional path): insight / persona / moment / product_role / punchline / differentiator / brand_fit_one_liner.
- `strategy_spine` (the business argument — the *source* of the builder's STRATEGY section): `brief` (the challenge) / `insight` (+ `evidence[]`: grounds from observation, data, news, target's own words) / `strategy` (the one move) / `concept_rationale` (*how* this concept was derived from the insight — no jumps) / `brand_right` (why it must be this brand = product truth) / `payoff` (expected effect / evaluation criteria, reverse-engineered). The spine & mapping framework: `lsb-treatment-builder/REFERENCE/deck-logic.md` §1.
- **The concept (one-line concept · creative_device) must be derived from `strategy_spine.insight`** — if there's a concept before any insight, rewrite. Don't just pin the one-liner; attach the evidence and the derivation logic.
- If the brief (challenge) · payoff (evaluation criteria / KPI / contest scoring weights) aren't in the user's input, get them via STEP 0.4 follow-up questions.
- If either of these two (the cognition path + strategy_spine) is empty, outputting the concept is *forbidden* (the builder must receive it to render STRATEGY).
**(C)** narrative_arc (an abstraction level that captures the principle — don't copy the structure, only the principle) + **`narrative_structure`** (a narrative-structure enum: `linear_continuous` continuous movement in one space / `cross_cutting_montage` cross-cutting same time / different space / `parallel_narrative` two people in parallel / `nested_flashback` time jump) + tone/mood keywords + pacing_curve + music_tempo_curve.
**(C-2) The character roster `character_pool[]` (required if 2+ people or cross-cutting):** define the people *before* you build cuts. Each item = `id` (free string, e.g. `protagonist_main` · `cafe_customer_A` · `cafe_barista`; for crowds use the reserved value `background_crowd`, for cuts with no person use `none_environment`) · `description` (one line) · `appears_in_cuts[]`. **If this is empty, a multi-character video collapses into "the protagonist does every cut"** (the multi-character mixup: the protagonist enters the cafe and pays — the opposite of the treatment). E.g.: `{"id":"protagonist_main","description":"the protagonist at the crosswalk","appears_in_cuts":[1,2,5,6,8,9,10,11,12]}`, `{"id":"cafe_customer_A","description":"a different customer paying at the cafe","appears_in_cuts":[3,7]}`.
**(D)** The 6 director keywords (optional) — 6 short phrases each ending in a period.
**(E)** Copy seeds — tagline · CTA · key lines + match to the handbook's 12 copy patterns.
- **Copy cross-pollination (copy_bank · ★ a mechanical procedure — don't skip):** before writing the copy seeds, read `<LIBRARY>/002_ad_copy_bank/` (COPYPEDIA: 4,039 real copy lines · 2023-07~2026-01) **with code**. **Join contract:** `index_by_industry.json` = `{industry(English token): [array of integer indices]}` — those integers are **positions `entries[i]`** in `copy_bank.json` (each item: `industry` · `category_kr` · `brand` · `copy` Korean original · `date`). The file is ~1MB, so **do NOT Read it whole** — pick via the index and extract with code only, like this:

```python
import json, os, random
CB = os.path.join(LIBRARY, "002_ad_copy_bank")
idx = json.load(open(os.path.join(CB, "index_by_industry.json"), encoding="utf-8"))
entries = json.load(open(os.path.join(CB, "copy_bank.json"), encoding="utf-8"))["entries"]
# pick 2-3 deliberately-far industries by weight (same 0.2 / adjacent 0.5 / distant 1.0 / contrast 1.2 — schema.md §3 map)
far = ["fashion", "public_gov"]  # e.g. when brief industry=finance
picks = [(i, entries[i]) for ind in far for i in random.sample(idx[ind], k=min(15, len(idx[ind])))]
```

 Sample only 10–20 lines per industry × 2–3 industries, borrow only the *approach/structure (device)*, and **vary it into new copy**. The industry-selection weights use the same profile as the entries (currently LOOSE: same 0.5 / adjacent 0.8 / distant 1.0 / contrast 1.1 · STRICT restore values 0.2/0.5/1.0/1.2). For hero-cut copy, same-category weak referencing (0.3) is allowed under LOOSE (hard-banned under STRICT). ⚠ **No verbatim reuse / no word-swapping of the original** — copy_bank is *inspiration*, not a copy-paste source. **Recording duty:** attach to each copy seed `copy_refs[]` = `[{bank_index, industry, brand, device_borrowed}]` and leave a one-line "original device → new copy" variation log (checked in STEP 5 (B)). The chosen seeds must pass the STEP 5 (A) plagiarism-similarity gate. **Omission is only when the copy-bank folder is absent** — if omitted, state the fact and the reason in the output.
**(F)** Tracing — name the reference entry IDs + the borrowed fields/signatures (e.g.: "borrowed *only the shape* of the balloon typo from ADV-2026-001#shot5; copy written fresh").

**Spreading them apart:** deliberate separation across the tone axis / the mechanism axis (celebrity, personification, metaphor) / the thinking-method axis / the medium axis / the narrative-structure axis — the 5 must not cluster on the same axis. Variations on one idea have no value.

**Handling a regeneration request:** if the user picks "I don't like any of them — give me new candidates," produce **5 new ones qualitatively different from the previous round's 5** (no reheating the same thinking method or mechanism; swap out the cross-pollination sources too). Infer in one line what the user effectively rejected last round, and reflect it in the new round's spreading axis. No limit on the number of rounds.

**(G) Sharpness gate (R1 required):** confirm each concept has ⓐ an ownable reframe ⓑ a sticky line ⓒ a restrained, fresh visual device. If it's "averaging references," benefit-listing, accountant copy, or a category-cliché device, outputting the concept is *forbidden* — rewrite.

**(H) Instantly-readable-in-one-scene gate (Q7):** can each concept be described as *one shootable/renderable scene where the product is the protagonist*? **A pure metaphor that only makes sense once you add an explanation** (e.g. a virtual human = only a personification of water) does NOT pass. ※ The bold/abstract *device itself* from cross-pollination is allowed — the point isn't "no abstraction," it's *whether that device has been translated into product-as-protagonist + one scene*. If it can't be translated, replace it with a concrete scene.

**(I) Brief cut composition — required per candidate (★ don't just throw a concept):** each candidate must show *how that concept actually flows as a real video* so it can be picked. Attach a **brief cut list** to each candidate — the cut count follows STEP 4's length bands (15s: 8–11 / 30s: 14–21 …), each cut with 4 fields: `cutNumber` · `duration` (e.g. "0-3s") · `scene` (one line — who, where, doing what) · `caption` (on-screen subtitle/copy, "" if none) · `voiceover` (**the V.O / Na Korean line** — what's heard in that cut, "" if none). Korean in Hangul (R5). Apply the R10 double gate to the brief cut list too (the change between adjacent cuts). Do not include image prompts or internal tokens (the detailed 30+ fields come in STEP 4 of the chosen one). This brief cut list goes straight out to the outside (as `script_options`' `cuts[]`).

### STEP 4 — Detail the chosen one (aligned 1:1 with the treatment-builder input schema)

STEP 4's output is the *complete input* the builder runs on directly. **The analyzer→treatment key conversion follows `schema.md` §5's mapping table** (e.g. total_duration→total_duration_sec, typography→typography_global, vfx→vfx_global, inferred_creative_thinking→client_perception_path).

Aligned 1:1 with the builder input schema (`lsb-treatment-builder/scripts/cut_template.json` + `treatment_global_template.json`).

**(A) Global meta (same keys as treatment_global_template):** brand · product · target_demo / total_duration_sec · shot_count · fps · aspect_ratio · hook_position_sec · cta_position_sec / narrative_arc · pacing_curve · music_tempo_curve · wow_cut_index[] · creative_device / production_signature.* / global_layout.* / recurring_motifs[] / typography_global.* / vfx_global.* / copywriting.* / **client_perception_path (7-step emotion, exactly as STEP 3 B)** / **strategy_spine (the 6 plan-logic fields brief · insight + evidence · strategy · concept_rationale · brand_right · payoff, exactly as STEP 3 B — the builder renders it as the STRATEGY section)** / **narrative_structure (STEP 3 (C))** / **character_pool[] (exactly as STEP 3 (C-2) if 2+ people or cross-cutting)** / audio_intent.bgm/narration.

**(B) Full per-cut fields (same keys as cut_template.json):**
- Identification: index, no, duration, framing, function
- Person & action: **subject_identity** (the person in this cut = an id from character_pool, or background_crowd/none_environment — required for multi-character), subject_position, subject_action, subject_motion, pose_description, gaze, eye_contact_effect
- Camera: camera_motion, camera_motion_intensity, camera_angle, camera_facing, shot_scope, camera_effect_local, motion_blur
- Composition: `composition` (1–2 of the 7 composition laws for this cut — `rule_of_thirds`/`golden_ratio`/`leading_lines`/`framing`/`symmetry`/`depth`/`fg_mg_bg`) + `eye_path` (the intended order, e.g. headline → key visual → evidence → CTA). Don't center the subject by default. This feeds `comp_bias` in image generation. Reference: `lsb-treatment-builder/REFERENCE/composition-principles.md`.
- Rhythm & transitions: intra_cut_rhythm, transition_in, transition_out
- Props & set: props[], prop_motion, prop_semantics
- Color: color_mood, color_palette[], color_intent
- Typography & subtitles: copy_overlay, layout_grid, subject_typo_layout, typo_motion, typo_color_strategy
- VFX: vfx_in_shot[], vfx_intensity_local, vfx_in_board_prompts
- Audio: audio_intent.sfx / narration_line / bgm_change / silence
- Visual inventory: visible_elements, texture, lighting, color_analysis, style_prompt
- Frame recreation: **recreation_prompts** (t2i_start_frame · t2i_negative · i2v_motion · i2v_params · fidelity_note)
- Meta: wow_cut, fact_check_flag, notes, source_refs[]

> Pull the visual inventory & recreation_prompts from the reference entry's same fields as *inspiration* and write them fresh for the new cut. **Preserve subtitle/copy originals**; only *celebrity face photo-clones* and real *logo marks* go generic (likeness / trademark). No pixel cloning.

**(C) Transition inventory (transition_template.json):** no, from_cut, to_cut, type, direction, **`direction_observer_view`** (state *both* the camera rotation as seen from above AND the resulting on-screen streak direction: if the camera goes left→right, the world streaks right→left. Prevents the whip-pan direction confusion seen in the multi-character mixup job), duration_sec, **single_canvas auto-determination** (true if whip_pan/morph/match_action/push_in/pull_out/360_spin/dolly_through), motion_blur_intensity, lighting_morph, narrative_role, audio_note. **If cross-cutting (`cross_cutting_montage`), state that the transition is a *spatial jump*** (not continuous movement).

**(D) Copy draft:** reference the *feel* of the dataset copy but don't take the original and just swap words (plagiarism). Use cross-pollination to pull in another category's expression and write fresh. State the match to the handbook's 12 copy patterns.

**Length & cut count = decided by tone/genre pacing (Q5 · no blanket numbers).** A dynamic/punchy tone = fast multi-cut at 1–3s; luxury/emotional = a few long cuts. Recommended bands by length: 15s 8–11 cuts / 30s 14–21 cuts / 45s 21–55 cuts / 60s has room. Adjacent cuts must differ in screen size / action / location, and repeating the same action should be minimized. **Apply the R10 cut-grammar gate to every adjacent pair** — for the same subject/space, satisfy one of ① 2+ size steps ② 30°+ angle ③ subject/space/time change; otherwise no hard cut (seamless transition or merge — R10). (Per-campaign learning is separate from general rules — e.g. "drink once" is a session memo for that job, not a universal rule.) Self-verify that length & aspect ratio fit the brief's spec (medium).

### STEP 5 — Self-check (required before output)

**(A) Plagiarism self-check:** visual/narrative similarity, narrative_arc, copy structure, typography pattern, VFX signature, direct creative_device matches.
- **★ Currently active thresholds = LOOSE test profile (_2606101300):** **<0.80 pass** / 0.80~0.90 warn (state the similar source and leave it to the user's judgment) / **>0.90 block** / same category **>0.85 block**. If a hero cut resembles the same category, warn + state the source (no auto-regeneration).
- (STRICT original / restore values: <0.50 pass / 0.50~0.65 warn / 0.65~0.80 regeneration recommended / >0.80 block / same category >0.60 block / hero cut resembling same category = always regenerate.)
- Invariant rules regardless of profile: **no verbatim cloning / no word-swapping**, preserve copy/subtitle originals, treat celebrity faces & real logos generic (likeness / trademark).

**(A-2) Sharpness self-check (R1):** is the one-line slogan *a reframe or an info summary* / is the visual device *a cliché ("number ticking to ₩0" type) or fresh* / do the copy and visual actually land? If any of the three is weak, rewrite before output. (A "bland average" is not a pass.)

**(A-3) Double (jump-cut) self-check (R10):** sweep **every adjacent pair** of the cut list; if it's the same subject/space and ① shot size under 2 steps ② angle change under 30° ③ same subject/space/time — all three true = **double violation**. Fix by changing `transition_in/out` to a seamless-family value or merging the cuts, then re-check (exceptions are R10 ⓐⓑⓒ — only intentional jump cuts with a notes annotation pass). If a violation remains, outputting is forbidden.

**(B) Schema completeness:** the 7-step cognition path (7 items) + **strategy_spine 6 fields (brief · insight + evidence · strategy · concept_rationale · brand_right · payoff)** / global required (brand · product · target_demo · total_duration_sec · aspect_ratio · narrative_arc · pacing_curve) / cut required (index · no · duration · framing · function · intra_cut_rhythm · transition_in/out) / copy_overlay · layout_grid · typo_motion on subtitle cuts / vfx_in_shot · vfx_intensity_local · vfx_in_board_prompts on VFX cuts / single_canvas marked on transitions / **if multi-character or cross-cutting, character_pool[] · narrative_structure · each cut's subject_identity are required** / **if the copy bank (`002_ad_copy_bank`) is connected, `copy_refs[]` is required on copy seeds** (STEP 3 (E) — without a stated reason, no-reference = no pass) / **in 5-candidate mode, each candidate includes the (I) brief cut list** (cut-count band · 4 fields · V.O/NA lines). If anything is missing, outputting is *forbidden*.

**(C) Logic gate (`lsb-treatment-builder/REFERENCE/deck-logic.md` §3):** does the strategy_spine (1) answer "why this ad" in one sentence even with 0 cuts (2) derive the concept from the insight (3) break down if you swap the brand for a competitor (justification) (4) touch logic to each evaluation criterion (5) connect beats with "so / that is" — if it fails, reinforce then re-output.

### STEP 6 — Output + hit-rate recording slot

**(A) Two modes:** ① 5-candidate mode (A~E markdown — each with the STEP 3 (I) brief cut list; picking one → STEP 4 / a "none of these" option can regenerate a new 5). ② single-detailed mode (markdown + JSON together).
**(B) treatment-builder input format:**
```json
{ "global": { /* treatment_global_template */ }, "cuts": [ /* cut_template array */ ], "transitions": [ /* transition_template array */ ] }
```
This JSON is the builder's Phase 0 input as-is. To pass, the user must be able to trigger the builder *without edits*.
**(B-2) Character-sheet-needed flag `requires_character_sheets[]`:** for each person in character_pool who *appears clearly on screen*, `{id, priority(critical/high), exists_in_session(bool)}`. The builder first generates the master sheet for any person with `exists_in_session:false` and uses it as the reference for that person's cuts. Crowds/extras (`background_crowd`) don't need a sheet.
**(C) Hit-rate recording slot:** "# of candidates generated / # passed / hit rate" (filled by the human).
**(D) Tracking meta:** source_refs[] + copy_refs[] (copy-bank sources, STEP 3 (E)) + the matched thinking method & copy pattern + the human's judgment result, recording recommended.

## What the human (director) does — the AI must not encroach
- The final concept selection (aesthetic judgment) is the human's. The sense-of-the-times judgment is also the human's.
- The AI only gives candidates fast, plentiful, and plagiarism-safe — it does not pick.

## Don't
- Don't output dataset copy with only words swapped (invariant regardless of profile). For hero cuts, same-category weak referencing (0.3) is only allowed under the current LOOSE profile — must pass the plagiarism gate.
- Don't declare it "finished" — the output is candidates for a human to judge.
- If the dataset is empty, tell the user that entries must first be accumulated with lsb-ad-analyzer.
- The brief normalization & index keys are **English tokens** (via the KO-alias table). No Korean lookups.
- **(R1)** Don't produce bland candidates by averaging references, listing benefits, or accountant copy — if there's no reframe, no sticky line, no fresh device, rewrite.
- **(R2)** Don't assume an abstract tone word like "팝하게 (poppy)" means a specific art style — confirm the meaning, then interpret via the brand assets.
- **(R4)** Don't generate a real brand's character/logo/mascot as a placeholder — request user assets (PNG/JPG) / research.
- **(R5)** Don't romanize Korean (Hangul only).
- **(R6)** Don't declare a model/feature "doesn't exist / can't be done" — verify against the full list / actual responses before speaking, and confirm a specified model (GPT Image 2, etc.) first.
- **(R10)** Don't hard-cut adjacent cuts of the same subject/space with a 1-step size change or under-30° angle — that's a double (jump cut). If the change is insufficient, it's not a cut but a seamless transition or a merge.

---
## Thinking-method catalog — usage guide
See `lsb-treatment-builder/REFERENCE/keyword-vocabulary.md`: 11 categories / 12 thinking methods / 12 copy / the 6 director keywords / product×visual code mapping / Runway / traces of advertiser negotiation / 8 special patterns / page structure.
Reference it directly: ① a seed when the dataset is thin (<10) ② category decision ③ concept derivation ④ copy ⑤ traces of advertiser negotiation. With 50+ entries, prefer cross-pollination.

---
## Why STEP 0's form is the first step (UX)
Users dislike writing a long free-text brief right when the session opens. A form takes the essentials in 5 seconds, with free text optional. It compresses a 5-minute back-and-forth into 1 minute. The user's time = value.

---
*Version: lsb-ad-planner_260614_v11 · 2026-06-14 KST. (version scheme = YYMMDD_vN; earlier inline _2606xxxx codes are legacy timestamps. v11 = STEP 0.45 **brief internal-contradiction check** (aspect vs format, length vs cuts, medium vs deliverable, must-include vs must-avoid → confirm before producing; LSB-014 family / prevents the "16:9 brief came out 9:16" class). _2606140100 = added a per-cut `composition` + `eye_path` field (1–2 of the 7 composition laws — rule-of-thirds/golden-ratio/leading-lines/framing/symmetry/depth/fg-mg-bg; feeds image-gen comp_bias; no center-by-default). Ref: lsb-treatment-builder/REFERENCE/composition-principles.md. _2606140000 = English rewrite + de-jargon. Prior _2606101300 = **LOOSE test profile active** — plagiarism gate <0.80 pass / >0.90 block / same category >0.85 block · hero-cut resemblance downgraded to a warning, cross-pollination weights same 0.5 / adjacent 0.8 / distant 1.0 / contrast 1.1 · hero-cut same 0.3 weak referencing. STRICT restore values noted in-file (<0.50 pass · >0.80 block · same >0.60 block / 0.2 · 0.5 · 1.0 · 1.2 · hero hard-ban 0). No-verbatim / preserve-original / generic-treatment are invariant regardless of profile.) Prior _2606101200 = **the 5-candidate system + mandatory brief cut composition** — STEP 3 candidates 3→5 (A~E) · 5 spreading axes · regeneration-request handling (qualitatively separate from the prior round), STEP 3 (I) a brief cut list per candidate (cut-count band · cutNumber/duration/scene/caption/voiceover V.O·NA Korean lines) required — wired straight to script_options cuts[], linked to STEP 5 (B) · STEP 6 (A).) Prior _2606101100 = **STEP 3 (E) copy_bank actually-wired fix** — the problem where it was referenced by name only with no join contract, so it was never actually read: the `index_by_industry.json`{industry: [int index]} → `copy_bank.json` `entries[i]` join contract + extraction code spelled out (no whole-1MB Read · sample 2–3 far industries × 10–20 lines), the copy-seed `copy_refs[]` recording duty + STEP 5 (B) check & STEP 6 (D) tracking link, omission only when the copy bank is absent (state the reason). schema.md §0 copy-bank contract added. _2606101000 = **R10 the double (jump-cut) prevention cut-grammar gate** — the 7-step shot-scale ladder (ECU→CU→MCU→MS→MLS→FS/LS→ELS), the adjacent-cut validity condition for the same subject/space (2+ size steps / 30°+ angle / subject·space·time change — one of), no hard cut if unmet → seamless transition or merge, exceptions (2+ step punch-in · match cut · intentional jump cut with notes) + STEP 4 adjacent-pair check + STEP 5 (A-3) self-check + builder Phase 1.1-b double defense.) Prior lsb-ad-planner_2606041500 · 2026-06-04 15:00 KST. See 적용방법.md for the change history. (_2606041500 = **post-mortem of the redesign-gap session reflected**: STEP 0.1 explicit aspect-ratio question (ask it, don't assume) · product_spec_lock (lock the fixed product spec) · STEP 0.5 read the physical basis of the mood · quote style_prompt adjectives · moodboard confirmation (don't swing between extremes) · R4 explicit-user-exception takes priority (the use-the-real-logo override) · R8 each deliverable's downstream use in one line (the spec-baked-on-product-sheet / English-baked-main-copy lessons) · R9 confirm before expensive steps · no tool pre-announcement (the tool-call-loop / no-announce-text lesson) · analyzer panel_layout `layered_collage` recognized. _2606032200 = library folder reorganization — `<DATASET>`=connected folder (`<LIBRARY>`)/001_ad_video_dataset · copy_bank→`<LIBRARY>/002_ad_copy_bank`. _2606022203 = STEP 0.6 proactive brand & product web research. New _2606032044 = **multi-character & cross-cutting support (the multi-character-mixup lesson)**: R7 + STEP3 (C) narrative_structure · (C-2) character_pool[] · (H) instantly-readable-in-one-scene gate (Q7) + STEP4 global narrative_structure · character_pool · per-cut subject_identity + transition direction_observer_view + tone-based pacing (Q5, blanket cut counts dropped) + STEP6 (B-2) requires_character_sheets + STEP5 completeness check updated. _2606032130 = STEP3 (E) **copy cross-pollination** (`<LIBRARY>/002_ad_copy_bank/` COPYPEDIA 4,000+ real copy lines — preserve originals · English industry labels — vary far-category copy into fresh copy as inspiration, no verbatim · pass the plagiarism gate).) _2606140000 = English rewrite + de-jargon (faithful, no content dropped).*
