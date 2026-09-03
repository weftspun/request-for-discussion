# RFD 2187: Identity ANNY via OmniGen2

**State:** discussion
**Feature:** hair/eyes/skin/face overlay on the ANNY base mesh
**Scope:** identity stage of the atelier-workshop, upstream of RFD 2183

Shelved 2026-09-02: waiting for RFD 2183 (layer-decomp pipeline)
baseline from CUDA and for training compute on the 3090.

## Decision

OmniGen2 (Apache-2.0 on Qwen-VL-2.5) generates hair, eye, skin,
and face-detail overlays on the ANNY base mesh, once per character
(frozen across scenes, unlike dressing in RFD 2186 which changes
per frame).

Owns V3 parts (See-Through's taxonomy, RFD 2183 stopgap):
`front-hair`, `back-hair`, `iris`, `eyewhite`, `eyebrow`,
`eyelash`, `mouth`, `ear`.

Trained under RFD 2184's three-signal pattern: EditScore (RFD 1157
reward model) for semantic quality, cross-view consistency on
`sphere_hammersley_sequence` renders for anti-hacking, and
constructed anchor data (real anime character reference,
licence-clean corpus TBD).

## Problem

ANNY is a template mesh, not a character. No hair, no iris colour,
no eyelash, no eyebrow, no skin detail, no mouth painting. RFD
2183's layer-decomp pipeline assumes an identified character; those
V3 training pairs cannot exist without this stage.

## Related

RFD 2183 (layer-decomp pipeline; consumes this), RFD 2184 (EditScore
three-signal training pattern), RFD 2186 (dressing overlay, parallel),
RFD 2136 (gacha ladder; slots upstream of Rung 6).

This RFD was drafted by an AI and read by a human before it shipped.
