# RFD 1166 details: the table, the runoff, and what each row rests on

## The STAR rank

STAR applied repeatedly: take the two highest sums, let the six
dimensions vote between them, seat the winner, remove it, repeat.
`runoff` reads wins-losses-ties against the runner-up it beat.
`loops` is which of RFD 1143 to RFD 1146 the model appears in.

     #  model                     fit shp ref clr val adp ask wnt  sum  runoff loops
     1  rf-detr keypoint         100 100 100  80 100  95 100  85  760  7-0-1  1
     2  cyclegan_style_transfer   95  95  60  50  45  95  80  35  555  4-3-1  2 in
     3  OmniGen2                  50  50  15  50  95  75 100  55  490  5-2-1  2
     4  EditScore, Qwen3-VL-8B    40  45  90  55  60  70 100  10  470  5-3-0  1,2,4
     5  Kimodo                    95  40  10  55  40  85  30  80  435  4-3-1  -
     6  MoGe                      85  90  55  50  40  60  40  50  470  4-4-0  -
     7  SkinTokens                95  15  10  45  35  80  30  85  395  4-3-1  -
     8  MuJoCo MJX                95  30   5  15  20  90  85  70  410  4-4-0  -
     9  unified-modal-embedder    90  85  15  50  25  75  30  20  390  4-4-0  -
    10  See-Through               75  60  10  55  50  45  40  40  375  6-2-0  -
    11  TRELLIS.2 / Pixal3D       60  35   5  25  75  30  35  90  355  4-3-1  4
    12  Mitsuba 3 shading         95  75   5  10  30  15  95  25  350  4-4-0  -
    13  residual-fsq-recommender  90  30  10  40  20  70  30  45  335  7-1-0  -
    14  qwen35-defiant            45   5   0   5  15  15  70  20  175  4-3-1  -
    15  VoxHammer                 30   0   0  15  25  10   5  60  145  last   4

The sum is not the order. MoGe outscores EditScore by 20 and sits
below it, having lost the runoff that decided the seat.

**TRELLIS.2 and Pixal3D are one row.** They were never independent
candidates: Pixal3D's README says it is "heavily built upon Trellis.2
... the foundation of our codebase and model architecture", and its
install step begins by following TRELLIS.2's. Scoring them separately
counted one backbone twice and let the derived model rank below the
thing it is made of. The row takes the staged view RFD 1154 arrived
at -- the 1.3 B sparse structure stage rather than the 12.02 B whole
-- which is why `fit` is 60 rather than Pixal3D's old 30.

**Gemma 4 is struck from the ranking.** It placed last at 75 and it is
not a close call: GGUF carries no graph, so the format alone ends it
before memory or operators are reached, and RFD 1155 abandoned it.
Ranking a candidate with no path flatters the ranking rather than
informing it. `qwen35-defiant` is the same case and is kept at
fifteenth as the one worked example of it, so the table still shows
what that failure looks like.

## `wanted`, scored against the survey

The other seven dimensions all ask whether a model is tractable. None
asks whether anyone wants what it does, and a twelve-person survey of
wanted features in a massive multiplayer game answers that. Two
clusters take five respondents each:

    creation and UGC   a meshing pen to build everything in world,
                       moddable, user generated content, user created
                       content unlocking most things, save and share
    social presence    a social setting to be with people, experiencing
                       something with them, voice, dancing or emotes,
                       small groups, squad cooperation

`TRELLIS.2 / Pixal3D` takes 90 as the closest thing here to a meshing
pen; `SkinTokens` 85 because a user-made mesh that cannot be rigged
cannot be worn; `rf-detr` 85 and `Kimodo` 80 on the social cluster,
where dancing and emotes were asked for by name. `MuJoCo MJX` takes 70
on "absolute interactability with world and mechanics".

**EditScore takes 10, the lowest in the table.** It is a scorer: no
player ever sees it, and nothing in twenty-four answers asks for
better scoring. It remains fourth overall, which is the point of
having eight dimensions rather than one.

Nobody asked for an LLM. `qwen35-defiant` takes 20 on that basis.

## The critical path, and there are three loops rather than four

`value` was first scored per invocation, which ignored that the loops
share their models. It also over-counted the loops.

