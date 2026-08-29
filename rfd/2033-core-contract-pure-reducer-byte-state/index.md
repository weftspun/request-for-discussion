---
title: "RFD 2033: Cores as pure reducers over byte-serialized state"
rfd: "2033"
state: published
scope: hexagonal core contract (state, replay, snapshots)
---

## Problem

Every hexagonal core needs to be replayable, snapshot-able,
fixture-testable, and transport-agnostic. A stateful object that
hides mutation behind its own methods defeats all four needs. The
project had no shared contract that gave a core all four properties
at once.

## Decision

Every hexagonal core (`rfd/2028-hexagonal-core-ports-adapters`) needs
to be replayable, snapshot-able, fixture-testable, and
transport-agnostic. A stateful object that hides mutation behind
methods defeats all four. The project models each core as a pure
reducer, `step : State -> Event -> State x Effects`, and serializes
`State`, `Event`, and `Effects` to bytes deterministically, so the
core reads bytes and writes bytes. The flat C ABI exposes `step` plus
`snapshot` and `restore` over the byte state. Combined with the
integer-seeded determinism rule, this makes replay byte-exact and a
snapshot a plain value copy. Snapshots and rollback become copies of
the state bytes, a fixture pins exact output bytes so a divergence
fails a test, and every adapter shares the same `step`, so
`webtransportd` and the engine carry the same bytes.

## References

- Full context, considered options, and confirmation steps:
  `DETAILS.md`
- Original record:
  `decisions/20260611-core-contract-pure-reducer-byte-state.md`

## Related

- `rfd/2028-hexagonal-core-ports-adapters`: the core/ports/adapters
  layout this contract fills in.
- `rfd/2034-deterministic-cores-integer-seeded-rng`: the determinism
  rule that makes replay byte-exact.
- `rfd/2032-core-codegen-lean-slang`: the compute kernels this
  contract's cores dispatch on the GPU.

## Detail

{{< include DETAILS.md >}}
