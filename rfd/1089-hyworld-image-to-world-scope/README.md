# RFD 1089: HY-World 2.0, a quality path beside the fast one

**State:** discussion
**Scope:** `config/models.yaml`, a new `hyworld2_image_to_world_adapter.py`

## Problem

`weftspun_image_to_world` (TripoSplat plus optional TRELLIS props)
answers in minutes, on roughly 20 GB of VRAM, with a single-view
splat blob, room-sized at best. Tencent's HY-World 2.0 can produce a
trained, multi-view-consistent, navigable 3D Gaussian world instead,
at the cost of a multi-stage, multi-hour pipeline needing 17-billion-
parameter models. Nothing scoped how that pipeline would plug into
this project's existing job and manifest contract.

## Decision

Add `hyworld2_image_to_world` as a second, disabled-by-default model
next to the existing fast path, not a replacement for it. One
orchestrating adapter runs five pipeline stages plus an optional
panorama step as subprocesses (panorama, trajectory generation,
trajectory render, world expansion, Gaussian-splat data prep, and
the 3DGS train itself), writing `job_progress.json` per stage for
client polling, and only publishes the world manifest once training
completes. The client needs no new task type, only a model-picker
entry and a multi-stage progress UI.

See `DETAILS.md` for the stage table, the proposed job schema, the
infrastructure prerequisites, the phased rollout, and the risk
table.

## Related

RFD 1107 gives the world-manifest contract this pipeline extends to
a version 2. RFD 1094 gives WorldMirror 2.0, the reconstruction path
already shipped, which this RFD's scope explicitly excludes.
