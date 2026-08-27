# RFD 1152 details

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

## Cost

HR-matting runs at 2048px and takes 5-9 s per image against 1.2 s for the 1024px
variants, on M2 Pro MPS. Weights are 220M parameters.

Float32, not bfloat16: BiRefNet's ASPP uses deformable convolutions and MPS has
no bf16 kernel for them, failing with `Failed to create function state object
for: deformable_im2col_bfloat`. At 220M parameters fp32 is under a gigabyte.

## What is not settled

Whether HR-matting is actually the best of the three. The ranking above rests on
a proxy that is known to misfire, and the attempt to confirm it with a judge is
recorded in RFD 1153, which did not succeed at ranking. The claim that all three
successfully remove the background is confirmed; the ordering among them is not.
