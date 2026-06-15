---
name: lsb-ad-analyzer
description: >
  LSB Production reference-ad analysis skill. Takes an ad video file (mp4),
  breaks it down cut by cut, and reads the within-cut motion, transitions, rhythm,
  layout, and typography motion, plus global capture effects (e.g. wiggle), and the
  spoken narration (via Whisper) — then structures all of it into the LSB ad-metadata
  schema (JSON + a review table). Always use this skill when the user says things like
  "analyze this ad", "build me a reference dataset", "break it down cut by cut",
  "extract the ad metadata", or attaches an ad mp4 and asks for analysis. (Korean triggers:
  "이 광고 분석해줘", "레퍼런스 데이터셋 만들어줘", "컷별로 분해해줘", "광고 메타데이터 뽑아줘".)
---

# lsb-ad-analyzer — LSB reference-ad analysis skill

Takes one ad video and turns it into **one LSB dataset entry** (a JSON file + a review table).
The goal is to structure "**HOW** a well-made ad was directed" (motion, layout, grid, typography
motion, capture effects, narration) into a form the system can reference WITHOUT a human copying it.
**We do not train on or replicate the video itself.**

> No prior context? Read `../GLOSSARY.md` first — it defines every shared term (dataset, cut, hero cut, cross-pollination, etc.).

## Core principles (absolute)

0. **Perceive, but do not judge.** Reading frames in order lets you read the time structure (cut
 rhythm, transitions, motion) as well as a human can. Record those objective labels. The aesthetic
 judgment of "is it good or bad" is the human's job.
1. **Don't just look at the image — look at the DIRECTION.** The point is not "what got filmed"
 (the subject) but **"how it was directed"**: subject (person) motion / prop motion / camera movement /
 placement on the grid / typography entrance and movement motion / layout where a person and on-screen
 text coexist / global capture effects (e.g. 3D wiggle). If this is empty, the analysis is meaningless.
2. **Never settle a motion label from a thumbnail — you MUST zoom into the individual frame.** (Lesson:
 once, looking only at a contact-sheet thumbnail, we misread something as "dance" — it was actually a
 static pose plus a typography color change.) You may use the thumbnail to tell THAT there is motion,
 but whether it is a person dancing / a typography animation / a camera wiggle **must be confirmed by
 enlarging the individual frame.**
3. **Enforce abstraction (visual).** Visual *descriptions* are Level 2–3 only. Proper nouns go only in
 source_ref/brand/product/model. (Appendix A §0)
4. **Copy: store the original text + a meta tag.** Preserve short slogans/CTA/captions verbatim. For long
 narration or legal disclaimers, keep only the key lines (excerpt_only).
5. **Never invent numbers or labels.** duration, cut count, fps, ratio come from the manifest. Leave
 fields you couldn't observe empty and flag it in analyst_notes.

## Dataset storage path (resolved at runtime — cross-platform, mac/Win)

**Do not hardcode paths.** `<LIBRARY>` is the folder that **directly contains `001_ad_video_dataset/`**
(resolve by structure: check the connected folder; if `001_ad_video_dataset/` isn't there, drop into a
`library/` subfolder and use that — one central library that accumulates over time). Each session,
resolve that folder's absolute path and use `<LIBRARY>/001_ad_video_dataset` as `<DATASET>`.

```
<LIBRARY> = the folder directly containing 001_ad_video_dataset/ (connected folder, or its library/ subfolder)
            API (console Managed Agent): connected shitbin/lsb-demo repo -> its library/
            Local (Mac Cowork): /Users/soobin/Desktop/LSB_AD_ENGINE/library
<DATASET> = <LIBRARY>/001_ad_video_dataset   (entries/, index/, dataset_view.md live inside it)
 mac example: /Users/<id>/Desktop/LSB_AD_ENGINE/library
 win example: C:\Users\<id>\Desktop\LSB_AD_ENGINE\library
<DATASET>/
 entries/ ADV-YYYY-NNN.json + ADV-YYYY-NNN_review.md (official location)
 index/ by_<10 axes>.json + master.json
 dataset_view.md
```

- Resolve order: (1) `<LIBRARY>` = the connected folder if it has `001_ad_video_dataset/`, else its `library/` subfolder if that has it; `<DATASET>` = `<LIBRARY>/001_ad_video_dataset`
 (entries/ + index/ inside it) → (2) if missing, request it via `mcp__cowork__request_cowork_directory` →
 (3) if it's an empty folder, seed it by copying dataset_template/.
- New entries go in `<DATASET>/entries/`; index updates go in `<DATASET>/index/`.
- The relative paths `entries/` and `index/` in workflow/examples work on both OSes (Python accepts `/`
 forward slashes on Windows too; scripts use `os.path.join`).
- Working temp artifacts (the frame cache `*_frames/`, etc.) stay in a separate working folder and are not
 exported into the dataset folder.
- If the user specifies a different path, that path wins.

## Workflow (in order)

### STEP 0 — Setup
- Input: an ad mp4. Study Appendix A (the entry schema). Resolve `<DATASET>` (section above).
- Dependencies: `pip install --break-system-packages scenedetect opencv-python-headless pillow faster-whisper`

### STEP 1 — Frame pipeline (every frame · **native resolution** · no grid)

> ⛔ **Reading is done one frame at a time at *native resolution*. Do not analyze from a contact sheet
> (a downscaled grid) or a downscaled image.** A frame shrunk small inside a grid can't be read by a human
> and even less by a model — that is not "analysis". Contact sheets are allowed ONLY as a *file-list index*.

```bash
# 1) Extract every frame at native resolution, leaving none out (no downscale, no sampling, no grid)
mkdir -p frames/allframes
ffmpeg -i <input.mp4> -vsync 0 -qscale:v 2 frames/allframes/f%06d.png
# 2) Metadata (fps, resolution, rotation):
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_read_frames -count_frames -of json <input.mp4>
# 3) (optional) Auto-detect cut boundaries — timecodes only, do NOT save images:
scenedetect -i <input.mp4> detect-adaptive list-scenes
```
- Even if you use ad_frames.py, **do not use the `--max-edge` (downscale) or `--contact-cols` (grid)
 options.** The old-version defaults were `--max-edge 1024 --contact-cols 6`, so a *downscaled 6-column grid*
 got used for analysis and ruined the results. Leave `allframes/` at **native resolution**.
- Output: `frames/manifest.json` (or the ffprobe result — fps, width/height, rotation, cut timecodes) +
 `frames/allframes/` (every frame, native resolution). Either don't make contact_sheets, or if you do, keep
 them strictly as a *file-navigation index* — **not for reading**.
- **Confirm rotation:** use ffprobe rotation (or the manifest) to settle portrait vs. landscape. Record
 aspect_ratio on that basis.
- **Full extraction (absolute):** every frame at native fps and native resolution. STEP 4 **opens these
 `allframes/` files one by one** to read them (for fine text, UI, or wiggle, *crop-enlarge* the relevant frame).

### STEP 1.5 — Audio (narration) extraction
```bash
python scripts/ad_audio.py <input.mp4> --model base --beam 1
```
Output: `<stem>_frames/audio.json` (narration timecodes, text, speech coverage, BGM estimate). On CPU,
base + beam1 is recommended (small and up are slow).
- Whisper's raw transcript can mis-recognize short words (e.g. Korean '우월한' → '우와란'), so cross-check
 against the on-screen captions and correct it.

#### STEP 1.5-a — When Whisper won't run in the sandbox (fallback order — never just stop)

Common failures: faster-whisper install failure (CTranslate2 binary), model-weight download blocked
(network allowlist), ffmpeg missing, OOM / excessive delay. **Walk down the list below, but if nothing works
all the way, fill the audio from captions and keep going with the visual analysis.**

1. **Check ffmpeg and the audio stream first.**
 `ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 in.mp4` → if there's no
 output, there's no audio track → finish immediately with `has_audio:false` (no transcription needed). If
 ffmpeg is missing, `pip install --break-system-packages imageio-ffmpeg` (bundled ffmpeg) or install it on
 the system. Separate the audio: `ffmpeg -i in.mp4 -vn -ac 1 -ar 16000 audio.wav`.
2. **If the model download is blocked**, use a smaller model: `--model tiny` (or `base`) — the weights are
 small and easy to fetch. Reuse the HF cache (`~/.cache/huggingface`); if huggingface.co is on the allowlist,
 it caches after one download.
3. **If faster-whisper itself won't install, use an alternate ASR:**
 `pip install --break-system-packages openai-whisper` → `whisper audio.wav --model base --language ko
 --output_format json` (no CTranslate2 needed, torch-based). A lighter alternative: the whisper.cpp binary +
 `ggml-base.bin`.
4. **If all ASR is impossible — manual fallback from captions (do not block the entry):** ads often have
 speech ≈ on-screen captions. Fill the narration in reverse from the on-screen captions
 (`copy_overlay` / `captions`) and mark each line with `source:"caption_inferred"`. If `speech_coverage` /
 `bgm_likely` can't be estimated, set them to `null` and record in `analyst_notes`: "audio transcription
 failed (reason: model download blocked, etc.)".
5. **In every case, the visual analysis (STEP 2–5) proceeds as normal.** Audio can be backfilled later in
 a better environment.

