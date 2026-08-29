# RFD 1171: The presence loop, and every role in it

**State:** ideation
**Feature:** make a persona, dress it, be it, make a friend
**Scope:** `3-interactor`

## Problem

RFD 1166 ranked twelve models against each other and never says **what
any of them is for**, so a reader cannot tell which stage is missing.
Ranking stages of one pipeline against each other was the error.

## Decision

One loop, four movements:

    make      language and an image become a persona
    dress     its worn layers are swapped and tried on
    be it     a person wears it, live, through a camera
    a friend  it wears itself, and has presence to someone

**`be it` and `make a friend` are the same avatar and opposite loops.**
In the first a person supplies motion and voice; in the second nobody
does. That is why Kimodo sits beside rf-detr rather than behind it.

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

## Related

RFD 1166 has the measurements; 1168, 1169 and 1170 the mechanisms.
