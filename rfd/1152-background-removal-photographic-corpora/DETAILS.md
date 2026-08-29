# RFD 1152 details: the garment the union deleted

## Why a matting model rather than a segmenter

A dichotomous segmenter is trained against binary ground truth, so its only soft
pixels are silhouette antialiasing; a veil comes back either fully kept or fully
cut. A matting model is trained against real alpha, so partial transparency is a
value it can express.

The scale-free test is soft-alpha pixels per pixel of silhouette perimeter.
Antialiasing is a constant band along the outline, so it stays near 1 whatever
the subject. Transparency is area with no perimeter to pay for it.

Six photographs chosen for sheer fabric, specular surfaces and wispy hair:

| source | BiRefNet | BiRefNet-matting | HR-matting (2048px) |
|---|---|---|---|
| sheer lace | 4.01 | 1.58 | 2.84 |
| veil | 1.21 | 1.44 | 2.89 |
| latex | 1.02 | 2.08 | 2.61 |
| latex | 1.14 | 1.55 | 3.39 |
| wispy hair | 0.82 | 2.25 | 2.91 |
| missed garment | 1.85 | 2.94 | -- |

The segmenter clusters near 1.0 as predicted. The matting variants run higher,
and the high-resolution variant is the most consistent.

**This ratio ranks model families and must not be read per image.** The 4.01 is
the highest number in the table and is not transparency: it is a soft uncertainty
blob. The metric conflates partial alpha with an unsure model.

## Cost, and the dtype that decides it

HR-matting runs at 2048px, 5.7 s per image measured over 27 images on M2 Pro MPS,
against ~1.2 s for the 1024px variants. Weights are 220M parameters.

**Float16, not bfloat16.** BiRefNet's ASPP uses deformable convolutions, and MPS
ships `deformable_im2col_half` but not `deformable_im2col_bfloat`, so bf16 fails
inside the forward pass while fp16 is fine. Reading that bf16-specific error as
"no half precision available" forced fp32, and fp32 at 2048x2048 exhausts 32 GB
of unified memory: one image per five minutes with the machine paging, which
looked like the model being infeasible on this hardware. It is not. The dtype is
not about the weights, which are under a gigabyte either way; it is about
activations, where a single feature map at that resolution runs to gigabytes.

## Settled by ground truth

The alphamatting.com training set has true alpha, so the ordering does not need a
judge. On the 16 images all three backends completed (lower is better):

| backend | SAD | Gradient | Connectivity |
|---|---:|---:|---:|
| birefnet | 7.09 | 0.076 | 6.00 |
| birefnet-matting | 4.75 | 0.032 | 3.80 |
| birefnet-hr-matting | **4.42** | **0.026** | **3.16** |

`hr-matting < matting < segmenter` on every metric, none dissenting. HR-matting
separately completed all 27 images alone: SAD 4.48, MSE 1.370, gradient 0.04,
connectivity 3.97, consistent with the subset.

This also corrects the `soft_per_perimeter` proxy, which had ranked HR-matting
first for the right answer by an unreliable route, and RFD 1153's judged ordering,
which had ranked the segmenter best on gradient -- inverted, since ground truth
puts it roughly 3x worse.
