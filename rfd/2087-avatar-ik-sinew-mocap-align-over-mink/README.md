# RFD 2087: Avatar ik sinew mocap align over mink

**State:** moved

## Decision

See `DETAILS.md` for the full argument.

## Problem

`sinew-mocap/solve` (FK + LBS skinning) was flagged as less trusted
than [`kevinzakka/mink`](https://github.com/kevinzakka/mink), a
widely-used differential inverse-kinematics library built on MuJoCo
(which `zone-server-h2o` already vendored for entity/prop contact
physics, `thirdparty/mujoco` pinned to 3.11.0, at the time).

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
