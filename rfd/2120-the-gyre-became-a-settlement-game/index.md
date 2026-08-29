---
title: "RFD 2120: The Gyre became a settlement game"
rfd: "2120"
state: discussion
scope: the Gyre's shape, the player's role, and what the ward simulates
---

## Problem

RFD 2085 records the Gyre as a MUD on the loot and action shell: a Hub in the Under-Market and the Commons, bounded contracts out in the field, six zones, and a player who is a Spark taking work to pay down a debt. `service-store` built something else — the player is the Queen, the Sparks act on their own, and the loop is commissioning rather than travelling. The code has run this way since the first ward played while the record still describes the earlier design, so anyone reading 0085 to understand what `queen` does will be wrong about the player, the loop, and the map. This RFD records what was built, so the two stop disagreeing.

## Decision

**The player is the Queen, and the Queen never takes a contract.** The shape is `My Life as a King`: commission, then
wait. Sparks choose their own work, and the whole of the player's game is deciding what to build and in what order. The comment in `src/queen.c` states the reasoning, which is that a loop like this is a state machine over days with nothing in the critical path to draw, and that is the one game shape genuinely better as a database than as an engine.

**Six venues replace six zones.** The Under-Market and the Commons survive as the two decks a venue stands on, thirty
metres apart. What they hold is a build list rather than a map to travel: Cycle's End Tavern, Splicer's Den, Transit Rails, Exchange Plaza, Chapel of the Backup, Broadcast Row. Each changes how Sparks behave rather than granting a number, so the Tavern makes them bolder because they rest and the Rails put more work on the board.

**A contract resolves against risk, on the board, in a cycle.** Nine kinds post to a board of six, or nine once the
Rails stand. A Spark takes one if its nerve carries it, and a draw against the contract's risk decides the outcome. Seven of the nine still resolve without a fight, which is the part of 0085 that carried over unchanged.

**The Debt Clock is the antagonist, and it compounds.** Debt grows one percent per cycle and the treasury pays it
down. Income from contracts is the only thing that makes scrip, which is what lets one sum decide whether the ward is honest.

**The currency is scrip.** 0085 calls it chits. The implementation calls it scrip throughout, and the invariant is
written in those terms.

**A cycle is game time and never wall-clock time.** The ward publishes at 20 Hz because the rest of the fabric does,
and that clock says nothing except how often the ward publishes. Tying the two would tie the rate debt compounds at to the rate the network publishes at, and it would end the replay check.

## References

- RFD 2085: the setting, which this amends rather than replaces. RFD 2119: the interaction model that depends on which loop is real
- `service-store`: `src/queen.c`, the venues, the board, and the clock

## Detail

{{< include DETAILS.md >}}
