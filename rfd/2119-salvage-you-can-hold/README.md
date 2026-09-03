# RFD 2119: Salvage you can hold

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

| | Loose, between cycles | Claimed, at the cycle | |
------------------ | ------------------------------------------ |
------------------------------------- | | Enforced by | Ownership
sequence number, host arbitrates | Transaction across two databases |
| Cost | Nothing. Rides in the state update | About one round trip | |
Wrong for | A few frames, then converges | Never | | Checked by |
Convergence | `honest()`, every cycle | | Failure looks like | A crate
snaps to another pose | Scrip or salvage that does not add up |

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
