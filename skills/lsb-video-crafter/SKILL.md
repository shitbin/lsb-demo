---
name: lsb-video-crafter
description: >-
  LSB Production video-generation (i2v) skill. Takes the treatment produced by lsb-treatment-builder
  (treatment.json + the locked-frame board + per-character master sheets) and turns each cut into a
  motion clip using an image-to-video model (e.g. Seedance 2.0), then joins the clips into the final
  ad video. Handles multi-character / cross-cutting (cut-montage) structures by splitting clips per
  person/space segment. Adds Korean voice-over (VO) and animated brand motion-typography, but never
  bakes on-screen subtitles. When the video tool refuses a generation because it detected real
  brand/celebrity likeness (status `ip_detected` — an "IP moderation block"), it stops and uses the
  user-approval protocol. Use this skill whenever the user says (Korean trigger phrases kept):
  "영상으로 뽑아줘" (make it into video), "이 컷 영상화해줘" (turn this cut into video), "i2v 클립 만들어"
  (make an i2v clip), "Seedance로 만들어" (make it with Seedance), "트리트먼트를 영상으로" (treatment to
  video), "30초 광고 영상 결합" (assemble a 30-second ad), or hands over a treatment/storyboard and asks
  for video production. Concept and planning belong to lsb-ad-planner; the treatment PDF and boards
  belong to lsb-treatment-builder, so this skill does not redo those.
---

# lsb-video-crafter — LSB ad video-generation skill

