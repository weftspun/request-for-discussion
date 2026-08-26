# RFD 1142 details: what the Neural Engine reaches, and what it holds

Every number here is from `scripts/ane_bench.py` on one machine: Apple M2 Pro,
32 GiB unified, 16-core ANE, macOS 26.5.2, coremltools 9.0. A timing without the
machine is not a measurement, so the machine is printed by the script rather than
recalled into the table.

## The placement gate, and why it comes first

`rfd1122-plan.usda` carries `neuralEngineUsefulForBackbone = 0`, backed by 1685.1 ms
at 576 against the CPU's 476.4. That ran through ONNX Runtime's CoreML execution
provider, which partitions a graph and falls back per operator, and it recorded no
placement. So the number is consistent with two opposite worlds and selects neither.

`MLComputePlan` answers it per operation. Two details cost time to find:

- It requires a **compiled** model. Handed an `.mlpackage` it does not raise — it
  aborts the process with an `ios_base::failure` from libc++. The compile step is
  inside `placement()` so no caller can meet that.
- Constants carry no device and are **excluded from the denominator**. A graph is
  mostly weights, so counting them lets anything look well placed.

The negative control is `ComputeUnit.CPU_ONLY`, which cannot reach the device:

    positive (ComputeUnit.ALL)      ane=8/8   {'ane': 8}  consts=28
    negative (ComputeUnit.CPU_ONLY) ane=0/8   {'cpu': 8}  consts=28

Rule 2 is the whole reason that second line exists. A placement gate that has never
returned "no" certifies nothing, which is precisely the defect it was built to correct.

## Two ceilings, and the first sweep found neither

The first sweep grew width at depth 8 and found a cliff between 1543.7 MiB and
1599.3 MiB of fp16 weights, placement collapsing from 16/16 operations to 1/16.
Read alone, that says the device holds about 1.5 GiB.

It says nothing of the kind. Holding parameters near constant and changing the shape
moves the cliff:

    depth  width   params        pkg MiB   ANE fraction
    8      3584    809,392,640   1543.7    1.000
    8      3648    838,554,816   1599.3    0.062
    32     1704    810,263,928   1545.3    1.000
    32     1800    904,123,800   1724.3    1.000

A **larger** model passed where a smaller one failed. Shape decides the cliff; total size
fails to explain it.
The decisive control is a two-layer graph, where the total is small and one tensor is
large:

    depth  width   one weight   total MiB   ANE fraction
    2      3584    220.5 MiB    220.7       1.000
    2      3648    228.4 MiB    228.6       0.250
    2      4096    288.0 MiB    288.2       0.250

Same boundary as depth 8, at a seventh of the total. **The limit is a single weight
tensor between 220.5 and 228.4 MiB**, and 224 MiB sits inside that bracket. The sweep
resolution is one width step, so the bracket is the answer and 224 is a guess at a
round number inside it.

RETRACTED, IN THE SAME SESSION THAT WROTE IT: "the Neural Engine has no model-size
ceiling worth planning around. It has a layer-width ceiling." The second sentence
stands. The first was an artifact of stopping the sweep at 1.7 GiB, and the paragraph
is kept because the error is instructive — a shape control disproved a total-size limit
and was then read as proving no total-size limit existed. It disproved one number, not
the category.

### The total ceiling is 2 GiB, and it is exactly 2^31 bytes

Continuing the sweep with a deep, narrow stack — every tensor 55.6 MiB, far under the
per-tensor cap — finds the second limit:

    depth  width   weights MiB   ops   ANE fraction
    36     1800    1946.8         72   1.000
    37     1800    2002.4         74   1.000
    38     1800    2058.0         76   0.000
    40     1800    2169.3         80   0.000
    64     1800    3504.1        128   0.000

2048 MiB sits between the passing 2002.4 and the failing 2058.0, and 2^31 bytes is
2,147,483,648 against those two at 2,099,520,000 and 2,157,840,000. The limit is 2 GiB
of weights.

It is bytes rather than operation count, and one control separates them: depth 32 at
width 2020 carries 2171.5 MiB in only 64 operations and fails, while depth 36 at width
1800 carries 1946.8 MiB in 72 operations and passes. Fewer operations and more bytes
still fails.

When it fails it fails wholesale. Placement goes to 0.000 and every operation moves to
the GPU together, rather than the graph splitting across the two.

### What the literature does and does not say

Bryngelson's *Apple Neural Engine: Architecture, Programming, and Performance*
(arXiv 2606.22283) documents a per-axis extent cap of 16384 on the M1 generation,
"applied per-axis rather than to the last axis alone". The weights measured above are
`[3648, 3648, 3, 3]` — every axis is an order of magnitude inside that cap. So the
boundary found here is **not** the documented one, and searching turned up the reason:
Apple does not publish the internal buffer limits. This bracket is measured, not cited.

