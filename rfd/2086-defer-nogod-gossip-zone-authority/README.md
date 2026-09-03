# RFD 2086: Defer nogod gossip zone authority

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

`lean-rebac-core`'s `Rebac/core/NoGod.lean` (imported by `ReBAC.lean`)
is a proven, coordinator-free gossip protocol for zone-range
consensus: vector clocks (`VClock`), Hilbert-range containment
(`ZoneRange`, `geometricAuthority`, `geometricInterest`), a hybrid
logical clock (`HLC`), and theorems that gossip-based range adoption
preserves `DisjointRanges` — no two zones ever claim overlapping
authority — without a central coordinator.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