This is the stage that turns locked frames (the board stills) into motion clips and joins them.
**This is the expensive stage (it spends credits) — always get explicit confirmation before starting.**
It used to be Phase 7 of lsb-treatment-builder, but the treatment skill grew too large so it was split
out (the builder's core job is the PDF).

> No prior context? Read `005_skills/GLOSSARY.md` first — it defines every shared term (i2v/t2v, seamless transition, IP moderation block, preset hijack, motion typography, etc.).

## Input / Output
- **Input (produced by builder/planner):** `treatment.json` (containing `global`, `cuts`, `transitions`,
  and especially `narrative_structure`, `character_pool[]`, and each cut's `subject_identity`) +
  `확정컷/` (the locked-frame board stills) + per-character master sheets + the product-lock product
  images.
- **Output:** `video[_onetake]/` (one mp4 per clip) · `{project_name}_length.mp4` (the joined final
  video) · `seedance_prompt*.md` (the prompts). After joining, do QA by extracting frames.
- Characters (especially a brand mascot or a real product) follow the same rule as planner R4: do NOT
  generate them yourself — use the user's official asset / supplied file as the reference.

## STEP 1 — Read structure and characters (do this first)
Read `narrative_structure` and `character_pool[]` from `treatment.json`.
- `linear_continuous` (one continuous space): one clip can hold several beats.
- `cross_cutting_montage` (same moment, different spaces, intercut): **split clips per space/person
  segment (STEP 2).** Do not force everything onto one continuous path of movement — that was the
  direct cause of the multi-character mixup, where the protagonist was shown *walking from a crosswalk
  into a cafe* and paying in person, the exact opposite of the treatment.
- Use each cut's `subject_identity` to confirm *who appears in which cut*. A protagonist cut is not the
  same as a cut featuring a different person.

## STEP 1.5 — Generation mode: i2v (default) / t2v (option)
The default is **i2v** (animate the locked-frame stills). However, if the manager (the system) offers
the user a **t2v option** and the user **chooses t2v**, switch to the following:
- Do **not** lay the locked-frame stills down as start/end/image. Instead put **only the
  strictly-necessary brand-asset / character references** into `medias` (only what is essential to lock
  IP and identity — the product label, the brand mascot, the protagonist master sheet, etc. — usually
  1–3 images).
- Call `generate_video` in **t2v mode** (no start_image; the text prompt drives it). The prompt is the
  same as STEP 4: **full 4000-character spec** (since there is no still, describe space, action, people,
  and layout even more densely).
- Everything else (15-second chunks, **seamless transition always**, **brand motion-typography
  required**, Korean VO, concat, QA) is identical to i2v.
- t2v has lower fidelity to the cut still, so in STEP 8 QA scrutinize product-label and character-identity
  matching especially hard (if it drifts, add only the key references and regenerate).

## STEP 2 — Splitting clips (split montages · overrides the "4000-char single clip" assumption)
If you cram all 12 beats of a sequence into one clip, the model will statistically drop some of them
(in the multi-character mixup it dropped the whip-pan and the time-freeze). Therefore:
- **Total length → split into 15-second-max chunks · minimize the number of generations (★).** A single
  Seedance clip is at most **15 seconds**. Divide the user's requested total length into 15-second
  chunks but **minimize the count**: 30s = 15+15, 35s = 15+15+5, 18s = 15+3, 45s = 15+15+15, 60s = 15×4.
  **Do not generate one clip per cut** — a single clip (up to 15s) holds the several cuts/beats of that
  span. Only the leftover remainder becomes a short clip (minimum 4 seconds; if under 4 seconds, make it
  4 and trim).
- **Seamless transition applies unconditionally (★ no exceptions · all lengths 15/30/45/60s):** when
  you join clips, the **last frame of the preceding clip must equal the first frame of the following
  clip** (extract the preceding clip's actual last frame with ffmpeg → feed it as the next clip's
  `start_image`, STEP 3 and STEP 7). Design so that motion direction, color, and camera movement do not
  break between cuts. **The only exception is the single cut the user has explicitly instructed to be a
  "hard cut"** (an intentional abrupt jump). Otherwise never skip seamless.
- **`linear_continuous`:** keep the full 4000-character prompt (STEP 4 below) per 15-second clip. For
  30s, that's 15s × 2.
- **`cross_cutting_montage`:** **split into a separate clip every time the space/person changes**, and
  join with ffmpeg. Example (the multi-character mixup): crosswalk intro (protagonist) / cafe payment
  (a different customer) / crosswalk time-freeze / cafe time-freeze (the barista, extractor liquid
  overflowing) / protagonist close-up → brand stinger → punch line. Each clip receives only the
  reference for its own space and person.
- ⚠️ **Minimum clip length = 4 seconds** (Seedance duration is 4–15s). A 3-second clip cannot be
  generated — if a segment is short, set it to 4 seconds and trim in post.
- Intent fidelity becomes incomparably higher, but credits go up — tell the user the split plan and the
  expected clip count, and get confirmation.
- **Layered collage cuts (pieces overlaid on a base — the GMA-2018 style) are NOT animated as one whole
  image via i2v.** Treat the base clip and the piece PNGs as **separate layers** and composite them
  with ffmpeg `overlay` (time-staggered `enable`, `scale`, `rotate`, `fade`), or give each piece a short
  motion and then composite. Control opacity, scale, position, crop, slight rotation, and parallax
  separately per piece → the whole reads as one collage frame while keeping a layered feel and editing
  rhythm. The sources (base + pieces) come straight from what the builder made in its steps 1 and 2.
  Shared rules: `lsb-treatment-builder/REFERENCE/layered-collage-protocol.md` (step 3).

## STEP 3 — Per-person / per-space reference grouping (medias ≤ 9 slots)
Put **only that clip's people and space** into the clip's reference slots.
- Multiple characters: a protagonist clip gets only the protagonist master sheet; a cafe clip gets only
  the cafe-person sheet. Do not mix the protagonist sheet into a different person's cut (this prevents
  the multi-character mixup degradation).
- Composition: `start_image` (first cut) + `end_image` (last cut) + `image` (a few key middle cuts) +
  a contact sheet (English labels). **Because seamless is the default, extract the preceding clip's
  actual last frame with ffmpeg and use it as the next clip's start_image** (do not use a static hinge
  image — it causes mismatch).
- **9-reference limit — 4 or more is stable. Too many (greedily filling all 9) can cause generation to
  fail, so lead with the essentials.** The values are cut job_id / media_upload UUID / https URL.
- **Product fidelity (product-lock):** for real products and labels, lock the user's official image as a
  reference + add to the prompt "the real label is always shown accurately" + add the negative
  "no unlabeled / empty bottle / label-less product" (same rule as builder Phase 3.2).

