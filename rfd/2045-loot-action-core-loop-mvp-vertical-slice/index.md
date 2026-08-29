---
title: "RFD 2045: Loot-action core-loop MVP vertical slice"
rfd: "2045"
state: published
scope: loot-action vertical slice (playable MVP)
---

## Problem

The project needed one playable slice of the instanced, four-player
loot-action loop, small enough to build in one week. The slice also
needed to exercise every integration seam, such as transport, server
authority, loot contention, inventory persistence, and performance
budgeting.

## Decision

The project ships one vertical slice of an instanced, four-player
loot-action loop: a Hub where players gather, a Field room with one
timed melee combo and one loot drop, and the round trip back to the
Hub. The slice is small enough to build in one week and complete
enough to exercise every integration seam: transport, server
authority, loot contention, inventory persistence, and performance
budgeting. Five hexagonal cores implement each concern behind ports.
The `zone-server` is the sole authority per instance, with client
interpolation and no prediction at the deadline. Content stays
first-party and curated, gated by the `zone-baker`'s build budgets.
The sign-off gate is a SteamVR build at 90 Hz, under 500,000 visible
triangles and 200 draw calls per eye. On 2026-06-29 the smoke test
proves the loop runs end to end, though some scoped pieces stay
unbuilt and carry forward as deferred work.

## References

- Full scene layout, loop steps, the cores table, downsides, rejected
  alternatives, and the full confirmation record: `DETAILS.md`
- Original record:
  `decisions/20260611-loot-action-core-loop-mvp-vertical-slice.md`

## Related

- `rfd/2028-hexagonal-core-ports-adapters`: the core/ports/adapters
  shape each hexagon follows.
- `rfd/2035-first-party-curated-content-zone-baker-budgets`: the
  content and performance gate.
- `rfd/2039-hexagon-budgeter-core` through `rfd/2043-hexagon-progression-core`:
  the five cores this slice wires together.
- `rfd/2046-server-authoritative-simulation-deferred-rollback`: the
  authority model for the Field instance.

## Detail

{{< include DETAILS.md >}}
