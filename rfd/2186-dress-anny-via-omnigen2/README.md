# RFD 2186: Dress ANNY via OmniGen2

**State:** discussion
**Feature:** clothing/accessory overlay on the ANNY base mesh
**Scope:** dressing stage of the atelier-workshop, upstream of RFD 2183

Shelved 2026-09-02: waiting for RFD 2183 (layer-decomp pipeline)
baseline from CUDA and for training compute on the 3090.

## Decision

OmniGen2 (Apache-2.0 on Qwen-VL-2.5) generates clothing, footwear,
handwear, and accessory overlays on the ANNY base mesh, per-scene
(changes across frames unlike identity, which is frozen per
character in RFD 2187).

Owns V3 parts (See-Through's taxonomy, RFD 2183 stopgap):
`footwear`, `handwear`, `torso-back` (cloth surface), `accessory`.

Trained under RFD 2184's three-signal pattern: EditScore (RFD 1157
reward model) for semantic quality, cross-view consistency on
`sphere_hammersley_sequence` renders for anti-hacking, and
constructed anchor data (real fashion / commercial-cleared cloth
assets, or Live2D clothing drawables where available).

## Problem

ANNY is undressed. RFD 2183's layer-decomp pipeline assumes a
dressed composite; without this stage, footwear/handwear/accessory
training pairs cannot exist and RFD 2184's bootstrap has nothing to
score for those V3 parts.

## Related

RFD 2183 (layer-decomp pipeline; consumes this), RFD 2184 (EditScore
three-signal training pattern), RFD 2187 (identity overlay, parallel),
RFD 2136 (gacha ladder; slots upstream of Rung 6).

This RFD was drafted by an AI and read by a human before it shipped.