## STEP 4 — Writing the prompt
- **Length (★ hard minimum 4000 characters · do not submit under-length · do not ignore):** every i2v/t2v
  prompt is **at least 4000 characters per 15-second clip**. Structure: one-take/cut declaration →
  character lock → color/grade → per-beat timecoded motion, camera, transition → sound → Korean
  narration → **brand motion-typography** → text rules → negative → art direction. **Right before
  submitting, count the prompt's characters yourself, and if it is under 4000 characters, add more beat
  description until it exceeds 4000, and only then submit (never submit while under-length).** Short
  montage segments split out (4–5 seconds) are written at the *same density* but with a minimum of 1500
  characters. A thin one- or two-sentence prompt is the direct cause of dropped cuts and low quality —
  do not skip this rule.
- **CRITICAL — front-load the make-or-break beats (lesson from the multi-character mixup):** beats that
  break the concept if missed (a transition, a time-freeze, "this cut is a different person", etc.) get
  pinned **separately at the very top** of the prompt one more time. Example:
  ```
  CRITICAL — DO NOT SKIP:
  - (4-5s) MUST be a whip pan, NEVER a hard cut, hold FULL 1 SECOND
  - this action is performed by a CAFE CUSTOMER, NOT the protagonist
  - (11-13s) the freeze MUST be visible on screen, hold FULL 2 SECONDS
  [then the main body prompt]
  ```
- **Text policy + brand motion-typography required (★ frequently omitted — do not ignore):** do not bake
  on-screen subtitles or narration into the video. The only text shown on screen is **brand
  motion-typography** (slogan, logo lockup, key numbers). **Every clip must specify at least one piece
  of brand motion-typography in the prompt — slogan / CTA / number beats must always include it. Do not
  submit a prompt that is missing motion-typography (check every time).** Describe how it appears and
  animates (position, timing, in/out motion, font weight). Write narration as a **Korean VO spec, with
  the Korean dialogue in Hangul script** in the prompt (Seedance generates the voice). In the negative,
  put "no subtitles/captions/lower-thirds, only intended brand motion-typography". Korean stays in
  Hangul — no romanized phonetic spelling (R5). **Do NOT put sexual/suggestiveness blocker phrases (no
  nudity · no sexual content · NSFW, etc.) in the negative — they actually trigger moderation and become
  the bottleneck that blocks generation.**
