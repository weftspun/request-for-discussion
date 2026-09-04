# RFD 2201: The coordinate-agents ceremony

**State:** discussion
**Feature:** what "coordinate agents" means as a repeatable procedure the coordinator runs on demand
**Scope:** the coordinator role (RFD 2200) and any session that steps into it

## Decision

Fold the workspace's ad-hoc coordination sweep into a named, bounded
ceremony that the coordinator role runs when asked. The ceremony has
seven steps and each step's output is a specific artefact — a KV read,
a peer message, a PR enqueue, a surface to the operator — with the
next step gated on the previous. The steps are enumerated in
`DETAILS.md`; a companion skill `coordinate-agents` in
`weftspun/dot-claude` is the operational how-to.

## Problem

"Coordinate agents" was a sentence the operator said and the
coordinator did a pass by memory: check the store, message peers,
enqueue clean PRs, surface stuck ones, remember the do-not-touch-peer-
branch rule. A pass done by memory shipped good work in one turn and
broke a peer's PR the next, because the safeguards were named
retroactively (in RFD 2195 DETAILS, after the mistake) rather than
carried in the procedure itself. A named ceremony carries them
prospectively.

## Non-goals

Not a scheduler; not a hook (the prettier-only exception is a shape a
hook would reject); not any-agent-runs-this — only the coordinator
role from RFD 2200.

## Related

RFD 2195 (Bao PKI + Gotchas), RFD 2200 (roles), `agent-sync` and
`coordinate-agents` skills in dot-claude.

This RFD was drafted by an AI and read by a human before it shipped.
