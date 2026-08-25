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

If the emulator cannot run a layer, that is RFD 1129's question. Record
it and stop, rather than substituting an operator to get a number.

## Four bits does not always buy speed, and here it bought none

Measured on the desk, OmniGen2 at 1024 square and 30 steps, same input
and same seed:

| precision | weights | peak | seconds |
| --- | ---: | ---: | ---: |
| bf16 | 14.75 GiB | 17.14 GiB | 131 |
| NF4  |  4.33 GiB |  6.72 GiB | 133 |

Four bits bought memory and **not** speed: 133 s against 131 s, because
dequantisation costs about what the narrower reads save on this card.
Report both numbers. A four-bit result presented as an optimisation,
with only the memory column shown, says something the measurement does
not.

The consequence is a decision rather than a preference. CLAUDE.md's
generated-synthetic condition 5 bars quantised weights from producing
corpus data, so a sweep run at NF4 is evidence that can never become
data. When four bits also costs time, there is nothing left to trade,
and the run should be bf16.

## Watch for the failure that does not raise

On Windows the WDDM driver pages into shared system memory rather than
returning an allocation failure. A configuration that does not fit does
not stop; it slows. Three cases in one session, none of which raised:

- TaylorSeer at 1024 square ran over eight minutes against 103 s for the
  row before it.
- Two bf16 pipelines started two seconds apart, 14.76 GiB each on a
  24 GiB card, both about 12x slow; a 131 s row took 27 minutes.
- A LoRA training step at 512 square did not complete in twelve minutes,
  and completed in 13.1 s at 256 square.

So a timing row is also a fit check. A step five times slower than the
step before it has not fitted, whatever the absence of an error implies.
`osqueryi` is the quickest way to see whether a second process is on the
card, because `nvidia-smi` reports per-process memory as `N/A` here.
