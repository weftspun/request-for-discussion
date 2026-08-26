# RFD 1147: What EditScore costs and returns

**State:** published
**Feature:** the scorer shared by all four loops
**Scope:** `2-contract/weftspun-manuals/fourloops-plan.usda`

## Problem

EditScore is the `score` stage of every loop in `fourloops-plan.usda`.
Loops 1 through 4 each name it, and loop 1 pairs it with the Referee.

Its measurements were written into RFD 1144 because loop 2 is the
smallest loop that exercises it. That put a figure belonging to four
loops inside the document for one of them, so a reader of loop 3 had to
know to look in loop 2 for what the scorer costs.

## Decision

Give the scorer its own RFD, and let the loops cite it.

`DETAILS.md` holds what it costs and what it returns: peak memory at
512 and at 1024 square, the overall score for an instruction the edit
matched, and the two-axis spread behind that overall. Both
`fourloops-plan.usda` and `fourloops-etnf.usda` name it as a source, so
a quantity in either layer resolves against the scorer's own document.

**Its negative control is what makes the number a measurement.** A
nonsense instruction returns 0.0 overall. A scorer that returns a
middling figure for nonsense has not discriminated, and its score for a
real edit would mean nothing.

`logbook-fourloops-first-runs.md` keeps the apparatus, and this RFD
keeps the result. The entry says how the runs were made, which is what
lets somebody make them again.

## Related

RFD 1143 through RFD 1146 are the four loops that score with it. RFD
1122 is the goal they serve.
