# RFD 1166 details: the table, the runoff, and what each row rests on

## Scores

Six dimensions, 0 to 100 each. Sorted by sum, which is the STAR score
round and not the result.

    model                    fit shape  ref clear value adapt   sum
    rf-detr keypoint         100   100  100    80   100    95   575
    cyclegan_style_transfer   95    95   60    50    70    95   465
    MoGe                      85    90   55    50    60    60   400
    unified-modal-embedder    90    85   15    50    50    75   365
    Kimodo                    95    40   10    55    70    85   355
    EditScore, Qwen3-VL-8B    40    45   90    55    30    70   330
    OmniGen2                  50    50   15    50    85    75   325
    See-Through               75    60   10    55    75    45   320
    SkinTokens                95    15   10    45    55    80   300
    TRELLIS.2                 70    30   10    40    75    50   275
    residual-fsq-recommender  90    30   10    40    35    70   275
    MuJoCo MJX                95    30    5    15    25    90   260
    Mitsuba 3 shading         95    75    5    10    20    15   220
    Pixal3D                   30    35    5    20    95    20   205
    qwen35-defiant            45     5    0     5    25    15    95
    VoxHammer                 30     0    0    15    35    10    90
    Gemma 4                   30     5    0     5    35    15    90

## The runoff

Finalists are rf-detr at 575 and `cyclegan_style_transfer` at 465.
Six dimensions, one vote each:

    dimension     rf-detr  cyclegan   prefers
    fit               100        95   rf-detr
    shape             100        95   rf-detr
    reference         100        60   rf-detr
    clear              80        50   rf-detr
    value             100        70   rf-detr
    adapt              95        95   tied

**rf-detr wins five to nil with one tie.** The margin matters less
than the unanimity: it is not carried by one column, it leads or ties
every one. No other candidate does that against any other.

The runoff earns its place further down. `Pixal3D` scores 95 on
`value`, the second highest in the table, and 205 overall. A sum
weighted toward payoff would rank it well; it loses every other
dimension, and STAR is what keeps one strong column from deciding.

Two pairs worth reading, because the sum alone hides them:

    EditScore vs See-Through   sum 330 to 320, runoff 3-2 to
                               See-Through on fit, shape and value
    CycleGAN vs MoGe           sum 465 to 400, runoff 5-0-1 to
                               CycleGAN

EditScore leads the sum and loses the runoff. Its 330 is carried by
`reference` 90, the Hailo fork targeting Qwen3-VL exactly, against
`fit` 40 and `value` 30. That is precisely the shape STAR exists to
catch, and an earlier revision of this ranking put it second overall.

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

`adapt` leans on RFD 1140: the desk trains an OmniGen2 LoRA at 256
square in 22 minutes and does not finish one step in twelve minutes
at 512. Pixal3D's 20 and Gemma 4's 15 come from that, and from GGUF
carrying no graph to train against.

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
