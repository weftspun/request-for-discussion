# RFD 1089: HY-World 2.0, a quality path beside the fast one

**State:** abandoned
**Scope:** `config/models.yaml`, a new `hyworld2_image_to_world_adapter.py`

## Decision

Abandoned 2026-09-03. The fast path this RFD augmented
(`weftspun_image_to_world`, RFD 1049) is abandoned; HY-World 2.0 as
proposed here was never enabled. RFD 1102 (task catalog) is the
current inventory.

Historical decision, as published: add `hyworld2_image_to_world` as
a second, disabled-by-default model next to the existing fast path.
One orchestrating adapter ran five pipeline stages plus an optional
panorama step as subprocesses, writing `job_progress.json` per
stage, and only published the world manifest once training
completed.

## Problem

`weftspun_image_to_world` answered in minutes, on ~20 GB of VRAM,
with a single-view splat blob, room-sized at best. HY-World 2.0
could produce a trained, multi-view-consistent, navigable 3D
Gaussian world at the cost of a multi-stage, multi-hour pipeline
needing 17-billion-parameter models. Nothing scoped how that
pipeline would plug into the existing job and manifest contract.

## Related

RFD 1049 (weftspun_image_to_world, abandoned), RFD 1094 (multi-
photo routing, also abandoned), RFD 1102 (task catalog, current
inventory), RFD 2174 (open-to-abandoned citation index).

This RFD was drafted by an AI and read by a human before it shipped.
