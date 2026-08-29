# RFD 1166 details: the table, and what each row rests on

## The ranking

    model                     fit shape ref clear value   /25   /10
    rf-detr keypoint            5    5    5     4     5    24   9.6
    EditScore, Qwen3-VL         5    3    5     3     2    18   7.2
    See-Through                 5    3    0     3     4    15   6.0
    Kimodo                      5    2    0     3     4    14   5.6
    OmniGen2                    3    3    1     3     3    13   5.2
    TRELLIS.2                   4    2    0     2     4    12   4.8
    SkinTokens                  5    1    0     3     3    12   4.8
    Pixal3D                     2    2    0     1     5    10   4.0
    VoxHammer                   2    0    0     1     2     5   2.0
    Gemma 4                     2    0    0     0     2     4   1.6

The `/10` column is `score_range / 10`, the reduction EditScore applies
to its own scores, kept so the two scales cannot drift apart.

## What each row rests on

Provenance differs sharply and the ranking is only as good as the
weakest row in it.

    row               basis
    rf-detr           MEASURED. 40.852 M parameters from the
                      checkpoint, 25.245 M in the device half from the
                      ONNX initializers. Exported and translated.
    OmniGen2          MEASURED. 15.87 + 15.02 + 0.34 GB of safetensors
                      on disk, fp32, so 7.81 B.
    Pixal3D           MEASURED since scoring. The repo's safetensors
                      total 24.04 GB against RFD 1026's estimated
                      24.05, and the SS stage is 5.36 GB at 4 bytes a
                      parameter.
    See-Through       RFD 1026 ESTIMATE, and the four components it
                      covers are not recorded.
    TRELLIS.2         RFD 1026 estimate.
    SkinTokens        RFD 1026 estimate.
    Kimodo            RFD 1026 estimate.
    EditScore         INFERRED from a published name, and the name was
                      wrong: scoring assumed Qwen3-VL-4B and
                      `weft_score.py` loads the 8B.
    Gemma 4           INFERRED from a published name.

## Two rows that have moved since they were scored

**Pixal3D's 10 was scored on the wrong unit.** It treats the model as
one 12.02 B blob. RFD 1154 now records four stages, the sparse
structure stage at 1.3 B fitting at every precision. Its `fit` of 2
and `clear` of 1 belong to the whole model, not to the stage. The
score is left as recorded rather than restated, because a ranking
edited after the fact stops being a record of what was decided.

**EditScore's 18 was scored against the 4B.** The deployed model is
the 8B at 6.75 GiB NF4, which meets RFD 1128's four-bit question that
the 4B avoided. `fit` would fall.

## VoxHammer, scored on what it costs rather than what it weighs

It holds no weights. No `nn.Module`, no `nn.Parameter` and no
checkpoint exists in `3-interactor/voxhammer-upstream`; its one class
is a sampler with no parameters, and everything else is free functions
bound onto TRELLIS objects with `types.MethodType`.

**AN EARLIER REVISION SCORED IT n/a ON THAT BASIS, AND THAT WAS THE
WRONG QUESTION.** Weighing nothing does not make it absent from the
ranking. It has a cost, and the cost is the edit it forces on the base
model: `run_edit` replaces `ss_flow`'s and `slat_flow_model`'s forwards
with `MethodType`, threading `kv`, `kv_mask`, `t_latent`, `order`,
`pos` and `layer` through TRELLIS's own attention. Using it with
Pixal3D means writing those patches against Pixal3D.

That is what `shape` 0 records, and it is worse than a low score.
**A compiled graph cannot be monkey-patched.** A HEF is a fixed
artifact and `MethodType` is a Python-time substitution, so a base
model on the accelerator is a base model VoxHammer cannot reach. Its
presence subtracts from the accelerability of whatever it wraps rather
than being neutral to it.

`fit` 2 inherits Pixal3D's four-bit-only band. `clear` 1 is the
TRELLIS 1 to TRELLIS.2 port plus the Pixal3D edits, against wrappers
that are still stubs. `value` 2 is mesh editing being a real catalog
task whose acceleration would have to happen in the base anyway.

The arithmetic it adds is refused independently. `edit_pipeline.py`
matches sparse coordinates by building an N x M boolean matrix,
`(k.coords.unsqueeze(1) == kv_mask.unsqueeze(0)).all(dim=-1)`, then
`.float().argmax(0)`, then scatters -- once per layer, per timestep,
per CFG branch -- and carries an attention key-value cache from the
inversion pass into the editing pass. Data-dependent indexing and
state held across invocations are both what RFD 1131 refuses.

Its base is also not the base the workspace claims. Upstream loads
`microsoft/TRELLIS-image-large`, TRELLIS 1, while RFD 1047 and the
image-editing Dockerfile name TRELLIS.2. Both weftspun wrappers raise
`NotImplementedError` outside stub mode, so the re-basing is asserted
and not implemented.
