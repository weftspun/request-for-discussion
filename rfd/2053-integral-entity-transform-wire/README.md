# RFD 2053: Integral entity transform wire

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

- The wire has no floating point; replication is deterministic across
platforms. - The packet speaks the predictive BVH's native
int64-micrometer language, so position flows into the BVH with no
conversion. - Tying velocity to `PBVH_V_MAX_PHYSICAL_DEFAULT` closes a
latent drift (the codec had an ad-hoc times-1000 scale that the
BVH-sync review surfaced). - Density, when it matters, comes from
value delta-from-baseline rather than origin rebasing; entropy coding
stays off the per-tick path because variable length breaks the fixed
datagram layout.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
