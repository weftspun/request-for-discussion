# RFD 1166: How the accelerator candidates were scored

**State:** ideation
**Feature:** the method behind RFD 1154 to RFD 1162
**Scope:** `2-contract/manuals-weftspun`

## Problem

Eight RFDs cite a score out of 25 and no document says what the 25
measures. A reader can see the ranking and cannot reproduce it,
challenge a row, or tell which scores rest on measurement and which on
a published name. The scale was applied before it was written and was
too coarse: at five steps a dimension, four candidates sat inside two
points with no meaning in their order.

## Decision

Seven dimensions, each scored 0 to 100:

    fit        headroom at a workable precision
    shape      is the graph fixed-shape
    reference  does a working precedent exist
    clear      is anything else blocking it
    value      what accelerating it buys
    adapt      can this desk train, tune or LoRA it
    ask        can we get an answer out of it at all

`adapt` and `ask` are duals: one changes the model, the other queries
it, and `weft_ask` is already the workspace's verb for the second. A
model can score well on `fit` and `shape` and have never answered.

Rank by **STAR**, score then automatic runoff, the seven dimensions
voting: take the two highest sums, let them vote, seat the winner,
remove it, repeat. `DETAILS.md` has the rank and the rows. **The
earlier 0 to 5 scale, summing to 25 because EditScore's `score_range`
is 25, is retracted** as a borrowed number.

## Related

RFD 1154 to RFD 1162 hold the candidates; RFD 1163 places them.