- **Exact action + concretize human motion (★ prevents preset videos):** write the beat's action as the
  *exact real action*. Example: cafe payment = "card tapped on the POS terminal" (NOT placing something
  on the extractor — that was the multi-character-mixup error). Do not arbitrarily reinterpret the
  treatment's actions. **For any cut where a person appears, pin the person's movement concretely —
  starting pose → action (hands, feet, head, gaze, expression) → speed, direction, and end pose. If you
  leave the action blank, then: ① the model fills the empty action information with a learned *generic
  default motion* (the movement that is statistically common in such a scene) and it comes out flat, or
  ② the prompt's keywords resemble a particular preset and the platform similarity-matches it, then
  layers that preset on (forced through with STEP 5's `declined_preset_id`). In neither case is the
  model or platform "understanding" your intent and changing it — it's because of the blank field or
  keyword similarity-matching, which is why you get a "preset video" that differs from your intent (an
  observed problem). For static cuts too, specify a micro-motion like "subtle breathing, slight head
  turn".**
- **Transition direction:** pin *both* the camera direction (per `direction_observer_view`) and the
  on-screen streak direction (e.g. "camera rotates right → world streaks LEFT").
- **Token hygiene (saves context · separate from the 413 issue):** **write each prompt once and pass it
  to the tool call**, and in later turns do not re-quote or repeat the whole prompt (report only cut ID,
  completion, and file size). Store the final prompt as a `seedance_prompt*.md` **file**. (The 413 error
  is caused by images, not prompts — this is purely for token/cost savings.)

## STEP 5 — Generation and operation (Seedance 2.0)
- **Audio is generated** — response params `generate_audio:true`. It generates music, SFX, and VO. Listen
  to the VO quality and swap the voice actor if needed.
- **mode = std / fast, those two only.** "Not fast" = "std" (high quality). There is no "pro".
- **Length:** duration 4–15s. Join 15s × 2 with ffmpeg `-f concat` (STEP 7).
- **Preset hijack (`declined_preset_id`) — decline by DEFAULT, not only reactively (LSB-001):** on **every**
  `generate_video` call, pass `declined_preset_id` carrying any preset IDs already seen this session (start
  with the known "IN THE DARK" preset and add more as they appear) so the platform cannot silently apply a
  preset. If a new recommendation pops up ("this prompt looks like preset X"), add that ID too and resend.
  **This can chain multiple times** — record each recommended ID and keep the running decline chain. Default
  posture = always declining; never rely on catching the recommendation after the fact. (Observed trigger
  keywords — *unverified, do not hard-block*: "ONE CONTINUOUS UNBROKEN SINGLE-TAKE", "vertical descent",
  "world freezes", "dark cafe interior". If hijacking is frequent, try substituting synonyms.)
- ※ The preset hijack (a recommendation) and the `ip_detected` below (an IP moderation block) are
  **different phenomena**. Do not conflate them.

## STEP 5.5 — Verify the output is authentic (★ never use a preset/sample/demo video as the deliverable)

Do not treat any clip as a deliverable **until you have confirmed it is a new generation from your own
job**. **A preset / sample / demo / template / gallery / example / preview video is never the final
deliverable under any circumstances** — during the preset-similarity-matching process (STEP 5) the
platform can surface an existing preset's preview/sample video as if it were your output (the flip side
of the preset hijack).

1. **No generation without a reference.** Every `generate_video` request must include a **real input the
   user approved** as the reference — i2v = the locked-frame still's real file / upload UUID / URL
   (start_image, medias); t2v = approved brand/character references (STEP 1.5). Do not send a request
   with an empty reference (and do not generate from an unapproved image either).
2. **On receipt, cross-check three things.** When you get a clip: ① **job id** — is this a job I
   requested and recorded? ② **output video url** — does it match the url returned when I queried that
   job id? ③ **reference usage** — are the medias/start_image, duration, and aspect_ratio I put in the
   request stamped into the job response's params unchanged? If any one of the three does not match, do
   not use that url.
3. **URL / length character check.** If the output url's path or filename shows tokens like
   `preset`/`sample`/`demo`/`template`/`gallery`/`example`/`preview`, or if the ffprobe duration is far
   off from the requested length, suspect a preset sample — discard that url, re-query by job id, and if
   there is no authentic output, **regenerate**.
4. **Final delivery (video_ready) = only the new-generation output url from my own job.** Never use a
   preset preview, tool preview, or example url in the join (STEP 7) or in delivery.
5. **Aspect-ratio hard-lock + post-generation verify gate (LSB-012 — the all-9:16 failure).** Put the
   campaign's `aspect_ratio` (from the brief/treatment) into **every** generate_video call, and after the
   clip returns, **verify the actual output with ffprobe** — `ffprobe -select_streams v:0 -show_entries
   stream=width,height` — and check width/height matches the requested ratio (16:9 vs 9:16). If it does
   not match, **regenerate** (do not letterbox/stretch a wrong-ratio clip into shape, and do not deliver
   it). Run this check per clip before STEP 7 join.

## STEP 6 — `ip_detected` protocol (★ no automatic retry)
If the `status` in a job-query response is the string **`"ip_detected"`** (an IP moderation block), that
generation is *not something I can unblock by changing the prompt* — the user must directly "allow" that
item in Higgsfield. Therefore:
1. **Stop immediately.** Do not first attempt extra retries or workarounds. (In the multi-character
   mixup, not knowing this led to 4 retries → wasted credits and time.)
2. **Tell the user** — including which generation is `ip_detected`.
3. The user allows that item in Higgsfield.
4. When the user signals "I allowed it / proceed again", retry/continue then.

