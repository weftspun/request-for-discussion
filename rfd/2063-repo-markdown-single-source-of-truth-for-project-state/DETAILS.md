## Context and problem statement

An agent working a project over many sessions accumulates project
knowledge: what is decided, what works, what is still open, which
avenues are dead. That knowledge has to live somewhere a future
session can read it. A file-based agent auto-memory is the convenient
place to put it, but auto-memory is not reviewed in diffs and does not
travel with the code. When the code moves and the memory does not,
the two desync, and a memory that names a file, function, or flag
that no longer exists reads as authoritative while being wrong. Where
should project state live so that it stays checkable against the code
it describes?

## Decision drivers

- A record of project state is trustworthy only when a reader can
  check it against the code as it stands.
- State that changes with the code must change in the same diff as the
  code, so a reviewer sees both together.
- Knowledge has to survive across agent sessions and across machines,
  not just inside one assistant's private store.
- The split between "project state" and "how to work" stays mechanical
  enough to route a new fact without debate.

## Considered options

- Keep all project knowledge in the agent's file-based auto-memory.
- Keep project state in versioned repo markdown, and keep auto-memory
  for durable behavioural rules only.
- Scatter state across commit messages and code comments with no
  dedicated index.

## Decision outcome

Chosen option: "project state in versioned repo markdown, auto-memory
for behavioural rules only", because a fact committed next to the
code it describes travels with the repo, shows up in review, and goes
stale visibly the moment the code it names changes — whereas a fact
in private auto-memory desyncs silently.

Project state lives in three repo-root markdown files, each holding
state in a distinct status, so every fact has exactly one home:

- `CHANGELOG.md` — decisions and completed, verified work, grouped by
  area, plus a top **Conventions** section of durable project rules.
  Entries record change events, so past or imperative tense is fine
  here, as in commit messages.
- `OPEN_GAPS.md` — unfinished work and open problems, each stated as
  the gap stands now, with the decisive next lever where it is known.
- `TOMBSTONES.md` — dead-ends, disproven hypotheses, and blocklisted
  avenues, each saying why it is dead and where any surviving
  knowledge lives, so a reader checks here before re-attempting
  something.

A new fact routes by status: finished or decided or verified goes to
`CHANGELOG.md`; still open goes to `OPEN_GAPS.md`; tried and failed
goes to `TOMBSTONES.md`; a rule about how to work, rather than about
the project, goes to auto-memory. An item moves between files as its
status changes — a gap becomes a changelog entry when it is done, a
hypothesis becomes a tombstone when it is refuted — and lives in
exactly one file at a time.

Auto-memory stays thin: it holds only durable behavioural rules (for
example "no Python, build Lean tools", "no CSV, emit Parquet", the
voice rule, the blocklists) plus a single pointer telling a future
session to read the three repo docs first. Project status — file
layouts, what is done, what is open — never goes in auto-memory,
because that is exactly the class of fact that desyncs.

## Consequences

- Good, because a state fact and the code it describes change in one
  diff, so a reviewer catches a divergence and a stale fact signals a
  real one.
- Good, because the three files travel with the repo and any session
  or machine reads the same state, rather than depending on one
  assistant's private store.
- Good, because the three-way status split makes "where does this fact
  go" a mechanical routing decision.
- Bad, because a fact's home changes as its status changes, so an
  author has to move entries between files instead of appending
  everywhere.
- Bad, because the discipline holds only while every contributor
  routes new facts rather than dropping them into memory or a stray
  comment.

## Confirmation

Review checks that a change which alters project state also touches
the matching repo doc in the same diff, that each fact appears in
exactly one of the three files, and that auto-memory carries only
behavioural rules plus the pointer, with no file layouts, completion
status, or open problems. The `repo-state-docs` skill encodes this
routing and is invoked whenever a finding, a completion, an abandoned
avenue, or an open problem surfaces.

## More information

This convention suits any project that an agent carries across many
sessions; the work that prompted it is a long reverse-engineering
effort, but nothing in the routing rule depends on that domain. This
applies the house tenseless continuous-present voice:
`OPEN_GAPS.md` and `TOMBSTONES.md` state current truth, while
`CHANGELOG.md` entries record change events and so read in past or
imperative tense like commit messages. See
`rfd/2025-tenseless-continuous-present-voice`.
