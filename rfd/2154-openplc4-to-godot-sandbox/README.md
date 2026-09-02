# RFD 2154: OpenPLC v4 into Godot Sandbox, from Elixir

**State:** prediscussion
**Feature:** compile RECTGTN → FBD → OpenPLC v4 → RISC-V shared
object, load into Godot through Godot Sandbox (`libriscv`), embed
that Godot from Elixir via the `lib_godot_connector` NIF
**Scope:** taskweft compile chain, new `taskweft-godot-sandbox`
project (Elixir + Godot scene + Godot Sandbox addon)

## Problem

RFD 2150 names Godot Sandbox as one runtime host for OpenPLC v4's
compiled binary. The compile lives in OpenPLC v4's toolchain (MIT
runtime, GCC-style runtime exception on the compiler). The load-
and-execute lives in a Godot process. Elixir owns the coordinator.
This RFD is the wire.

## Decision

Reuse three MIT pieces:

1. **OpenPLC v4** compiles FBD XML to a RISC-V shared object.
2. **Godot Sandbox** (`libriscv/godot-sandbox`) ticks it per frame.
3. **`lib_godot_connector`** is the Elixir NIF over LibGodot.

Flow: `RECTGTN → to_grafcet → PLCopen.emit → openplc-cli compile
--target riscv64 → Godot scene loads plan.riscv via Godot Sandbox →
BEAM embeds that Godot via lib_godot_connector`.

`DETAILS.md` carries the Godot scene shape, the Sandbox addon config,
the frame-tick contract, and verification.

## References

1. lib_godot_connector: https://hex.pm/packages/lib_godot_connector
2. Godot Sandbox: https://github.com/libriscv/godot-sandbox (MIT)
3. RFD 2148, 2144, 2145

This RFD was drafted by an AI and read by a human before it shipped.
