# RFD 1053: The API avatar rig export contract

**State:** committed
**Scope:** `src/library/aigcRigContract.js`, `3DAIGC-API/core/utils/aigc_rig_contract.py`

## Problem

An upside-down rig, a backward-facing character, and a rig
floating at the hips were real, repeated regressions from the
Blender export path. Two sides, the client and the DGX API, each
validated a rigged GLB independently, with no shared spec, so a fix
on one side could still drift from the other.

## Decision

One canonical spec, this document (mirrored at
`3DAIGC-API/docs/API_AVATAR_RIG_CONTRACT.md`, kept in lockstep), for
every skinned humanoid GLB export: Y-up, -Z forward, feet on the
floor, applied transforms, hips near mid-torso height. Both sides
log `[API-Contract] PASS` or `FAIL`. The API fails the job outright
on a critical code (upside down, facing backward, no skinned mesh,
too few joints); the client applies only targeted skinned-mesh
repair, and never reuses VRM-loader flags on an AIGC GLB, since a
VRM upload and an AIGC rig follow deliberately separate paths (RFD
1068 gives the VRM side).

See `DETAILS.md` for the coordinate system, the full requirement and
failure-code tables, the Blender export steps, and the retest
procedure.

## Related

RFD 1054 gives the avatar pipeline that produces the GLB this
contract validates. RFD 1068 gives the separate, contract-free VRM
upload path.
