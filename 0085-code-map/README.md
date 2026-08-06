# RFD 0085: A code map, not a copied API reference

**State:** published
**Scope:** the browser client, `src/`

## Problem

RFD 0018 deleted the M3 API reference this project's client forked:
seven managers documented, while the real code had grown past
forty. RFD 0000's own DRY policy forbids a copy of the source, since
a copy drifts and the source stays correct.

## Decision

Replace the reference with a map: name each module group, point at
its path, and stop. Read the source itself for the current API, not
a restated signature list. See `DETAILS.md` for the full module
table, by group: React contexts, scene and rendering, WebXR, avatar
and traits, export and generation, tasks, wallet and payments,
hardware bridges, and pages.

## Related

RFD 0018 gives the reason this page exists at all. RFD 0000 gives
the DRY policy it follows.
