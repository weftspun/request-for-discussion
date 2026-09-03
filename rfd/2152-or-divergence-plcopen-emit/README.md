# RFD 2152: OR-divergence emit in PLCopen SFC

**State:** discussion
**Feature:** extend `Taskweft.OpenPLC.PLCopen.emit/1` to cover `|>`
and `|<` markers from the compact GRAFCET DSL
**Scope:** taskweft (`lib/taskweft/openplc/plcopen.ex`)

## Decision

Cover the single-branch OR case first (the blocks_world `get:
pickup_from_table | unstack` shape), then multi-branch, then multi-
step branches. Each branch becomes an SFC alternative sequence
between an `OrDivergence` connector and an `OrConvergence` connector,
with **mutually exclusive receptivities** enforced at emit time.
A chart with overlapping receptivities is what RFD 2149's Lean
analyser flags as a concurrent pair; the emitter reads that flag on
the source compact GRAFCET and refuses if the pair appears.

**Parked.** No taskweft caller needs OR-divergence in an OpenPLC
target today. The lower/raise pair already covers OR on the HTN side
(RFD 2148 test); this RFD closes only the PLCopen leg.

`DETAILS.md` carries the PLCopen XML shape, the exclusivity gate, the
interaction with RFD 2149, and multi-step branch semantics.

## Problem

RFD 2148's compact GRAFCET carries `|>` (OR-divergence) and `|<`
(OR-convergence) markers; `Taskweft.Grafcet.lower/1` already lowers
them to a synthesised chooser method (RFD 2148 stage 1). The PLCopen
SFC emitter refuses them today with `RuntimeError` pointing here.

## References

1. RFD 2148 compact GRAFCET, RFD 2149 static analyser, RFD 2150 emit
2. `test/fixtures/grafcet/blocks_get_or.grafcet.jsonld`

This RFD was drafted by an AI and read by a human before it shipped.
