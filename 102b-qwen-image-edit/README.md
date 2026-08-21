# RFD 102b: Model image for qwen_q4_k_m_image_edit

**State:** discussion
**Feature:** model packaging

## Problem

Qwen image edit is the largest model in the catalog at 27.0 B
parameters. In bf16 it needs 54.0 GB, which is 46 percent of the whole
catalog on its own.

The model id already names the format. It ships Q4_K_M, and the
catalog entry records that choice in its name.

## Decision

Ship Q4_K_M only. Never build a bf16 variant of this model image.

At 0.55 bytes per parameter it needs 14.85 GB, and not 54.0 GB. That
one choice saves 39.15 GB, which RFD 101b records as the largest
single saving in the catalog.

See `DETAILS.md` for the model's memory and license, the `predict()`
interface, and the open question on quantization quality.

## Related

RFD 101b selects the format and records the saving. RFD 101a gives
the row. RFD 101c clears Apache 2.0.
