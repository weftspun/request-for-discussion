---
name: ugen300-throughput-measurement
description: Measure what a Hailo-10H USB accelerator delivers in practice, separating transfer from compute. Use when deciding whether a stage belongs on the device, and whenever a published TOPS figure is about to be quoted as throughput.
---

# Measuring a USB accelerator

A rate without a transfer figure beside it is not a measurement of a
USB device, because the bus is the part that decides.

## Order

1. **Check the prerequisites are answered.** RFD 1128 for four-bit
   tolerance, RFD 1129 for operator coverage. Measuring throughput on a
   model that fails either produces a number about nothing.
2. **Time the first inference on its own.** Cold: compilation,
   allocation and weight transfer included. Report it as its own row.
3. **Run long enough to amortise.** Ten minutes rather than ten
   seconds, because a USB stick's thermal budget is small and the
   short number is the optimistic one.
4. **Record transferred bytes per inference.** This is what says
   whether the weights are resident, and it is the quantity that
   transfers to a different bus or a different host.
5. **Repeat on the 3090 with the same input**, and state in the table
   that it is a workstation card against a USB stick.

## Traps

Nothing else may use the controller during a run. USB bandwidth is
shared and a background copy silently halves the result.

Do not average the cold inference into the steady-state rate. They
answer different questions and the mean answers neither.

TOPS is not throughput. It is a ceiling under conditions nobody
reaches, and quoting it as a rate is how a plan acquires a number that
was never measured.
