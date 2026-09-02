# RFD 2151: CoAP + OSCORE NIF for taskweft

**State:** abandoned
**Feature:** Elixir NIF over libcoap for CoAP RFC 7252 + OSCORE RFC 8613
**Scope:** taskweft (`Taskweft.OpenPLC.CoAP`), OpenPLC v4 CoAP plugin

## Problem

RFD 2150 puts an OpenPLC v4 runtime on the far side of a constrained
UDP link, reached over CoAP+OSCORE. Elixir has no first-class CoAP
client, and no first-class OSCORE library. Building the whole
transport as an Elixir library would take much longer than wrapping a
C library that already ships it.

## Decision

Wrap **libcoap** (BSD-2-Clause, MIT-compatible) with a NIF, modelled
on `taskweft-nmm-personas/c_src/weft_bus_nif.cpp`: a resource holds
one CoAP context, `ask/3` publishes a request-id-tagged CoAP request
under an OSCORE security context and polls until the matching reply
lands. OSCORE key material is a `Taskweft.OpenPLC.CoAP.Keyset` struct
configured at start. EDHOC key exchange (RFC 9528) is staged.

**Parked.** Execution today is static / dynamic linking (RFD 2154):
OpenPLC v4's compiled RISC-V .so loads into Godot Sandbox via
`libriscv`; the coordinator is `lib_godot_connector`'s in-process
NIF. No wire. Local testing needs no networking. This RFD unblocks
only when a deployment leaves Godot's networking layer for a
constrained-UDP target Godot itself does not reach.

`DETAILS.md` carries the C ABI the NIF wraps, the resource shape, the
OSCORE key rotation model, and the OpenPLC-side plugin sketch.

## References

- RFC 7252 (CoAP), RFC 8613 (OSCORE), RFC 9528 (EDHOC)
- libcoap: https://libcoap.net/ (BSD-2-Clause)
- RFD 2150 RECTGTN on OpenPLC v4; the caller

This RFD was drafted by an AI and read by a human before it shipped.
