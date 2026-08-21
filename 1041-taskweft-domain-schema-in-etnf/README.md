# RFD 1041: Taskweft domain schema in essential tuple normal form

**State:** discussion
**Scope:** RFD 1040's `domain.ex` and its 15,000 `problem.ex` files

## Problem

RFD 1040 asks Claude to inspect 15,000 dataset rows and write one
`problem.ex` per row. Many rows share the same hair color, eye
color, and pose, worded in different ways. A fixed trait list misses
new values, and free text per row repeats the same fact many times.

## Decision

Design the `domain.ex`/`problem.ex` schema per essential tuple normal
form (ETNF), from Darwen, Date, and Fagin (ICDT 2012). See
`DETAILS.md` for the definition and its worked example. Three rules
follow.

1. `@variables` holds a trait map, keyed by trait name, one value per
   character, matching the `have`/`handle`/`loaded` pattern in RFD
   102c's `domain.ex`. The key is a superkey, so the map sits in BCNF.
2. The trait taxonomy comes from the training data, not from
   preconceived categories. `capabilities` starts empty, and a
   domain action grows it as it resolves each trait value to a
   capability id. `problem.ex` stores a `:ref` to that id, never text.
3. The resolve step runs inside taskweft, through the `HRR`/
   `HRR.Cleanup` library RFD 1015 already supplies, not through
   `WeftspunStudio.FactVector` outside it. A near-duplicate caption
   binds to the existing id, instead of creating a new one.

Rule 2 and rule 3 remove the redundancy together. A functional
dependency anchored on the capability id, a superkey, blocks the
redundant tuple that ETNF targets, with no fixed enum to maintain.

## Related

RFD 1040 sets the domain/problem split. RFD 1025 gives the
`:ref`/`capabilities` rules. RFD 1015 gives the `HRR` library. RFD
102c gives the worked `domain.ex` this schema follows.
