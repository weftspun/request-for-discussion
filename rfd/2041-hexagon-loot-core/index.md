---
title: "RFD 2041: Loot hexagon — core, ports, and adapters"
rfd: "2041"
state: published
scope: loot hexagon (proof of concept)
---

## Problem

Loot generation and first-touch contention need to be deterministic
and replayable. A drop and its winner must reproduce from the seed
and the receipt order. Loot generation had no structure that gave it
this property.

## Decision

Loot generation and first-touch contention need to be deterministic
and replayable, so a drop and its winner reproduce from the seed and
the receipt order. The project structures loot as a hexagon. The core
rolls drops from loot tables keyed by enemy type and difficulty using
a seeded generator, and resolves first-touch contention by receipt
timestamp, granting the first requester and rejecting the rest, as a
pure reducer over deterministic state. The driving port
`loot_request_source` carries an interact event with a receipt
timestamp and a requester id. The driven ports are `grant_sink` (the
award or rejection per requester) and `inventory_delta_sink` (the
change to persist). The `zone-server` orders requests by receipt, the
progression persistence adapter applies `inventory_delta_sink`, and a
fixture adapter replays contention races for CI. The Hub shop degrades
to a free starting kit behind this core, so a slipping economy does
not block the loop. The roll reproduces from the seed in the state,
and contention resolves on the server, so two clients see one winner.
The core replays a recorded contention race to one grant against the
rest rejected, with no network.

## References

- Original record: `decisions/20260611-hexagon-loot-core.md`

## Related

- `rfd/2034-deterministic-cores-integer-seeded-rng`: the seeded RNG
  this core's drop roll uses.
- `rfd/2043-hexagon-progression-core`: the persistence adapter that
  applies `inventory_delta_sink`.
