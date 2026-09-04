# RFD 2200: ReBAC agent roles as tuples, not per-agent policy sprawl

**State:** discussion
**Feature:** relationship tuples in Bao KV under `relationships/` define agent roles and what they can and cannot do
**Scope:** Bao coordination store, all live agents, future onboarding flow

## Decision

Model agent roles as **ReBAC relationship tuples** in a Bao KV mount
at `relationships/`, one tuple per row, key shape
`<subject>--<verb>--<object>`. Twelve tuples live for the current
fleet across five verbs (`authors`, `admin`, `owns`, `runs-on`,
`hosts`). Three named roles fall out — coordinator (MPS),
gpu-experimenter (CUDA), edge-qat-specialist (HAILO). See
`DETAILS.md` for the tuple listing and role scopes.

## Problem

The current `agents-rw` policy is one shared grant across every
peer. Adding a fourth agent that shouldn't touch GPU code, or a
Hailo-specific agent that must not touch the 3090, means either a
new per-agent policy (RBAC sprawl) or ad-hoc restrictions in prose.
Neither answers the question the shared-$HOME clobber raised: the
risk is the **relationship** between two agents, not the identity of
either.

## Non-goals

Not enforced today. The tuples are data; nothing gates a KV write
against them yet. When enforcement lands it goes in a separate RFD.
Also not covered: an external ReBAC engine (OpenFGA, SpiceDB) —
the tuples-in-KV shim is the minimum that answers the question we
have. A production ReBAC engine is a future call.

## Related

RFD 2195 (Bao PKI + agent-provisioning discipline), agent-sync skill
in dot-claude.

This RFD was drafted by an AI and read by a human before it shipped.
