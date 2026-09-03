# RFD 2190: Multi-camera rig extrinsics calibration

**State:** discussion
**Feature:** solve `view` matrices for every physical rig camera
**Scope:** `pose-consensus` silhouette pipeline, `renders.camera_id` FK

## Decision

Pick a calibration method and land it as
`pose-consensus/python/calibrate_rig.py`, producing per-camera
`view` matrices consumed by `Camera.project`. Three candidates:
bundle adjustment via structure-from-motion, checkerboard
calibration via a computer-vision toolkit, or a Kimodo-fit reusing
the workspace's own silhouette solver. The method is the decision;
implementation follows. Constraint: it must run on owned hardware,
so a CUDA-only calibrator is rented-compute by another name.

## Problem

`pose-consensus/python/silhouette.py` carries a pinhole `Camera`
with pixel intrinsics, a world-to-camera `view` matrix, and a
differentiable `project`; `renders.camera_id` is a foreign key.
Nothing solves the `view` matrices for a physical rig, so every
consumer of `Camera.project` holds a placeholder. RFD 1122
(unrolled Kusudama solver) sits on that placeholder, so its
residual is not measurable in world units until calibration lands.
Issue 30 closed stale.

## References

Original issue: `weftspun/request-for-discussion` issue 30.
`pose-consensus/python/silhouette.py` (Camera class).

## Related

RFD 1122 (unrolled Kusudama solver; consumes `view`),
RFD 2168 (wholebody detector retract),
RFD 2191 (unrolled solver residual; blocked by this).

This RFD was drafted by an AI and read by a human before it shipped.
