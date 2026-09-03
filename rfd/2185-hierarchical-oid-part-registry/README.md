# RFD 2185: Hierarchical OID part registry under PEN

**State:** discussion
**Feature:** stable OID identity for every body/clothing/accessory part
**Scope:** shared taxonomy for layer decomposition, segmentation, retargeting

Shelved 2026-09-02: waiting for measurement showing See-Through V3
(23 parts, RFD 2183 stopgap via `anny_v3_face_groups.py`) is a
bottleneck. Resume when a task lands that V3 cannot label.

## Decision

Every part gets a stable OID under `1.3.6.1.4.1.66606.<arc>.parts.<hierarchy>`.
Hierarchical addressing: `body/head/hair/front-fringe`, so a v4
addition is a new child, not a schema break.

Four leaf alias sets, each pointing at the same OID hierarchy:

- See-Through V3 (23 anime-illustration parts, RFD 2183 stopgap).
- ANNY 104 joints (native rig, RFD 1122 topology).
- PASCAL-Part (39 general human parts, public benchmark interop).
- VRM 1.0 humanoid bones (deployment interop).

Ingest maps any leaf alias to the canonical OID. Storage is OID,
not string, so V3 v3->v4 upgrades never rewrite a corpus.

## Problem

RFD 2183's `anny_v3_face_groups.py` (See-Through V3 stopgap) covers
10 of 23 parts today. Any future task with finer parts (skin/makeup,
cloth sub-parts, multi-character, hair sub-strands) breaks a flat
23-label schema. String labels lose their meaning when v3 becomes
v4; OIDs do not. RFD 1122 (AlternativeTopology) is the same shape
for joint schemas and shows the pattern works.

## Related

RFD 2183 (layer-decomp pipeline; V3 stopgap sits under this),
RFD 2184 (EditScore bootstrap for unmapped parts), RFD 1122
(AlternativeTopology; reference precedent), RFD 1000 (RFD
conventions; OID arc rules).

This RFD was drafted by an AI and read by a human before it shipped.
