---
title: "RFD 2040: Combat hexagon — core, ports, and adapters"
rfd: "2040"
state: published
scope: combat hexagon (proof of concept)
---

## Problem

The combat concern, combo timing, hit validation, the enemy
spawn-invulnerability window, and damage, needs to be deterministic
and testable with no server and no headset. Combat had no structure
that gave it this property.

## Decision

The combat concern — combo timing, hit validation, the enemy
spawn-invulnerability window, and damage — needs to be deterministic
and testable with no server and no headset. The project structures
combat as a hexagon (`rfd/2028-hexagonal-core-ports-adapters`). The
core resolves the combo timing, validates each hit against the
authoritative positions, holds the enemy invulnerable for its spawn
window, and deducts health, as a pure reducer
(`rfd/2033-core-contract-pure-reducer-byte-state`) over deterministic
state (`rfd/2034-deterministic-cores-integer-seeded-rng`). Driving
ports: `input_source` (player commands), `tick_source` (the
constant-step clock), `behavior_source` (enemy intents). Driven ports:
`state_sink` (authoritative entity state), `event_sink` (hits, deaths,
door unlocks). `feat/module-http3` feeds `input_source`. The
`zone-server` hosts the core and drives `tick_source` under server
authority. Sandboxed behavior (`rfd/2037-generated-behavior-sandboxed-riscv`)
implements `behavior_source`, and a fixture adapter replays recorded
inputs for CI. The server-authoritative adapter binds `input_source`
and `state_sink` with interpolation and no prediction for the
deadline; a rollback adapter lands after the gate behind the same
ports. The combat core runs headless against fixtures, so a flaky
adapter fails in isolation. The melee archetype ships first, and
ranged and caster land after the gate.

## References

- Full context and consequences: `DETAILS.md`
- Original record: `decisions/20260611-hexagon-combat-core.md`

## Related

- `rfd/2037-generated-behavior-sandboxed-riscv`: the `behavior_source`
  adapter for generated enemy behavior.

## Detail

{{< include DETAILS.md >}}
