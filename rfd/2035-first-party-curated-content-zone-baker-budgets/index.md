---
title: "RFD 2035: First-party curated content with zone-baker budgets"
rfd: "2035"
state: published
scope: content pipeline (zone-baker budget enforcement)
---

## Problem

A user-generated-content runtime carries arbitrary, unpredictable
per-frame cost. This cost is fatal on a mobile GPU holding a stereo
VR frame. The MVP needs predictable cost, and the freedom to
co-optimize content against the engine, and an unpredictable runtime
gives neither.

## Decision

A user-generated-content runtime carries arbitrary, unpredictable
per-frame cost, which is fatal on a mobile GPU holding a stereo VR
frame. The MVP needs predictable cost and the freedom to co-optimize
content against the engine. The project ships first-party curated
content only, with no user-generated-content runtime, and lets the
`zone-baker` enforce hard budgets at bake time, because curated
content lets the engine co-optimize with the art and lets the baker
reject anything over budget before it reaches a device. A four-player
Field room holds its geometry, four avatars, and props under roughly
500,000 visible triangles and 200 draw calls per eye on the standalone
VR build. The baker rejects any asset that exceeds the budget, so cost
stays predictable, and the content surface stays small, which keeps
the determinism and the budgeter tractable. Every shipped asset passes
the `zone-baker` at budget, and a four-player room holds the per-eye
limits on the standalone VR build.

## References

- Original record:
  `decisions/20260611-first-party-curated-content-zone-baker-budgets.md`
- `zone-baker`

## Related

- `rfd/2039-hexagon-budgeter-core`: the runtime degradation this bake-time
  budget complements.
