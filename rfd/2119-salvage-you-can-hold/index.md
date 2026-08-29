---
title: "RFD 2119: Salvage you can hold"
rfd: "2119"
state: discussion
scope: client interaction model, authority, the boundary between physics and the ledger
---

## Problem

`service-store` holds an invariant: salvage is unique, and no item is in two Sparks' hands. A transaction across two databases enforces it, and `honest()` checks it every cycle. Glenn Fiedler's VR cubes hold the same invariant under another name — ownership stops two players holding one cube, and a sequence number per cube enforces it while a host arbitrates. His rule is exact: "Ownership sequence increments each time a player grabs a cube. Ownership is stronger than authority, such that an increase in ownership sequence wins over an increase in authority sequence number."

One invariant, two mechanisms, three orders of magnitude apart in cost: the transaction is exact and takes a round trip, the sequence number converges and takes nothing. RFD 2085 makes the question urgent by naming the object that carries it. Memory Drives house a Spark's consciousness, drop on death, and can be looted or ransomed. A drive is holdable, contested, and the one item where duplication is unsurvivable in the fiction as well as in the ledger: two people holding one drive is two people holding one person.

## Decision

**Two authorities, split by what a mistake costs.** Physics authority is distributed and taken by whoever last touched an object, and it is allowed to be briefly wrong. Economic authority stays with `service-store`, single-writer and transactional, and is never allowed to be wrong. A dropped crate costs a frame of jitter; a duplicated drive costs the invariant every other check rests on.

**The cycle is the line, because a cycle is already one transaction.** `service-store` makes each cycle a single group commit across the ward and every Spark it touches. Salvage loose in the world between cycles is physics the ledger has never heard of, and the cycle that ends is the commit that takes it. The boundary the interaction model needs is the one the store already draws, so nothing new carries it.

**A claim is one transaction that deletes and inserts together.** Converting loose salvage into a row removes the physical object and writes the `held` entry in the same commit, and drawing an item back into the world runs it backwards. Uniqueness holds because the ledger counts only what it has committed, and the conversion is the only place the two representations meet.

**Memory Drives never enter the distributed regime.** Fiedler states his model suits "cooperative experiences only, as it does not provide the security of a server-authoritative network model". Seven of the Gyre's nine contracts resolve without a fight, so that limitation costs almost nothing. Drive looting and ransom is the exception and is adversarial by design, so custody stays transactional even while the physical shell is thrown around.

**Physics never reaches the seeded simulation.** `CLAUDE.md` requires that a cycle not advance on wall-clock time and that the RNG draw order never move. PhysX is non-deterministic, which is why Fiedler rejected lockstep. A thrown crate may not decide a contract, feed a draw, or advance a cycle: the physics layer reads the ward and the ward declines to read it back.

**The board is the second layer, played at the same time.** PRAGMATA runs Hugh's movement and Diana's hacking together, one player coordinating both. The Gyre has both halves already — hands in the world at frame rate, and the Queen's board of contracts and cycles deciding what the object in your hand is worth. Neither pauses for the other.

## References

- [Networked Physics in Virtual Reality](https://gafferongames.com/post/networked_physics_in_virtual_reality/), Glenn Fiedler: the authority model, the priority accumulator, and the delta encoding; [PRAGMATA](https://store.steampowered.com/app/3357650/PRAGMATA/), CAPCOM: two characters played at once
- RFD 2085: the setting, the Hub and Field loop, and Memory Drives
- `service-store` (the ward, the invariants, the parallel commit), `transport-fanout` (the interest filter and entity packet), `interactor-authority` (the single writer the ledger keeps)

## Detail

{{< include DETAILS.md >}}
