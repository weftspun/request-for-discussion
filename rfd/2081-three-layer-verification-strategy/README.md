# RFD 2081: Three layer verification strategy

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

| Layer | Tool | Scope | What it proves | | --------------- |
--------------------- | -------------- |
------------------------------------------------------------ | | C
invariants | CBMC | Implementation | SPSC ring FIFO, bounds,
head-tail, NURand range | | Specification | Lean 4 | Design | SPSC
linearizability, push/pop preserve bounds | | TPC-C semantics |
plausible-witness-dag | Runtime | NewOrder atomicity, Delivery
correctness, Stock non-negative |

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