## Throughput, and a cliff that is not the ceiling

Convolution stacks at 3x3 stride-1, FLOPs counted as `2 * MACs` — `gpu_tops.py`'s
convention, so the numbers compose with the GPU rows already in the plan.

    width   GMAC/inf   ms med    TFLOP/s   of 15.8 peak   ANE fraction
    128       16.97      6.484     5.234   0.331          1.000
    256       67.76     15.339     8.835   0.559          1.000
    512      270.81     45.887    11.803   0.747          1.000
    768      609.15     89.694    13.583   0.860          1.000
    1024    1082.78    168.062    12.886   0.816          1.000
    1536    2435.93    371.910    13.100   0.829          1.000
    2048    4330.23   1319.102     6.565   0.416          1.000

**13.583 TFLOP/s, 86.0% of the cited 15.8 TOPS**, is the best rate with every
operation on the device.

The last row matters more than the best one. At width 2048 the rate halves while
placement stays at 1.000 — the work is still on the Neural Engine and is running at
half speed. Its weights are 72 MiB per tensor, well inside the 224 MiB cap, so this is
a bandwidth or residency effect and not the ceiling above. **Throughput degrades before
placement does**, which means a placement check alone is not a health check, and a
model sized by the cap alone will be slow before it is rejected.

## The same graph on Metal

The Neural Engine's rate means little without the other engine in the same machine
running the same work. `--units gpu` confines the identical convolution stack to
`CPU_AND_GPU`:

    width   GMAC/inf   ms med    TFLOP/s   placement
    512      270.81     80.472     6.731   {'gpu': 16}
    768      609.15    174.665     6.975   {'gpu': 16}
    1024    1082.78    311.664     6.948   {'gpu': 16}
    1536    2435.93    719.915     6.767   {'gpu': 16}

**6.98 TFLOP/s against the Neural Engine's 13.58 on the same graph — 1.95x.** This also
corroborates `gpu_tops.py`'s 6.20 TFLOP/s fp16 for this desk from dense GEMM, measured
by a different route on a different shape.

The GPU has no 2 GiB wall: it ran the 3504.1 MiB stack the Neural Engine refused. So
above 2 GiB this machine still executes the model, at half the rate.

## The comparison, on the two axes that decide it

Compared at ONE precision, fp16, because both parts offer a choice of precision and a
comparison across two of them measures the choice rather than the hardware.

| | M2 Pro ANE | M2 Pro Metal | Hailo-10H / UGen300 |
| --- | --- | --- | --- |
| fp16 rate | **13.58 TFLOP/s** measured | **6.98** measured | ~10 TOPS, halved from 20 INT8 |
| of cited peak | 0.86 of 15.8 | 1.03 of the 6.8 fp32 derivation | not measured, no device |
| weights it holds | **2 GiB**, measured | >= 3.5 GiB, measured | 8 GiB nominal |
| per-tensor cap | ~224 MiB, measured | none found | unknown |
| host bandwidth | ~200 GB/s | ~200 GB/s | USB 3.1 Gen2, ~1.2 GB/s |
| power | unmeasured, needs sudo | unmeasured | 2.5 W typical |

**The crossover is 2 GiB of weights.** Under it the Mac runs at 13.58 against the
UGen300's derived 10, and wins. Over it the Neural Engine refuses wholesale, Metal
picks the work up at 6.98, and the UGen300 holds its rate over four times the memory.

The earlier reading of this table had the memory axis backwards. It compared the Mac's
32 GiB of unified memory against the device's 8 GiB, when the quantity that decides
placement is the 2 GiB the Neural Engine will accept.

### Four confounds, stated rather than buried

1. **The units measure different work.** 13.58 TFLOP/s fp16 against 12 TOPS INT4
   assumes one INT4 operation is worth one fp16 operation. It does less. The comparison
   is generous to the Hailo, and it only holds under 2 GiB.
2. **The Hailo column is derived.** No UGen300 is attached to this machine and none of
   its rows were observed. RFD 1130 exists to replace them.
3. **0.86 is an upper bound, and it is this device's.** A 3x3 stride-1 stack is the
   friendliest shape either part sees. Carrying 0.86 across to the Hailo would be
   assuming what the plan already declines to assume at 0.3.
5. **The Hailo fp16 rate is halved from its INT8 row, not read from a datasheet.**
   20 TOPS INT8 halving to about 10 at sixteen bits follows the pattern its own INT4
   and INT8 rows set. The plan carries no fp16 entry for this part, and one belongs
   there before the crossover above is planned against.
