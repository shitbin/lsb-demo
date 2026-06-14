# Composition Principles — 7 laws for placing things on screen

> Used in TWO places: (1) the photographic look of generated stills (their internal composition), and
> (2) deck-page layout (which archetype, where the eye goes). Source: a card-news primer on visual
> composition, distilled for LSB use. Aligns with our existing rules (don't default to center, white
> space = frame, keep real optical/light logic).

## The one rule above the seven
A good frame is not "place things prettily." It needs: a single clear subject, a deliberate eye-path,
front/back separation, and a chosen balance-vs-tension. **Pick only 1–2 of the seven laws per frame** —
do not apply all of them at once.

## The seven laws

1. **Rule of thirds** — split the frame 3×3; put the subject on a line/intersection, NOT dead center.
   Eye tends to enter top-left. Put the most important thing off-center; separate headline / product /
   CTA into different cells. Token: `rule_of_thirds`. Use for: natural, informational, asymmetric balance.
2. **Golden ratio** — place the subject at the focal point of a ~1:1.618 spiral; size big vs small blocks
   ~1.6:1 instead of equal halves. Don't chase exact math — use it to avoid monotone equal splits.
   Token: `golden_ratio`. Use for: organic, premium, high-end feel.
3. **Leading lines** — lines in the frame (roads, architecture, an arm, a gaze, light, shadow, a type
   baseline) pull the eye to the subject; the convergence point is the focus. Diagonals = speed/tension;
   curves = elegance. On a deck the path is headline → key visual → evidence → CTA. Don't let lines run
   off-frame; converge them on what matters. Token: `leading_lines`.
4. **Framing** — surround the subject (a shape/box, a window, a door, a phone screen, negative space) to
   trap the eye. The frame must stay weaker than the subject. In premium work, imply the frame with light
   and white space rather than drawing a literal box. Token: `framing`.
5. **Symmetry** — mirror elements around a center axis for balance, formality, authority. Good for beauty,
   luxury, architecture, tech, brand-declaration. Full symmetry is stable but static — wake it with one
   small asymmetric accent. Token: `symmetry`.
6. **Depth** — make a flat frame feel 3D: overlap/layering, shadow, blur (further = blurrier), size
   contrast, perspective. Front = big and sharp, back = small and soft. Keep shadows consistent with one
   light source. Token: `depth`.
7. **Foreground / midground / background** — split the frame into three spatial layers for depth + story.
   Foreground pulls you in (a cropped object), midground holds the main subject, background gives context
   (place, mood, brand color, secondary type). Don't put strong info in all three — keep the midground
   subject clearest. Token: `fg_mg_bg`.

## How this wires into the pipeline
- **Image generation (biggest impact):** each cut carries a `comp_bias` from the photographic-treatment
  axis. Set it to one or two of the tokens above so the generated still actually composes that way (e.g.
  `rule_of_thirds` + `leading_lines`). See `photographic-treatment.md`.
- **scene_board prompts:** the Style/composition line names the chosen law(s) for that cut.
- **planner:** each cut gets a `composition` note (chosen law + the eye-path: headline → visual →
  evidence → CTA) so the intent is explicit before the image is made.
- **deck-page layout (treatment_deck archetypes):** the archetypes already encode composition
  (left-aligned hierarchy, center only for 1–2-line slogans, full-bleed KV, letterbox single hero).
  Use the seven laws to *justify* the archetype choice, not to override it. Center alignment is only for
  authority / static stability / frontality — never the default.

## Claude's check (run on every frame/page)
1. Is there one clear subject, and is it off-center on an intersection / spiral focal point (unless
   center is deliberately chosen for authority)?
2. Does the eye-path lead to the subject and on to the CTA?
3. Are foreground / midground / background (or overlap/blur/perspective) separated?
4. Is the balance-vs-tension the one you intended?

## Cautions
- Eye-distribution percentages (e.g. 41/20/25/14) and "top-left first" are practical heuristics, not
  universal constants — consider reading direction and medium.
- Golden ratio is a guide, not a requirement; not every good design is exactly 1:1.618.
- Composition never overrides the content's purpose, the medium's aspect ratio, the amount of text, or
  the brand's character.

---
*Distilled from the 7-law composition primer. Wired to photographic-treatment.md (comp_bias),
scene_board.md, the planner cut `composition` field, and treatment-deck-system archetype selection.*
