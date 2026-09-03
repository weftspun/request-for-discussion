# RFD 2075: Fdb over cockroachdb for zone state

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

**1. Write throughput.** TPC-C is 88% writes (NewOrder + Payment).
FDB's log-structured MVCC separates transaction processing from
storage, giving fundamentally lower write latency than CockroachDB's
Raft consensus path. For a write-heavy benchmark, the database is the
bottleneck.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
