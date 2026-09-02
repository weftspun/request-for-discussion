# DETAILS: Lean 4 FBD -> RISC-V ELF compiler

## The three MIT pieces the compiler stitches together

1. **PLCopen FBD XML** produced by `Taskweft.OpenPLC.PLCopen.emit/1`
  (RFD 2150). Full body inside a `<pou pouType="program">`, no `<SFC>`
  wrapper (blocklisted), no `<ST>` / `<LD>` (blocklisted).
2. **Lean 4 v4.34.0-rc1** (matches RFD 2149), stdlib only for stage 1.
  `Std.Xml` supplies the XML parser; no mathlib fetch until the
  correctness theorem lands under its own RFD.
3. **`riscv64-elf-gcc`** already installed on this box (`brew install
  riscv64-elf-gcc`, RFD 2154 bootstrap). The Lean compiler emits
  `.s`, the toolchain runs `as` + `ld` to produce the `.elf`.

## FBD AST; full IEC 61131-3 standard block library

Stage 1 lists every standard block in the AST but implements the
emit for only the subset our own emitter produces today (SR_L, AND,
MOVE, TON). Later stages fill in the rest as consumers name them.

    inductive Block where
      | sr_l  | rs   | sr        ; bistables
      | and_ | or_  | not_ | xor ; boolean
      | move | mux  | sel  | limit | min | max  ; selection
      | ton  | tof  | tp        ; timers
      | ctu  | ctd  | ctud      ; counters
      | add  | sub  | mul  | div | mod  ; arithmetic
      | eq   | ne   | lt   | gt  | le | ge  ; comparison
      | f_trig | r_trig                    ; edges

Each carries its typed inputs and outputs. `POU` wraps a variable
list and a network of `Block` instances connected by `Wire`s.

## godot-sandbox syscall ABI to target

The ELF exports one entry (`on_tick`) and calls back into the host
via a small syscall table libriscv/godot-sandbox already defines for
its `gdscript.elf` sample. The exact numbers come from godot-sandbox's
`syscalls.hpp`; pinning that header's version is a follow-on so ABI
drift is caught. Stage-1 uses:

    ecall #1  print(cstr)
    ecall #10 get_variable(cstr_name) -> Variant
    ecall #11 set_variable(cstr_name, Variant)
    ecall #20 register_callable(cstr_name, fn_ptr)
    ecall #21 call_callable(cstr_name, args...)

The RECTGTN `done_*` booleans become variables the host reads with
`get_variable`; RECTGTN actions register as callables the host
invokes with `call_callable`.

## Stages

| stage | scope |
|---|---|
| 1 (this RFD) | Skeleton: lakefile, AST types, `Std.Xml` parser, RISC-V IR + emitter stubs, `Main.lean` smoke on `weftspun-build.plcopen.xml` |
| 2 | RISC-V emitter body for SR_L / AND / MOVE / TON; round-trip test compiles and runs in godot-sandbox |
| 3 | Semantics module + `compile_correct` theorem (brings mathlib in) |
| 4 | Emit for the remaining standard blocks per the AST above |
| 5 | GDScript companion module (`get_variable` / `set_variable` / `call` wrappers on the Godot side), `mix openplc.compile --target elf-lean` |

## RECTGTN -> FBD mapping; deferred

RECTGTN's own shape (domain, problem, plan) still needs a mapping
into POUs. Stage 1 accepts hand-authored PLCopen FBD; the mapping
lands under its own RFD once the compiler works. Candidate shape,
recorded here so it doesn't get lost: domain = Function Block library
(one FB per RECTGTN action), problem = Program POU wiring initial
state, plan = Program POU wiring action-FB calls in the planned
order.

## Verification

1. `lake build` in `3-interactor/taskweft-fbd-compiler/` succeeds in
  seconds; no external deps.
2. `./.lake/build/bin/taskweft_fbd_compiler` runs on
  `weftspun-build.plcopen.xml` produced by `mix openplc.emit` and
  prints the AST's variable and step counts.
3. Workspace anti-entropy passes; no blocklist rows added; serial
  S2157 registered.

## What is deliberately not here

1. mathlib fetch + build (stage 3).
2. RECTGTN -> FBD mapping decision (its own RFD).
3. The RISC-V emitter body (stage 2).
4. Semantics + correctness theorem (stage 3).
5. GDScript companion module (stage 5).
6. Runtime performance profiling; real fbd -> elf -> sandbox tick
  timing lands with stage 2.