> Record the path actually used in `audio.transcribed_by`:
> `faster_whisper | openai_whisper | whisper_cpp | manual_from_captions | none`. This is what lets you later
> tell "is this entry's audio a real transcription or inferred from captions".

### STEP 2 — Cut-split verification (transition false positives)
- Check shot_count and cut lengths. **Verify cut boundaries by directly comparing individual frames from
 `allframes/` at native resolution** (no contact sheet — the tiny change at a boundary frame is invisible in
 a downscaled grid):
 - Around the candidate boundary timecode, open the adjacent frames (f(n-1), f(n), f(n+1)) one at a time and
 confirm the scene actually changes.
 - One cut split into two → raise the threshold and re-run. Two cuts merged into one → lower it and re-run.
 - **Same-color (e.g. blue→blue) match cuts / split screens / dissolves are almost impossible for auto-detect
 to catch.** If changing the threshold doesn't fix it, report it as an auto-split limitation, look at every
 frame one by one, and **manually identify the real cut boundaries**, recording them in shot_count_corrected.

### STEP 2.5 — Preserve per-cut mid frames + a contact sheet (kept as images in the dataset)

> Why: an entry is text (JSON). For a cut where one frame holds several scenes arranged as a split /
> multi-panel / filmstrip (e.g. the filmstrip and split typography zones in adv009), text labels alone can't
> let another session draw the spatial layout. So save the mid-duration frame image of each cut along with the
> dataset, so another session or the builder can see the actual picture and understand the layout.

Right after settling the cut boundaries in STEP 2, pick the mid-point frame of each cut from allframes, copy
it into the dataset, and make a labeled contact sheet (no extra decoding — just copy the already-extracted
native frames).

```bash
python3 scripts/ad_midframes.py --allframes frames/allframes --fps <FPS> --cuts "0:1.30,1.30:3.04,3.04:5.20,..." --out "<DATASET>/entries/<ID>_frames" --id <ID> --cols 4
```

- Output (permanently kept in the dataset): `<DATASET>/entries/<ID>_frames/cut01_mid.png …` (the mid frame of
 each cut, native resolution) + `contact_sheet.png` (all cuts at a glance, labeled with cut number and
 timecode) + `frames_index.json`.
- This folder is the exception that is kept inside the dataset (the full allframes cache is still not exported —
 only one mid frame per cut + the contact sheet are preserved).
- Embed the paths in the entry JSON: top-level `frames_dir` and `contact_sheet_path`; per shot,
 `mid_frame_path`. (Appendix A §1, §5)
- For split / multi-panel cuts, confirm them visually here and structure them as `panel_layout` in STEP 4.

### STEP 3 — Identify global signatures (before reading cut by cut)
Enlarge the individual frames of a few cuts to first grab **the effect laid across the whole ad**:
- `capture_style`: live action / 3D / AI-generated / mixed?
- `camera_signature`: is there a faint left-right viewpoint jitter (**wiggle_3d / parallax**) across every cut?
 Handheld shake? Locked-off?
 - ★ A wiggle is laid even on static scenes, so it looks "still" in a thumbnail. Enlarge 2–3 individual frames
 and check whether the background/subject edges shift slightly left-right. (If the shooting camera is a
 multi-lens 3D type like a Nishika, it's almost certainly a wiggle.)
 - If a camera model is mentioned in the video/description, look up that model's effect on the web and note it
 in signature_note.
- Also record `color_grade` and `texture_fx` globally.
- `global_layout`: the grid system (rule of thirds / center / split), the dominant subject placement, the
 subject↔typography relationship, negative space.

### STEP 4 — Read every frame, cut by cut (every frame, synthesized per cut)

**Every single frame (absolute principle):** for each cut, read the `allframes/` frames **in order from the
first frame to the last frame, one by one**. Do not skim past with one representative frame or a contact-sheet
thumbnail. You must view every frame in order so you can (a) accurately catch the *frame-to-frame change* of
subject, props, and camera (subject_motion, camera_motion, wiggle, prop_motion), and (b) not miss a 1–2 frame
expression or typography change. `contact_sheets/` is only an *index*, not the unit of reading. If a cut is
long, *don't skip* — read it in sequential batches (e.g. f000–f030, f031–f060 …) but view every frame.

Read it **as a frame sequence, but synthesize the labels per cut.** For each cut, fill in **all 7** of the
following (if any one is empty, you "only looked at the image"):
1. **Static**: framing, color_mood, subject_action, copy_overlay (the cut's representative state after
 checking all frames).
2. **Layout**: layout_grid, subject_position, subject_typo_layout (placement when a person + on-screen text
 coexist).
3. **Typography motion**: typo_motion — track across frames *in which frame the text appears, moves, and
 disappears, and how*.
4. **Camera angle, shot, gaze** ★ camera_angle (eye_level/high/low/overhead), camera_facing
 (frontal/¾/profile), shot_scope (face/bust/full-body/environment), gaze (to-camera / averted / at product).
5. **Props, color, posing** ★ props (prop list), prop_semantics (why used = symbolic/functional),
 color_palette (the dominant HEX from the manifest), color_intent (intent such as complementary contrast /
 brand color), pose_description (the impression the pose/gesture gives).
6. **Dynamic (frame by frame)**: subject_motion (judge real motion vs. a static pose by comparing adjacent
 frames), prop_motion, camera_motion + intensity, camera_effect_local (confirm a wiggle from the left-right
 viewpoint difference between adjacent frames), motion_blur, intra_cut_rhythm, transition_in/out (confirm at
 the boundary frames).
7. **Fact-check**: fact_check_flag.

> `rep_frame` is just a *representative thumbnail for storage*, not the unit of reading (reading is every
> frame). Use the manifest's per-shot `color_palette` (dominant HEX) as is; the intent (color_intent) is
> interpreted by a human.

### STEP 4.5 — Full visual inventory · texture · lighting · color · style prompt (5 axes)

If the 7 items of STEP 4 are *a classification of the direction*, STEP 4.5 is *the information needed to
re-make the image*. It feeds straight into the downstream builder's board generation, so it must be precise.

#### 4.5.1 `visible_elements` — every visual element on screen (5-layer cataloging)

`props` is only *grab-able props*. The screen also has *environment, light sources, atmosphere, background
detail*. Catalog them per cut in 5 layers.

```json
"visible_elements": {
 "foreground": ["protagonist / main subject", "directly held props"],
 "midground": ["background people", "table/chairs/equipment"],
 "background": ["building facade", "mountains/sea/sky", "signage/LED"],
 "lighting_env": ["window daylight", "studio key light", "neon sign"],
 "atmosphere": ["dust", "fog", "rain", "snow", "backlit glow"]
}
```

For each layer, *write down everything visible*. If you drop a small detail (e.g. "a book in the background"),
it disappears when the builder re-draws it.

#### 4.5.2 `texture` — per-cut surface texture

The global `texture_fx` (clean_digital/film_grain, etc.) is the whole video's *render tone*. The per-cut
`texture` is *the texture of each surface on screen*. Look at both. The vocabulary is English (international
standard): matte/glossy/metallic/chrome, glass_clear/frosted/tinted,
fabric_cotton/silk/denim/velvet/leather, wood_polished/raw, concrete/brick/stone, skin_natural/makeup,
plastic_glossy/matte, foliage/fur/hair, paper/cardboard, etc.

```json
"texture": { "primary_subject":"fabric_silk", "secondary_objects":["glass_clear","wood_polished"], "background_surface":"concrete", "atmospheric":["dust","atmospheric_haze"] }
```

#### 4.5.3 `lighting` — light source · contrast · color temperature (the most important variable for image generation)

```json
"lighting": {
 "key_direction":"front/back/side_left/side_right/top/bottom/45deg_above/45deg_side",
 "key_hardness":"hard/soft/diffused",
 "key_color_temp":"warm_3000K/neutral_5500K/cool_7000K/colored_neon/mixed",
 "fill_strength":"strong/moderate/minimal/none",
 "key_to_fill_ratio":"1:1/2:1/4:1/8:1/silhouette",
 "rim_light":true/false,
 "practical_lights":["window","neon","candle"],
 "shadow_presence":"deep/soft/minimal/none",
 "overall_contrast":"low_key/mid_key/hi_key/high_contrast"
}
```
The lighting vocabulary is English. practical_lights can be free Korean description. Judge live-action by
shadows/highlights, AI-generated by color-grade and shading contradictions.

#### 4.5.4 `color_analysis` — precise color analysis

Add *relationships and strategy* to the existing `color_palette` (dominant HEX).

```json
"color_analysis": {
 "palette_hex":["#6ab3cb","#29282d","#dfcac2","#667b76"],
 "palette_role":{"#6ab3cb":"background_dominant","#29282d":"subject_dark_anchor","#dfcac2":"skin_or_warm_accent","#667b76":"midtone_bridge"},
 "color_relationship":"complementary/analogous/triadic/split_complementary/monochrome/brand_dominant",
 "temperature_balance":"warm_dominant/cool_dominant/balanced/split_warm_cool",
 "saturation_strategy":"vivid/muted/desaturated_with_pop/monochrome",
 "contrast_type":"luminance_high/luminance_low/hue_complementary/temperature_split",
 "accent_color":"#dfcac2", "accent_ratio":"5_percent/15_percent/30_percent",
 "brand_color_match":["approx. match to brand blue #0046AA"]
}
```

#### 4.5.5 `style_prompt` — a one-line prompt for AI image generation (key cuts)

For *cuts likely to be re-made* — key visual, hero cut (the highest-impact cut), hook, cta — write a one-line
English prompt (200–350 chars). Structure:
[subject+pose]→[outfit/material]→[location]→[lighting]→[framing+angle]→[palette+mood]→[texture+atmosphere]→[post
look]→[style anchor]. State nationality/culture, and brand colors as HEX. **Do not generate a celebrity's
*photographic face replica* or a real logo mark (keep them generic/typed). Preserve on-screen text / copy
verbatim (same rule as 4.5.6 below).**

#### 4.5.6 `recreation_prompts` — cut start-frame t2i + i2v motion (preserve for every cut) ★

For **every cut**, make and store in `recreation_prompts`: a *long t2i prompt that recreates the start frame
(**≥500 words per cut**, target 500–650)* + an *i2v prompt that turns that still into video with the original
cut's motion*. (At 300 words the detail evaporates and it can't be implemented later — hence the 500-word
floor.) **For a split / multi-panel cut, spell out every panel's position, size ratio, content, and divider
in the t2i (Appendix B §2 Part 13).** Weave 4.5.1–4.5.4 (the visual inventory) into one paragraph, and
synthesize the i2v from the dynamic fields
(subject_motion, camera_motion, camera_effect_local, prop_motion, typo_motion, intra_cut_rhythm, duration,
transition, motion_blur). **For a multi-character cut, state *that cut's character ID* in the t2i/i2v** (e.g.
"the protagonist, character ID protagonist_main" / "a different person — cafe customer, NOT the protagonist").
This makes it clear to the builder which master sheet to insert.

