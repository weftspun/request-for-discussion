# RFD 1165: Fine-tuning exhausts the desk card, and batch size is the lever

**State:** ideation
**Feature:** the second wall in the compile
**Scope:** `3-interactor/rf-detr-cpp/scripts/compile_hef.py`

## Problem

Two walls stopped this compile, and they are different walls.

The first was system memory. Statistics Collector took SIGKILL at
Docker's 30.26 GiB; raising `.wslconfig` to 48 GB cleared it and the
stage completed in 14:58. The run then peaked at 39.87 GiB, which is
85 per cent of the new ceiling and well above the old one, so the
lift was load-bearing rather than precautionary.

The second is video memory, and no amount of system RAM answers it:

    AccelerasResourceError: GPU memory has been exhausted. Please
    try Quantization-Aware Fine-Tuning with lower batch size.

QAFT ran about thirty minutes of epoch 1 of 4 on 1024 frames and
exhausted 24 GiB. RFD 1140 says match the card to the wall you hit;
this is a second wall behind the first, and clearing the RAM ceiling
only bought the right to meet it.

## Decision

Lower the fine-tune batch size before renting anything:
`post_quantization_optimization(finetune, policy=enabled,
batch_size=2)` parses against this HAR and costs nothing.

Rent only if that fails. More video memory does answer it -- the
L40S rented earlier carries 48 GiB against the desk's 24 -- but
paying to avoid a one-line directive is the wrong trade.

## Related

RFD 1140 rents the card. RFD 1163 divides the work. RFD 1164 says
what the calibration set becomes.
