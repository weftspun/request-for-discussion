# RFD 2153: PLCopen FBD to VRChat Udon assembly

**State:** prediscussion (Udon is the only target)
**Feature:** convert taskweft's PLCopen FBD (RFD 2150) directly into
Udon assembly for VRChat
**Scope:** taskweft (`Taskweft.OpenPLC.Udon`)

## Problem

RFD 2150 makes PLCopen FBD the one runtime target. The two platforms
taskweft ships to are **godot-sandbox** (RFD 2154, C++ + Rust ELFs
via RFD 2159) and **VRChat Udon**. Udon has its own native
assembly language; FBD needs a direct compiler into it.

## Decision

**Ship FBD -> Udon assembly, direct.** **C# as an intermediate is
blocklisted**; UdonSharp adds Roslyn as a dep for one output format
and duplicates verification outside RFD 2159's C++/Rust cross-check.
Direct mirrors godot-sandbox's SafeGDScript pattern (source
language -> target ISA, no C++ intermediate). VRChat's creator
feedback loop demos in-world without a compile-and-flash cycle.

**Dropped (were parked previously):**
- UE 4/5 Blueprint; out of scope for taskweft.
- Resonite ProtoFlux; out of scope.
- glTF Interactivity; out of scope.

Udon assembly's opcode + directive surface lives at
`taskweft-fbd-compiler/sigs/vrchat_udon_asm.sigs` (extracted from
UdonSharp's own assembler, MIT). The FBD emitter walks each block
and writes the corresponding uasm opcodes into the RFD 2160 USD
plan's `/Deliveries/UdonAsm` string.

`DETAILS.md` carries the block-to-uasm mapping and the round-trip
against the `blocks_get_or` fixture.

## References

- `sigs/vrchat_udon_asm.sigs`; the target instruction set
- RFD 2150 FBD target, RFD 2160 USD intermediate
- UdonSharp (source of truth for opcode set): vrchat-community/UdonSharp

This RFD was drafted by an AI and read by a human before it shipped.
