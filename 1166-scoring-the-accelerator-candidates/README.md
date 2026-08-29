# RFD 1166: How the accelerator candidates were scored

**State:** ideation
**Feature:** the method behind RFD 1154 to RFD 1162
**Scope:** `2-contract/manuals-weftspun`

## Problem

Eight RFDs cite a score out of 25, each saying what it scored and
what it lost to, and no document says what the 25 measures. That is
a register with no source: a reader can see the ranking and cannot
reproduce it, challenge a row, or tell which scores rest on
measurement and which on a published name. Nothing fails when the
rows and the criteria disagree, there being no criteria.

The scale was also applied before it was written. A rubric recorded
after the ranking it produced is a rationalisation unless the rows
can be checked against it.

## Decision

Five criteria, 0 to 5 each, summing to 25:

    fit        headroom at a workable precision
    shape      is the graph fixed-shape
    reference  does a working precedent exist
    clear      is anything else blocking it
    value      what accelerating it buys

Twenty-five because EditScore's own `score_range` is 25 and it
normalises by `score_range / 10`. `value` is the softest column and
named so rather than defended.

VoxHammer is scored on the edit it forces on its base, not the
weights it lacks: it patches the backbone's forwards at runtime and a
compiled graph cannot be patched. `DETAILS.md` carries every row.

## Related

RFD 1154 to RFD 1162 hold the candidates.
