# RFD 1170 details: what the study found, and what it deliberately did not read

## Why cleanroom, and what that means here

`victor/gemma-avatar` carries no `LICENSE` and its card states none.
Absent a grant the default is all rights reserved, which is the same
finding RFD 1166 reached for the See-Through checkpoints and the same
rule the blocklist applies to `24yearsold/metricdepth3d_tmp`.

So this study read the **README, the card metadata and
`package.json`** — what components the thing is built from, which is
factual and stated by the author for that purpose. It did not read
`index.ts`, `src/app.js`, `src/avatar.js` or `src/s2s/*.js`, because
those are the integration and the integration is the part that cannot
be taken.

**That distinction is worth holding even when nobody is watching.**
Knowing which four public models somebody wired together is not the
same as taking their wiring, and the value here is almost entirely in
the former.

## The pipeline, as the author documents it

    you speak -> silero-VAD -> parakeet-tdt-1.1b -> gemma-4-31B-it
              -> Qwen3-TTS -> avatar speaks

Six components, and every one of them is separately licensed:

    component               licence      where it runs

    silero-vad              MIT          browser or host
    nvidia/parakeet-tdt     CC-BY-4.0    host
    google/gemma-4-31B-it   Apache-2.0   Cerebras, hosted
    Qwen3-TTS-12Hz 1.7B     Apache-2.0   host
    met4citizen/TalkingHead MIT          browser
    three.js                MIT          browser

**Only the glue is unlicensed.** That is what makes a rebuild cheap
rather than a research project: the parts are all obtainable under
their own terms and the missing piece is an evening of wiring.

## Convergence on the TTS, and how much weight it carries

RFD 1166 seated `Qwen3-TTS-12Hz-1.7B-CustomVoice` at 4 on the same day
this Space was read, chosen from the Qwen model index rather than from
anybody's example. Independent selection is weak evidence and it is the
useful kind — it says the artifact is discoverable and that a second
party building a voice loop reached for the same thing.

It says nothing about quality. Nobody here has measured it against
anything, and RFD 1166's `value` and `wanted` scores for that row remain
judgements.

## The two swaps, and why each is a swap rather than a preference

**Parakeet out, Qwen3-ASR-1.7B in.** Parakeet is CC-BY-4.0, which
clears the commercial bar and is not blocklisted — CC-BY-**SA** is the
blocked one, and the pose rule already admits CC-BY-4.0 sets with
citation metadata. So this is not a licence swap.

It is an acceleration swap. RFD 1169 establishes that Qwen3-ASR's
encoder is fixed-shape with every operator inside `DEVICE_OPS`, and no
such path has been established for Parakeet's TDT decoder, which is a
transducer rather than an encoder-decoder and whose loop is a different
shape again. One of these has a device half in this workspace's terms
and the other has not been looked at.

**Gemma 4 out, Qwen3-VL-8B in, and one correction falls out of it.**
`google/gemma-4-31B-it` is **Apache-2.0**. RFD 1155 abandoned Gemma 4
and the reasons it gave were the GGUF artifact carrying no graph and
autoregressive decode against fixed shapes — shape reasons, not licence
ones — so nothing there needs revising. Recording the licence anyway,
because "abandoned" invites a reader to assume the worst about a model
and this one is permissively licensed.

31 B is the operative number: at four bits it is roughly 17 GB against
8 GB of device memory, so it does not fit at any precision this part
offers. Running it on Cerebras answers that by not running it locally
at all, which is a different architecture from the one this workspace
is building.

**A hosted API is not blocklisted for inference.** CLAUDE.md blocks
hosted-API generators as a **corpus source**, because condition 1 cannot
be satisfied without a checkpoint. Talking to a remote model in a live
loop is passthrough and is not that. The reason to replace it is
independence and latency, not the blocklist, and saying otherwise would
stretch a rule past what it says.

## The lip-sync, which is the genuinely new part

TalkingHead is MIT and drives a glTF head from visemes with real-time
audio. Two things make it a good fit and the third — whether our
avatars carry the morph targets it needs — was the unknown at the
first draft. That check has run.

**Visemes are morph targets, and morph targets are data.** CLAUDE.md's
deployment rule allows skin weights, animation samplers and morph
targets in a glTF export and forbids runtime modifiers, drivers,
constraints and custom extensions. A viseme-driven head is the allowed
side of that line, which is not an accident — it is why the rule is
written that way.

