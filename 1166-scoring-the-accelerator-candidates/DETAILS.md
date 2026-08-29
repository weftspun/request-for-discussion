# RFD 1166 details: the table, the runoff, and what each row rests on

## The STAR rank

STAR applied repeatedly: take the two highest sums, let the six
dimensions vote between them, seat the winner, remove it, repeat.
`runoff` reads wins-losses-ties against the runner-up it beat.
`loops` is which of RFD 1143 to RFD 1146 the model appears in.

     #  model                     fit shp ref clr val adp ask wnt  sum  runoff role
     1  rf-detr keypoint         100 100 100  80 100  95 100  85  760  7-0-1  fit
     2  cyclegan_style_transfer   95  95  60  50  70  95  80  60  605  5-2-1  style, both
     3  OmniGen2                  50  50  15  50  95  75 100  55  490  4-3-1  2D edit only
     4  EditScore, Qwen3-VL-8B    40  45  90  55  60  70 100  70  530  4-3-1  all three
     5  Kimodo                    95  40  10  55  40  85  30  80  435  4-1-3  -
     6  SkinTokens                95  15  10  45  35  80  30  85  395  4-3-1  -
     7  MuJoCo MJX                95  30   5  15  20  90  85  80  420  3-3-2  presence
     8  Mitsuba 3 shading         95  75   5  10  55  15  95  45  395  5-3-0  3D views
     9  See-Through               75  60  10  55  50  45  40  40  375  6-2-0  -
    10  TRELLIS.2 / Pixal3D       60  35   5  25  75  30  35  90  355  8-0-0  3D backbone
    11  VoxHammer                 30   0   0  15  60  10  30  80  225  last   3D ingest+edit

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

**Gemma 4 and `qwen35-defiant` are both struck from the ranking.**
Neither was a close call. Both are GGUF, so the format ends them
before memory or operators are reached, and no exporter can close that
gap because GGUF carries no graph at all. RFD 1155 abandoned Gemma 4
on the same ground.

Ranking a candidate with no path flatters the ranking rather than
informing it, and keeping one as a worked example only made the table
look like it had considered language models on their merits. It had
not: it had rediscovered the blocklist. BLOCKLIST.md is where that
argument lives.

**`unified-modal-embedder` and `residual-fsq-recommender` are struck
for a different reason: they are not what this product is.** One
embeds content for search and the other recommends a next item. Both
are infrastructure for finding things, and the two wants this ranking
serves are making and being present. Neither is in a chain, neither
has run here, and the embedder held the lowest `wanted` of any
surviving row at 20.

Nothing is wrong with either. A ranking of accelerator candidates is
not a list of the workspace's models, and the checkouts stay in the
manifest where they are placed.

**MoGe is struck because the inversion deletes its input.** It is not
an independent candidate: it is in Pixal3D's core `requirements.txt`
and `app.py` calls it from `get_camera_params_wild_moge`, which takes
a photograph somebody else shot and estimates the camera that shot it
-- intrinsics, then `camera_angle_x` and `distance`, which is exactly
the `camera_params` dict `run()` demands.

*Wild* is the operative word. Render the view yourself and there is no
wild image and no camera to recover: the angle, the distance and the
mesh scale are yours by construction. So the inverted chain does not
make MoGe redundant, it removes the case MoGe exists for, which is the
same thing that happened to the consensus panel.

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

## The critical path is a chain, not a set of loops

`value` was first scored per invocation, which treated the models as
independent candidates. They are stages of one shape:

    2D edit   CycleGAN  ->  OmniGen2                          ->  EditScore
    3D edit   CycleGAN  ->  VoxHammer over TRELLIS.2/Pixal3D  ->  EditScore
    fit       rf-detr   ->  ANNY fit                          ->  EditScore
                                                                  + soma_referee

OmniGen2 appears in one chain and not the other, which is a decision
rather than an omission. See below.

**The two are siblings here and the corpus already orders them.**
`pose-consensus/README.md` records the inversion: instead of
estimating poses from images, ANNY originates the pose, renders it,
and a diffusion model stylizes the render with the geometry pinned,
so the label is true by construction. That inversion ended the
consensus panel outright -- you do not convene three estimators to
adjudicate a pose you authored.

Run that way the chain is one, not two:

    originate 3D  ->  render views  ->  style views  ->  edit  ->  score

and 2D is an operation on views rather than a stage before 3D. Three
things follow.

**The camera question disappears.** OmniGen2's 0.04 obedience slope
only matters if the camera is asked for. Rendering from
`sphere_hammersley_sequence` gives it exactly, and the measurement
below stops being a problem to work around.

