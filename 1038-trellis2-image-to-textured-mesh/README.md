# RFD 1038: Model image for trellis2_image_to_textured_mesh

**State:** discussion
**Feature:** model packaging

## Problem

TRELLIS.2 is the default for image to 3D. It is the backbone of four
other catalog entries. A model image that packages it badly costs five
models, and not one.

## Decision

Package TRELLIS.2 once, and publish the image as the base for
RFD 1039, RFD 1047, RFD 1048, and RFD 1049. Those four add a
`predict.py`, and they add no weights.

See `DETAILS.md` for the model's memory and license, the `predict()`
interface, and why both flow stages stay in one container.

## Related

RFD 1036 gives the model image convention. RFD 1053 gives the asset
format. RFD 1026 gives the memory. RFD 1002 records the pipeline stage
this model fills.