**The Space ships `model-en-mixed.bin` and two minified vendor
modules**, `headworklet.min.mjs` and `headaudio.min.mjs`. Those are the
audio-to-viseme path and they are shipped minified with no stated
licence in the Space. Whatever they are, they are the part to replace
rather than reuse, and TalkingHead upstream is where to look for a
licensed equivalent.

**The morph-target check resolved.** ANNY does not carry viseme-named
blendshapes; it carries 52 facial-action blendshapes covering the FACS
action units, exposed in `3-interactor/anny/src/anny/models/facial_actions.py`
under `FACIAL_ACTION_LABELS`. Verified against the on-disk target
files at `3-interactor/anny/src/anny/data/faceunits01/targets/faceunits/*.target`.
The 52 shapes are enough to render every viseme by weighted sum — mouth
opening from `jawOpen`, lip rounding from `mouthPucker` + `mouthFunnel`,
lip closure from `mouthClose` + the `mouthPress*` pair, and so on.

**A phoneme-to-viseme-to-facial-action mapping ships as data**, at
`3-interactor/anny/src/anny/data/phoneme_viseme_facial_action.json`
(`interactor-anny#1`). Two-stage: an ASR-emitted phoneme picks a
viseme, the viseme selects a weighted subset of the 52 facial-action
blendshape identifiers, the lip-sync stage wires the resulting weights
into `anny_soma(...)` at the frame rate. Consistency asserted by
`test/test_phoneme_viseme_facial_action.py` (every blendshape name
exists in `FACIAL_ACTION_LABELS`, every viseme referenced in
`phonemes` exists in `visemes` keys, every weight sits in [0, 1]) with
a companion self-test planting one typo per rule per rule 2.

**The mapping's weight numbers are placeholders**, cited in the file's
own `weight_sources` note as derived from Oculus Lipsync and Preston
Blair public references. A real per-language measurement replaces them
in a refinement — the mapping ships as documented-placeholder, not
as-if-measured (rule 4 shape: a number without a baseline is not a
measurement, so the file names its baseline as the pending refinement).

## The body half, which that Space does not have at all

The Space animates a head. This workspace has the rest, and it is the
half the accelerator actually serves.

    source              path                              state

    live camera         rf-detr keypoints -> SOMA-X ->    rf-detr is at
                        ANNY                              rung 3, alone
    no camera           Kimodo-SOMA, with a LoRA          wrapper unwired

**Two motion sources, and the split is presence against authoring.**
A camera in the room makes somebody present -- their movement is theirs,
in real time, which is what "people are present to each other" means and
what mocap is for. Without a camera the motion has to be authored, and
that is Kimodo's job. They are not fallbacks for one another.

**The accelerated half is the body, and the host half is the voice.**
That falls out of what has been measured rather than from a preference:

    rf-detr keypoints    rung 3, the only model the DFC has accepted
    Qwen3-ASR encoder    operators clear, untranslated
    Qwen3-TTS backbone   autoregressive, does not compile
    the LLM              Qwen3-VL-8B NF4 + EditScore LoRA (RFD 1157);
                         autoregressive, does not compile; per-turn
                         cost measured in the tail section below

So the device carries the thing that must be low-latency and continuous
-- a body tracked every frame -- while the host carries the turn-taking
speech, which is bursty and tolerates more delay. That is a better
division than it would have been if chosen deliberately.

**SOMA-X to ANNY is already the sanctioned route**, and the blocklist
row for the SMPL family says so: `anny_from_soma` exists in RFD 1122's
`AlternativeTopology` list, so the retarget is a code path rather than
an intention. rf-detr emits keypoints, not a SOMA pose, and what sits
between them is RFD 1122's wholebody gap rather than anything new here.

## A LoRA on Kimodo is a much smaller thing than the retrain

RFD 1166 records that retraining Kimodo is blocked by its corpus:
BONES-SEED is behind an acceptance gate, so it is not licence-clean and
the retrain has no data. **A LoRA is not that, and the distinction is
worth stating because the two were nearly conflated.**

