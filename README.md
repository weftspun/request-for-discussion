# RFD Index

This repository holds Request-for-Discussion documents, across every
weftspun project. It follows the Oxide RFD style.

Each RFD number has four hexadecimal digits. The first digit names
the organization. This repository uses digit 1. RFD 1000 gives the
rule. `ALIASES.md` maps the old decimal numbers to the new ones.

Each RFD is a reference design. It records a decision and points to
the canonical documentation, in whichever project's own repository
holds the code. It does not restate the documentation. See the STE
policy below for the writing rules.

## DRY policy

The repository keeps one source of truth for each design.

- The README describes the feature surface.
- The docs/ tree holds the detailed designs and roadmaps.
- The src/ tree implements the behavior.
- This directory records the durable decisions only.

An RFD points to the source. It does not copy the source.
An RFD that restates a document will drift. It must instead link the
document. When a design changes, update the source first. Then update
the RFD to point at the new source.

## Structure gate

`scripts/check-rfd-structure.py` checks the shape of each RFD against a
CommonMark AST: the title, the `State`/`Feature`/`Scope` preamble, the
section order, the README line limit, and every RFD citation.
`scripts/check-rfd-numbers.py` checks numbering. Both carry negative
controls and run in CI.

Every rule the structure gate holds was measured against all RFDs first.
RFD 107c gives each rule, its count, and the conventions that were
measured and deliberately left ungated.

## The logbook

This repository also holds the engineering record. `weftspun/logbook` is archived
and its contents moved here: the working agreements in CLAUDE.md, the recurring
failure modes in PITFALLS.md, the narrative entries whose names begin
`logbook-`, and the apparatus and gates under `scripts/`.

An RFD and an entry are a matched pair. The RFD records the decision. The entry
records the measurement that justified it, or the measurement that retracted it.
They cited each other across a repository boundary that no gate could check, and
now they do not. CLAUDE.md gives the move and what it cost, under "Why the
logbook moved here".

An entry records what was measured, not what was intended, and it clips the
apparatus so a number can be re-run rather than believed. Retractions stay in
place beside what they retract.

## STE policy

Each RFD uses ASD-STE100 Simplified Technical English. The rules:

- One sentence per instruction.
- Keep sentences under 25 words.
- Use active voice.
- Do not use marketing adjectives.
- Do not use phrasal verbs.
- Do not use semicolons or em dashes in prose.
- Name one thing by one name.

The repository enforces this with the `simplified-technical-english`
Claude Code plugin (`fire/claude-ste-plugin`), not a repo-local
script. Its `Stop` hook lints each reply as it is written and asks
for a rewrite on a violation. RFD 103f records the move and why no
CI step or pre-commit hook duplicates it.
