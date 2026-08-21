# RFD 1054: The avatar pipeline, image to downloaded VRM

**State:** published
**Scope:** `src/library/avatarPipelineCatalog.js`, `taskManager.js`, `avatarPipelineExport.js`

## Problem

"Avatar from Image" chains two API jobs (mesh generation, then
template rigging) and a client-side export step. Nothing stated the
chain in one place, so "does VRM export upload anywhere" and "why
does the rig look backward" were open questions each time someone
hit them.

## Decision

State the chain once: a photo goes to `3DAIGC-API`'s mesh-generation
task, then its template auto-rigging task (`rig_mode: template`),
landing a rigged GLB in the viewport. `exportAvatarPipelineVrm()`
then builds a `.vrm` blob client-side and triggers a browser
download; nothing uploads unless the user mints or saves elsewhere.
Rig alignment is validated against RFD 1053's contract, checked with
a `[API-Contract] PASS` log line, and the client applies no
rig-repair heuristic of its own for `fromAigc` loads — a backward or
floating rig means re-running after pulling the latest API, not a
client-side patch.

See `DETAILS.md` for the task-type table, the blend-shape source
table, and the key files.

## Related

RFD 1053 gives the rig contract this pipeline validates against.
RFD 1068 gives the separate, user-uploaded-VRM path this pipeline
does not use.
