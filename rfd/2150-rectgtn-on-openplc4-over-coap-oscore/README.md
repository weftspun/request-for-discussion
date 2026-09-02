# RFD 2150: RECTGTN as FBD, on OpenPLC v4 and node-graph editors

**State:** prediscussion
**Feature:** compile RECTGTN plans to IEC 61131-3 **FBD**. Runtime
hosts for OpenPLC v4's compiled binary: PLC, ESP32, Godot Sandbox
(RISC-V). Node-graph converter targets from the same FBD network:
glTF Interactivity, VRChat Udon, UE 4/5 Blueprint, Resonite ProtoFlux.
Coordination is in-process linking (RFD 2154); CoAP+OSCORE (RFD 2151)
is parked until a deployment leaves Godot's networking.

## Problem

Taskweft targets the BEAM. Constrained runtimes (PLC, ESP32, Godot
Sandbox RISC-V VM) and node-graph editors (glTF Interactivity, Udon,
Blueprint, ProtoFlux) cannot host BEAM. All those consumers speak
the same shape; typed function blocks with dataflow wires, state
persisted through named variables; which IEC 61131-3 calls **FBD**.

## Decision

Translate RECTGTN to **FBD** via RFD 2148's compact GRAFCET, emit
PLCopen XML with an `<FBD>` body encoding the state machine as
`SR_L` flip-flops per step and `AND` gates per transition. Compile
with OpenPLC v4 to a shared library or RISC-V binary; a Godot game
loads that binary through Godot Sandbox. Hand the same FBD network
to a converter for a node-graph editor.

Language ranking collapses to **FBD only**. **SFC is blocklisted**
(new row in `CLAUDE.md`, argument in `BLOCKLIST.md`). ST and LD
were already blocklisted; IL is deprecated.

Coordination rides linking: Elixir NIF → LibGodot → Godot Sandbox
→ OpenPLC compiled `.riscv`. One address space. No wire.

## References

- OpenPLC Runtime v4 (MIT), Godot Sandbox (`libriscv/godot-sandbox`)
- RFD 2148, 2144, 2146 (parked), 2149

This RFD was drafted by an AI and read by a human before it shipped.
