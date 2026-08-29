# RFD 1142: The Mac against the UGen300

**State:** discussion
**Feature:** accelerator comparison for edge deployment
**Scope:** `scripts/ane_bench.py`

## Problem

RFD 1130 sequences the plan around the UGen300, an 8 GiB Hailo-10H
behind USB, and the Mac was written off as the weak node on a figure
that could not support it: `rfd1122-plan.usda` recorded
`neuralEngineUsefulForBackbone = 0` from an ONNX Runtime CoreML run
that partitions per operator and logged no placement. Which engine the
Mac would even use went unasked.

## Decision

**Metal is the Mac's engine here, and the Neural Engine is blocklisted.**
Measured at fp16 on the RF-DETR device half, converted natively so
placement is known rather than inferred:

    engine   ms med   max|diff|   bound 4.2e-03   placement
    ane       121.6   4.311e-02   FAIL            373/373
    gpu        62.0   3.524e-03   ok              373/373
    cpu       133.0   2.425e-01   FAIL            373/373
Metal is twice as fast and the only one inside the bound. The Neural
Engine also stops at 2 GiB of weights, at 2^31 bytes, where Metal holds
8176.2 MiB — the UGen300's whole working set. Both caps are undocumented.

The comparison against the device stays open: its fp16 rate is halved
from its INT8 row rather than measured, and the part has yet to arrive.
The Neural Engine wins on a synthetic convolution stack, 13.58 TFLOP/s
against 6.98, and loses on the shipped graph, so both are reported.

`DETAILS.md` has the apparatus, `SKILL.md` the order.

## Related

RFD 1128 asks whether four bits survive, RFD 1129 whether the operators
compile, RFD 1130 what the device delivers. RFD 1122 is the goal.
