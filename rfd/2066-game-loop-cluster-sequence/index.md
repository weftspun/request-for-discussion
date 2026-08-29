---
title: "RFD 2066: Game-loop-first delivery sequence"
rfd: "2066"
state: published
scope: delivery sequencing across the loot-action concerns
---

## Problem

Four other concerns, uiux-polish, cassie-pen-mesh, shop-economy, and
openUSD-i/o, all need a verified game loop as their integration
target. None of them tests end to end without one. Advancing another
concern in parallel risks landing work on a loop that is still
changing.

## Decision

The team stabilizes the game loop first, ahead of uiux-polish,
cassie-pen-mesh, shop-economy, and openUSD-i/o. A team poll picked
game-loop as the next concern, with 2 of 4 votes. Each of the other
four concerns needs a verified game loop as its integration target,
and none of them tests end to end without one. The OpenXR Windows
build is the external feedback artifact: it runs the full
hub-to-field-to-loot round trip and is the SteamVR-compatible path
for PCVR reviewers. The game loop counts as complete once `smoke.sh`
passes, the OpenXR Windows build exports without error, and one
external reviewer runs the full loop against a live server. Advancing
another concern in parallel risks landing work on a loop that is
still changing, so the other four concerns wait. If the game-loop
verification slips, all four wait with it; no parallel path absorbs
the delay.

## References

- Full context and rejected alternatives: `DETAILS.md`
- Original record: `decisions/20260624-game-loop-cluster-sequence.md`

## Related

- `rfd/2045-loot-action-core-loop-mvp-vertical-slice`: the vertical
  slice this sequencing decision prioritizes.

## Detail

{{< include DETAILS.md >}}
