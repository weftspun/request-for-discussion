# RFD 1092: Kimodo backend integration

**State:** committed
**Scope:** `KimodoMotionPromptBar.jsx`, `taskManager.js`, the DGX-side Kimodo ops

## Problem

The frontend triggers text-to-motion through
`KimodoMotionPromptBar.jsx` and `taskManager.js`. The DGX side owns
every failure mode, prefetch step, and timeout, in its own ops
document, not in this repository. An agent debugging a Kimodo job
failure needs to know that document exists, and where.

## Decision

Read the DGX-side ops document first, before debugging a Kimodo job
failure here. Its path:
`/home/sifr/3DAIGC-API/memory-bank/kimodo-text-to-motion-ops.md`, on
the DGX host, not in this repository.

Run prefetch, restart, and test directly on the DGX. Do not ask the
user to run those scripts by hand.

Verified working, this session's own check: job `544b726e…`
produced `studio_motion.json`, the expected output.

## Related

`taskManager.js` dispatches the job. `KimodoMotionPromptBar.jsx`
triggers it from the animation bar.
