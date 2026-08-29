---
title: "RFD 2050: Five-second transaction limit (bounded operations)"
rfd: "2050"
state: published
scope: connection recovery and blocking operations across the fabric
---

## Problem

A connection that silently desyncs wastes a player's time. A past
loop bug let a client believe it joined while the server dropped it,
and the client waited forever with no bound. No operation across the
fabric carried a fixed time limit before this.

## Decision

A connection that silently desyncs wastes a player's time: a past
loop bug had a client believe it was joined while the server had
dropped it, and the client waited forever. FoundationDB bounds every
transaction to five seconds and aborts past that, so a stuck
operation fails fast instead of hanging. The project applies the same
guarantee across every operation that can block: connection recovery,
runtime MCP round trips, and any commit. No operation waits longer
than five seconds; past that it aborts or self-heals. The connection
state machine re-joins a client that stops hearing the server. A Lean
plus Plausible model proves the protocol sound — the client's belief
never disagrees with the server once settled — and complete within a
five-second budget: an awake client returns to a healthy joined state
within five ticks. The buggy protocol without the re-join rule is
shown incomplete, since Plausible finds a permanent ghost that stays
unhealthy after a hundred seconds. Runtime MCP operator calls carry a
five-second deadline, and a commit past that budget aborts rather
than blocking the loop. The bound is a proof, not a hope: the model
is the source of truth, and the loop client's connection logic
matches it.

## References

- Original record:
  `decisions/20260612-five-second-transaction-limit.md`
- Model repository:
  `https://github.com/v-sekai-multiplayer-fabric/connection-fsm`

## Related

- `rfd/2057-vertical-slice-repository-map`: lists `lean-connection-fsm`
  among the wire and determinism specs.
