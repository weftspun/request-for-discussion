# RFD 2069: Defer loot slice hardening until needed

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The loot-action core-loop MVP vertical slice
(`rfd/2045-loot-action-core-loop-mvp-vertical-slice`) decides a large
scope: five named cores, a CockroachDB adapter, a measured 90 Hz
performance gate, and a SteamVR build. Its stated goal, though, is
narrow — one slice "complete enough to exercise every integration
seam." The running `godot-loop-slice` already carries that loop end to
end (Hub to Field to Hub, through transport, server authority, loot
contention, and SQLite-backed persistence), and the playable-loop
smoke passes. The integration goal is met.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
