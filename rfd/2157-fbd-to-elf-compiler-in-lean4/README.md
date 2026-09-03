# RFD 2157: Lean 4 FBD -> RISC-V ELF compiler

**State:** prediscussion
**Feature:** RECTGTN in IEC 61131-3 FBD (PLCopen XML) -> RISC-V ELF
godot-sandbox loads. Spirit of UdonSharp and SafeGDScript.
**Scope:** new `3-interactor/taskweft-fbd-compiler` (Lean 4)

## Decision

New repo `taskweft-fbd-compiler`, Lean 4 v4.34.0-rc1 (matches RFD
2144), MIT. Pipeline:

    PLCopen FBD XML
      -> Lean 4 parser (Std.Xml, stdlib only)
      -> FBD AST (full IEC 61131-3 standard block library)
      -> RISC-V instruction encoder + ELF64 writer, both in Lean
      -> plan.elf bytes to disk, no external assembler or linker
      -> godot-sandbox loads

**ABI:** matches `gdscript.elf`'s syscall table.
**GDScript I/O:** `get_variable`/`set_variable` for state,
`sandbox.call('fn', args)` for actions.

RFD 2156 is the parallel GDScript-side path. `DETAILS.md` carries
AST, ABI, staging.

## Problem

RFDs 2154-2151 reach godot-sandbox through GDScript. There's no
compiler for the direct path: FBD in, ELF out. A verified compiler
in Lean 4 would carry proofs the ELF's state graph matches the
FBD's own, not just tests.

## References

1. godot-sandbox: https://github.com/libriscv/godot-sandbox
2. UdonSharp: https://github.com/vrchat-community/UdonSharp
3. RFD 2149, 2145, 2149, 2150, 2151

This RFD was drafted by an AI and read by a human before it shipped.
