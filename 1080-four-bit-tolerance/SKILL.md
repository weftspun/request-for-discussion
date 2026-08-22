---
name: four-bit-tolerance-measurement
description: Measure whether a model survives four-bit quantisation, using bf16 on the same card as the baseline. Use before any edge-deployment work, and whenever somebody reports that a quantised model looks fine.
---

# Measuring four-bit tolerance

The result is a distance in millimetres, not an impression. If the
procedure ends with somebody looking at two meshes and nodding, it was
not this procedure.

## Order

1. **Render the input once, deterministically.** `render_view.py` with
   `--threads 1`, and confirm the repeat render reports IDENTICAL
   before going further. An input that differs between runs makes
   every later number meaningless.
2. **Run bf16 first.** Keep the mesh and the seed. This is the
   baseline and it comes from this card, not from a paper.
3. **Quantise with the DFC** rather than a general tool, and run its
   host emulation on the same input.
4. **Compare surfaces, not pictures of surfaces.** Median, p95 and
   maximum deviation in millimetres, each with a household equivalent.
5. **State the detection floor.** A sampled comparison sees defects
   larger than about 3/n. For a fixed vertex set, enumerate instead.

## Traps

`--fov` is radians. 40 degrees is 0.698; passing 40 means 2292 degrees
and the run will look like it worked.

An identical-looking mesh with one moved extremity is the expected
failure mode, so a single mean deviation hides exactly what matters.

Do not compare a four-bit run against a published bf16 figure. The
baseline is free here, and a borrowed one is not a baseline.

If the emulator cannot run a layer, that is RFD 1081's question. Record
it and stop, rather than substituting an operator to get a number.
