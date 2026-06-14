# Photographic Treatment — kill the "AI look" in generated stills

> Applies to every image this skill generates (key visuals, character sheets, scene boards, cuts).
> Goal: turn generic "AI-looking" images into editorial / photographic stills that look real.
> ⚠️ Never put sexual/NSFW blocker words in the negative prompt (they trigger moderation and block
> generation). Anti-AI negatives like "plastic skin" are fine.

## Why images look AI-generated
The usual style block is just `Style: cinematic photographic look, 4K quality.` That tells the model
"just make it pretty" — so it fills in the most average default, which reads as AI. Decisions, not
adjectives, are what make an image look real.

**Ten AI tells (if you see these, it failed):** waxy plastic skin with no pores; over-symmetry /
subject dead-center; flat uniformly-bright lighting with no shadows; HDR/clarity overdrive,
over-saturation; everything in focus (no lens); dead glassy eyes, stiff front-facing smile;
stock-photo composition (centered, facing camera); no medium identity (neither film nor digital — a
"render"); the most predictable obvious visual; too-clean environment (no lived-in texture).

## The fix: shooting specs, not adjectives
Ban evaluative adjectives ("beautiful, high quality, cinematic, 4k"). Instead bake the decisions a real
photographer makes on set: film stock / lens / lighting setup / grain / color grade / composition bias /
intentional imperfection / reference aesthetic.

## `photographic_treatment` — an 8-field axis (add to keyword-vocabulary.md)
Stamp these eight fields on each cut. The planner maps the cut's `tone` to one of the presets below and
fills them in automatically.

| field | example tokens |
|---|---|
| medium | `kodak_portra_400` / `cinestill_800t` / `fuji_pro_400h` / `ilford_hp5_bw` / `kodak_gold_200` / `digital_clean` |
| lens | `35mm_f1.8` / `50mm_f1.4` / `85mm_f1.4` / `vintage_helios_swirl` / `anamorphic_2x` |
| light_setup | `single_window_softlight` / `golden_hour_backlight` / `hard_directional_chiaroscuro` / `practical_neon_night` / `overcast_softbox_sky` |
| grain_texture | `fine_film_grain` / `heavy_grain` / `clean` + `subtle_halation` |
| color_grade | `muted_editorial` / `warm_faded` / `teal_shadow_warm_skin` / `desaturated_filmic` / `high_contrast_bw` |
| comp_bias | one or two of the 7 composition laws (see REFERENCE/composition-principles.md): `rule_of_thirds` / `golden_ratio` / `leading_lines` / `framing` / `symmetry` / `depth` / `fg_mg_bg` — plus modifiers `off_center` / `negative_space` / `candid_unposed`. Avoid dead-center unless authority is intended. |
| imperfection | `lens_vignette` / `chromatic_aberration` / `gate_flare` / `dust_specks` / `motion_blur_slight` |
| ref_aesthetic | `editorial_fashion` / `documentary_reportage` / `film_still_cinema` / `lifestyle_kinfolk` (no stock photo) |

## Six presets (drop the whole snippet into the image prompt's Style block; planner picks by tone)

**P1 · Film documentary (warm, human)** — warm_emotional / friendly / family
```
Shot on Kodak Portra 400, 35mm f1.8 prime, single soft window light from frame-left.
Fine natural film grain, subtle halation on highlights. Muted editorial color grade, lifted blacks,
warm skin tones, desaturated background. Real skin with visible pores and micro-texture, not retouched.
Off-center composition, candid unposed gesture, gaze off-camera. Deep natural shadows (chiaroscuro, not flat).
Looks like a documentary film still — NOT a 3D render, NOT stock photography, NOT a beauty ad.
```

**P2 · Cinestill night (moody urban / neon)** — cinematic / mystery_teaser / dynamic_powerful
```
Shot on CineStill 800T tungsten film, 50mm f1.4, practical neon night lighting.
Heavy halation glow around lights, visible grain, teal shadows with warm highlights.
Shallow focus, gentle bokeh, mild lens vignette and chromatic aberration. Rain-wet reflective surfaces.
Cinematic film still, moody and atmospheric. NOT clean digital, NOT HDR, NOT over-saturated.
```

**P3 · Faded editorial (airy, fashion)** — clean_minimal / premium / calm_refined
```
Shot on Fuji Pro 400H, 85mm f1.4, soft overexposed daylight (high-key but filmic).
Pastel faded color grade, airy, slightly blown highlights, low contrast. Fine grain.
Negative space, off-center subject, editorial fashion framing. Natural skin texture.
Like a magazine editorial film scan — NOT plastic, NOT symmetrical, NOT stock.
```

**P4 · High-contrast B&W (graphic, resolute)** — serious_classic / determined_focused / confident
```
Shot on Ilford HP5 Plus black-and-white film, 35mm, hard directional light, deep blacks.
Strong contrast, visible coarse grain, dramatic shadow shapes. Documentary reportage framing.
Real texture, candid moment. Film still — NOT a digital B&W filter, NOT flat, NOT clean.
```

**P5 · Golden-hour anamorphic (premium cinematic)** — cinematic_luxury / emotional_lyrical
```
Shot on anamorphic 2x lens, golden hour backlight, warm rim light, gentle horizontal lens flare.
Cinematic 2.39 feel, oval bokeh, soft halation, warm faded grade, slight haze in air.
Off-center, layered foreground/background depth. Premium film still — NOT CGI, NOT over-sharp.
```

**P6 · Product hero (real studio — no render)** — product cuts
```
Real studio product photography, 100mm macro, controlled soft light with ONE hard accent.
Genuine surface reflections, real micro-scratches and dust, true material texture (metal/fabric/glass).
Shallow focus on hero detail, dark gradient backdrop. Editorial product shot — NOT a 3D render,
NOT a glossy CGI mockup, NOT floating-in-void perfection.
```

## Style block in the image prompt — before → after
**Before:** `Style: Cinematic photographic look, 4K quality.`
**After:**
```
Style — {the P1–P6 snippet mapped from the cut's tone}:
- Brand accent: {brand color} is the ONLY saturated color in frame.
- Light: {preset lighting} reinforced by the cut's own lighting (key direction / hardness / color temp).
- Texture: render the cut's surfaces as real (keep pores, fabric weave, surface imperfections).

Anti-AI (avoid): waxy plastic skin, over-smoothing, HDR clarity, perfect symmetry, everything-in-focus,
dead glassy eyes, over-saturation, centered stock-photo framing, airbrushed perfection.
```

## Calibration
v1 is the general-photography baseline. Calibrate against the director's own reference images
(the moodboard library, REFERENCE/moodboard-library.md) to lock which preset matches their taste, then
commit it as the default for that tone.

---
*Source: the 0613 anti-ai rulebook, translated and folded into the skill. Used by the image-generation
path (scene_board.md) and selected per cut by the planner.*
