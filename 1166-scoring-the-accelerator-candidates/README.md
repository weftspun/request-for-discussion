# RFD 1166: How the accelerator candidates were scored

**State:** ideation
**Feature:** the method behind RFD 1154 to RFD 1162
**Scope:** `2-contract/manuals-weftspun`

## Problem

Eight RFDs cite a score out of 25 and no document says what the 25
measures. A reader can see the ranking and cannot reproduce it,
challenge a row, or tell which scores rest on measurement and which
on a published name.

The scale was applied before it was written and was too coarse: at
five steps a dimension, four candidates sat inside two points with no
meaning in their order.

## Decision

Six dimensions, each scored 0 to 100:

    fit        headroom at a workable precision
    shape      is the graph fixed-shape
    reference  does a working precedent exist
    clear      is anything else blocking it
    value      what accelerating it buys
    adapt      can this desk train, tune or LoRA it

Aggregate by **STAR**, score then automatic runoff, with the six
dimensions as voters: sum to find two finalists, then decide between
them by how many dimensions prefer each. A sum alone lets one column
carry a candidate, and `value` is the softest, so the runoff stops it
deciding alone. `DETAILS.md` carries every row.

**The earlier 0 to 5 scale, summing to 25 because EditScore's
`score_range` is 25, is retracted.** It was a borrowed number.

## Related

RFD 1154 to RFD 1162 hold the candidates.
