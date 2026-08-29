---
title: "RFD 2044: Lean 4 build-time kernel cores with flat-C host adapters"
rfd: "2044"
state: published
scope: hexagonal core language boundary (Lean at build time, flat C at run time)
---

## Problem

The hexagonal cores hold dependency-free domain logic that Godot, the
Elixir backend, and a CLI all bind. The team wants strong spec and
proof guarantees on that logic. Linking a heavy language runtime into
every host would work against this goal.

## Decision

The hexagonal cores (`rfd/2028-hexagonal-core-ports-adapters`) hold
dependency-free domain logic that Godot, the Elixir backend, and a CLI
all bind. The team wants strong spec and proof guarantees on that
logic without linking a heavy language runtime into every host. The
project uses Lean 4 at build time as the kernel, the spec, and the
code generator, and ships each runtime core as a flat C ABI behind the
port ring, with no Lean runtime linked into any host, because this
keeps the proof leverage while the hosts bind only a flat C surface.
Each core models a pure reducer over byte-serialized state
(`rfd/2033-core-contract-pure-reducer-byte-state`). Its compute
kernels lower through `lean-slang` to SPIR-V
(`rfd/2032-core-codegen-lean-slang`), and the spec suite drives the C
ABI through Python ctypes, with property tests on Plausible and a
handful of theorems pinning invariants that never break. This mirrors
`idtx-flow`, where `flow/core` compiles to a flat-C library,
`flow/ports` is the flat C ABI, and `flow/core/spec` drives that ABI
through ctypes with no engine and no hardware. A host binds only the
flat C ABI and never sees core internals or a Lean runtime.

## References

- Full context, considered options, consequences, and confirmation
  steps: `DETAILS.md`
- Original record:
  `decisions/20260611-lean4-kernel-cores-flat-c-host-adapters.md`

## Related

- `rfd/2032-core-codegen-lean-slang`: the Lean-to-SPIR-V compute
  kernel codegen these cores dispatch.
- `rfd/2033-core-contract-pure-reducer-byte-state`: the pure-reducer
  contract each core implements.

## Detail

{{< include DETAILS.md >}}
