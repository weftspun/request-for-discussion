# RFD 1167 details: one table per rung, and the evidence for each place

Ranks in brackets are RFD 1166's, carried so the two can be read
together without being confused for each other.

The rungs run low to high, which is also early to late: a model
climbs, so the document is read in the order the work happens.

## Rung 0 -- assessed, never exported

    model                    [1166]  what the score rests on

    cyclegan_style_transfer     [2]  read only
    OmniGen2                    [3]  measured at runtime, not exported:
                                     131 s bf16, 133 s NF4, 14.75 GiB
    EditScore, Qwen3-VL-8B      [4]  measured at runtime: 6.75 GiB NF4,
                                     28-36 s a score
    Kimodo                      [5]  RFD 1026 estimate
    MoGe                        [6]  read only; a Pixal3D dependency
    SkinTokens                  [7]  RFD 1026 estimate
    MuJoCo MJX                  [8]  read only
    Mitsuba 3 shading           [9]  measured at runtime: 14.1 ns a
                                     pixel shading, 48.1 G-buffer
    See-Through                [10]  RFD 1026 estimate
    VoxHammer                  [12]  read only, and its DINOv2 stage is
                                     rung-1-ready: stock
                                     `dinov2_vitl14_reg` at 518 square,
                                     150 passes an asset

Eleven of twelve. Four carry runtime measurements, which is not
nothing, but a model that runs on a 3090 has said nothing about
whether it compiles for a dataflow part.

## Rung 1 -- exports to ONNX

    model    evidence

Empty as a resting place. Everything that reached it went further in
the same sitting, which is what makes rung 1 the cheap one: it costs
no weights, no device and no rented card.

## Rung 2 -- the operator set is known

    model                  [1166]  evidence

    TRELLIS.2 / Pixal3D      [11]  the SS stage exports at 544 nodes
                                   with RoPE rewritten in reals,
                                   bit-identical at max|diff| 0.000e+00.
                                   28 operators, of which `Cos`, `Sin`
                                   and `ReduceL2` sit outside
                                   DEVICE_OPS. Rung 3 refused it in
                                   `_add_input_layers`, four times, on
                                   input rank rather than arithmetic.

## Rung 3 -- the Dataflow Compiler accepts the graph

    model              [1166]  evidence

    rf-detr keypoint      [1]  825 nodes, 22 operators, parse OK on
                               arch hailo10h, operators outside the
                               allowlist: none. 61 s to translate.

One model. It is also the only row in RFD 1166 whose scores rest on
something run rather than read.

## Rung 4 -- quantises

    model    evidence

Empty, and rf-detr has attempted it twice. Statistics Collector took
SIGKILL at Docker's 30.26 GiB, cleared by a 48 GB ceiling; then
Quantization-Aware Fine-Tuning exhausted the 3090's 24 GiB at the
default batch and again at `batch_size=1, epochs=1` over 64 frames.
RFD 1165 carries that retraction.

## Rung 5 -- runs on the device

    model    evidence

Empty. No HEF has executed on `usb/004:013` from this workspace. The
device itself is measured -- HAILO10H, firmware 5.3.2, 2.27 ms
hardware latency on a zoo classifier -- but nothing of ours has
reached it.

## What the shape of this says

The ranking's top three have never been exported and its eleventh has
been further up the ladder than any of them. That is not a fault in
the ranking -- RFD 1166 asks what is worth doing -- but it is why the
two tables are separate documents.

The cheapest thing that would change this picture is rung 1 on
anything: an export costs no weights, no device and no rented card,
and `gate_onnx_device.py` already does it for one model. VoxHammer's
DINOv2 stage is the shortest of those, being a stock checkpoint at a
fixed resolution that the same family already cleared at rung 3.
