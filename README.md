# RFD Index and Logbook

Taskweft builds a loop where a person makes a character, dresses it, and
then either wears it or talks to it. This repository is that project's
design record.

## Start here

Read these three in order. Together they take about fifteen minutes.

1. **RFD 1171** names what the project is building and which part every
   model plays.
2. **RFD 1000** says how to read any document here. States, numbering,
   section order.
3. **`CLAUDE.md`** holds the standing constraints. What may enter a
   training corpus, and what may not.

The rendered site is at
<https://weftspun.github.io/request-for-discussion>.

## Two things that confuse new readers

**Documents contradict themselves on purpose.** When a number turns out
to be wrong, the correction goes next to the original instead of
replacing it. A document can state a thing and withdraw it a paragraph
later. This is deliberate. A reader who knows which roads are dead ends
is better off than one who knows only where the road ends today. A
paragraph in bold capitals is usually a retraction.

**A number is an identity, not a date.** RFD 1171 is not newer than RFD
1170 in any useful sense, and a low number is not obsolete. A serial is
allocated once and never reused, because it is the last arc of an OID.

## What is in here

The Request-for-Discussion documents, across every weftspun project,
following the Oxide RFD style. An RFD records a decision.

The logbook: the cross-project engineering record of what was measured,
what it cost, and which roads turned out to be dead ends. `PITFALLS.md`
holds the recurring failure modes and `BLOCKLIST.md` the excluded
sources. A `logbook-*.md` entry records a measurement.
`weftspun/logbook` is archived, and its history is here.

Each RFD number has four decimal digits. The first digit names the
site. This repository authors digit 1. The last three digits are the
serial. RFD 1000 gives the rule and the OID arc it comes from.

It also holds digit 2, and does not author it. `v-sekai-fabric` was
site 2 of PEN 66606 and was decommissioned on 2026-08-29. Its 129
documents are under `rfd/`, its register is
`SERIALS-vsekai-fabric.usda`, and `pen-66606.usda` composes both. The
arcs are kept and never reused, and no serial is allocated under
`66606.1.2` again.

**Those 129 are not gated by the rules below.** They were written to a
different shape -- `rfd/NNNN-slug/index.md` with YAML front matter,
where this site writes `NNNN-slug/README.md` under 40 lines with a
`DETAILS.md` beside it -- and 110 of them exceed that limit.
`check-rfd-structure.py` reads root-level directories, so it does not
see them. That is stated here because an unchecked thing that nobody
names reads exactly like a checked one. They are a frozen record, not
a corpus this site maintains.

Each RFD is a reference design. It records a decision and points to
the canonical documentation, in whichever project's own repository
holds the code. It does not restate the documentation.

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
