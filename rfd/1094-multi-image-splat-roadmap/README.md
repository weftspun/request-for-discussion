# RFD 1094: Multiple photos, routed by count, not by user choice

**State:** abandoned
**Scope:** `image-to-splat`, `image-to-world`, avatar mesh generation

## Decision

Abandoned 2026-09-03. Every underlying model this RFD routed
between is abandoned per RFD 1102 (task catalog) retraction record:
TripoSplat, WorldMirror 2.0, weftspun_image_to_world, LingBot-Map
(RFDs 1049-1052 abandoned). The three-phase routing contract has no
targets to route to.

Historical decision, as published: three shipped phases on one
contract. Phase 1 accepted a primary `image_file_id` plus up to
seven references. Phase 2 flipped `use_multiview_mesh: true` at
two-plus images. Phase 3 auto-routed by count between TripoSplat
(single), WorldMirror 2.0 feed-forward 3DGS (two-plus), and COLMAP
fallback.

## Problem

A single photo gave a weak splat and a weak mesh. More photos
helped both, but only if the API and client agreed on how many
photos meant which engine.

## Related

RFD 1102 (task catalog, current inventory), RFDs 1049-1052
(underlying models, abandoned), RFD 1089 (HY-World 2.0 companion
path, also abandoned), RFD 2174 (open-to-abandoned citation index).

This RFD was drafted by an AI and read by a human before it shipped.
