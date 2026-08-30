# RFD 1166: How the accelerator candidates were scored

**State:** abandoned
**Feature:** the method behind RFD 1154 to 1162
**Scope:** `2-contract/manuals-weftspun`

## Problem

Eight RFDs cite a score out of 25 and no document says what the 25
measures, so a reader cannot reproduce it or tell which scores rest on
measurement. It was also applied before it was written.

## Decision

Eight dimensions, each scored 0 to 100:

    fit        headroom at a workable precision
    shape      is the graph fixed-shape
    reference  does a working precedent exist
    clear      is anything else blocking it
    value      what accelerating it buys
    adapt      can this desk train, tune or LoRA it
    ask        can we get an answer out of it
    wanted     does anyone want the thing it does

`adapt` and `ask` are duals. `check_rfd1166_rank.py` recomputes the
**STAR** order with `starvote`.

**ABANDONED 2026-08-29, and RFD 1171 replaces it.** The ranking asked
which candidate is most worth accelerating, and that was the wrong
question: these are stages of one loop, not competitors for one device,
and a stage does not outrank the stage it feeds. `Qwen3-ASR` entering at
seat 2 made it plain.

<!-- retain-details -->
`DETAILS.md` keeps the table and the measurements that RFD 1171 cites.

## Related

RFD 1154 to 1162 hold the candidates; RFD 1167 says where each is.
