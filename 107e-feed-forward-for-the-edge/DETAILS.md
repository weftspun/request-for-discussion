# RFD 107e details: the stage classification, the part, and what the student costs

Every section names its gate in an HTML comment under its heading, per RFD 107d.

## The six stages, by kind

<!-- gate: ste100 -->

RFD 107a's `DETAILS.md` lists what each stage recovers. This table adds what
each stage *is*, which is the property the hardware question turns on.

| stage                     | kind                            | runs on an NPU |
| ------------------------- | ------------------------------- | -------------- |
| RF-DETR wholebody, 104 kp | feed-forward graph              | yes, see below |
| `AnnyInverter` and LBFGS  | `float64` descent loop          | no             |
| silhouette fit            | differentiable raster, descent  | no             |
| depth fit and Marigold    | one model, then a descent fit   | model only     |
| MediaPipe, 51 ARKit       | feed-forward graph              | yes            |
| hm08 groups on the fit    | mesh set operations             | no, host CPU   |

`4-entities/anny-pose-retarget-work/lbfgs_polish.py` line 16 builds the model
`.to(dtype=torch.float64)`, and the comment states "float64 for tighter
numerical convergence". The accelerator carries INT8 activations. The mismatch
is one of kind, and more devices do not reduce it.

## What the part is

<!-- gate: ste100 -->

The ASUS UGen300 carries a Hailo-10H: 20 TOPS INT8, 40 TOPS INT4, 8 GB
LPDDR4-4266, over USB 3.1 Gen2 Type-C at 10 Gbps.

Five properties decide this RFD. Each is sourced, not assumed.

1. **Inference only.** The flow is a pretrained model, then the Dataflow
   Compiler, then a HAR file, then a HEF for HailoRT. No training path exists.
2. **No model parallelism across chips.** HailoRT's VDevice schedules whole
   network groups over several devices. The documented way to split one network
   puts one part on the device and the rest on the host CPU.
3. **The generative envelope is near 1.5B.** Hailo's own engineering note runs
   Qwen2-1.5B-Instruct in 1.2 GB with a 2K KV-cache. Marketing cites
   Llama2-7B at 10 tokens per second.
4. **"4-bit" describes the weights only.** The scheme is INT4 group-wise
   weights, INT8 per-tensor activations, and an INT8 KV-cache. Read the compile
   report for the per-layer assignment; do not infer it from the headline.
5. **`grid_sample` blocks the DETR family.** RT-DETRv2 added a
   `discrete_sample` operator because `grid_sample` limits deployment. The
   Hailo Model Zoo carries DETR with a ResNet-50 backbone, which uses dense
   attention. That is not evidence about deformable attention.

## Two things the port does not have

<!-- gate: ste100 -->

`3-interactor/rf-detr-cpp` holds no ONNX export. The port is GGUF and ggml from
end to end, and `src/ops.cpp` line 94 selects between `GGML_TYPE_F16` and
`GGML_TYPE_F32` and nothing else. Phase 2 training is ggml autodiff.

`src/deform_attn.cpp` is a core component, not an option. Its bilinear gather at
learned offsets is the operation item 5 above names.

So the go/no-go test costs one device: export the existing COCO-17 keypoint head
to ONNX, gate it against `gen_reference/` at the tolerances `test_keypoints`
already holds, and compile it. The Dataflow Compiler fails at compile time
rather than falling back for each operation, so the answer is unambiguous.

## The fitter licence survey

<!-- gate: ste100 -->

`3-interactor/pose-consensus/python/backend_licenses.py` gives the shape. Every
off-the-shelf fitter fails it.

| candidate    | licence               | verdict                                      |
| ------------ | --------------------- | -------------------------------------------- |
| Multi-HMR    | CC-BY-NC-SA-4.0       | denied twice: NC is the Sapiens class, and SA is blocklisted |
| Sapiens      | CC-BY-NC-4.0          | denied already, and recorded in the roster   |
| SAM 3D Body  | "SAM License"         | field-of-use restrictions, which propagate like OpenRAIL. Its DINOv3 backbone carries separate terms |

Read the SAM License and the DINOv3 terms from the LICENSE file before any use.
A model card is not a licence, and this roster admits nothing on a card alone.

## What ten devices buy

<!-- gate: ste100 -->

Once the chain is feed-forward it holds four models: the keypoint head, the ANNY
student, MediaPipe, and Marigold if it survives. Together they stay well below
8 GB, so one device holds them.

Ten devices give ten independent streams, or four models resident at once with
no reconfiguration between frames. They do not pool into 80 GB, and they do not
split one model. Buy one for the go/no-go test above.

## Why the student is affordable

<!-- gate: tropes -->

The substitution looks expensive and is not, because the corpus RFD 107a already
builds is the corpus a regressor needs.

Look at what the schema holds. `identities` carries 11 phenotype values, 256
local changes and 52 facial actions. `pose_rotations` carries a 3x2 rotation per
bone. Both are authored relations, reached by foreign key from `renders`. Every
frame therefore arrives with its pose and its identity attached, true by
construction rather than annotated. A regressor wants exactly this supervision,
and the renderer already produces it for a different reason.

RFD 107a's own flowchart branches a second student off the verified frames to
fine-tune Pixal3D. This is a third student at the same branch point, and the
marginal cost is one training run rather than a new corpus.

One simplification follows and is worth naming, because it removes a model
rather than adding one. `depth_map` is an emitted relation, so depth can
supervise the student during training instead of being computed at inference.
If that holds, Marigold leaves the deployed chain entirely. It also removes a
signal, which is a change to measure rather than a saving to assume.

## What this decision costs

<!-- gate: tropes -->

Two costs, and neither is hypothetical.

RFD 107a states that "every fit here is descent through a forward we own", and
that "where the forward is differentiable there is no inverse model to license,
train or trust". After this decision the first clause still holds and the second
does not. There is an inverse model now. It is ours, so nothing is licensed, but
it has to be trained and it has to be trusted, and trust here means measured.
That retraction belongs in RFD 107a beside the sentence it corrects, which is
where RFD 1000 says a retraction goes.

The second cost is subtler and more dangerous. The student and the keypoint head
would learn from the same renders, so their errors can agree. A chain whose
stages fail together looks like agreement and is not. This is the failure that
ended the estimator panel, where three COCO-trained members looked like three
opinions and were one lineage. It returns here through a different door, and the
answer is the same: report the joint failure rate against the product of the
marginals, and treat a correlated pair as one member rather than two.

## What is not decided here

<!-- gate: ste100 -->

Whether `grid_sample` compiles. That is a measurement, it costs one device, and
this RFD states the test rather than predicting the result.

If it does not compile, cut the graph at the backbone and decoder seam. The
DINOv2 backbone and the multi-scale projector go to the device, and the
deformable decoder stays on the host. Both seams have passing tests already:
`test_backbone` at 2.5e-4 or better, and `test_projector` at 1.0e-5. Report
device time, host time and bus time as three numbers, because one end-to-end
figure hides which side carries the cost.
