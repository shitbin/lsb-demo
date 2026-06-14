# VFX in the board — per-type visualization (image stage)

Post-production VFX is shown in the still as **one line of concrete visual description** (never abstract
wording like "added in post"). The board makes the client *see* the effect in 5 seconds; the actual
motion happens at the video (i2v) stage.

| VFX token | How to render it in a STILL (one visual line) |
|---|---|
| `time_freeze` | colors stay normal, only motion frozen — "everyone alive, normal, paused mid-motion; the protagonist sharp and warm while the crowd holds still" (NOT grey statues / corpses). |
| `color_pop` | one saturated brand color in an otherwise near-desaturated frame — "only the orange jacket is saturated; street muted." |
| `wiggle_3d` / parallax | cannot show motion in a still — render the *intended depth*: "strong foreground/background separation, slight lenticular depth, subject popping off a softly blurred plate." |
| `lens_flare` | "anamorphic horizontal flare streak across the upper third from a warm off-screen key." |
| `dust` / `atmosphere` | "fine dust motes / haze catching the backlight, volumetric light shafts." |
| `glitch` / CRT | "subtle RGB-split fringing and one scanline band — restrained, not a full broken screen." |
| `split_screen` | a panel_layout, not a VFX — see scene_board panel/`panel_layout`. |
| `3d_render` typography/number | draw only the **shape** of the 3D balloon numeral/word (e.g. "glossy inflated 3D '2X' form"); the actual text is handled per typo_mode (G5) — if baked, write the verbatim text; numbers/Latin bake reliably. |

Rules: keep it physical (a real light/optics logic), one line per effect, never "post-production" as a
word in the prompt. For text-bearing VFX, follow GATE G5 (bake the verbatim copy; do not suppress text).
Time-dependent effects (wiggle, motion blur) are realized at i2v — carry them in `i2v_params`.

*Version: lsb-image-crafter_260614_v1 · new stub (was referenced but missing). Keep in sync with
prompts/scene_board.md principles 6 & 8 and REFERENCE/typography-in-image.md.*
