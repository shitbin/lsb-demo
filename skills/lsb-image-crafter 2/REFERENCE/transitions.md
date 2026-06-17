# Transitions — per-type patterns (board apex + i2v motion)

A flashy camera-movement transition gets its OWN single-canvas board (see `prompts/transition_board.md`):
[end of cut N] | [apex] | [start of cut N+1]. This file describes how to render each apex in the still
and how it animates at the video (i2v) stage.

| transition | apex in the STILL (one visual line) | i2v motion (video stage) |
|---|---|---|
| `whip_pan` | "horizontal motion-blur streak across the frame, subject smearing left-to-right, near-abstract." | fast horizontal pan blur N→N+1. |
| `morph` | "the two subjects' silhouettes dissolving through each other, edges melting." | shape morph N→N+1. |
| `push_in` / `dolly_through` | "camera diving into a dark foreground object that fills the frame (a doorway / phone / mouth of shadow)." | continuous push through the dark object into the next scene. |
| `pull_out` | "the current scene shrinking into an object/window that becomes part of the wider next scene." | dolly back revealing the next context. |
| `360_spin` | "the world streaked into a circular motion-blur ring around the subject." | orbit spin N→N+1. |
| `match_action` / `match_cut` | "a shape/gesture in cut N aligned exactly with the same shape in cut N+1 (e.g. a round key ring → a round app button)." | the matched shape holds position across the cut. |

Rules: same world / lighting / protagonist (master sheet) across the three beats; not sliced into the
storyboard (stays whole on the transition page / feeds the transition clip). All 7 gates apply (G1
declined_preset, G2 ≥~5,000 chars per beat, G3 composition, G4 fg/mg/bg, G5 text policy, G7 model/preset
lock). See also `prompts/transition_board.md`.

*Version: lsb-image-crafter_260614_v1 · new stub (was referenced but missing). Pair with transition_board.md.*
