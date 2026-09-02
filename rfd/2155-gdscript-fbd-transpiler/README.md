# RFD 2155: GDScript <-> IEC 61131-3 FBD transpiler

**State:** prediscussion; reader half (FBD -> GDScript) landed
**Feature:** bidirectional transpile between GDScript and PLCopen FBD
(RFD 2150): Godot users author in a familiar language, taskweft renders
RECTGTN-produced FBD back as GDScript for humans
**Scope:** taskweft, new sibling `taskweft-gdscript-fbd`

## Problem

RFD 2150's target is PLCopen FBD. Godot devs author in GDScript.
The gap is what Merlin's **UdonSharp** solved for VRChat: Udon is a
node graph, C# is a familiar language, UdonSharp compiles C# to Udon
so the author never sees the graph unless they want to. Taskweft has
the same shape:

1. **GDScript author**: `.gd` -> transpiler -> FBD -> RFD 2150
   compile -> RFD 2154 loads into Godot Sandbox.
2. **FBD reader**: compiled RECTGTN plan renders back as `.gd` for
   humans debugging the state machine in Godot's editor.

godot-sandbox ships **SafeGDScript** (its own GDScript-to-RISC-V
compiler; Dec 2025 "42 demo projects" milestone landed feature
parity). SafeGDScript is the second half: transpiler emits GDScript,
SafeGDScript compiles to RISC-V, Godot Sandbox loads it. No OpenPLC
Editor needed for GDScript-authored plans.

## Decision

**Parked.** Design frozen against UdonSharp's pattern. Lands when
the first taskweft user names a GDScript-authored domain. `DETAILS.md`
carries the UdonSharp study and the GDScript subset covered stage 1.

## References

1. UdonSharp: https://github.com/vrchat-community/UdonSharp
2. SafeGDScript: https://libriscv.no/blog/godot-sandbox-fortytwo/
3. RFD 2148, 2145, 2149

This RFD was drafted by an AI and read by a human before it shipped.