A retrain needs the original distribution, which is 288 hours nobody
here can read the terms for. A LoRA adapts a checkpoint that already
has it, and needs only the motions this workspace wants it to learn --
which is exactly what ANNY and SOMA's own pose library is, plus
constructed synthetic rendered deterministically from rigs held here.

Kimodo-SOMA is the shippable variant, NVIDIA Open Model Licence, which
explicitly permits derivative models and makes the maker their owner.
**So a LoRA is permitted, the base is licence-clean, and the data can be
our own.** None of the three blockers that stop the retrain apply.

What it does not fix is that the weftspun wrapper raises
`NotImplementedError` outside stub mode. The model is reachable and the
service around it is not, which RFD 1167 records as rung 0 with a
wrapper rather than a model.

## Can Mitsuba 3 render this in real time, and the answer is at a head

Proposed as the renderer instead of Godot. The arithmetic comes from
figures this workspace already measured -- 48.1 ns a pixel for the
G-buffer and 14.1 for MToon shading -- so the answer is a multiplication
rather than an opinion:

    target          pixels      ms a frame    fps

    1080p          2 073 600       129.0       7.8
    720p             921 600        57.3      17.4
    512 square       262 144        16.3      61.3
    256 square        65 536         4.1     245.3

**At a full frame it is not close, and at a head it is comfortable.** A
talking-head viewport is the 512 or 256 row, and a presence loop only
ever renders a head and shoulders. So the honest answer is that Mitsuba
is fast enough for exactly the thing being asked about, and nowhere near
fast enough for a scene.

**One number in that table should be distrusted, and it is stated
because it changes the conclusion if it goes the wrong way.** The same
corpus puts intersection at 77 per cent of the combined cost, and
whether the 48.1 ns G-buffer figure already contains intersection or
sits beside it is not resolved by the text recording it. If it sits
beside it, every row above is roughly four times slower and the 512
square row drops to about 14 fps. **Nobody should plan a frame budget
on this table until that is settled**, and settling it is a matter of
reading the benchmark rather than running anything.

## Decided: Mitsuba is the reference renderer, Godot is the runtime

Real-time Mitsuba is too expensive, and the useful consequence is that
**the number flagged above stops mattering.** A reference renderer has
no frame budget, so whether intersection sits inside the 48.1 ns figure
is no longer load-bearing on anything. It is still worth reading, and
nothing now waits on it.

**This workspace already runs exactly this pattern.**
`rf-detr-cpp/gen_reference/` holds six generators whose own comment
reads *"The oracles. Each writes a `.bin` that a `tests/test_*.cpp`
reads back and diffs."* PyTorch is slow and correct; the C++ is fast and
has to prove it agrees. Mitsuba against Godot is the same relationship
one level up:

    slow and correct        fast and shipped     the check

    PyTorch reference       rf-detr C++          .bin diff, per tensor
    Mitsuba 3              Godot                 per-pixel, per view

**And it answers rule 4 for the renderer.** A number without a baseline
is not a measurement, and until now the realtime renderer had none --
"it looks right" is the proxy, and rule 1 says the proxy is always the
one that is easy to read. A physically-based render of the same scene
from the same camera is the physical quantity.

**The camera sequence is already settled**, which is what makes the
comparison cheap. CLAUDE.md requires views from
`sphere_hammersley_sequence` and gives the reason -- a hand-picked front
view showed error of five stacked soda cans along the travel axis
against three and a half across it. So the oracle renders that sequence,
Godot renders the same sequence, and the diff is per-pixel per view with
no new convention to agree.

**The tolerance is the open question and it is not a small one.** Godot
will not match Mitsuba: MToon is a stylised shading model and the
runtime is rasterised, so the two disagree by construction and the
useful bound is not zero. What the oracle catches is a *change* --
a rig edit, a material change or an export regression that moves the
runtime away from where it was -- rather than absolute physical
agreement. Stating that first avoids the trap of building a gate whose
only possible verdict is failure.

That also makes it a negative control: perturb a material and the diff
must move. A renderer comparison that has never rejected anything has
not shown it can.

## But the frame rate is not the reason to choose## But the frame rate is not the reason to choose

Even at 245 fps, Mitsuba is the wrong instrument for this loop, and
saying so matters more than the arithmetic above.

