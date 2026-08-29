---
title: "Taskweft — Manuals"
toc: false
---

The design record for the Taskweft workspace: what was decided, what was
measured, and what has since been withdrawn.

## What is here

[**RFDs**](pages/rfd.qmd) — 159 Request-for-Discussion documents,
numbered rather than dated, each carrying a state it declares for
itself. RFD 1000 holds the format.

[**Serials**](pages/serials.md) — the register. Every serial this site
has allocated and every one it has retired, generated from
`SERIALS.usda` rather than maintained beside it.

[**Logbook**](pages/logbook.qmd) — entries recording what was measured,
with enough apparatus clipped to re-run the test.

[**Working agreements**](pages/agreements.qmd) — the standing
constraints, which live in the repository rather than in this site, and
why.

## How to read a document here

A number is an identity, not a date. A serial is appended once, never
removed and never reused, because it is the last arc of an OID under the
66606 Private Enterprise Number, and an arc names one document for as
long as that document exists. A retitle renames a document; it does not
renumber it.

Retractions stay next to what they retract. Where a document states a
number that later turned out to be wrong, the withdrawal sits beside the
original rather than replacing it, because a reader who knows which
roads are dead ends is better off than one who only knows where the road
ends today.

Where a document states a measurement or a rule, that statement should
be machine-checked against live code, so drift fails a command rather
than being discovered six months later.
