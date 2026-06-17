# Data contract — cut_plan.json (in) · stills.json (out)

The pipeline passes structured JSON between stages so nothing is lost in prose. The image-crafter
**consumes `cut_plan.json`** (from the planner) and **emits `stills.json`** (for the deck + video).

## cut_plan.json  (lsb-ad-planner → lsb-image-crafter)

```jsonc
{
  "project": "LSB_Carrot_PerHour_15s",
  "brand": { "name": "Carrot", "primary_hex": "#F54200", "product_lock_asset": "uploads/app.png|null" },
  "aspect_ratio": "9:16",
  "moodboard_bucket": "05_필름그레인_인물무드",     // bucket key from REFERENCE/moodboard-library.md
  "characters": [
    { "id": "protagonist_main",
      "master_brief": "Korean man, early 20s, ordinary friendly face, off-white tee under warm-orange coach jacket …" }
  ],
  "key_visual": {
    "photographic_preset": "P5",
    "composition": ["rule_of_thirds", "leading_lines"],
    "eye_path": "headline(top) → face → key fob",
    "typo_mode": "baked",
    "baked_text": "운전하기 전, 캐롯 먼저",
    "visible_elements": { "foreground": ["key fob mid-air"], "midground": ["protagonist half-smile"],
                          "background": ["blurred golden-hour street"], "lighting_env": ["warm backlight"],
                          "atmosphere": ["soft haze"] }
  },
  "cuts": [
    { "no": 1, "subject_identity": "protagonist_main",   // = the planner's per-cut subject_identity (id from character_pool)
      "framing": "MS", "camera_angle": "eye_level", "camera_facing": "three_quarter",
      "shot_scope": "waist_up", "subject_action": "friend flicks a car key fob to him; he catches it, startled",
      "pose_description": "both hands up catching", "gaze": "at the fob", "props": ["black car key fob"],
      "composition": ["rule_of_thirds"], "eye_path": "friend(left) → fob → protagonist(right)",
      "photographic_preset": "P1",
      "typo_mode": "none", "baked_text": null,
      "visible_elements": { "foreground": ["key fob arc"], "midground": ["two young men"],
                            "background": ["small city cafe storefront"], "lighting_env": ["soft daylight"],
                            "atmosphere": ["candid energy"] },
      "color_intent": "warm orange single-color pop on near-neutral street",
      "texture": "fabric_cotton, concrete",
      "vfx": "none",
      "recreation_prompt": "<optional long t2i base from analyzer cross-pollination>"
    }
    // … one object per cut
  ]
}
```

Required per cut (image-crafter gates check these; **names match the planner's STEP 4 (B) cut fields
exactly**): `framing, camera_angle, camera_facing, shot_scope, subject_action, pose_description, gaze,
props, composition (1–2), eye_path, photographic_preset, typo_mode, baked_text, visible_elements
(foreground/midground/background/lighting_env/atmosphere), color_intent, texture`, plus `subject_identity`
on multi-character cuts. `moodboard_bucket` + `photographic_treatment` are global (STEP 4 (A)). Note:
`baked_text` = the cut's verbatim `copy_overlay` when `typo_mode=baked`; `photographic_preset` (P1–P6) is
tone-mapped from the global `photographic_treatment`. Missing → ask/fill, don't generate.

## stills.json  (lsb-image-crafter → lsb-treatment-builder / lsb-video-crafter)

```jsonc
{
  "project": "LSB_Carrot_PerHour_15s",
  "aspect_ratio": "9:16",
  "declined_preset_ids": ["24bae836-…"],            // accumulated, applied to every gen
  "master_sheets": [ { "character_id": "protagonist_main", "path": "assets/char_protagonist.png",
                       "media_uuid": "0b8fbf87-…" } ],
  "key_visual": { "path": "assets/kv.png", "ratio": "16:9", "typo_mode": "baked",
                  "baked_text": "운전하기 전, 캐롯 먼저", "baked_ok": true },
  "cuts": [
    { "no": 1, "role": "story", "path": "assets/확정컷/cut01.png", "ratio": "9:16",
      "media_uuid": "60348cca-…",
      "typo_mode": "none", "baked_text": null, "baked_ok": null,
      "gen_params": { "model": "gpt_image_2", "resolution": "2k", "quality": "high",
                      "moodboard_refs": ["uuid…"], "declined_preset_id": "24bae836-…" } }
    // … per cut
  ]
}
```

- `baked_ok`: informational, default `true`. Korean main copy / headline / CTA is **always baked**
  (user-set _260614 — gpt_image_2 renders Korean reliably; no attempt/fallback, no romanizing). `subtitle`
  is reserved only for long running subtitle lines / legal fine print.
- The deck uses `cuts[].path` for `cut_board` / `storyboard_grid`; the video uses `media_uuid` for i2v
  `medias`. Both reuse the SAME declined_preset id list.
- **Re-send = reuse, not regenerate.** If `stills.json` already lists a verified path, downstream stages
  reuse it; do not re-run `generate_image` for the same cut.
