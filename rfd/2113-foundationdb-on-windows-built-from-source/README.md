# RFD 2113: Foundationdb on windows built from source

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The store must satisfy four constraints at the same time: free and
open source, reachable from a second machine, a native Windows server,
and linear scaling per machine. It must also supply an ordered byte
keyspace, atomic multi-key commits, and read-write conflict detection
for the fence.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
