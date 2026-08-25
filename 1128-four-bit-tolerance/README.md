# RFD 1128: Does the cascade survive four bits

**State:** discussion
**Feature:** quantisation tolerance for edge deployment
**Scope:** `3-interactor/pixal3d-image-to-textured-mesh`

## Problem

The ASUS UGen300 is a Hailo-10H with 8 GB, specified for 4-bit
weights. Pixal3D's checkpoints are 24.045 GB in bf16, three times the
device. At four bits they are about 6 GB, which fits.

So the arithmetic permits it and nothing says the model survives it. A
1.3B diffusion transformer at four bits may produce a mesh nobody can
tell from the original, or a worse one, or a broken one. RFD 1043
records the same open question for another model.

## Decision

Measure tolerance first, because a failure here makes RFD 1129's
operator work pointless.

The 3090 is the instrument. Its 24 GB holds bf16 and four-bit forms of
one stage at once, so the same input runs both ways and the difference
is the quantity. The device cannot do this: 8 GB holds one form.

Three rules make it mean something: the input is identical rather than
similar, since `render_view.py` is bit-reproducible; the baseline is
bf16 on this card rather than a paper; and the error is millimetres of
surface deviation rather than an impression.

Quantise with the Dataflow Compiler: bitsandbytes measures a four-bit,
and the DFC's host emulator runs the device's.

See `DETAILS.md` for the apparatus, and `SKILL.md` for the order.

## Related

RFD 1129 asks whether the operators compile. RFD 1040 packages the
model, and RFD 1122 is the goal this serves.
