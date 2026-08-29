# RFD 1166 details: the table, the runoff, and what each row rests on

## The STAR rank

STAR applied repeatedly: take the two highest sums, let the six
dimensions vote between them, seat the winner, remove it, repeat.
`runoff` reads wins-losses-ties against the runner-up it beat.
`loops` is which of RFD 1143 to RFD 1146 the model appears in.

     #  model                     fit shp ref clr val adp ask wnt  sum  runoff role
     1  rf-detr keypoint         100 100 100  80 100  95 100  85  760  7-0-1  fit
     2  cyclegan_style_transfer   95  95  60  50  70  95  80  45  590  4-4-0  2D+3D style
     3  OmniGen2                  50  50  15  50  95  75 100  55  490  4-3-1  2D edit
     4  EditScore, Qwen3-VL-8B    40  45  90  55  60  70 100  70  530  6-2-0  all three
     5  Kimodo                    95  40  10  55  40  85  30  80  435  4-3-1  -
     6  MoGe                      85  90  55  50  40  60  40  50  470  4-4-0  -
     7  SkinTokens                95  15  10  45  35  80  30  85  395  4-3-1  -
     8  MuJoCo MJX                95  30   5  15  20  90  85  70  410  4-4-0  -
     9  unified-modal-embedder    90  85  15  50  25  75  30  20  390  4-4-0  -
    10  See-Through               75  60  10  55  50  45  40  40  375  6-2-0  -
    11  TRELLIS.2 / Pixal3D       60  35   5  25  75  30  35  90  355  4-3-1  3D edit
    12  Mitsuba 3 shading         95  75   5  10  30  15  95  25  350  4-4-0  -
    13  residual-fsq-recommender  90  30  10  40  20  70  30  45  335  7-1-0  -
    14  qwen35-defiant            45   5   0   5  15  15  70  20  175  4-3-1  -
    15  VoxHammer                 30   0   0  15  35  10   5  60  155  last   3D edit

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

## `wanted`, and what the product is for

The other seven dimensions all ask whether a model is tractable. None
asks whether the thing it does is wanted, and a model can be easy to
accelerate and serve nothing anybody needs.

What the product is for answers it, and the manifest says: a social
world with avatars people wear. `v-sekai` and `v-sekai-fabric` carry
the client and the fabric, ANNY is the body, and RFD 1122 is the chain
that puts a person into it. Two things follow and nothing else does.

**People make things and wear them.** A mesh someone made is worth
nothing until it is rigged, textured and in the world, so
`TRELLIS.2 / Pixal3D` takes 90 as the shortest path from an image to a
wearable asset and `SkinTokens` 85, because an unrigged mesh cannot be
worn at all. `VoxHammer` takes 60 for editing what exists.

**People are present to each other, and keypoints are how.** rf-detr
is markerless motion capture: a camera, a body, and the pose that
carries one person's movement onto another's avatar. That is
embodiment rather than a step toward it, so it takes 85, and `Kimodo`
80 for moving a body without a camera in front of it. `MuJoCo MJX`
takes 70, because a world that responds is the difference between a
room and a backdrop.

**EditScore takes 70, and an earlier revision had it at 10.** That
scored it as a thing nobody wears or sees, which is true and beside
the point: **it is a dependency of every making flow above it.** A
mesh generated, edited or restyled is a proposal, and something has to
say whether the proposal is good before it reaches a wardrobe. Without
a scorer the loops do not converge, so what people make is not made
well. It is invisible and load-bearing at once, and 10 recorded only
the first half.

`qwen35-defiant` takes 20. A language model is a fine thing to have
and it is not what this product is.

## The critical path is a chain, not a set of loops

`value` was first scored per invocation, which treated the models as
independent candidates. They are stages of one shape, run twice:

    style change  ->  edit  ->  score

    2D edit loop   CycleGAN  ->  OmniGen2             ->  EditScore
    3D edit loop   CycleGAN  ->  Pixal3D + VoxHammer  ->  EditScore
    fit loop       rf-detr   ->  ANNY fit             ->  EditScore
                                                          + soma_referee

Three consequences, and each moved a row.

**EditScore terminates every chain.** Nothing reaches a wardrobe
without passing it, so a gain there lands three times rather than
once. Its `value` is 60 for that and its `wanted` 70 for being the
dependency of the making it does not perform.

**CycleGAN is a shared first stage, not an input transform.** An
earlier revision had it inside the 2D loop only and scored `value` 45.
Both edit chains begin with a style change, so it is 70, and it holds
second on a runoff it drew four-all -- seated by score, the narrowest
result in the table.

**Pixal3D and VoxHammer are one editor between them**, the 3D
counterpart to OmniGen2 rather than two candidates. That is a second
argument for the merged row, independent of Pixal3D being built on
TRELLIS.2: they occupy one slot in one chain.

The loop count was also wrong before this. Loops 2 and 3 in the
notebooks call the same proposer with the same control variable and
the same scorer, differing only in whether the input has been through
a style change, which is what identifies style as a stage rather than
a loop.

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
