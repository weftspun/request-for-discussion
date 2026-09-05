# RFD 2204: RECTGTN fleet coordination

**State:** discussion
**Feature:** peers pick their next work item by running the same RECTGTN
query against one shared fleet domain, rather than by reading prose
relayed from the coordinator
**Scope:** every session that participates in the coordinate-agents
ceremony (RFD 2201); the Taskweft engine already in tree; a new
fleet-domain document

**Coordinator adapter as an Elixir module:** retracted 2026-09-05,
see [RFD 2205](../2205-taskweft-in-bao/README.md) — superseded by
an in-Bao database-plugin (Go binary, cgo-linked C++ planner) that
callers reach via `bao read taskweft/creds/<goal_id>`. This RFD's
"fleet-domain document" scope stays live; the "adapter" scope
moves to 2205.

## Decision

Feed the Taskweft engine a **fleet domain** — a single JSON-LD
document conforming to
`3-interactor/taskweft/priv/schemas/rectgtn_domain.schema.json` — that
names the live peers as entities, their owned resources as capability
edges, the verbs peers execute as actions, and known decompositions as
methods. Every peer answers "what should I do next?" with the same
call: `Taskweft.plan(fleet, actor: self_cn)`. Contention becomes
capability tuples; ordering becomes ISO-8601 durations; peer authority
becomes the ReBAC relations Taskweft already speaks
(`HAS_CAPABILITY`, `OWNS`, `IS_MEMBER_OF`, `DELEGATED_TO`,
`SUPERVISOR_OF`, `PARTNER_OF`, `CAN_ENTER`, `CAN_INSTANCE`). No new
planner, no new SQL layer, no port of RECTGTN into Bao; the engine is
the ground-truth solver and the fleet is a domain that feeds it.

The seven-step coordinate-agents ceremony (RFD 2201) stays. One line
of step 3 ("notify peers") becomes `Coordinator.snapshot |>
Coordinator.pick(self) |> Coordinator.publish(self)`. Determinism
against the shared snapshot removes the need to relay next-item picks
in prose. Assignment rows carry a `SqlarCas.Caveat` with
`{"type":"expires_at","at":start+duration}` — the compute-lease broker
RFD 2202 named as future work, filled by reusing the caveat primitive
that already exists in service-sqlar-cas.

## Problem

Peer sessions coordinate through three ad-hoc channels: Bao rows, free-
form `SendMessage` prose, and operator-typed un-park signals. There
is no shared representation of *why* a peer is doing what it is doing,
so a peer that reranks does it by hand, a peer that finishes an item
picks the next one from a board it interprets alone, and the operator
carries the priority ordering in their head each turn. The
`may-use--<device>` tuples RFD 2202 introduced are documentation only —
nothing gates work on them. When two peers want the same GPU or the
same HF repo, prose adjudicates.

## Non-goals

Not a scheduler; not a hook; not a replacement for the operator's
right to reprioritise mid-turn. The fleet domain is a snapshot the
operator edits like any other document — the planner is deterministic
against whatever the snapshot says. Not a claim that RECTGTN scales to
100+ peers today; the pilot is single-Goal, single-decomposition, and
the engine's search bounds already surface a "no assignable Task"
answer rather than looping.

## Related

- RFD 2200 (ReBAC agent roles) — supplies the relation vocabulary the
  fleet domain reuses.
- RFD 2201 (coordinate-agents ceremony) — step 3 gets the one-line
  hook; the other six steps are unchanged.
- RFD 2202 (ReBAC Bao enforcement) — this RFD fills the compute-lease
  broker gap RFD 2202 named as future work.
- RFD 2195 (weftspun-bao) — the Bao row shape the coordinator reads
  from and writes back to.
- Taskweft engine RFDs 0005 (unify capabilities with ReBAC) and 0008
  (MCP public API) — the surfaces the fleet uses without modification.

This RFD was drafted by an AI and read by a human before it shipped.