> **Forbidden:** trying to bypass the filter by, e.g., lightening the tone (it's a baseless assumption and
> inappropriate under the terms of service). The likely trigger is real brand / real-person likeness, not
> tone.
> **Video-job status categories:** waiting / in_progress / **waiting-for-user-intervention (`ip_detected`)**
> / done / failed. `ip_detected` is neither a "permanent block" nor "something the AI can unblock" — it is
> a *waiting-for-user-action* state.

## STEP 6.5 — Content-filter FALSE-POSITIVE — bounded retry (LSB-008 · NOT the same as `ip_detected`)
A plain content-filter rejection (the model/tool refuses, but the status is **not** `ip_detected` and
there is **no** real brand/celebrity likeness involved) is usually an over-rejection. Do not retry it
forever, and do not retry it zero times either — bound it:
1. **Try once** with a light rephrase (reword the flagged phrase; keep meaning/intent identical).
2. If still blocked, **remove reference images one at a time** and retry (a reference can trip the filter).
3. **Maximum 3 attempts total.** If still blocked, **stop and report** to the user (state what was tried).
- Never strip the creative intent or bypass a genuine policy block to get through. If at any point the
  status becomes `ip_detected`, switch to STEP 6 (stop + user-allow) — that is a different thing.

### Render-wait protocol (★ no tool-call loop — fixes the 2606041430 critical defect)

Do **not** poll a long render (1080p 15s ≈ 15–20 min) by chopping it into short sleeps. Repeating a 30–60s
sleep dozens of times makes the polling explode to 40–60 calls, and you fall into a self-reinforcing loop
that only repeats announce-text like "now I'll check" (this actually happened). Follow the below **exactly**.

1. **Sleep long once.** 1080p 15s = `sleep 900` (15 minutes) **once**. No repeated polling at 30/60-second
   intervals. (Do not finely separate the wait task from the next task — an unavoidable wait is one long
   sleep.)
2. After waking, **check status once**. If still `in_progress`, sleep **once more** for the remaining
   estimated time (e.g. `sleep 300`) and re-check. **If you've checked the same status twice and it's still
   in progress, do not re-check more frequently — wait with one longer sleep.** Never repeat short re-checks.
3. **No announce-text.** If you're going to call a tool, **just call it** without announcing "now I'll do
   ~ / calling now / one moment". Keep any pre-call explanation to one sentence or less. The pattern of
   announcing but not actually calling is the seed of the loop.
4. Tell the user once at the start, just "the render takes ~N minutes, I'm waiting" (do not relay on every
   poll).
5. `job_display` has intermittent errors and status-transition delays, so recover by re-querying by job id.
   For multiple clips, **queue them all and wait once with a long sleep**, then collect them in a batch (do
   not poll per clip).

> Bottom line: **"Sleep long once, and call tools without announcing." sleep 900 > sleep 30 × 30.**

## STEP 7 — Joining (concat · force the pixel format)
**Do not make a separate "compressed master video" or "summary version".** Take the chunks split in STEP 2
(e.g. 15s + 5s) and **ffmpeg-join them into exactly one final video** and **save it as a file** in the work
folder (it must be saved to be delivered to the user · do not claim "done" without actually making the
video).

