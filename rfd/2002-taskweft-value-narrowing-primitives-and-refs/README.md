# RFD 2002: Taskweft value narrowing primitives and refs

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

`taskweft/nif` (the C++ core behind the `taskweft/taskweft` Elixir
host, a separate repo from the one the name suggests) narrows every
value that crosses an interpreter or ABI boundary down to one small
tagged union, `TwValue`, with seven kinds: `NIL`, `BOOL`, `INT`,
`FLOAT`, `STRING`, `ARRAY`, `DICT`. There is no eighth kind for
references. A reference is a plain `STRING` value, shaped as an RFC
6901 JSON Pointer, resolved against a flat `var -> Dict` state tree at
the point of use. This RFD records that real design, checked directly

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
