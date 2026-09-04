# RFD 2199: Real 4-bit QAT with Hailo as target hardware

**State:** discussion
**Feature:** real QAT loop producing int4 weights, compiled and
deployed on Hailo, filling the PR #256/#257 gap
**Scope:** int4 only, end-to-end training loop to Hailo HEF

Parked 2026-09-04: Hailo USB firmware stuck in bootloader from a
partial update; operator parked rather than requiring admin recovery.
RFD stays scoped as authored; un-park requires firmware recovery and
a named use case. See `[[hailo-ugen300-shelved]]`.

## Decision

Build real 4-bit QAT infrastructure with Hailo as the deployment
target. Int4 only. Int8 QAT is not the fallback. If Hailo hardware
or the DFC toolchain does not support int4 weights, this RFD
terminates with that finding and the operator picks the next
target (different NPU vendor, GPU-only int4 QAT via Torchao, or
wait for the field).

Model choice deferred to the first spike.

**First spike (parked):** verify Hailo hardware and DFC support int4.
**Loop:** forward fake-quant, STE backward, single quantized ckpt.
Torchao `Int4WeightOnlyQuantizer` or custom STE.
**Model priority:** small mtmd model first; workspace target after.

## Problem

PR #256 blocks bnb NF4 + post-quantization fine-tuning. PR #257
blocks PTQ. The compliant shape has no framework support for our
generative models; the only real-QAT FOSS today is Gemma 4 QAT
(language-only). This RFD closes that gap.

## Related

RFD 2186, RFD 2198, PR #256, PR #257, `[[hailo-ugen300-shelved]]`.

This RFD was drafted by an AI and read by a human before it shipped.
