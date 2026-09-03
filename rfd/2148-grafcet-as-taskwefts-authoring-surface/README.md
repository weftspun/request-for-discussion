# RFD 2148: GRAFCET as taskweft's authoring surface

**State:** prediscussion
**Feature:** taskweft domains authored as compact IEC 60848 GRAFCET,
lowered to HTN at load, driven over `2-contract/bus`
**Scope:** taskweft, taskweft-nmm-personas, and any future planner
domain that fits the propositional-with-parameters class

## Decision

Author domains as compact IEC 60848 GRAFCET (SFC-shaped notation) in
a JSON-LD profile aligned with Project-AGRAFE. A taskweft mix task
lowers into the HTN JSON the NIF loader consumes. The authoring
shape is GRAFCET; the *runtime target* under RFD 2150 is IEC
61131-3 **FBD** (SFC as a runtime target is blocklisted). The mapping is
total on the AND/sequential fragment; `|>`, `|<`, `!>`, `%`, `#`
markers extend it to OR-divergence, macro-steps, enclosing steps, and
forcing orders. Those higher-level 60848 constructs cover HTN
parameter dispatch and method decomposition without leaving the
standard. `DETAILS.md` carries the mapping table, the loss ledger,
the transport, the persona rate contract, and the verification.

The reference implementation and proof is
`3-interactor/taskweft-nmm-personas`: three GRAFCET personas play a
128-agent Neural MMO 2 episode over `2-contract/bus` with CBOR+zstd
on the wire, effective persona rate 26 Hz against a 10 Hz floor.

## Problem

A taskweft HTN domain is a hand-authored 40+ line JSON-LD block of
`variables / actions / methods / tasks / pointer/get / pointer/set /
math/eq`. Each action carries redundant preconditions the author
keeps in sync by hand. No model checker consumes the shape. Two
hazards follow: the file drifts against itself, and no gate reads it.

## References

1. `3-interactor/taskweft/lib/taskweft/grafcet.ex`; lower and raise
2. `3-interactor/taskweft-nmm-personas/`; reference implementation
3. RFD 1065, 2093, RFD 1173 MASKSCORE.md, Project-AGRAFE

This RFD was drafted by an AI and read by a human before it shipped.
