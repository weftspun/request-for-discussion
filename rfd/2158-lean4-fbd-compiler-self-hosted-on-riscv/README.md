# RFD 2158: Self-host the Lean 4 FBD compiler on RISC-V; abandoned

**State:** abandoned (stage 0-1 kept as evidence)
**Feature:** cross-compile RFD 2157's Lean 4 FBD compiler to RISC-V
so it runs inside godot-sandbox
**Scope:** was `taskweft-fbd-compiler` build target; superseded

## Why abandoned

Upstream RFC `leanprover/lean4#12655` open with no pickup. Local port
of Lean's ~50 runtime `.cpp` files is speculative work with no
consumer. **RFD 2159 replaces the intent**: two independent `.elf`
implementations (C++ + Rust) cross-check against the Lean 4 spec;
both cross-compile today using standard toolchains.

## What stays

- **Stage 0-1 landed**: `TaskweftFbdCompiler.Elf` writes valid
  RISC-V ELF bytes directly from Lean (no external assembler); the
  ELF loads into a live Godot Sandbox and Godot ticks clean.
  Evidence: `ladder/hello.elf`. That's the "Lean can emit ELF bytes"
  proof; it doesn't require Lean itself to run on RISC-V.

## What was dropped

- Stage 2: Lean-emitted C cross-compiling to RISC-V.
- Stage 3: Full compiler running inside a Sandbox.
- The trap-list around Lean runtime shims on libriscv.

RFD 2159 is the successor; both C++ and Rust ELFs land using
standard cross-compilers and cross-check byte-for-byte against the
Lean spec. The Lean formal-verification story survives without
paying the self-host cost.

## References

- RFD 2157 (Lean spec), RFD 2159 (two-impl replacement)
- `leanprover/lean4#12655` (upstream RFC, watched not blocked-on)

This RFD was drafted by an AI and read by a human before it shipped.
