# RFD 2202: ReBAC role tuples enforced via Bao identity groups

**State:** committed
**Feature:** wire `relationships/*--role--*` tuples to Bao identity groups so role capabilities are gated at the API, not just documented
**Scope:** Bao coordination store, mps-admin policy, all live agent identities

## Decision

Bao **identity groups** enforce the ReBAC role tuples RFD 2200
landed. One group per role, each carrying role-scoped policies;
agent entities as members. `scripts/sync_rebac_groups.py` reads
`relationships/<agent>--role--<role>` and reconciles group
memberships. See `DETAILS.md` for the mapping, reconciler contract,
and non-enforcement scope for hardware `may-use` tuples.

## Problem

RFD 2200 shipped the role tuples as data and named enforcement as a
separate RFD. Today's provisioning cycles bit twice on the gap: MPS
had to hand-attach an `agents-rw` policy to HAILO's entity to unblock
a 403 (documented in RFD 2195's cert-auth-swap gotcha), and the
"assist" role change for HAILO landed as a tuple update with no
mechanical effect on what capabilities HAILO's token actually
carried. Groups close that gap: a role change is one tuple write and
one reconciler run, and the token's next login reflects the new
policies through group membership.

## Non-goals

`may-use--<device>` tuples stay documentation; Bao does not gate
GPU/NPU access. Future compute-lease broker consults them, out of
scope here.

## Related

RFD 2200 (tuples as data), RFD 2195 (PKI + cert-auth), RFD 2201
(coordinate-agents ceremony).

This RFD was drafted by an AI and read by a human before it shipped.