```json
"recreation_prompts": {
 "t2i_start_frame": "<12 (+13 if split) part structure, ≥500 words>",
 "t2i_negative": "<negative>",
 "i2v_motion": "<i2v with the original cut's motion>",
 "i2v_params": {"clip_duration_sec":<duration>,"camera_move":"...","subject_motion_level":"...","signature_effect":"wiggle_3d/none","pacing":"...","loopable":<bool>},
 "fidelity_note": "craft-faithful; on-screen copy preserved verbatim (per copywriting); celeb face-likeness & logo mark generic"
}
```

For writing rules, the 12-part t2i structure, the i2v motion mapping, the t2i→i2v chain, a worked example,
and the boundaries, see **Appendix B** at the bottom of this document.

> **Boundaries (summary):** On-screen text / copy is **preserved** (short copy and figures verbatim, only long
> disclaimers as an excerpt — same as copywriting). But a celebrity's *photographic-level face replica* and a
> real *logo mark* are generic (likeness / trademark). A brand name or model name inside the copy text stays as
> is, because it's a caption. The craft (composition, lens, lighting, color, motion) is faithful — "the original
> feel" comes from there. The result is an input for cross-pollination (cross-pollination = deliberately
> borrowing the approach/structure of an ad from a DISTANT category to make a new original).

### STEP 5 — Synthesize top-level structure + copy + audio
- narrative_arc, pacing_curve, hook/cta_position, wow_cut_index (the index of the hero cut), creative_device.
- copywriting: on-screen copy verbatim + each line's `source` (voice/caption/both), filled by cross-checking
 against audio.json.
- audio: narration_lines (corrected text + raw text), voice_vs_caption, bgm_likely.
- typography (including typo_motion_dominant), vfx.

### STEP 5.5 — Reverse-infer the thinking · search keywords · reverse-infer the brief

Reverse-infer the ad's *cause* and embed it at the bottom of the entry. Every inferred field gets a
`confidence: "inferred"` label.

**5.5.1 Reverse-infer the thinking (7 steps)** — `inferred_creative_thinking`:
insight / persona / moment / product_role / punchline / differentiator / brand_fit_one_liner (same schema as
treatment-builder REFERENCE/client-vs-internal.md).

**5.5.2 Search keywords (10 axes)** — `search_keywords`. The index the planner uses to match a brief. 1–5
values per axis.

```json
"search_keywords": {
 "industry": ["finance"],
 "product_category": ["salary_account"],
 "target_demo": ["late20s_early30s","early_career","office_worker","mz"],
 "media_format": ["shortform_landscape_30s"],
 "tone": ["punchy_humor","friendly"],
 "pacing": ["front_loaded","ramp_up"],
 "technique": ["celeb_hook","balloon_typo_3d","filmstrip_collage"],
 "vfx_keywords": ["wiggle_3d","color_pop","3d_render","split_screen"],
 "copy_strategy_keywords": ["product_name_pun","refrain_repetition","model_name_drop"],
 "concept_derivation_pattern": ["celeb_fashionfilm"]
}
```

**Language rule (must follow): all 10 axes of search_keywords are English tokens.**
Category / product / target / media / tone / technique / copy strategy / thinking — *all of them as English
tokens* (the old Korean axes are retired). For a value that came to mind in Korean, find the English token via
the KO alias table in `lsb-treatment-builder/REFERENCE/keyword-vocabulary.md` and use that. If it's not in the
table, use the closest token; if it's new, add `English token + KO alias` to the table.

**Why unify on English:** if you mix KO/EN, a search for "통신" won't catch a "telecom" entry in the same
dataset and the index breaks. Unify with English tokens for every axis + a KO alias table.

