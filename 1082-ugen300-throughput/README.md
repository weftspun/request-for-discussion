# RFD 1082: What the UGen300 actually delivers

**State:** discussion
**Feature:** edge throughput measurement
**Scope:** `3-interactor/rf-detr-cpp`

## Problem

The ASUS UGen300 is a Hailo-10H behind USB 3.1 Gen2. Two numbers are
published and neither is the one that matters: the accelerator's
compute, and the bus at 10 Gbps, about 1.2 GB/s.

What a pipeline gets is neither, because a USB accelerator pays for
every crossing. Resident weights cost nothing per frame and streaming
weights cost everything, and which happens depends on whether the
model fits 8 GB after quantisation. No measurement here has said.

## Decision

Measure the device, once the two questions before it have answers.
RFD 1080 asks whether four bits are survivable and RFD 1081 asks
whether the operators compile. Throughput measured on a model that
fails either is a number about nothing.

Report three quantities rather than one rate: time to first output,
which includes transfer; steady-state rate once transfer amortises;
and transferred bytes per inference, which separates a resident model
from a streaming one and predicts other hardware.

Compare against the 3090 on the same input, saying plainly that it is
a workstation card against a USB stick. The point is not which wins,
but what the accelerator costs and buys.

See `DETAILS.md` for the rig and the confounds. `SKILL.md` gives the
procedure.

## Related

RFD 1080 and RFD 1081 come first. RFD 107a is the goal, and its
detector is what ships to this device.
