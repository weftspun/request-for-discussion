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
In the first a person supplies the motion and voice; in the second
nobody does. That is why Kimodo sits beside rf-detr rather than behind
it, and why a cloned voice is a persona's property.

**The See-Through taxonomy is the vocabulary and already splits right.**
`VALID_BODY_PARTS_V3` names 23 parts, nine of them worn — `headwear`,
`eyewear`, `earwear`, `neckwear`, `topwear`, `handwear`, `bottomwear`,
`legwear`, `footwear`. The rest are body, and **that line is the try-on
axis**, drawn by somebody solving a different problem.

**A try-on is masking treated as corruption**: remove `topwear`, LaMa
fills the hole, the new garment takes its place — RFD 1168's mechanism.
`DETAILS.md` places every candidate and names the five empty stages.

## Related

RFD 1166 holds the measurements; RFD 1168 the masking mechanism, 1169
the ear and voice, 1170 the cleanroom study.