**The labels land on the right side of CLAUDE.md's synthetic rule.**
A render is constructed, deterministic from assets held here, with
labels true by construction. An image generated first and reconstructed
after is generated, and carries all five conditions.

**rf-detr changes job without changing score.** Estimating an unknown
pose and confirming an authored one survived a restyle are different
questions, and `test_pose_survives_restyle.py` asks the second. Its
`wanted` 85 covers the live case, a person in front of a camera, which
the inversion does not touch.

**The 3D chain does not go through the 2D one.** Pixal3D's `run()`
takes a single `Image.Image`, so reading it as an image flow suggests
2D must produce that image. It need not. `get_cond` one layer down
takes `list[Image.Image]`, and VoxHammer already drives that path:
`extract_feature.py` renders 150 views, runs DINOv2 over them,
projects voxel centres into each view and averages the patch tokens,
reproducing the encoder input for an asset that already exists.

So the views come from rendering an asset rather than generating an
image, which is also the cleaner side of CLAUDE.md's synthetic line:
constructed rather than generated. `sphere_hammersley_sequence` is the
mandated sequence and Mitsuba renders a view in 1.79 ms.

**Go through VoxHammer rather than calling the multi-view path
directly.** Both reach the same samplers, and only one of them is
already written, tested against a real asset and handling the
inversion the edit needs.

Three consequences, and each moved a row.

**EditScore terminates every chain.** Nothing reaches a wardrobe
without passing it, so a gain there lands three times. Its `wanted` is
70 for being the dependency of making it does not itself perform.

**CycleGAN styles both chains, and style is not 2D-only.** A 3D asset
is restyled through its views: render, restyle the views, ingest the
styled views. It is the same stage doing the same work in both chains
rather than a 2D step the 3D chain routes around, so `value` 70 and
`wanted` 60. It holds second on a runoff it drew four-all, seated by
score and the narrowest result in the table.

The hazard in that is already guarded. `test_pose_survives_restyle.py`
restyles and re-detects to measure joint drift, and
`verify_restyle.py` scores silhouette against the render's own alpha
with a shifted-reference control that must fail. A restyle that moves
the body is the failure both exist to catch, and styling views before
reconstruction is exactly where it would happen.

**Mitsuba is the 3D chain's view source, not a bystander**, which
takes `value` from 30 to 55 and `wanted` from 25 to 45.

## OmniGen2 is 2D only, and the measurement is why

The 3D chain could route through it and does not. Camera control is
what it would be for, and `write_omnigen2_jsonl.py` records what that
costs: asked for eight azimuths in plain language, the recovered
azimuth tracked the request with **a slope of 0.04**, where 1.00 is
obedience and 0.00 is a body that never turned. Six of eight views
came back between -1 and -11 degrees whatever was asked. The trained
adapter reached 0.099.

The 3D chain does not ask. It renders the view it wants from
`sphere_hammersley_sequence`, exactly, in 1.79 ms. Paying 133 s for a
slope of 0.04 when a camera transform is exact and free is the trade
this records, and it is why the 3D chain takes rendered views instead.

**What OmniGen2 keeps is the 2D chain, and nothing else here can do
it.** CycleGAN is style transfer, one learned mapping. OmniGen2 is
instructed editing: change this specific thing, in words. Those are
different capabilities and the second is what "moddable" means. It is
also `anny-camera-lora`'s base, so dropping it orphans RFD 1141's
published adapter, and it generates the corpus restyles.

Its `value` of 95 is the highest here because it is 133 s of a 163 s
round, so removing it takes out the largest cost in the loop. `value`
measures what accelerating a stage buys, not whether the stage should
exist, and on OmniGen2 those two point in opposite directions.

## VoxHammer, and where its low scores are ours

`shape` 0 and `fit` 30 are the model's own. `ask` 30 is not: upstream
runs, and it is the two weftspun wrappers that raise
`NotImplementedError` outside stub mode. That is a wiring gap in this
workspace rather than a capability the method lacks, and an earlier
revision scored it 5 without making the distinction.

`value` 60 and `wanted` 80 follow from the chain: it is two stages,
ingestion and edit, and the 3D chain has no other route in.

It still ranks last, because `shape` 0 stands. A compiled graph cannot
be monkey-patched, and monkey-patching is how it works. Being
load-bearing in the chain and unacceleratable are not in tension --
they are the finding.

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

**MuJoCo MJX serves presence, and was twice mis-filed.** First as
tooling, then as interactability at the edge of the product. Physics
is embodiment: a body that collides, stands on ground and responds is
present, and one that floats and clips is not. Its `wanted` is 80,
with `rf-detr` and `Kimodo`.

 `mjx/mujoco/mjx`
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
    CycleGAN          UNEXAMINED. Scored from what it is, not from
                      anything run. `clear` 50 says so.

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
