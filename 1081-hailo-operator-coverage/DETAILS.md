# RFD 1081 details: the two stages, and what an export has to carry

## Sparse submanifold convolution

`o_voxel` and `flex_gemm` convolve over occupied voxels only, and the
saving is the whole point: a dense 1024 grid is 2^30 cells while the
occupied set is a thin shell.

ONNX has `Conv` and no submanifold sparse convolution. An export
therefore either densifies, which destroys the saving and the memory
budget with it, or emits a gather, matmul and scatter pattern whose
support is exactly the open question.

## Neighborhood attention, reached through a model nobody declares

Pixal3D's image conditioning loads `valeoai/NAF` over `torch.hub`, and
NAF's attention layers call natten:

    naf.py:115 -> attentions.py:72 -> natten.functional.na2d
    -> neighborhood_attention_generic -> cutlass_fna_generic

Nothing in Pixal3D imports natten, which is why grepping for it finds
only a README line and concludes wrongly that it is unused.

It is not optional. `IMAGE_COND_CONFIGS` sets `use_naf_upsample: True`
for three of the four conditioning models, and the projection width
depends on the flag -- `proj_channels = embed_dim * 2 if
use_naf_upsample` -- so the published weights were trained with it in
place. Turning it off mismatches the checkpoint rather than skipping a
step.

## What the gate already knows

`scripts/gate_onnx_device.py` exports the device half and
`scripts/gate_dfc_parse.py` runs the compiler against it. The two run
as a pair, and their disagreement is the result:

| macOS gate | DFC       | meaning                       |
| ---------- | --------- | ----------------------------- |
| PASS       | parses    | the allowlist held            |
| PASS       | rejects X | `DEVICE_OPS` is too generous  |
| FAIL on X  | parses    | `DEVICE_OPS` is too strict    |

`weftspun-hailo-dfc:5.3.0` is built and `hailo_sdk_client` imports.
The wheel is Linux-only, which is why that image exists at all.

## The order that saves time

Export the attention layer before the sparse convolution. It is
smaller, it is the dependency nobody expected, and a rejection there
blocks the conditioning path -- which makes the convolution question
moot until it is answered.