*Before* joining clips, confirm the two clips have the same format. If they differ, it breaks (in the
multi-character mixup, playback failed after 15 seconds — the front was yuv420p, the back yuv444p).
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt,profile,has_b_frames -of default=noprint_wrappers=1 clip1.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt,profile,has_b_frames -of default=noprint_wrappers=1 clip2.mp4
# If identical, lossless join:
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4
# If different, re-encode the second clip into the first's format, then join:
ffmpeg -i clip2.mp4 -c:v libx264 -pix_fmt yuv420p -profile:v high -level 4.0 -preset fast -crf 18 -c:a copy clip2_fixed.mp4
```
**When doing post-processing (overlay, drawtext, etc.) always specify `-pix_fmt yuv420p -profile:v high`.**
If you leave a PNG's RGBA as-is, ffmpeg falls into yuv444p and the concat breaks.

## STEP 7.5 — Required post-processing: VO + editorial subtitles (LSB-013/016)
After the join, run a required checklist (the brief's language decides which apply):
- **Voice-over present.** If the brief calls for narration and the generated audio VO is missing or poor
  quality, add it in post (TTS or recorded) over the joined video. Korean stays in Hangul; an English-VO
  brief gets English VO. Do not deliver a narration-brief video with no VO.
- **Subtitles = editorial overlay, never burned in (LSB-016).** If subtitles are needed, add them as an
  editing-layer overlay in post (so they can be re-edited), not baked into the generated frames. Long copy
  / legal lines are always overlay, never pixel-burned.
- This is a distinct, mandatory step — do not assume the generation step already handled VO/subtitles.

## STEP 8 — Pre-delivery checks (★ do NOT Read images/frames · program + user judgment)
**Do not load generated videos/frames/images into context with `Read`.** Image/frame base64 inflates the
request to tens of MB and is the main cause of **`Request exceeds the maximum size` (413)**. **Inlining bytes
into the conversation/tool payload at all is forbidden — the platform request cap is a fixed 32MB**; if the
transcript exceeds it the session dies. Always reference videos/frames only by file path, job id, or URL.
Automatic visual review is abolished; pre-delivery checks are **by program only**:
- Use `ffprobe` to verify duration, pix_fmt, and codec of each clip and the joined video (prevents broken
  playback after the join — STEP 7).
- Verify the joined **file actually exists and has a normal size** (0 bytes or a few KB means failure).
- **Authenticity check (STEP 5.5):** verify **every clip** used in the join is a new-generation output
  from my own job id — **zero** preset/sample/demo/template/gallery/example/preview urls, and reference
  input confirmed used.
- Self-check via the prompt text that the product label, the CRITICAL beats, the brand motion-typography,
  and the Korean VO were all included **in the prompt text** (do not open it as an image).
- **Aspect-ratio gate (STEP 5.5 #5):** ffprobe the joined video's width/height and confirm it matches the
  campaign ratio (16:9 / 9:16). Mismatch → do not deliver; fix at the clip level and re-join.
**Aesthetic/content judgment (is the label clearly visible · is it the right person · did the
motion-typography appear) is made by the user watching the video directly** — the agent does not read
frames to judge. If the user says "redo this clip", regenerate only that clip.

## Status label + delivery integrity (LSB-E01/E04/011/016 — CP-3)
- **One status label, single source of truth:** `[draft]` (사내 초안 — what this skill produces) →
  `[verified]` (a human reviewed it) → `[delivery]` (final hand-off). This skill's output is **always
  `[draft]`**. Never present a "verified/complete/final" claim and the draft notice at the same time —
  pick one, and for AI-generated output it is `[draft]`.
- **Do not over-claim completion.** Say "done" only after the file is actually saved and delivered; the
  delivery message always carries the draft notice (system prompt §7).
- **Resend = reuse, do not regenerate (LSB-011).** If the user asks for the file again / re-shares it,
  return the **already-produced** output (its saved path/URL). Do not regenerate a new video on a resend
  request. Keep each deliverable's path/job-id recorded so it can be re-handed without re-running. (A
  permanent hosting URL + artifact registry is an infra task for the console/site side.)
(Trade-off: instead of automatic visual review, secure quality by writing the prompt precisely — the
quality gap that visual review used to catch is small, and the gain of preventing 413 and token blowup is
large.)

## Do not do
- Cram a montage into one clip. When the space/person changes, split the clip.
- Retry on your own without telling the user on `ip_detected`. Stop and tell them.
- Break moderation via a tone bypass. (Against the terms; baseless.)
- Bake long subtitles or terms-of-service text into the video. Narration is VO; on-screen subtitles
  forbidden.
- Assume every cut is the protagonist. Follow `subject_identity`.
- Deliver a preset/sample/demo/gallery/example video as the result. The final is always **only the
  new-generation url from my own job id** (STEP 5.5). A generation request with no reference is also
  forbidden.
- Deliver "done" without ffprobe and file-existence checks. **But do not open images/frames with `Read`
  (prevents 413) — visual judgment is the user's.**

## Trigger keywords
"영상으로 뽑아줘" (make it into video) · "영상화" (turn into video) · "i2v" · "Seedance" · "클립 생성/결합"
(generate/join clips) · "30초 광고 영상" (30-second ad) · handing over a treatment and asking for video
production.

## Read alongside
- Input structure and character fields: `lsb-ad-planner` STEP 4 (character_pool, narrative_structure,
  subject_identity) · `lsb-treatment-builder/REFERENCE/cut-schema.md`.
- Boards, product-lock, master sheets: `lsb-treatment-builder` Phase 2 and 3.
- Typography handling: `lsb-treatment-builder/REFERENCE/typography-in-image.md`.

---
*Version: lsb-video-crafter_260614_v11 · 2026-06-14 KST. (version scheme = YYMMDD_vN; earlier inline _2606xxxx codes are legacy timestamps. v11 = **problem-summary doc gaps closed (CP-1/2/3)**: STEP 5 declined_preset attached by DEFAULT every call (not reactive, LSB-001); STEP 5.5 #5 aspect-ratio hard-lock + ffprobe post-generation verify gate (LSB-012); STEP 6.5 content-filter false-positive bounded retry (1 rephrase → drop refs → max 3 → stop, LSB-008, distinct from ip_detected); STEP 7.5 required VO + editorial-subtitle post step (LSB-013/016); status-label taxonomy [draft]/[verified]/[delivery] + resend=reuse-not-regenerate (LSB-E01/E04/011); STEP 8 aspect gate. Source: lsb production 문제점 정리/solutions.) Previous _2606101200 = STEP 8 **codifies the 32MB payload
cap** — inlining video/frame bytes is forbidden; reference only by file path, job id, URL.) Previous
_2606101000 = **STEP 5.5 output authenticity verification** — forbids using a preset/sample/demo/template/
gallery/example/preview video as the final deliverable, requires the real file/URL of a user-approved
image/cut as the reference input (no generation without a reference), requires a three-way cross-check on
receipt (job id · output url · reference usage), a url/length character check (on preset suspicion, discard ·
re-query · regenerate), final delivery (video_ready) of only new-generation output urls + linkage to STEP 8
authenticity check and the Do-not-do list. Previous lsb-video-crafter_2606081200 · 2026-06-08 KST.
(_2606081200 = ① 4000-character hard minimum · no under-length submission (self-count before submitting)
② brand motion-typography required in every clip + QA check ③ seamless transition unconditional (only the
cut the user explicitly marked a hard cut is excepted) ④ STEP 1.5 t2v option mode — on user choice, t2v
using only the strictly-necessary brand/character references instead of the locked-frame stills. ⑤ STEP 8
abolishes automatic image/frame Read review → ffprobe · file-existence · prompt self-check + user visual
judgment (prevents request 413 · token blowup) · no prompt re-quoting · file storage. ⑥ corrects the video
prompt unit to 4000 characters (was formerly 4000 words) · no sexual/suggestiveness blocker phrases in the
negative (moderation trigger) · concretize human motion in cuts where a person appears (prevents preset
videos).) Previous _2606051640 · 2026-06-05 16:40 KST. (_2606051640 = split total length into 15-second-max
chunks · minimize generation count (30=15/15, 35=15/15/5, 18=15/3) + forbid a "compressed master video" ·
single-concat final saved to file + forbid thin prompts (thousands of characters). Previous _2606051100 =
seamless transition made the default — for all of 15/30/45/60s the preceding clip's last frame = the
following clip's start frame, STEP 2 and 3 updated.) Previous _2606041430 = render-wait protocol — fixes the
tool-call-loop critical defect: sleep 900 once · no short polling · no announce-text · batch-wait for clips.
The "A14" lesson from the redesign-gap post-mortem (the past low-quality-first-build session). Previous _2606032044 = new skill, split out of builder Phase 7, lessons from the
multi-character mixup (multiple characters · cross-cutting · concat codec · ip_detected · preset chain).
_2606140000 = English rewrite + de-jargon (faithful, no content dropped).*
