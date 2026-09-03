# RFD 2032: Core codegen lean slang

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The cores carry compute kernels — hit raycasts, the budgeter solve,
geometry costing — that need to be verified once and run as GPU
compute, with the dispatch wrapped behind the flat C ABI port
(`rfd/2044-lean4-kernel-cores-flat-c-host-adapters`). Hand-porting a
kernel from a separate spec to a shader drifts.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