**It renders where the compute is, and a presence loop renders where
the viewer is.** Mitsuba is Python over Dr.Jit compiling to LLVM IR and
PTX. TalkingHead runs in the browser on three.js; Godot has a native
runtime and a web export. A loop whose whole purpose is two people
seeing each other cannot round-trip every frame through a server.

**Its strength is the job this workspace already gives it.** RFD 1166
scores the Mitsuba row as `3D views`, and CLAUDE.md's rule that views
come from the `sphere_hammersley_sequence` is exactly that: evaluation
renders, and video-ready deliverables, where physical correctness and
determinism are worth more than latency. That is a different job from
being present, and it is not a lesser one.

So: Godot or TalkingHead for the live loop, Mitsuba for the renders
that get looked at afterwards. The measurement says the head would fit;
the architecture says it should not have to.

## What to do, cheapest first

1. ~~**Check ANNY for viseme morph targets.** One file.~~ **Resolved
   2026-09-04**: no viseme-named morphs; 52 facial-action blendshapes
   under `FACIAL_ACTION_LABELS` handle it via the phoneme→viseme→
   facial-action mapping at `anny.data.phoneme_viseme_facial_action`.
   Lip-sync is an authoring question no longer; it is a data-file
   question, and the data file ships.
2. **Run Qwen3-ASR-1.7B and Qwen3-TTS on the host**, end to end, no
   device and no avatar. That is the loop's spine and it needs nothing
   from this Space.
3. **Wire rf-detr keypoints through SOMA-X to ANNY**, on the desk GPU
   before the device. The body path is further along than the voice
   path and is the half that eventually moves onto the accelerator.
4. **Only then the face, and the Kimodo LoRA after that.**

Steps 1 and 2 are independent and neither needs the accelerator, which
is the same ordering RFD 1168 and 1169 use and the same argument
arXiv:2608.12875 makes: find out with the cheap thing first.

## Measurement pass, 2026-09-04

The reasoning stage that RFD 1157 pairs with EditScore is
Qwen3-VL-8B-Instruct in bitsandbytes NF4, and cell 1 of this pass
measured its open-ended 40-token reply on RTX 3090 selected by UUID.
Clean p50 wall was 1980 ms. The 500 ms budget puts that at 396 per
cent. Under VRChat co-tenancy on the same card, p50 rose to 2745 ms
(549 per cent); the co-tenancy cost was 27.9 per cent.

Qwen3-VL-2B-Instruct in the same runtime ran the same prompt at clean
p50 1386 ms (277 per cent of budget). Contested p50 was 2763 ms; the
2B cell paid 49.8 per cent to co-tenancy against the 8B's 27.9, so the
smaller model is the more contention-sensitive of the two on this GPU.

Neither cell fits the 500 ms whole-loop budget on this reasoning stage
alone. The 2B is closer, but not within a factor.

The bitsandbytes NF4 slow-kernel warning fired on the 8B's inner
dimension 4304, the same failure mode CLAUDE.md's blocklist row
records against OmniGen2's inner dimension 2520: "inner dimension is
not aligned for fast kernel with blocksize=64, falling back to slower
implementation." The warning is a symptom, not the cost; the cost is
the wall above.

**Option B, unmeasured.** llama.cpp Q4_K_M via Vulkan on the same GPU
sidesteps the bitsandbytes slow-kernel fallback and typically runs
2-4x the bnb speed on this hardware class. The Q4_K_M target GGUF and
the mmproj were staged and a text-only measurement script was drafted;
the cell was not run. If Option B lands closer to budget, the
reasoning path has a live lever; if it lands in the same three-to-four
times zone, structural levers (streaming, moving EditScore off the
critical path) are next.

**What the pass does not say.** These are the reasoning-stage numbers
in isolation, and the 500 ms budget in this document is for the whole
turn (VAD, ASR, reasoning, TTS, viseme, render). VAD measured in the
same session at 0.48 ms p50 with Silero, uncontested, and is not the
lever. The other stages were parked before their cells ran.

Raw results and the co-tenancy snapshots at start and end of each
cell live at `scratchpad/rfd-1170-measure/`:
`results-reasoning-base-clean.json`,
`results-reasoning-2b-clean.json`,
`results-clean-window-summary.json`,
`nvsmi-clean-{cell1,2b}-{start,end}.csv`.
