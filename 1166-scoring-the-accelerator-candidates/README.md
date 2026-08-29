# RFD 1166: How the accelerator candidates were scored

**State:** discussion
**Feature:** the method behind RFD 1154 to RFD 1162
**Scope:** `2-contract/manuals-weftspun`

## Problem

Eight RFDs cite a score out of 25 and no document says what the 25
measures. A reader sees the ranking and cannot reproduce it or tell
which scores rest on measurement and which on a published name. It was
also applied before it was written, and was too coarse.

## Decision

Eight dimensions, each scored 0 to 100:

    fit        headroom at a workable precision
    shape      is the graph fixed-shape
    reference  does a working precedent exist
    clear      is anything else blocking it
    value      what accelerating it buys
    adapt      can this desk train, tune or LoRA it
    ask        can we get an answer out of it at all
    wanted     does anyone want the thing it does

`adapt` and `ask` are duals: one changes the model, the other queries
it. `wanted` asks what the product is for, where the rest ask only
about tractability.

Rank by **STAR**, score then automatic runoff, the eight dimensions
voting: take the two highest sums, let them vote, seat the winner,
remove it, repeat. `scripts/check_rfd1166_rank.py` recomputes that
with `starvote` and fails if `DETAILS.md` disagrees. **It ranks units
of work, not capabilities**: a chain delivers when every stage is
placed, and rows interact.

## Related

RFD 1154 to 1162 hold the candidates; RFD 1167 says where each is.
