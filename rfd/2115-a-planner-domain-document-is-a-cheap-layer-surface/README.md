# RFD 2115: A planner domain document is a cheap layer surface

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

`fabric-store-domain` reached for a hand-written CBOR codec before
this RFD existed. The encoder walked a `tsl::ordered_map` and wrote
pairs in insertion order, carrying a comment that called the order
correct.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