**Loops 2 and 3 are one loop.** Their proposers are the same call:

    loop 2   omnigen2_edit.py --image SOURCE   --steps STEPS[i-1] --precision bf16
    loop 3   omnigen2_edit.py --image STYLIZED --steps STEPS[i-1] --precision bf16

Same script, same control variable, same precision, same scorer. The
only difference is `STYLIZED`, which is `SOURCE` after a CycleGAN
pass, so CycleGAN is an input transform inside loop 2 rather than a
loop of its own. Loop 4 does differ: it defines `score_view` and
`score_all` and reduces over a set of views where the others score one
image.

    loop 1  keypoints to ANNY   rf-detr, EditScore, soma_referee
    loop 2  image to OmniGen2   OmniGen2, EditScore, CycleGAN on input
    loop 4  latent to Pixal3D   Pixal3D, VoxHammer, EditScore over views

**EditScore is in all three.** A gain on the shared scorer lands three
times, and scoring it per round recorded a third of its worth.
Correcting `value` from 30 to 60 moved it from eighth to second, the
largest move this document has recorded.

The correction cuts the other way. CycleGAN is not a loop and falls to
45; See-Through, Kimodo, MoGe, SkinTokens, MJX and Mitsuba are in
none, and their `value` says so.

## What the runoff caught

**rf-detr takes first five to nil with one tie**, leading or tying
every dimension. No other candidate manages that against anyone.

**EditScore is third on reach and would be eighth without it.** Its
`fit` is 40 and its `shape` 45; what carries it is `reference` 90, the
Hailo fork targeting Qwen3-VL exactly, and now `value` 60 for being on
every loop. It ties OmniGen2 three-all and is seated by score.

**TRELLIS.2 / Pixal3D and Mitsuba tie on 230 and the runoff splits
them**, three to two on `clear`, `value` and `adapt`. A sum alone
would have left the order to chance; the runoff is what decides it.

## Five models the earlier revision omitted

`cyclegan_style_transfer` is the serious omission. It is **Loop 3**,
called at `localhost:8000` by `3-stylized-to-omnigen2.livemd` before
OmniGen2 runs, so the ranking claimed to cover the candidates while
skipping a model already inside the pipeline the accelerator serves.
It is also the accelerator's home ground: fixed-resolution
image-to-image convolution, no autoregression, no sparse indexing.

`MoGe` recovers point maps, depth, normals and camera FOV from one
image, and depth estimation is a category the Hailo zoo already ships
for HAILO10H, which is what its `reference` 55 records.

`qwen35-defiant` is Qwen3.5-9B in GGUF, the same case as Gemma 4.
Omitting it made the table imply one LLM had been considered when
there were two.

`unified-modal-embedder` and `residual-fsq-recommender` are small
models on Nx and EXLA, neither examined.

**MuJoCo MJX was dismissed as tooling and is not.** `mjx/mujoco/mjx`
is MuJoCo reimplemented in JAX: a differentiable physics graph, made
fixed-shape on purpose through fixed-size contact buffers, which is
why `adapt` is 90 -- gradients run through the simulator itself.

Its blocker is the interchange. JAX lowers to StableHLO through XLA
and the Dataflow Compiler consumes TensorFlow, TFLite and ONNX, so
there is no path today. That is a different failure from GGUF's: GGUF
carries no graph at all and nothing can convert it, while StableHLO is
a graph in the wrong dialect. Blocked on format, not structurally,
and `clear` 15 says which.

**Mitsuba 3 is scored as its shading pass, not as the renderer.** It
is a pixi dependency of `anny-render-corpus` at 3.9.1 rather than a
manifest project, and the row covers only the half that could go.

Ray tracing cannot: BVH traversal is pointer chasing with
data-dependent branch depth, which is what a dataflow part is least
able to express. Shading over a G-buffer is the opposite -- per-pixel
arithmetic at fixed dimensions -- and the corpus already separates
them, at 48.1 ns a pixel for the G-buffer against 14.1 for MToon
shading.

Two things hold it at 220 anyway. Dr.Jit compiles to LLVM IR and PTX,
which is machine code rather than a portable graph, so it is a level
below even MJX's wrong-dialect problem, and whether the Slang shading
path can be expressed as ONNX at all is unverified. And the ceiling is
small: the same measurements put intersection at 77 per cent of the
combined cost, so the whole prize is the other 23 of a pass already
made 1,272 times faster.

