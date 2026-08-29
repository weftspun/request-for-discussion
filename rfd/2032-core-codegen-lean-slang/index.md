---
title: "RFD 2032: Core kernel codegen via lean-slang (Lean to Slang to SPIR-V)"
rfd: "2032"
state: published
scope: GPU compute kernel codegen for the hexagonal cores
---

## Problem

The hexagonal cores carry compute kernels, such as hit raycasts, the
budgeter solve, and geometry costing. These kernels need one verified
source. A hand-ported shader, written from a separate specification,
can drift from that source with no way to detect the drift.

## Decision

The cores carry compute kernels, such as hit raycasts, the budgeter
solve, and geometry costing. These kernels need one verified source. A
hand-ported shader from a separate spec can drift from that source.
The project authors each kernel in Lean and lowers it to Slang through
`lean-slang`. It then runs `slangc -target spirv` to produce SPIR-V,
and dispatches the compiled kernel behind the flat C ABI port. SPIR-V
runs the kernel on the GPU and gets the convergence integration the
CPU Slang target lacks. The `idtx-flow` repository already depends on
`LeanSlang` and byte-pins the emitted Slang against the committed
source with `native_decide`. The project commits the lowered Slang and
the compiled SPIR-V, and byte-pins both, so a drifting regeneration
fails the pin. The kernels use integer operations only, so the SPIR-V
output stays deterministic across conformant devices.

## References

- Full context, decision drivers, considered options, and confirmation
  steps: `DETAILS.md`
- Original record: `decisions/20260611-core-codegen-lean-slang.md`
- `lean-slang`: https://github.com/V-Sekai-fire/lean-slang

## Related

- `rfd/2034-deterministic-cores-integer-seeded-rng`: the integer-op
  determinism rule these kernels follow.
- `rfd/2044-lean4-kernel-cores-flat-c-host-adapters`: the flat C ABI
  these kernels dispatch behind.

## Detail

{{< include DETAILS.md >}}
