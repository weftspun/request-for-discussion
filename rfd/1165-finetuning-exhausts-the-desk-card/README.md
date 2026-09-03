# RFD 1165: Fine-tuning exhausts the desk card, and batch size is the lever

**State:** ideation
**Feature:** the second wall in the compile
**Scope:** `3-interactor/rf-detr-cpp/scripts/compile_hef.py`

## Decision

**RETRACTED 2026-08-29: this said batch size was the lever, and it is
not.** A probe at `batch_size=1, epochs=1` on 64 frames raised the same
`AccelerasResourceError` after 44 minutes.

**The requirement is measured: QAFT needs 32.5 GiB, on an A40.** The
desk 3090 holds 24, so the shortfall is 8.5 GiB and no batch size
closes it. Separately, `a16_w16` is refused by this part outright --
twelve `precision_change` layers the target will not take -- so
`a8_w8` is the precision ceiling. `DETAILS.md` carries both.

## Problem

Two walls stopped this compile, and they are different walls.

The first was system memory. Statistics Collector took SIGKILL at
Docker's 30.26 GiB; raising `.wslconfig` to 48 GB cleared it and the
stage completed in 14:58. The run peaked at 39.87 GiB, 85 per cent of
the new ceiling and well above the old, so the lift was load-bearing.

The second is video memory, and no amount of system RAM answers it:

    AccelerasResourceError: GPU memory has been exhausted. Please
    try Quantization-Aware Fine-Tuning with lower batch size.

QAFT ran about thirty minutes of epoch 1 of 4 on 1024 frames and
exhausted 24 GiB. RFD 1140 says match the card to the wall you hit;
clearing the RAM ceiling only bought the right to meet this one.

## Related

RFD 1140 rents the card. RFD 1163 divides the work. RFD 1164 says
what the calibration set becomes. RFD 1167 places the rung.