4. **Power went unmeasured.** `powermetrics --samplers ane_power` needs sudo and was
   not run, so the 2.5 W column has no counterpart. Named and counted, per rule 3,
   rather than dropped to make the table symmetrical.

## The real model, converted natively, and what it settles

`rf-detr-cpp/scripts/gate_coreml_device.py` converts the same traced module
`gate_onnx_device.py` hands its exporter, so the two gates measure one graph by two
routes. 373 operations, resolution 576, num_windows 1, fp16, 2 resizes folded:

    units   ms med   max|diff|   bound 4.2e-03   placement
    ane      121.6   4.311e-02   FAIL            {'ane': 373}
    gpu       62.0   3.524e-03   ok              {'gpu': 373}
    cpu      133.0   2.425e-01   FAIL            {'cpu': 373}

**`neuralEngineUsefulForBackbone = 0` is settled, and its evidence is retracted.** The
flag came from 1685.1 ms through onnxruntime's CoreML provider, reproduced here at
3758.9 with `--num-windows 1`. Natively the same graph runs at 121.6 ms, so that route
was 31x pessimistic and was measuring a partitioner. The VERDICT stands on a different
ground: at fp16 the Neural Engine misses the port's own bound by ten times, while Metal
passes it and is twice as fast. A right answer held for a wrong reason is corrected
because the wrong reason predicts wrongly elsewhere.

Metal's margin is thin and worth stating: 3.524e-03 against 4.2e-03 is 1.19x of headroom.

### Three faults paid for on the way

**A coremltools bug, shimmed rather than vendored.** `_cast` validates its input as "a
scalar or a (1 x 1 x ... x 1) tensor", then its constant branch calls `dtype(x.val)`
without the squeeze its non-constant branch applies. `int(np.array([48]))` raises. The
device half hits it at `encoder/encoder/embeddings/68`, where transformers' Dinov2
`interpolate_pos_encoding` computes `sqrt_num_positions` as shape (1,). Identical at
torch 2.11.0 and at the tested 2.7.1, so the version warning was a red herring — which
is why `rf-detr-cpp` gained a `coreml` feature pinning the tested torch rather than
repinning the shared `gate`.

**An unimplemented operator, folded with the project's own fold.** coremltools has no
converter for `_upsample_bicubic2d_aa`. `gate_onnx_device._fold_antialias` already folds
it for the ONNX route, exactly because the resize reads a parameter and a size rather
than the image, so at fixed resolution folding is exact. Borrowed rather than
reimplemented, so the two gates cannot disagree about the graph they measured.

**A comparison that paired outputs by shape.** The device half returns two tensors of
identical (1, 256, 48, 48) shape, so the first version compared one reference against
the other output and reported 2.501e+00 on every row. The CPU row exposed it: Core ML's
own CPU cannot disagree with PyTorch by 2.5. Outputs are now assigned to their closest
free reference and the chosen pairing is printed, so the assignment is auditable.

## What this does NOT resolve

`neuralEngineUsefulForBackbone = 0` **stands**. The synthetic result makes it
surprising — a part reaching 86% of peak looks unlike something four times slower than
its own CPU — but surprise falls short of evidence. The RF-DETR device half was never converted
to Core ML and never placed here, so the flag is unexplained rather than retracted.
Retracting a measured flag on the strength of a different model would be the same
error the flag itself embodies.

The next measurement is that conversion: `pixi run device-gate` in `rf-detr-cpp`
exports the half, and `ane_bench.py` already carries everything else needed to place
and time it.

## Four bits, and why the column is absent

The first plan for this work measured a precision ladder. Two findings closed it early.

Core ML does store four-bit weights: an int4 package is exactly a quarter of the fp16
one on disk, 126.0 MiB against 504.1 at 264M parameters. But the graph gains eight
`ios18.constexpr_lut_to_dense` operations, which carry no device assignment, and the
sixteen arithmetic operations stay exactly where they were. The compute width does not
change, because the int4 and int8-int8 fast paths arrived with A17 Pro and M4 and this
is an M2. Four bits buys disk here and adds decompression.

The ladder was dropped when the memory axis looked unbounded. With the ceiling at 2 GiB
that reasoning no longer holds: four bits would quarter the weights and move a model
from Metal's 6.98 back onto the Neural Engine's 13.58, which is a real trade rather than
a disk saving. Reinstating the ladder is the next work this RFD asks for.

An `int4-linear` row would still close the question cheaply, and it remains unrun.
`--precisions int4-linear` is wired and takes minutes; `int4` k-means does not, at
these sizes, and hung a sweep at 838M parameters before it was killed.