**5.5.3 Reverse-infer the brief** — `inferred_brief`: the brief the advertiser probably gave, in one sentence
(for direct comparison against the planner's brief matching).

**5.5.4 Cross-pollination tags** — `cross_pollination_tags`: adjacent/distant/contrast. As **English tokens**
(e.g. `"adjacent":["insurance","telecom","subscription_membership"]`). An auxiliary signal for planner
weighting.

**5.5.5 Concept-derivation pattern** — `concept_derivation_pattern`: an English token (the handbook's 12
patterns, keyword-vocabulary §8).

**5.5.6 Confidence label** — `confidence`: inferred / human_verified / partial. New ones are inferred; after a
human reviews, promote to human_verified.

### STEP 5.6 — Auto-update the category index

Right after saving a new entry to `<DATASET>/entries/`, update the index (if you skip it, the planner can't
find the new entry).

You do not need a separate `index_helper.py` file — update with the **inline snippet** below (self-contained).
`<DATASET>` is the connected `<LIBRARY>/001_ad_video_dataset` absolute path (`<LIBRARY>` — API: the `shitbin/lsb-demo` repo's `library/`; Local: `/Users/soobin/Desktop/LSB_AD_ENGINE/library`), `<ENTRY>` is the path of the entry you just saved. The
output (by_*.json, master.json) is **all strict JSON**. (If heredoc doesn't work on Windows, save the body
below as `idx_update.py` in a **working scratch folder** and run `python idx_update.py "<DATASET>" "<ENTRY>"` —
but keep that `.py` in scratch only, not in `<DATASET>`.)

```bash
python3 - "<DATASET>" "<DATASET>/entries/ADV-YYYY-NNN.json" <<'PYEOF'
import json, os, sys, datetime
D, ep = sys.argv[1], sys.argv[2]
AX = ["industry","product_category","target_demo","media_format","tone",
      "pacing","technique","vfx_keywords","copy_strategy_keywords","concept_derivation_pattern"]
e = json.load(open(ep, encoding="utf-8")); eid = e["id"]; sk = e.get("search_keywords", {})
os.makedirs(os.path.join(D, "index"), exist_ok=True); today = str(datetime.date.today())
for ax in AX:
    vals = sk.get(ax, []); vals = [vals] if isinstance(vals, str) else vals
    if not vals: continue
    p = os.path.join(D, "index", "by_%s.json" % ax)
    idx = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {"_meta": {}}
    for v in vals:
        v = str(v).strip()
        if not v: continue
        idx.setdefault(v, [])
        if eid not in idx[v]: idx[v].append(eid)
    ids = {i for k, val in idx.items() if k != "_meta" for i in val}
    idx["_meta"] = {"axis": ax, "language": "en", "updated": today, "entry_count": len(ids)}
    json.dump(idx, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
mp = os.path.join(D, "index", "master.json")
m = json.load(open(mp, encoding="utf-8")) if os.path.exists(mp) else {}
sr = e.get("source_ref", {})
m[eid] = {"path": "entries/%s.json" % eid, "category_primary": e.get("category_primary"),
          "brand": sr.get("brand"), "title": sr.get("title_or_campaign"), "year": sr.get("year"),
          "search_keywords": sk, "confidence": e.get("inferred_creative_thinking", {}).get("confidence", "inferred")}
json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("OK index updated:", eid)
PYEOF
```

1. Read the entry's 10-axis `search_keywords` (English tokens) → 2. add the entry ID to each
`index/by_<axis>.json` (duplicates allowed) → 3. update master.json. The index `_meta.language` is `en`
everywhere.

Example index file `index/by_industry.json`:
```json
{ "_meta": {"axis":"industry","language":"en","updated":"2026-06-02","entry_count":6},
 "finance": ["ADV-2026-001"], "automotive": ["ADV-2026-002","ADV-2026-003"] }
```

### STEP 6 — Self-check (mandatory before output)
- ★ Full reading: did you view each cut's `allframes/` **frames in order, all of them**? Did you avoid
 skimming with a representative frame or a contact sheet? Did you confirm dynamic labels (subject_motion,
 camera wiggle, etc.) by comparing adjacent frames?
- Abstraction: zero proper-noun leaks in the visual *descriptions* (proper nouns limited to
 source_ref/copywriting) → abstraction_checked.
- Direction completeness: each shot has subject_motion, layout_grid, typo_motion (when applicable) filled.
 Distinguish "a static pose where only the effect moves".
- No missing global signature (e.g. wiggle).
- ★ Each cut has camera_angle/facing/shot_scope/gaze, props/prop_semantics, color_palette/intent,
 pose_description filled.
- ★ STEP 5.5: inferred_creative_thinking (7 steps), search_keywords (10 axes), inferred_brief,
 cross_pollination_tags, concept_derivation_pattern, confidence filled. Inferred values carry
 `confidence: "inferred"`.
- ★ Vocabulary: are all 10 axes of search_keywords + cross_pollination_tags **English tokens**? No Korean
 values left over? (per keyword-vocabulary.md)
- ★ STEP 5.6: did the index-update script run? Were the new IDs added to the 10 files in `index/` +
 master.json? Is `_meta.language=="en"`?
- ★ STEP 4.5 (5 axes): each cut's `visible_elements` (5 layers), `texture`, `lighting` (9 sub-fields),
 `color_analysis` (9 sub-fields) filled.
- ★ STEP 2.5: are `cutNN_mid.png` per cut + `contact_sheet.png` saved in `<DATASET>/entries/<ID>_frames/`?
 Are `frames_dir`, `contact_sheet_path`, and each shot's `mid_frame_path` embedded in the entry?
- ★ Split / multi-panel cuts: did you fill `panel_layout` (panel position, ratio, content, divider) on that
 cut? (Not left as text only?)
- ★ STEP 4.5.6: each cut's `recreation_prompts` (t2i_start_frame, i2v_motion, i2v_params) filled. **Is
 t2i_start_frame ≥500 words per cut?** Did you spell out Part 13 (panel decomposition) in the t2i for split
 cuts? **Zero celebrity photographic-face replica / real logo-mark leaks? Captions kept verbatim per
 copywriting (only long disclaimers as an excerpt)?**
- ★ Storage path: were the outputs saved to `<DATASET>` (entries/, index/, dataset_view.md)?

### STEP 7 — Output (2 kinds)
1. `<DATASET>/entries/ADV-YYYY-NNN.json` — the Appendix A schema structure exactly. **Must be saved as a
 strict JSON file** (see ⚠️ below).
2. The review file `<DATASET>/entries/ADV-YYYY-NNN_review.md` (top-level meta + one line per cut). Update
 `<DATASET>/dataset_view.md`.
- Keep the dataset folder and the frame cache (`*_frames/`) separate. Do not export the frame cache.

> ⚠️ **The entry's final output is `.json` — not `.py`.** Write the entry directly to
> `entries/ADV-YYYY-NNN.json` as **strict JSON** with the `Write` tool (keys in double quotes,
> `true`/`false`/`null`, no trailing commas or comments). If you want to assemble it as a Python dict, run
> that **assembly script in working scratch (outputs) only**, and export *only the json* to `<DATASET>` via
> `json.dump(obj, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=2)` — **do not leave the assembly
> `.py` in `<DATASET>`.** Right after saving, verify parsing with
> `python3 -c "import json;json.load(open('<ENTRY>',encoding='utf-8'))"`. If it fails, Python literals got mixed
> in (`True`/`False`/`None`, single quotes, comments) — fix all of them to JSON. (Only `.json`, `_review.md`,
> and `dataset_view.md` should exist in the dataset.)

## Do NOT
- Don't analyze only the image (missing the direction). Don't settle a dynamic label from a thumbnail alone.
- Don't omit a global effect (e.g. wiggle). Don't ignore rotation.
- Don't guess without watching the video, and don't store Level 0–1 visual *descriptions*.
- **Don't save the dataset outside `<DATASET>` (inside the connected `<LIBRARY>`).** (Only an exception if the user
 specifies a different path.)
- **Don't save `.py`, scripts, or Python dict literals in `<DATASET>`.** Entries and indexes are all strict JSON
 (`.json`). Run assembly Python in scratch only and leave only `.json` in the dataset.
- Don't put **Korean values** in search_keywords or cross_pollination_tags (all English tokens).
- If you can't finish in one session, do a partial save and resume.
- **Don't write STEP 5.5 inferred fields as if they were *facts*.** `confidence: "inferred"` is required. If
 you'll leave it empty, state it explicitly as `null`.
- Don't put a **celebrity photographic-face replica or a real logo mark** in recreation_prompts. Preserving the
 on-screen text / copy verbatim is correct.
- **Don't shorten the t2i recreation prompt below 500 words per cut** (detail loss → can't implement). Don't
 lump a split / multi-panel cut into one line of text — decompose it panel by panel (panel_layout + Part 13).
- **Don't skip saving the per-cut mid frame / contact sheet** (STEP 2.5). If you save only text, another
 session can't draw the split layout.

---
*Version: lsb-ad-analyzer_260614_v11  (version scheme = YYMMDD_vN, checked against the real clock; earlier inline _2606xxxx codes are legacy timestamps, not reliable.) — prior base lsb-ad-analyzer_2606041200 · 2026-06-04 12:00 KST. See how-to-apply.md for the change log.
(_2606041200 = **preserve per-cut mid frames + contact sheet in the dataset (STEP 2.5, scripts/ad_midframes.py)**
+ entry `frames_dir`, `contact_sheet_path`, shot `mid_frame_path` · **split / multi-panel `panel_layout`** schema
(§5/§10) · **t2i recreation prompt raised to ≥500 words per cut** + Appendix B Part 13 panel-decomposition rule.
Motive: text alone could not let another session understand a single-frame split layout [the adv009 filmstrip].)
_2606140000 = English rewrite + de-jargon (faithful translation, no content dropped).*


---

# Appendix A — entry output schema (former schema.md merged in)

> Version: lsb-ad-analyzer_2606041200 · 2026-06-04 12:00 KST. For the accumulated changes (deep direction ·
> global signature · audio · camera/prop/color · 10-axis reverse inference · visual inventory · frame
> recreation · every-frame native-resolution reading / no grid · entry JSON-first / no `.py` in dataset ·
> shots subject_identity / narrative_structure meta [the multi-character mixup lesson, formerly "A3"] ·
> library reorganization DATASET=001_ad_video_dataset · **per-cut mid frame / contact-sheet preservation +
> panel_layout + t2i ≥500 words [2606041200]**), see SKILL.md.
> We turn "how it was directed" into data, not "what got filmed in the image".

---

## 0. Abstraction rule (absolute principle)

- **Visual *descriptions*** → Level 2–3 only. Level 0 (raw description) and Level 1 (description including a
 proper noun) are forbidden.
