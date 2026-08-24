# RFD 1083: Emulating the operators an edge compiler refuses

**State:** discussion
**Feature:** running the whole keypoint graph on the accelerator, with no host cut
**Scope:** `3-interactor/rf-detr-cpp`, `2-contract/lean-deform-exact`, `5-repository/hailo-model-zoo`

## Problem

A dataflow accelerator refuses to compute an address from the data. That rules out
`GridSample`, `ScatterND`, `GatherElements` and `TopK` — the whole indexing family the
DETR decoder is built from. The accepted answer is to cut the graph and run the decoder
on the host, which is what Hailo's own DETR does and what 50 of its 127 zoo configs do.
A cut costs a USB round trip per frame and a host pipeline that has to exist.

## Decision

Emulate them. One kernel does all four: bilinear interpolation is a tent that vanishes
beyond one pixel, so at integer positions it is exactly a one-hot.

    out[i] = sum_k data[k] * tent(idx - k)      tent(t) = relu(1 - sqrt(t*t))

The index moves out of the ADDRESS and into a MULTIPLIER. The addresses were the
objection; the arithmetic never was.

1. **Trace before rewriting.** Fold what is constant. All 85 `ScatterND` indices were
   predicted constant and measured data-dependent, which deleted the cheap route.
2. **A parse is not a measurement.** It says the operators are expressible. Separate
   translation error from precision error, because they call for different fixes.
3. **Every rewrite ships a control that must fail.** One that agrees with whatever it is
   handed proves nothing.
4. **Report what was not measured.** No schedule, no cycle count, no device.

Measured: four rewrites accepted for `hailo10h`, exact to float64 roundoff, 1,549 layers
against the backbone's 336. Whether that beats the cut is unanswered — layers are not
cycles, and saying so is the finding rather than a caveat.

## Related

RFD 107a is the corpus this detector trains on. `weftspun/lean-deform-exact` proves the
deformable rewrite. `DETAILS.md` carries the procedures and the traps.
