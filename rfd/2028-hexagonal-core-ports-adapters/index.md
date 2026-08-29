---
title: "RFD 2028: The hexagon layout as the component convention"
rfd: "2028"
state: published
scope: cross-language component architecture
---

## Problem

Components in the stack span several languages and run as separate
processes. Each component binds to hardware, a GPU, the network, or
an engine runtime. A shared monolith or one in-memory object model
cannot hold across these boundaries.

## Decision

Components in the stack span several languages, run as separate
processes, and each binds to hardware, a GPU, the network, or an
engine runtime. A shared monolith or one in-memory object model cannot
hold across those boundaries. Every component instead takes a uniform
`entities/` + `repositories/` + `datasources/` layout, in the Netflix
formulation of the pattern. Entities are the objects the component
works on, and they know nothing about where they are stored.
Interactors perform the actions on them. Together they have no
dependencies, and CI tests them against recorded data. A repository is
an interface that gets, creates, and changes entities; it stays at the
lowest common denominator every binding language can implement, often
a C-ABI struct of function pointers. A data source implements a
repository outside the interactor: a device, a socket, a recorded
fixture for CI, a renderer. A transport layer is the input that
triggers an interactor. All dependencies point inward. Components
compose when a data source of one component is the transport layer of
another, in one process or across two.

## References

- Full context, decision drivers, consequences, and the `sinew-mocap`
  worked example: `DETAILS.md`
- RFD 2111 sets these words, amends this RFD, and holds the rename
  list. It cites Netflix for the words and Cockburn for the pattern.
- Original record:
  `decisions/20260610-hexagonal-core-ports-adapters.md`
- `sinew-mocap` repos: `driver`, `mount_drift`, `solve`, `viewer`,
  `vr_bridge`

## Detail

{{< include DETAILS.md >}}
