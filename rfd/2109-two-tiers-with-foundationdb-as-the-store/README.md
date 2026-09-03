# RFD 2109: Two tiers with foundationdb as the store

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

Bandwidth per client sets the bill. `rfd/0100` caps a client at 256
kbps, and egress scales with concurrent clients and hours played. No
deployment runs, so no monthly figure exists.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