- **Copy (slogan, tagline, CTA, caption, short one-liner)** → store the original text as is + a classification
 meta tag. The only thing forbidden is the output resembling the original "with only the words swapped" (the
 plagiarism gate — a self-check that the output isn't too similar to a reference).
- **Long text (long narration, legal disclaimers)** → don't store it wholesale, only the key lines
 (`narration_handling: excerpt_only`).
- **Proper nouns (a brand, model, or product's official name)** → limited to `source_ref` / `brand` /
 `product` / `model` + the copy original (copywriting). Forbidden in the body of a visual *description*.

---

## 1. Top-level fields — structure · narrative

| Field | Type | Description | Source |
|---|---|---|---|
| `id` | string | `ADV-YYYY-NNN` | assigned |
| `source_ref` | object | `{platform, title_or_campaign, brand, product, model, year, production_note, url}` | meta |
| `category_primary` | string | one primary category (§6, `<domain>.<sub>`) | judgment |
| `category_tags` | array | secondary tags (descriptive, Korean allowed — not indexed) | judgment |
| `mood` | array | mood tags (descriptive) | judgment |
| `target_demo` | string | target demographic (descriptive) | judgment |
| `total_duration` | number | total length (seconds) | manifest |
| `shot_count` / `shot_count_corrected` | number | detected / corrected cut count | manifest/judgment |
| `fps` | number | frame rate | manifest |
| `aspect_ratio` | string | **display-basis** ratio (reflecting rotation) | manifest |
| `hook_position` / `cta_position` | number | hook / CTA time (seconds) | judgment |
| `narrative_arc` | string | narrative-structure summary (Level 3) | judgment |
| `narrative_structure` | string | linear_continuous / cross_cutting_montage / parallel_narrative / nested_flashback | narrative-structure enum (to retrieve ads of the same structure — same enum as the planner) |
| `pacing_curve` | enum | slow_build/steady/accelerating/front_loaded/staccato | judgment |
| `music_tempo_curve` | enum | steady/ramp_up/drop/fluctuate | judgment |
| `wow_cut_index` | array | index of the hero cut(s) | judgment |
| `creative_device` | string | the core device | judgment |
| `production_signature` | object | global capture / effect signature (§1.1) | judgment |
| `global_layout` | object | grid / subject-placement tendency (§1.2) | judgment |
| `recurring_motifs` | array | recurring visual motifs | judgment |
| `copywriting` | object | copy meta (§2) — **preserve the original text** | judgment |
| `typography` | object | typography meta (§3) | judgment |
| `vfx` | object | VFX meta (§4) | judgment |
| `audio` | object | audio analysis (§4.5) | Whisper+judgment |
| `frames_dir` | string | cut mid-frame folder name `"<ID>_frames"` (STEP 2.5, kept in the dataset) | meta |
| `contact_sheet_path` | string | `"<ID>_frames/contact_sheet.png"` — all cuts at a glance (to check split layouts) | meta |
| `shots` | array | per-cut detail (§5) + visual inventory / recreation (§10) | manifest+judgment |
| `search_keywords` | object | 10-axis search index — **English tokens** (§9) | judgment |
| `inferred_creative_thinking` / `inferred_brief` / `cross_pollination_tags` / `concept_derivation_pattern` / `confidence` | — | reverse inference (SKILL STEP 5.5) | judgment |
| `analyst_notes` | string | analyst comments / corrections | judgment |
| `verification` | object | `{frames_reviewed, audio_analyzed, hitrate_na, abstraction_checked}` | meta |

### 1.1 `production_signature`
`capture_style` (live_action/3d_cg/ai_generated/mixed/stop_motion) · `camera_signature[]`
(wiggle_3d/parallax/handheld_shake/locked_off/dolly_heavy) · `signature_note` · `color_grade`
(high_key/brand_color_dominant/desat/warm/cool) · `texture_fx` (film_grain/halation/glow/clean_digital).
> ★ A global faint viewpoint jitter like wiggle_3d is easily misjudged as "still" in a thumbnail. Confirm the
> left-right viewpoint shift by enlarging the individual frame → here + each shot's `camera_effect_local`.

### 1.2 `global_layout`
`grid_system` (rule_of_thirds/center/golden_ratio/split_screen/dynamic_symmetry) · `subject_placement_dominant`
(center/left_third/right_third/varies) · `subject_typo_relation`
(typo_opposite_subject/typo_over_subject/typo_separate_zone/alternating) · `negative_space_use`
(minimal/generous/asymmetric) · `layout_note`.

## 2. `copywriting` — preserve the original text
`tagline_text` (original) · `tagline_structure` · `tagline_length_syllables` · `tagline_position_sec` ·
`cta_text`/`cta_text_structure`/`cta_position_sec` · `copy_tone[]` · `copy_strategy` · `copy_lines_count` ·
`lines[]` (`{position_sec,text(original),function,tone,source}` — source: voice/caption/both) · `captions[]`
(`{position_sec,text(original),function}`) · `narration_handling` (excerpt_only/summary_only/none).

## 3. `typography`
`primary_font_class`/`secondary_font_class` · `animation_style[]`
(fade_in/typewriter/kinetic/static/pop/slide/blur_in/bounce/scale_in/track_in) · `subtitle_position_dominant`
(lower_third/center/full_screen/top/floating) · `tagline_position` · `color_strategy` · `appearance_count` ·
`key_typography_moments_sec[]` · `typo_motion_dominant`.

## 4. `vfx`
`primary_effects[]` (light_leak/particle/lens_flare/color_pop/glitch/morph/ui_motion/3d_render/data_viz/split_screen)
· `effect_intensity` (subtle/moderate/heavy/extreme) · `transition_style_dominant`
(cut/fade/light_wipe/match_cut/morph/whip_pan/camera_push_through) · `vfx_event_count` · `vfx_timing_array_sec[]`
· `wow_vfx_index[]`.

## 4.5 `audio` (Whisper)
`has_audio` · `language` · `speech_coverage` (0–1) · `bgm_likely` (true/false/null) · `narration_lines[]`
(`{start,end,text(corrected),text_raw(original),kind,source}` — source can be `caption_inferred`) ·
`voice_vs_caption` · `narration_handling` · `transcribed_by`
(faster_whisper/openai_whisper/whisper_cpp/manual_from_captions/none) · `audio_note`.
> If Whisper fails in the sandbox, use the SKILL.md STEP 1.5-a fallback (check ffmpeg → smaller model →
> openai-whisper/whisper.cpp → manual from captions). Even if you can't transcribe, proceed with the visual
> analysis and record the path in `transcribed_by`.

## 5. `shots[]` — per-cut detail

Order each shot by `index`. Reading is done **one individual frame at a time from `allframes/` at native
resolution** — whether the information is static or dynamic/directorial, do not read it from a contact sheet
(a downscaled grid).

- **Static**: `index` · `duration` · `framing` (ECU/CU/MCU/MS/MLS/LS/WS/EWS/grid/environment) · `function` ·
 `color_mood` · `subject_action` · `copy_overlay` (original).
- **Subject identity (multi-character ads)**: `subject_identity` (this cut's character classification — e.g.
 protagonist_main · supporting_A · cafe_barista · background_crowd · none_environment) ·
 `subject_relationship_to_protagonist` (main_character / supporting_character / extra_atmosphere). Lets you
 retrieve cut-montage / multi-character structures from the dataset (same concept as the planner's
 character_pool).
- **Frame image**: `mid_frame_path` ("<ID>_frames/cutNN_mid.png") — this cut's mid frame (STEP 2.5). The handle
 another session uses to see the actual picture.
- **Layout**: `layout_grid` · `subject_position` · `subject_typo_layout` · `typo_motion`.
- **Split / multi-panel layout (★ several scenes in one frame)**: if the screen is a split / multi-panel /
 filmstrip / grid / PIP / collage, fill `panel_layout` (otherwise omit / `null`). Leaving it as text only means
 another session can't draw the panel arrangement.
  ```json
  "panel_layout": {
    "is_multi_panel": true,
    "type": "filmstrip | split_vertical | split_horizontal | grid | picture_in_picture | collage | layered_collage | typo_zone_split",
    "panel_count": 6,
    "divider": "thin black gutter | white line | none | overlap",
    "orientation": "row | column | grid_RxC",
    "panels": [
      {"id":1, "rect":"x 0-16%, y 0-100%", "size_ratio":"~1/6 width", "content":"<Level 2–3 description>", "text_in_panel":"<original text if any>"},
      {"id":2, "rect":"x 16-33%, y 0-100%", "size_ratio":"~1/6 width", "content":"..."}
    ],
    "layout_note":"panel order, whether it repeats, gaze flow, etc."
  }
  ```
  Each panel's `rect` is a percentage relative to the frame (from the top-left), `size_ratio` is an approximate
  ratio, `content` is an abstracted description, and `text_in_panel` preserves the caption original. Seeing this
  structure + the `mid_frame_path` image together lets the builder reproduce the split layout exactly.
  - **`layered_collage` (pieces overlapping on a base — e.g. the GMA 2018 style)**: if it's not simply a
  *side-by-side* split but an *overlapping* collage, use `type:"layered_collage"` + `base` (a description of
  the base image) + `panels[]` as pieces, writing on each piece its `z` (layer order), `rotation_deg`, and
  whether it overlaps. In this case the builder / video-crafter handles it as a 3-stage separation —
  **never generate as one image · generate individual sources → compose a preview → layer motion in the video**
  (common rule: `lsb-treatment-builder/REFERENCE/layered-collage-protocol.md`).
- **Camera angle · shot · gaze**: `camera_angle` (eye_level/low_angle/high_angle/overhead/dutch/worm_eye) ·
 `camera_facing` (frontal/three_quarter/profile/back) · `shot_scope` (face_only/bust/waist_up/full_body/environment)
 · `gaze` (to_camera/off_camera/at_product/down/none) · `eye_contact_effect`.
- **Props · color · posing**: `props[]` · `prop_semantics` · `color_palette[]` (dominant HEX) · `color_intent`
 · `pose_description`.
- **Dynamic**: `subject_motion` · `prop_motion` · `camera_motion` · `camera_motion_intensity` ·
 `camera_effect_local` (none if absent) · `motion_blur` · `intra_cut_rhythm`
 (static/steady/accelerating/chaotic) · `transition_in`/`transition_out` · `vfx_in_shot[]` ·
 `vfx_intensity_local` · `fact_check_flag` · `notes`.
- **Visual inventory + frame recreation**: §10.

> All vocabulary (English tokens) and the treatment-key mapping are in
> `lsb-treatment-builder/REFERENCE/cut-schema.md` + `lsb-ad-planner/schema.md` §5.

---

## 6. `category_primary` value system (open / extensible)

Format: **`<domain>.<sub>`**. Domains beyond IT are allowed (the data already uses `auto.*`, `realestate.*`,
`retail.*`, `apparel.*`).

```
IT.smartphone / IT.wearable / IT.app_b2c / IT.app_b2b_saas / IT.ai_product
IT.laptop_pc / IT.smart_home / IT.fintech / IT.gaming_hardware / IT.platform
auto.sedan / auto.suv_hybrid / auto.pickup_truck / auto.ev / auto.luxury
finance.bank / finance.card / finance.insurance / finance.securities
realestate.apartment_presale / retail.beauty_platform / retail.commerce
apparel.sportswear / apparel.fashion / fnb.* / beauty.* / public.*...
```

New domains / subs extend freely. But keep it consistent with `search_keywords.industry` (English token, §9)
(e.g. category_primary `auto.pickup_truck` ↔ industry `automotive`).

## 7. Cross-pollination category mapping — (legacy, for reference)

> ★ **The single source of the weight map is now `lsb-ad-planner/schema.md` §3 (English-industry basis).**
> Two maps must not diverge, so use the planner's as canonical. The IT table below is left *for legacy reference*
> only.

| Client X | Adjacent (0.5) | Distant (1.0) | Contrast (1.2) |
|---|---|---|---|
| IT.fintech | app_b2c, platform | luxury, automotive | gaming, streetwear |
| IT.smartphone | wearable, laptop_pc | automotive, fashion | agriculture, traditional liquor |

> Same (X=X) = 0.2 (reference only); hero cut = 0 same-category references (hard ban).

---

## 8. A filled example
For a real example, see `<DATASET>/entries/ADV-2026-001.json` (finance, "우월한 월급통장"). It's a reference with
production_signature (3D wiggle), global_layout, audio, and the deep direction in shots[] + the visual inventory
+ search_keywords (English tokens) all filled.

---

## 9. `search_keywords` (10 axes) — every axis an English token

The index input the planner uses to match a brief. **All 10 axes are English tokens** (the old Korean axes are
retired). For a value that came to mind in Korean, find the English token via the KO alias table in
`lsb-treatment-builder/REFERENCE/keyword-vocabulary.md` and use that.

Axes: `industry` · `product_category` · `target_demo` · `media_format` · `tone` · `pacing` · `technique` ·
`vfx_keywords` · `copy_strategy_keywords` · `concept_derivation_pattern`.

```json
"search_keywords": {
 "industry": ["finance"], "product_category": ["salary_account"],
 "target_demo": ["late20s_early30s","early_career","office_worker","mz"],
 "media_format": ["shortform_landscape_30s"], "tone": ["punchy_humor","friendly"],
 "pacing": ["front_loaded","ramp_up"], "technique": ["celeb_hook","balloon_typo_3d","filmstrip_collage"],
 "vfx_keywords": ["wiggle_3d","color_pop","3d_render","split_screen"],
 "copy_strategy_keywords": ["product_name_pun","refrain_repetition","model_name_drop"],
 "concept_derivation_pattern": ["celeb_fashionfilm"]
}
```

- `cross_pollination_tags` (adjacent/distant/contrast) are also **English tokens**.
- Index update: use the **inline Python snippet in STEP 5.6** (no separate `index_helper.py` file needed; only
 a bulk rebuild is optional). The index `_meta.language` is `en` everywhere.
- **No mixing:** putting a Korean value in search_keywords breaks index matching ("통신" vs. "telecom").

## 10. Visual inventory + frame recreation — shots[] extension

For key cuts (or every cut), embed the *image/video re-generation input*. It feeds straight into the builder's
board generation.

- `mid_frame_path`: this cut's mid frame image (STEP 2.5). `panel_layout`: if split / multi-panel, per-panel
 position, ratio, content (§5).
- `visible_elements`: foreground/midground/background/lighting_env/atmosphere (5 layers).
- `texture`: primary_subject/secondary_objects[]/background_surface/atmospheric[] (English vocab).
- `lighting`: key_direction/key_hardness/key_color_temp/fill_strength/key_to_fill_ratio/rim_light/practical_lights[]/shadow_presence/overall_contrast.
- `color_analysis`: palette_hex[]/palette_role{}/color_relationship/temperature_balance/saturation_strategy/contrast_type/accent_color/accent_ratio/brand_color_match[].
- `style_prompt`: a one-line English prompt for the key cut.
- `recreation_prompts`: `t2i_start_frame` (**≥500 words**) · `t2i_negative` · `i2v_motion` · `i2v_params` ·
 `fidelity_note`. For a split / multi-panel cut, describe each panel's position, ratio, and content in the t2i
 (Appendix B §2 Part 13).

For the detailed writing method, examples, and boundaries, see STEP 4.5 / STEP 4.5.6 + **Appendix B** below
(in this document).

> **Boundary:** On-screen text / copy is **preserved** (short copy and figures verbatim, only long disclaimers
> as an excerpt). Only a celebrity's *photographic-level face replica* and a real *logo mark* are generic
> (likeness / trademark). The craft (composition, lens, lighting, color, motion) is faithful.


---

# Appendix B — cut-frame recreation t2i/i2v spec (former frame-recreation-prompts.md merged in)

For each cut, preserve a long t2i prompt that can re-make the cut's **start frame**, and an i2v prompt that
turns that still into video **with the feel of the original cut's motion**. This is the step where you *weave*
the STEP 4.5 visual inventory (visible_elements, texture, lighting, color_analysis) into a one-line prompt.

## 0. Purpose and boundaries (read first, mandatory)

- **Purpose:** preserve the *directorial craft* of a well-made cut — composition, lens, lighting, color,
 texture, motion — as a **reusable generation recipe**. The studio learns this craft and uses it as input for
 the planner's cross-pollination to make a **new original ad** (cross-pollination = deliberately borrowing the
 approach/structure of an ad from a DISTANT category so the result is fresh and not plagiarized).
- **Boundaries (craft + caption preservation + accuracy):**
 - This prompt is a craft recipe for the studio's *internal reference / recreation*, used as input for
 cross-pollination (generating a new original).
 - **Captions / copy are preserved verbatim (no abstraction or placeholder).** Put the **actual original text**
 recorded in the entry's `copywriting` into the prompt, along with its position, typography, and color-box
 treatment. Short slogans, captions, and figures verbatim; only long disclaimers as an excerpt (same as the
 existing copy rule). (The image model may not render Korean text cleanly, so the actual caption is usually
 added in post — but the prompt preserves the original.)
 - **Subject identity:** do not make a *photographic-level face replica* of a specific real person / celebrity
 (likeness / publicity rights). Instead, use a type ("a Korean woman in her mid-20s, calm confident"). If tone,
 lighting, and direction match, the feel is reproduced — the premise is the studio shoots / generates with its
 own model or talent. (A person's name appearing in the caption original is copy, so leave it.)
 - **Brand logo mark (visual symbol):** make a real logo *image* generic (trademark). A *brand name inside the
 copy text* is the caption original, so leave it as is.
- **Why "the original feel" still comes through:** an ad cut's "feel" comes not from the celebrity's identity but
 from **lighting direction / hardness / color temperature, lens / angle of view, composition, color grade, motion
 dynamics**. Preserve these precisely and the same tone, mood, and rhythm are reproduced even with an abstracted
 subject.

## 1. Field structure (per cut)

```json
"recreation_prompts": {
 "t2i_start_frame": "<t2i prompt recreating the start frame — English, ≥500 words per cut (target 500–650). If split / multi-panel, describe every panel>",
 "t2i_negative": "<negative prompt — model-agnostic common + cut-specific>",
 "i2v_motion": "<i2v prompt that moves that still with the original cut's motion — English>",
 "i2v_params": {
 "clip_duration_sec": <cut duration>,
 "camera_move": "<locked_off / push_in / pan_L...>",
 "subject_motion_level": "<still / micro / walk / dynamic>",
 "signature_effect": "<wiggle_3d / none...>",
 "pacing": "<static / steady / accelerating...>",
 "loopable": <bool>
 },
 "fidelity_note": "craft-faithful; identity/brand/on-screen-text abstracted (copyright-safe)"
}
```

- The goal is to embed t2i_start_frame + i2v_motion in **every cut** (preserve all). But the more key the cut
 (hook/cta/wow/key_visual), the more precise.
- The values are *synthesized* from the STEP 4.5 fields you already filled (see the §2 mapping below). Fill STEP
 4.5 first so you can assemble these without observing anew.

## 2. The t2i start-frame prompt — 12-part (+13 if split) structure (≥500 words per cut)

Weave the STEP 4.5/4 fields into one paragraph in the order below. Each part comes from *the value actually
filled on that cut* (don't invent). **Length is at least 500 words per cut (target 500–650).** At 300 words the
detail evaporates and it can't be implemented later — write each part out fully with *concrete figures,
directions, materials, ratios, color HEX*.

| # | Part | Source field |
|---|------|-----------|
| 1 | Subject & pose (abstracted) | `subject_action`,`pose_description`,`shot_scope`,`gaze` (identity removed) |
| 2 | Wardrobe / material | `texture.primary_subject`, wardrobe description (brand removed) |
| 3 | Location / set & background | `visible_elements.background/midground` |
| 4 | Foreground & props | `props`,`visible_elements.foreground`,`prop_semantics` (function only) |
| 5 | Lighting setup | `lighting.*` (direction/hardness/color_temp/ratio/rim/shadow/contrast) |
| 6 | Lens / framing / camera angle | `framing`,`camera_angle`,`camera_facing`,`shot_scope` (+ estimated angle of view) |
| 7 | Composition / grid | `layout_grid`,`subject_position`,`subject_typo_layout` (zone marking only) |
| 8 | Color palette & strategy | `color_analysis.palette_hex/role/relationship/accent`,`color_intent` |
| 9 | Texture & surfaces | `texture.*`,`visible_elements` surfaces |
| 10 | Atmosphere | `visible_elements.atmosphere`,`lighting.practical_lights` |
| 11 | Post / signature look | `production_signature` (capture_style, color_grade, texture_fx), `camera_effect_local` (e.g. wiggle depth) |
| 12 | Style anchor | one line of the photo/render genre (e.g. "clean 4K commercial, hi-key studio") + state nationality/culture |
| 13 | **Layout decomposition (split / multi-panel cuts only)** | `panel_layout` — if the frame is split/multi-panel/filmstrip/grid/PIP/collage, do each panel one by one: position (% from top-left), size ratio, each panel's content (abstracted), the divider between panels (gutter/line/none), the arrangement direction (row/column/grid RxC), and the caption original in the panel. Write it out so the model can draw "one frame = several scenes." |

**Writing rules**
- One paragraph (for a split cut, make the panel clauses long), clauses separated by semicolons and commas,
 **≥500 words per cut (target 500–650)**.
- **Split / multi-panel cut (Part 13)**: e.g. "a horizontal filmstrip of six equal panels separated by thin
 black gutters; panel 1 (leftmost, ~1/6 width, full height) shows …; panel 2 (next, ~1/6 width) shows …; …
 panel 6 (rightmost) shows …; the six panels read left-to-right as a rapid montage of …". Leave out none of each
 panel's position, ratio, content, and caption.
- If there's on-screen text, put the **actual original** from the entry's `copywriting` in, along with its
 position, typography, and color-box treatment (short copy and figures verbatim; only long disclaimers as an
 excerpt). No abstraction or placeholder.
- Brand colors as HEX (e.g. "brand-blue #2da1e7 dominant"). Preserve color and copy but make only the *logo mark
 (visual symbol)* generic.
- Time-dependent effects (wiggle_3d) can't be drawn directly in a still, so render them as *depth / parallax
 intent* (Part 11).

## 3. The i2v motion prompt — moving the start frame like the original cut

Feed the t2i result still as the **first frame** and apply the motion below. Synthesize from the cut's dynamic
fields.

| Motion axis | Source field | i2v expression |
|---|---|---|
| Subject motion | `subject_motion` | "near-static / micro-gesture / walking forward /..." (for a static pose, "hold pose, breathing-level only") |
| Camera move | `camera_motion`,`camera_motion_intensity` | "locked-off / slow push-in / handheld drift..." |
| Signature effect | `camera_effect_local`,`production_signature.camera_signature` | wiggle_3d → "subtle left-right viewpoint oscillation / lenticular parallax on edges, ~1–2px feel" |
| Prop motion | `prop_motion` | "prop lifts / rotates / floats in..." |
| Typography / graphic motion | `typo_motion`,`vfx_in_shot` | "headline pops in from right (placeholder text), 3D numeral inflates & color-shifts..." |
| Rhythm / length | `intra_cut_rhythm`,`duration` | "steady, ~2.0s, no cut" / "accelerating montage feel" |
| Motion blur / transition | `motion_blur`,`transition_out` | "light motion blur; ends on match-cut handoff to next shot" |

**Rule:** 1 cut = 1 i2v clip (the cut's length). Put camera + subject + effect + graphic motion into one prompt
*simultaneously*. If the `transition_out` to the next cut is flashy (whip_pan/match_cut, etc.), state that
handoff at the end (connecting to the transition board).

## 4. The t2i → i2v chain (restoring the original video's feel)

1. Generate a start-frame still with `t2i_start_frame` (image model).
2. Feed that still as the i2v model's first frame + `i2v_motion` (+ `i2v_params`) → a clip the cut's length.
3. Stitch the cuts together via `transition_in/out` (a transition board if needed, generated by the builder as a
 single canvas) and the original *rhythm, tone, and motion* are reproduced.
4. This result is also used as the input visual tone for the planner's cross-pollination (transformed into a new
 original).

## 5. Worked example (abstracted — no real names, logos, or verbatim)

### Example A — finance shortform hook cut (person beside a still object, frontal gaze, 3D wiggle)

`t2i_start_frame`:
> A confident Korean woman in her mid-20s seen from the waist up, resting her chin lightly on her right hand with a calm, self-assured to-camera gaze; she wears a structured navy silk-blend blazer (matte silk sheen), minimal styling, no visible logos; she is seated at a clean white table beside a single vibrant orange tulip arrangement in a glossy ceramic vase placed mid-ground to her side; plain teal-to-sky blue gradient studio wall behind (no signage); soft hi-key lighting with a large diffused key from 45° upper-left, gentle fill (key-to-fill ~2:1), no rim, soft short shadows, neutral 5500K; medium shot at eye level, frontal, ~50mm-equivalent look, shallow-to-moderate depth; rule-of-thirds with the subject centered-left and the recorded on-screen headline copy “원영이처럼 우월한 월급통장” set in a bold rounded sans-serif inside a brand-blue color box on the right third (white with emphasis lettering; typically finalized in post but preserved here for fidelity); muted high-contrast brand-blue-dominant palette (#6ab3cb background dominant, #29282d dark anchor, warm orange accent ~15% of frame for complementary pop); textures read as smooth silk fabric, glossy ceramic, matte gradient wall, natural lightly-retouched skin; calm, quiet, clean atmosphere with subtle ambient glow and no haze or grain; subtle retro-tech wiggle-3D parallax depth between the subject and the foreground vase (slight viewpoint offset suggesting lenticular dimensionality); clean digital 4K commercial production look, hi-key, polished but natural. Korean studio commercial aesthetic.

`t2i_negative`: "second person, extra hands, distorted fingers, real brand logos/marks, watermark, harsh shadows, low-key, grain, blur, deformed face" (leave the text out of the negative so the caption survives)

`i2v_motion`:
> Hold the opening pose with breathing-level stillness — the subject does not gesture, only the faintest natural micro-motion; camera locked-off; apply a subtle continuous left-right viewpoint oscillation (wiggle / lenticular 3D parallax) so the foreground vase and the subject's edges shift a hair against the background, giving retro-tech dimensionality; lighting and color steady; ~2.0s, steady rhythm, no cut; toward the end, the headline copy “원영이처럼 우월한 월급통장” settles into the right-third color box (finalized in post). Light, clean, no large motion.

`i2v_params`: `{ "clip_duration_sec": 2.07, "camera_move": "locked_off", "subject_motion_level": "still", "signature_effect": "wiggle_3d", "pacing": "static", "loopable": true }`

### Example B — finance shortform wow cut (3D balloon-figure typography reveal, color shift)

`t2i_start_frame`:
> A Korean woman in her mid-20s in a static, centered pose with a calm subtle smile, framed from the chest up, partly behind a large 3D inflatable balloon-style numeral reading “3.1%” (the recorded on-screen figure) floating at chest height in the foreground (a glossy puffed form); the balloon form carries a gradient that shifts from deep purple (#161761) at the top to bright brand-blue (#2da1e7) at the base, with soft reflective highlights; vivid solid brand-blue studio background, no signage; soft even frontal key light, minimal fill, almost no shadows, neutral 5500K, hi-key; medium shot, eye-level, frontal, ~35–50mm-equivalent, the 3D numeral occupying the upper-center foreground (~30% of frame); vivid saturated palette, brand-blue dominant with a purple-to-blue color-shifting accent on the balloon, white highlight glow; textures read as glossy inflated plastic/3D-render surface with reflective specular, smooth fabric on the subject, natural skin; clean, playful, retro-tech mood, no haze, no grain; subtle wiggle-3D parallax depth on the background behind the floating numeral; clean digital 3D-render-composited 4K commercial look, hi-key, glossy. Korean studio commercial aesthetic.

`t2i_negative`: "real brand logos/marks, second person, extra fingers, dark/low-key, grain, watermark, distorted balloon"

`i2v_motion`:
> The 3D balloon-style numeral inflates/scales in from chest level and settles, its gradient color-shifting from purple to brand-blue with glossy highlight travel; the subject holds a static pose behind it (breathing-level only); camera locked-off with subtle wiggle-3D parallax on the background; the side headline copy “우월~ 좋은데?” pops in briefly (recorded copy; finalized in post); ~1.7s, steady, no cut, ending on a clean cut handoff. Glossy, playful, hi-key.

`i2v_params`: `{ "clip_duration_sec": 1.73, "camera_move": "locked_off", "subject_motion_level": "still", "signature_effect": "wiggle_3d", "pacing": "steady", "loopable": false }`

## 6. Self-check
- Is t2i_start_frame **≥500 words per cut**? Did you fill the 12 parts (+ Part 13 if split) with *that cut's
 actual values* (zero invention)?
- For split / multi-panel cuts, did you spell out Part 13 (panel position, ratio, content, divider) in the t2i
 and also fill `panel_layout`? Is the `mid_frame_path` image in the dataset?
- Did no celebrity *face photo replica* or real logo mark get in? (Preserving the caption / copy original is
 correct.)
- Does the on-screen text match the copywriting original? (Short copy and figures verbatim, only long disclaimers
 as an excerpt.)
- Does i2v_motion reflect all of the cut's subject_motion, camera, effect, typo_motion, and duration?
- Did you move time effects like wiggle_3d into the i2v (only as depth in the still)?
- Do the length / camera move / signature effect match i2v_params?


---

# Appendix C — search_keywords English-token vocab (core, KO→EN)

Keep the KO alias alongside so the planner can match a Korean brief. **The stored value is the English token.**
(The technical axes framing/camera_*/vfx/transition/pacing/typo_motion are already English — REFERENCE/cut-schema.md.)

### industry
`telecom`←통신 · `finance`←금융 · `insurance`←보험 · `fashion`←패션 · `beauty`←뷰티 · `fnb`←F&B·식음 · `beverage_alcohol`←주류·음료 · `automotive`←자동차 · `home_appliance`←가전 · `mobility`←모빌리티 · `public_gov`←공익·정부 · `education`←교육 · `film_culture`←영화·문화 · `industrial_b2b`←산업B2B · `semiconductor`←반도체 · `construction_realestate`←건설·부동산 · `luxury`←럭셔리 · `healthcare_pharma`←헬스케어·제약 · `it_saas`←IT·SaaS · `content_ott`←콘텐츠·OTT · `retail`←유통·리테일 · `travel_tourism`←관광·여행 · `sports`←스포츠 · `sportswear`←스포츠·의류

### product_category
`salary_account`←월급통장 · `savings`←적금 · `card`←카드 · `mobile_banking`←모바일뱅킹 · `loan`←대출 · `insurance_product`←보험상품 · `data_plan`←요금제 · `pickup_truck`←픽업트럭 · `large_suv`←대형SUV · `hybrid_car`←하이브리드차 · `ev`←전기차 · `sedan`←세단 · `luxury_sedan`←럭셔리세단 · `apartment_presale`←아파트분양 · `same_day_delivery`←당일배송 · `beauty_platform`←뷰티 플랫폼 · `sportswear`←스포츠웨어 · `performance_runningwear`←기능성 러닝웨어 · `cosmetics`←화장품 · `apparel`←의류 · `sneakers`←운동화

### target_demo
`teens`←10대 · `20s`←20대 · `early_mid_20s`←20대 초·중 · `late20s_early30s`←20대 후·30대 초 · `30s`←30대 · `late30s_40s`←30대 후·40대 · `40s`←40대 · `50s_plus`←50대+ · `senior`←시니어 · `early_career`←사회초년 · `office_worker`←직장인 · `homemaker`←주부·맘 · `student`←학생 · `men`←남성 · `women`←여성 · `family`←가족·패밀리 · `family_end_users`←가족·실수요 · `couples`←부부·연인 · `single_household`←1인가구 · `mz`←MZ · `leisure_outdoor`←레저·아웃도어 · `running_fitness`←러닝·피트니스 · `active_consumers`←액티브 소비자 · `premium_buyers`←프리미엄 구매층 · `local_presale_prospects`←지역 분양 관심층 · `active_senior`←시니어 액티브

### media_format
`tvc_15s`←TVC 15초 · `tvc_30s`←TVC 30초 · `tvc_60s`←TVC 60초 · `shortform_vertical_30s`←숏폼 세로 30초이하 · `shortform_landscape_30s`←숏폼 가로 30초이하 · `shortform_vertical_30s_plus`←세로 숏폼 30초+ · `digital_30s`←디지털 30초 · `youtube_60s_plus`←유튜브 60초+ · `sns_viral`←SNS 바이럴 · `ooh_led`←OOH·옥외LED · `product_hero_film`←제품 히어로 필름 · `presale_lifestyle_film`←분양 라이프스타일 필름 · `cinemascope_lifestyle`←시네마스코프 라이프스타일 · `feature_demo_film`←기능소구 필름 · `pt_video`←PT·키노트 영상

### tone
`cinematic`←시네마틱 · `cinematic_serious`←시네마틱 시리어스 · `cinematic_luxury`←시네마틱 럭셔리 · `punchy_humor`←펀치·유머 · `friendly`←친근 · `warm_emotional`←감성·따뜻함 · `emotional_lyrical`←감성·서정 · `premium`←프리미엄 · `luxury_minimal`←럭셔리·미니멀 · `luxury_highend`←럭셔리·하이엔드 · `serious_classic`←시리어스·정통 · `serious_documentary`←시리어스·다큐 · `kitsch`←키치 · `retro`←레트로 · `calm_refined`←차분·정제 · `confident`←당당·자신감 · `relaxed_healing`←여유·힐링 · `family`←가족 · `empathetic_comforting`←공감·위로 · `upbeat`←경쾌 · `clean_minimal`←깔끔·미니멀 · `dynamic_powerful`←역동·파워 · `refreshing`←청량·상쾌 · `determined_focused`←결연·집중 · `mystery_teaser`←미스터리·티저

### technique
`celeb_hook`←셀럽 후크 · `anthropomorphism_character`←의인화·캐릭터화 · `time_freeze`←시간정지·동결 · `transformation`←변신 · `omnibus_series`←옴니버스·시리즈 · `oner_walking_shot`←1테이크·워킹샷 · `splitscreen`←분할화면·split · `teaser_mystery`←티저·미스터리 · `mirroring_contrast_edit`←미러링·대비편집 · `world_builder`←세계관 빌더 · `call_and_response`←콜앤리스폰스 · `balloon_typo_3d`←풍선타이포·3D · `filmstrip_collage`←필름스트립·콜라주 · `color_shift`←색 변환 · `bw_color_shift`←흑백↔컬러 톤전환 · `glitch_crt`←글리치·CRT · `facade_ooh_meta`←파사드·OOH 메타 · `morph`←모핑 · `landscape_travelling`←풍경 트래블링 · `overhead`←부감 · `kinetic_typo`←키네틱 타이포 · `silhouette_teaser`←실루엣 티저 · `dark_to_light_reveal`←어둠에서 빛 리빌 · `detail_closeup`←디테일 클로즈업 · `signature_lamp_ignition`←시그니처 램프 점등 · `product_solo_hero`←제품 단독 히어로 · `anaphora_copy`←애너포라 카피 · `lifestyle_cg_intercut`←라이프스타일+CG 교차 · `nature_intro`←자연 인트로 · `low_angle_tiltup`←로우앵글 틸트업 · `location_map_graphic`←위치맵 그래픽 · `empathy_copy_hook`←공감 카피 후크 · `product_app_cutout_float`←제품·앱 컷아웃 부유 · `dissolve_montage`←디졸브 몽타주 · `direct_cta`←직접 CTA · `slowmo_explosion_start`←슬로모 폭발 스타트 · `fabric_macro_proof`←원단 매크로 기능증명 · `product_solo_feature_demo`←제품 단독 기능소구

### copy_strategy_keywords
`product_name_pun`←제품명 펀 · `brand_name_pun`←브랜드명 펀 · `refrain_repetition`←후렴 반복 · `call_and_response`←콜앤리스폰스 · `neologism_slogan`←신조어 슬로건 · `question_hook`←의문형 후크 · `imperative_slogan`←명령형 슬로건 · `model_name_drop`←모델 이름 박기 · `place_city_drop`←지명·도시 박기 · `bilingual_subtitle`←영문+한국어 자막 · `number_emphasis`←숫자·수치 강조 · `building_climax`←점층 클라이맥스 · `caption_led`←캡션 주도 · `voice_caption_sync`←음성·자막 동기화 · `leadership_declaration`←리더십 선언 · `spec_caption_split`←스펙 자막 분리 · `new_model_naming`←신차 네이밍 고지 · `double_wordplay`←더블 워드플레이 · `facility_subcopy_match`←시설 서브카피 매칭 · `location_equation`←입지 등식 · `empathy_to_solution`←공감→솔루션 전환 · `immediacy_emphasis`←즉시성 강조 · `brand_green_keyword`←브랜드 그린 키워드 · `superiority_declaration`←우위 선언 · `feature_benefit_direct`←기능 베네핏 직설 · `visual_copy_proof`←비주얼로 카피 증명

### concept_derivation_pattern (handbook 12 + extensions)
`celeb_fashionfilm`←셀럽+패션필름st · `time_bridge_metaphor_device`←시간 잇는 메타포 장치 · `call_and_response_copy`←콜앤리스폰스 카피 · `giant_character_world_builder`←거대 캐릭터·세계관 · `metaphor_visual_sequence`←메타포 비주얼 시퀀스 · `teaser_mystery_concept`←티저·미스터리 컨셉 · `teaser_mystery_payoff`←티저·미스터리 회수 · `highend_fantasy_fusion`←하이엔드 판타지 결합 · `series_omnibus`←시리즈 옴니버스 · `three_part_time_flow`←3파트 시간 흐름 · `breaking_fourth_wall`←제4의 벽 넘기 · `space_structure_illustration`←공간·구조 일러스트 · `symbol_character_fusion_3d`←심볼+캐릭터 융합 3D · `everyday_problem_metaphor_product_release`←일상 문제→비유→제품 해방 · `dark_to_light_reveal_structure`←어둠→빛 리빌 구조 · `detail_to_whole_reveal`←디테일→전체 공개

> For a value not in the table, use the closest token; if new, add `English token ← Korean` here. The full /
> technical-axis vocab is in `lsb-treatment-builder/REFERENCE/keyword-vocabulary.md` (when present).
