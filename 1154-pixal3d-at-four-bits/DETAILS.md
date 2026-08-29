# RFD 1154 details: what the sparse structure stage actually does

## The stage, sized

`configs/gen/ss_flow_img_dit_1_3B_32_bf16_proj_finetune.json` builds a
`SparseStructureFlowModel`: resolution 8, 8 in and out channels, 1536
model channels, 30 blocks, 12 heads, `pe_mode` rope, `image_attn_mode`
proj. Roughly 1.3 B parameters.

Weights are `TencentARC/Pixal3D`, MIT and ungated:

    ss_flow_img_dit_1_3B_64_bf16.safetensors     5359.82 MB
    ss_dec_conv3d_16l8_fp16.safetensors           147.59 MB
    all safetensors in the repo                   24.04 GB

The 24.04 GB confirms RFD 1026's 24.05 GB, which was an estimate. The
flow file is 5.36 GB at 4 bytes a parameter, so `1_3B` is honest even
though the name says bf16.

## Why it runs here and the other stages do not

Its two configs are the only ones in `configs/gen` that do not set
`use_naf_upsample`, so they never reach NAF and never reach NATTEN.
RFD 1140 measured the consequence: stage 1 succeeds in 22 s, stage 2
dies on a missing sm_86 kernel.

That is a packaging failure rather than a hardware one, and RFD 1140
now says so. The failing run used the prebuilt NATTEN wheel from
`requirements-hfdemo.txt`; the README's own step 3 builds it with
`NATTEN_CUDA_ARCH` set for the machine. Nobody has tried that here, so
the later stages are untested on this desk rather than excluded from
it.

## The export, measured

A 2-block, 384-channel instance with random weights. Operator coverage
does not depend on weight values, and RFD 1129's skill asks for the
smallest graph that carries the question.

    instantiated        8.44 M parameters
    forward             OK, output [1, 8, 8, 8, 8]
    TorchScript 17/20/23  aten::view_as_complex is not supported
    dynamo              DispatchError on aten.unsqueeze: no
                        decomposition for complex-valued input

Two exporters, two messages, one cause: ONNX has no complex dtype, so
RoPE stops both. TorchScript names the operator that makes the complex
tensor and dynamo names the next one to touch it.

## Real-valued RoPE, and what it unblocked

The rotation is exact in reals. `(a + bi)(cos t + i sin t)` is
`(a cos t - b sin t) + i(a sin t + b cos t)`, so carrying cos and sin
instead of a complex tensor changes the encoding and not the
arithmetic. Checked before use rather than after:

    patched against original   max|diff| 0.000e+00
    perturbed control          max|diff| 5.278e-01

Bit-identical, and the control fires, so the equivalence check is not
vacuous. With the patch the graph exports:

    544 nodes, 28 distinct operators

Twenty-five are in `DEVICE_OPS`. Three are not: `Cos`, `Sin` and
`ReduceL2` -- the first two introduced by this patch, the third from
the qk RMS norm. NONE of RFD 1131's refused family appears: no
GridSample, ScatterND, GatherElements or TopK.

## What the compiler refuses, which is not the operators

    input                     verdict
    rank 5, x [1,8,8,8,8]     _add_input_layers: output_format is None
    rank 4 on x only          identical
    rank 4 on all four        IndexError, further into the parse

The first two die in `_add_input_layers` before any operator is read.
Making every input NHWC moves the failure, which is what identifies
the cause: the parser wants all four inputs image-shaped, and a rank-1
timestep and rank-3 conditioning have no format.

So the three operators outside `DEVICE_OPS` are still unjudged after
four attempts. What is measured is that this is a conditional
diffusion transformer with heterogeneous inputs meeting a parser built
for image graphs, and each fix reveals the next assumption.

`gate_dfc_parse.py` reported PASS on the first of these, because the
allowlist predicted a rejection and a rejection arrived. The two
disagreed about the reason. The gate compares verdicts and not causes,
so any rejection confirms whatever was predicted.

## What is still unasked

The Conv3D decoder, `ss_dec_conv3d_16l8`, is a separate 148 MB file
and nothing here has exported it. The three later stages need a card
this desk does not have, whatever their operators turn out to be.
