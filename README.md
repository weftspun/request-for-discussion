# RFD Index

This repository holds Request-for-Discussion documents, across every
weftspun project. It follows the Oxide RFD style.

Each RFD number has four decimal digits. The first digit names the
organization. This repository uses digit 1. The last three digits are
the serial. RFD 1000 gives the rule and the OID arc it comes from.

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
RFD 1124 gives each rule, its count, and the conventions that were
measured and deliberately left ungated.

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
for a rewrite on a violation. RFD 1063 records the move and why no
CI step or pre-commit hook duplicates it.
