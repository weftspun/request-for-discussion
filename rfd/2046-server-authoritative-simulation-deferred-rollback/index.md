---
title: "RFD 2046: Server-authoritative simulation with deferred rollback"
rfd: "2046"
state: published
scope: Field-instance authority model (zone-server)
---

## Problem

The loop needs one authority over combat state and loot contention.
An earlier geometric Hilbert-zone authority attempt, the Maglev
intercept smoke test, did not work. The one-week slice needed a
simpler model that still resists client tampering.

## Decision

The loop needs one authority over combat state and loot contention.
An earlier geometric Hilbert-zone authority attempt (the Maglev
intercept smoke test) was rejected, and the one-week slice needs a
simpler model that still resists client tampering. The headless
`zone-server` owns entity transforms, health, combat state, and loot
contention. Clients reconcile to the server snapshot. A single
authority per instance keeps the slice simple and tamper-resistant.
For the deadline the model runs with client interpolation and no
client prediction; the rollback adapter lands after the gate behind
the same `input_source` and `state_sink`, so the swap never touches a
core. One authority per instance means a per-connection transport
child relays to that single core rather than holding state itself.
The deadline trades input snappiness for a far smaller build. A
divergent client reconciles to the server snapshot, and combat and
loot resolve identically across the four clients.

## References

- Original record:
  `decisions/20260611-server-authoritative-simulation-deferred-rollback.md`

## Related

- `rfd/2040-hexagon-combat-core`: the combat core behind the same
  ports the rollback adapter will later swap.
- `rfd/2033-core-contract-pure-reducer-byte-state`: the pure-reducer
  contract that keeps the swap adapter-only.
- `rfd/2045-loot-action-core-loop-mvp-vertical-slice`: the slice this
  authority model serves.