Not models, correctly absent: `tropes-removal-model` is `ste-enforcer`,
a prose linter under a misleading directory name; `mujoco-riscv64` is
an engine port; `anny` and `soma-x` are parametric bodies;
`pose-consensus` is a solver; `bumblebee` is a framework.

## What each row rests on

    row               basis
    rf-detr           MEASURED. 40.852 M parameters from the
                      checkpoint, 25.245 M in the device half.
                      Exported and translated.
    OmniGen2          MEASURED. 15.87 + 15.02 + 0.34 GB on disk at
                      fp32, so 7.81 B. Trained here: anny-camera-lora,
                      200 steps at 256 square in 22 minutes.
    Pixal3D           MEASURED. Repo safetensors total 24.04 GB
                      against RFD 1026's estimated 24.05.
    See-Through       RFD 1026 ESTIMATE, and the four components it
                      covers are not recorded. Only `layerdiff` is in
                      this table; `marigold-depth`, `vae` and
                      `partseg` are separate repos.
    TRELLIS.2         RFD 1026 estimate.
    SkinTokens        RFD 1026 estimate.
    Kimodo            RFD 1026 estimate.
    EditScore         INFERRED, and the inference was wrong once:
                      scoring assumed Qwen3-VL-4B and `weft_score.py`
                      loads the 8B.
    Gemma 4           INFERRED from a published name.
    CycleGAN, MoGe,   UNEXAMINED. Scored from what they are, not from
    embedder, fsq,    anything run. `clear` near 50 says so.
    qwen35-defiant

## The `adapt` column, and the one number that bounds it

It leans on RFD 1140: the desk trains an OmniGen2 LoRA at 256 square
in 22 minutes and does not finish one step in twelve at 512.
Pixal3D's 20 and Gemma 4's 15 come from that, and from GGUF carrying
no graph to train against.

**One kind of adaptation is out of reach entirely, at any size in this
table.** Quantization-aware fine-tuning exhausts the desk's 24 GiB on
rf-detr's own device half -- 25.245 M parameters, the smallest graph
here -- at the default batch and again at `batch_size=1, epochs=1`
over 64 frames, the directive verified in the loaded model script.
RFD 1165 carries the retraction that batch size was ever the lever.

So `adapt` scores ordinary training and LoRA, which the desk does. It
does not score QAT, which the desk does not do for anything, and a
column that scored both would rate every row zero and say nothing.
The distinction matters because RFD 1128's four-bit question wants
QAT: compression without fine-tuning is what optimization level 1
gives, and that is a different artifact rather than a slower one.

## VoxHammer, scored on what it costs rather than what it weighs

It holds no weights. No `nn.Module`, no `nn.Parameter` and no
checkpoint exists in `3-interactor/voxhammer-upstream`; its one class
is a sampler with no parameters, and everything else is free functions
bound onto TRELLIS objects with `types.MethodType`.

**AN EARLIER REVISION SCORED IT n/a ON THAT BASIS, AND THAT WAS THE
WRONG QUESTION.** Weighing nothing does not put it outside the
ranking. Its cost is the edit it forces on the base: `run_edit`
replaces `ss_flow`'s and `slat_flow_model`'s forwards, so using it
with Pixal3D means writing those patches against Pixal3D.

That is what `shape` 0 records, and it is worse than a low score. **A
compiled graph cannot be monkey-patched.** A HEF is fixed and
`MethodType` is a Python-time substitution, so a base model on the
accelerator is a base model VoxHammer cannot reach. It subtracts from
the accelerability of what it wraps.

The arithmetic it adds is refused independently: an N x M boolean
coordinate match per layer, per timestep, per CFG branch, then
`.float().argmax(0)`, then a scatter, plus an attention key-value
cache carried from inversion into editing. Data-dependent indexing
and state across invocations are both what RFD 1131 refuses.

Its base is also not the base the workspace claims. Upstream loads
`microsoft/TRELLIS-image-large`, TRELLIS 1, while RFD 1047 and the
image-editing Dockerfile name TRELLIS.2, and both weftspun wrappers
raise `NotImplementedError` outside stub mode.
