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

Ten of twelve. Four carry runtime measurements, which is not
nothing, but a model that runs on a 3090 has said nothing about
whether it compiles for a dataflow part.

## Rung 1 -- exports to ONNX

    model                  [1166]  evidence

    VoxHammer, DINOv2 stage  [12]  1343 nodes, 22 operators, at
                                   [1,3,518,518] fixed. onnxruntime
                                   against torch: max|diff| 6.027e-04
                                   over max|ref| 120.355, 5.008e-06
                                   relative.

It went straight to rung 2 in the same run, so it is listed there
rather than resting here. It is the first model other than rf-detr to
earn a rung instead of being estimated onto one.

**THE EARLIER WORDING OF THIS SECTION FLATTERED US, AND THE EARLIER WORDING FLATTERED
US.** It said everything reaching rung 1 went further in the same
sitting, which reads as though the rung were merely a place nobody
lingers. Enumerating the checkouts says otherwise: across the whole
workspace, `torch.onnx.export` appears in `rf-detr-cpp` and in two
projects that are not candidates at all. Ten of the eleven others
have no export site of any kind.

Rung 1 is empty because nobody has written the export, not because
everybody sprinted past it. The rung is still the cheap one -- no
weights, no device, no rented card -- and that is now an argument
about work not yet started rather than work that left no trace.

## Rung 2 -- the operator set is known

    model                  [1166]  evidence

    VoxHammer, DINOv2 stage  [12]  22 operators, every one inside
                                   `DEVICE_OPS` -- the same allowlist
                                   rf-detr's device half carried
                                   through DFC 5.3.0 at 825 nodes.
                                   Nothing refused, so rung 3 is the
                                   next thing to run rather than the
                                   next thing to argue about.

    TRELLIS.2 / Pixal3D      [11]  the SS stage exports at 544 nodes
                                   with RoPE rewritten in reals,
                                   bit-identical at max|diff| 0.000e+00.
                                   28 operators, of which `Cos`, `Sin`
                                   and `ReduceL2` sit outside
                                   DEVICE_OPS. Rung 3 refused it in
                                   `_add_input_layers`, four times, on
                                   input rank rather than arithmetic.

**No script in this workspace reproduces that row.** `pixal3d-upstream`
has no export site, and the RoPE rewrite that produced 544 nodes lived
in a scratch file that is gone. The measurement is recorded and the
apparatus is not, which is the half CLAUDE.md asks for by name. Rung 2
therefore rests on a number nobody here can re-derive, and re-earning
it means writing the export that should have been committed the first
time.

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

## What rung 0 does not distinguish, and should

Rung 0 reads `blocklist clear, checkout present`, and eleven rows
satisfy it. They do not satisfy it in the same way, and the single
label hides two kinds of row that can never climb as written.

**Three rows have no model on disk.** Kimodo and SkinTokens are
`server.py` and nothing else: every path outside `WEFTSPUN_STUB=1`
raises `NotImplementedError`, so what is checked out is an HTTP
contract, not a network. `cyclegan_style_transfer` is the same shape
with a checkpoint path in it -- one file, no `nn.Module` anywhere.
For these three, rung 1 is not the next step; acquiring the model is.

**Two rows are not neural networks at all.** MuJoCo MJX is a physics
engine and Mitsuba 3 is a renderer. Neither has weights, neither has
a graph to export, and the ladder from ONNX through the Dataflow
Compiler is the wrong instrument for both. They sit at rung 0 the way
a boat sits at the bottom of a staircase. Accelerating them is a real
question and it is a different one, so the honest entry is `not on
this ladder` rather than a rung.

That leaves **eight rows the ladder actually measures**: rf-detr,
OmniGen2, EditScore, MoGe, Pixal3D/TRELLIS.2, VoxHammer, See-Through
and -- once it has a model -- CycleGAN. Seven of the eight hold real
module and checkpoint code, so for them rung 1 is genuinely the next
thing rather than a placeholder.

## What the shape of this says

The ranking's top three have never been exported and its eleventh has
been further up the ladder than any of them. That is not a fault in
the ranking -- RFD 1166 asks what is worth doing -- but it is why the
two tables are separate documents.

That was written with rung 1 empty, and the cheapest thing that would
change the picture was said to be an export of anything -- VoxHammer's
DINOv2 stage being the shortest, a stock checkpoint at a fixed
resolution in a family already cleared at rung 3.

**It was, and it cost one script.** 1343 nodes, no refused operator,
and two rungs in a single run. The prediction is kept because it was
made before the measurement rather than after it, which is the only
condition under which a prediction is worth anything.

Six of the eight measurable rows have still never been exported, and
the same argument applies to each of them unchanged.
