# RFD 0110: RepoResident, a file-based operating harness for coding agents

**State:** committed
**Scope:** `CLAUDE.md`, `AGENTS.md`, `.agent/` (`STATE.md`, `MAP.md`, `PROJECT.md`,
`DECISIONS.md`, `ISSUES.md`, `workflows/`, `designs/`, `areas/`, `journal/`, `scratch/`)

## Problem

A coding agent session that loads every project file, every closed
issue, and every past design spends context on history instead of
the current task. Without a named procedure per task type, agents
improvise process, and a large model and a small model handle
ambiguity differently. Without a place for state to persist,
knowledge learned in one session does not reach the next.

## Decision

Weftspun3DStudio adopted RepoResident on 2026-07-23, replacing an
earlier "MindLink" personal-memory approach, now archived to
`.agent/areas/mindlink.md`. Context loads in five capped layers:
`CLAUDE.md` (operating rules, every session), `STATE.md` (current
state, rewritten in full each session, every session), one workflow
file matched to the task, then project facts and decisions, then
targeted source. Five roles (Architect, Builder, Fixer, Reviewer,
Curator) carry different rules for the same repository, not
conversational personas. `STATE.md` stays a live handoff, not a
decision record; it holds no lasting content and does not become
part of this RFD.

See `DETAILS.md` for the file map, the context-layer table, the
workflow-selection rules, and the technical decisions from
`DECISIONS.md` not already covered by another RFD.

## Related

RFD 0086 gives the Surface/DGX topology `PROJECT.md`'s sync-ownership
rule depends on. RFD 0099 gives the operator command cheat sheet this
harness's workflows point to for exact commands.
