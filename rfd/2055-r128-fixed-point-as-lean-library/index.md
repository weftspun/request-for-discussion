---
title: "RFD 2055: r128 Q64.64 fixed-point as a Lean library for the cores"
rfd: "2055"
state: published
scope: fixed-point math library for the Lean kernel cores
---

## Problem

The deterministic cores need Q64.64 fixed-point math inside the Lean
kernels. The engine already vendors a C `r128` library, but the
kernels are authored in Lean, not C. Calling the vendored C library
from the host only would leave the kernels in floating point, and
floating point in the kernels breaks determinism. An ad-hoc Q64.64
implementation inside each kernel would also drift from the others.

## Decision

The deterministic cores need Q64.64 fixed-point math inside the Lean
kernels, which lower to SPIR-V through lean-slang. The engine already
vendors the C `r128` library (`thirdparty/misc/r128`), but the
kernels are authored in Lean. The team considered calling the vendored
C `r128` from the host only and keeping the kernels in floating
point, and reimplementing Q64.64 ad hoc inside each kernel. Both are
rejected: floating point in the kernels breaks determinism, and an
ad-hoc Q64.64 per kernel drifts. The project ports `r128` to a Lean
library that the cores import for their Q64.64 fixed-point math,
because one Lean implementation feeds every kernel and lowers to
SPIR-V over 64-bit integer pairs, while the vendored C
`thirdparty/misc/r128` stays the host reference the Lean library
matches. The cores share one fixed-point implementation, so the host
reference and the SPIR-V kernels agree bit-for-bit. A Plausible suite
checks the Lean `r128` against the vendored C `r128` for matching
results, and the lowered SPIR-V reproduces the same results.

## References

- Original record:
  `decisions/20260612-r128-fixed-point-as-lean-library.md`

## Related

- `rfd/2032-core-codegen-lean-slang`: the lean-slang lowering path
  this library's fixed-point ops travel.
- `rfd/2034-deterministic-cores-integer-seeded-rng`: the determinism
  doctrine this fixed-point library serves.
