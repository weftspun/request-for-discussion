# RFD 1171: The presence loop, and every role in it

**State:** ideation
**Feature:** make a persona, dress it, be it, make a friend
**Scope:** `3-interactor`

## Decision

One loop, four movements, and each runs both ways:

    forward                     inverse

    make    a description -> a body   fit      a picture -> the body
    dress   a layer onto the body     recover  the body out from under
    be it   a person supplies motion  friend   a model supplies it

**Each inverse is under-determined, which is why every one has a
checker** and why Kimodo sits beside rf-detr rather than behind it.

**The See-Through taxonomy is the vocabulary.** `VALID_BODY_PARTS_V3`
names 23 parts, nine worn and the rest body, and **that line is the
try-on axis**. A try-on is then masking treated as corruption: remove
`topwear` and LaMa fills the hole the garment leaves.

**The boundary is subtraction, not segmentation.** The posed ANNY mesh
gives the body outline through `silhouette.py`; MoGe depth gives the
person's outline and the camera both project through. What lies between
is worn — no taxonomy-aware segmenter, so no labelled corpus.
`contour.py` makes either a fixed ring. `DETAILS.md` places every
candidate and names the empty stages.

## Problem

RFD 1166 ranked twelve models against each other and never says **what
any of them is for**, so a reader cannot tell which stage is missing.
Ranking stages of one pipeline against each other was the error.

## Related

RFD 1166 has the measurements; 1168, 1169 and 1170 the mechanisms.
