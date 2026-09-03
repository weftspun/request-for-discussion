# RFD 1016: Deep learning model inventory

**State:** abandoned
**Feature:** model inventory

## Decision

Abandoned 2026-09-03. The named source-of-truth
`src/library/aiModelsCatalog.js` was retracted alongside RFD 2169
(strangler-fig studio-core abandonment). RFD 1102 (task catalog) is
the current inventory; its DETAILS.md lists every model, task, and
runtime footprint. This RFD is kept for the retraction record.

Historical decision, as published: `aiModelsCatalog.js` stayed the
source of truth for identifiers; this RFD recorded type, task, and
runtime location per model. Fifteen models formed the inventory,
each packaged as its own model image per RFD 1036.

## Problem

The repository referenced many model identifiers. The catalog
recorded no type and no runtime location. A reader could not tell a
neural model from a geometric algorithm.

## Related

RFD 1102 (task catalog, current inventory), RFD 2169 (studio-core
abandonment), RFD 2174 (open-to-abandoned citation index).

This RFD was drafted by an AI and read by a human before it shipped.
