## Context and problem statement

The cores carry compute kernels — hit raycasts, the budgeter solve,
geometry costing — that need to be verified once and run as GPU
compute, with the dispatch wrapped behind the flat C ABI port
(`rfd/2044-lean4-kernel-cores-flat-c-host-adapters`). Hand-porting a
kernel from a separate spec to a shader drifts.

## Decision drivers

- One verified Lean source per kernel, with no separate shader to
  drift.
- The kernel runs on the GPU and integrates with GPU convergence; the
  CPU Slang target lacks that integration.
- Integer ops keep the kernel deterministic across conformant devices.

## Considered options

- Hand-write each kernel as a shader from a separate spec.
- Lower a CPU host target through Slang.
- Author the kernel in Lean and lower it to SPIR-V.

## Decision outcome

Chosen option: author the compute kernels in Lean and lower them to
Slang through [lean-slang](https://github.com/V-Sekai-fire/lean-slang),
then run `slangc -target spirv` to SPIR-V (`.spv`), and dispatch the
`.spv` behind the flat C ABI, because SPIR-V runs the kernel on the
GPU with the convergence integration the CPU Slang target lacks, and
one verified Lean source produces the shipped kernel. The `idtx-flow`
repository already depends on `LeanSlang` and byte-pins the emitted
Slang against committed source with `native_decide`.

## Consequences

- One Lean kernel source produces the `.spv`, so the spec and the
  shipped kernel stay one artifact.
- The lowered Slang and the `.spv` are committed and byte-pinned, so a
  regen that drifts fails the pin.
- The kernels use integer ops, so the SPIR-V stays deterministic
  across conformant devices
  (`rfd/2034-deterministic-cores-integer-seeded-rng`).

## Confirmation

The emitted Slang matches its committed byte-pin, and the dispatched
`.spv` kernel passes the core fixtures.
