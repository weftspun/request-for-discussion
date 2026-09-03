# RFD 2045: Loot action core loop mvp vertical slice

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The fabric has transport, authority, persistence, and budget decisions
in place, but no running loop that exercises all of them together. The
team needs a first playable to find the gaps that only appear when the
whole stack runs end to end: a social hub where players gather, an
instanced combat zone where they fight and collect, and the round trip
that carries the result back. Without a bounded target the risk is
that each layer is individually correct but the integration is never
tested until it is too late to fix.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
