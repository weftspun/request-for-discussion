---
title: "RFD 2029: CASSIE desktop curvenet authoring for content, no Blender"
rfd: "2029"
state: published
scope: content pipeline authoring (feat/module-cassie)
---

## Problem

The content pipeline needs budget-bounded geometry for the Hub, the
Field, and the enemy content slice. Standing up Blender for this work
adds a dependency the one-week build does not need. In-headset
sketching ergonomics also were not ready in time for this build.

## Decision

The content pipeline needs budget-bounded geometry for the slice
without standing up Blender. The project authors the Hub, the Field,
and the enemy as CASSIE curvenets through the desktop path, with no
Blender, because a curvenet is a bounded, inspectable graph the
`zone-baker` can cost, and the desktop path skips the in-headset
ergonomics for the one-week build. The `feat/module-cassie`
curve-and-surface sketcher produces curve networks that triangulate to
a controllable poly count. The geometry arrives near budget, so it
passes the baker with little rework; the in-headset sketching
ergonomics land after the gate; and the pipeline carries no Blender
dependency.

## References

- Original record:
  `decisions/20260611-cassie-desktop-curvenet-authoring.md`
- `feat/module-cassie`, `zone-baker`

## Related

- `rfd/2031-content-build-merged-double-precision-mcp`: the build this
  authoring path targets.
