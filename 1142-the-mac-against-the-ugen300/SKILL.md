---
name: neural-engine-placement-and-ceiling
description: Measure whether work actually reached the Apple Neural Engine, and what that device can hold. Use before quoting any Core ML latency, whenever a part is called slow without a placement check, and when sizing a model for an accelerator.
---

# Measuring a Neural Engine without fooling yourself

The result is a placement fraction and a rate, in that order. A latency
without a placement fraction is the mistake this procedure exists to
stop: it is consistent with the device being slow and with the device
never having run, and those have opposite consequences.

## Order

1. **Run the self-test first.** `ane_bench.py selftest` asserts a
   positive AND a negative control. If the negative control ever
   reports operations on the Neural Engine, stop — nothing measured
   after that means anything.
2. **Place before you time.** Every row `ane_bench.py` prints carries
   its own ANE fraction. Read that column before the millisecond
   column, every time.
3. **Sweep shape, not just size,** when looking for a ceiling. A sweep
   that only grows width finds a number that misses the limit. See the
   trap below.
4. **Report the bracket, not a round number.** The sweep resolution is
   one step. If 220.5 MiB passes and 228.4 fails, the answer is that
   bracket; 224 is a guess inside it.
5. **State what went unmeasured.** Power needs sudo and stayed unrun
   here. Name it rather than omitting it — an unmeasured row and a zero
   row look identical in a table that does not say.

## Traps

**`MLComputePlan` needs a compiled model.** Handed an `.mlpackage` it
does not raise. It aborts the process with an `ios_base::failure` from
libc++, which reads like a crash in your own code.

**Constants have no device.** Leave them in the denominator and a graph
of mostly weights looks well placed no matter where the arithmetic ran.
Exclude `const`, and name what is left rather than pooling it: an
`unreported` bucket hides `constexpr_lut_to_dense`, which is expected to
carry no device, among ops that genuinely failed to place.

**Expect TWO ceilings, and find both.** On an M2 Pro there is a cap on
any single weight tensor near 224 MiB, and a separate cap on total
weights at exactly 2 GiB, 2^31 bytes: 2002.4 MiB places entirely on the
device and 2058.0 MiB places entirely on the GPU.

Finding one hides the other. A width sweep alone reports "about 1.5
GiB" and means the per-tensor cap. A shape control then disproves that
total-size reading — and the trap is to read the disproof as showing no
total limit exists. It disproves one number. Sweep depth as well, with
tensors held small, until the second wall appears.

Separate bytes from operation count before believing either. Depth 32
at width 2020 carries 2171.5 MiB in 64 operations and fails; depth 36
at width 1800 carries 1946.8 MiB in 72 operations and passes. Fewer
operations and more bytes still fails, so the limit is bytes.

**Throughput degrades before placement does.** At width 2048 the rate
halved while placement stayed at 1.000. The work was on the device and
running at half speed. So a placement check is not a health check, and
a model sized only by the per-tensor cap will be slow before anything
rejects it.

**Your own grep can manufacture a silent skip.** A sweep here appeared
to produce six agreeing int4 rows. Two rows had failed on a missing
`scikit-learn` and the filter that tidied the output had removed them.
Read the JSON, not the console, when a row is absent.

**A floor-only version pin can buy nothing.** `scikit-learn >= 1.4`
installed 1.9.0, which coremltools 9.0 refuses with *"Disabling
scikit-learn conversion API"* — a warning, after which k-means
palettization fails exactly as if the package were missing. The pin
needs both ends.

## Four bits, on a part that computes in sixteen

Core ML will store four-bit weights: the package is a clean quarter of
the fp16 one. On an M2 the arithmetic does not change — the int4 and
int8-int8 fast paths arrived with A17 Pro and M4 — and the graph gains
`ios18.constexpr_lut_to_dense` operations that carry no device.

So four bits buys disk and adds decompression. Ask what the memory is
for before reaching for it: with 32 GiB and no total-size ceiling, it
buys real capacity once a ceiling is in view. Under a 2 GiB wall,
quartering the weights moves a model from the GPU's rate back to the
Neural Engine's, which on this part is a 1.95x difference. Ask what the
ceiling is before deciding four bits buys only disk.

Do not use `mode="kmeans"` on a large tensor to find this out. It
clusters single-threaded and a sweep at 838M parameters does not finish.
`int4-linear` answers the same question in minutes.
