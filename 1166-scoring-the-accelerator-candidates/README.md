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

Rank by **STAR**, score then automatic runoff, with the six dimensions
as voters: take the two highest sums, let the dimensions vote between
them, seat the winner, remove it, repeat. The rank is the result and
the sum only its first round; eight of seventeen seats differ. A sum
alone lets one column carry a candidate. `DETAILS.md` has both.

**The earlier 0 to 5 scale, summing to 25 because EditScore's
`score_range` is 25, is retracted.** It was a borrowed number.

## Related

RFD 1154 to RFD 1162 hold the candidates.
