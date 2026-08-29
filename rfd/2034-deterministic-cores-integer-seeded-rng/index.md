---
title: "RFD 2034: Deterministic cores via r128 fixed-point and seeded RNG"
rfd: "2034"
state: published
scope: authoritative-core numerics (fixed-point, RNG)
---

## Problem

Replay, recorded fixtures, and the future rollback adapter need the
authoritative cores to be bit-exact across the RTX 4090 workstation
and the Steam Deck. IEEE-754 floating point diverges across
platforms, through fused multiply-add, instruction reordering, and
transcendental functions. A float value in the authoritative path
breaks replay silently.

## Decision

Replay, recorded fixtures, and the future rollback adapter need the
authoritative cores to be bit-exact across the RTX 4090 workstation
and the Steam Deck. IEEE-754 floating point diverges across platforms
through fused multiply-add, instruction reordering, and transcendental
functions, so a float in the authoritative path breaks replay
silently. The authoritative cores use r128 Q64.64 fixed-point and a
seeded RNG threaded through state, with no floating point, because
fixed-point over 64-bit integers reproduces bit-exact across machines
while an explicit seed in the state makes the loot roll replayable.
The cores import r128 as a Lean library that lowers to SPIR-V, and the
engine's vendored `thirdparty/misc/r128` stays the host reference.
Replay and snapshots stay byte-exact, so the rollback adapter becomes
cheap. The fixtures pin exact outputs, so a divergence shows up as a
failing fixture rather than a silent drift. The loot roll is
reproducible from the seed in the state, and replaying an input log
reproduces the state hash on every target.

## References

- Original record:
  `decisions/20260611-deterministic-cores-integer-seeded-rng.md`
- `thirdparty/misc/r128`
- `decisions/20260612-r128-fixed-point-as-lean-library.md`

## Related

- `rfd/2033-core-contract-pure-reducer-byte-state`: the byte-state
  contract this determinism rule makes replayable.
- `rfd/2041-hexagon-loot-core`: the seeded roll this rule backs.
