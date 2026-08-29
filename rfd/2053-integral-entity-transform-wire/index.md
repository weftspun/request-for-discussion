---
title: "RFD 2053: Integral entity-transform wire (int64 micrometers, no origin shift)"
rfd: "2053"
state: published
scope: entity-transform wire packet (XRGridEntityPacket)
---

## Problem

The determinism doctrine keeps the authoritative state in integers
and r128 fixed point. The entity-transform packet instead carried
position as `f64`, three doubles whose 52-bit mantissa cannot even
represent a Q64.64 value. This reintroduced cross-platform divergence
into an otherwise deterministic wire format.

## Decision

The fabric replicates entity transforms in a fixed 100-byte packet.
The determinism doctrine keeps the authoritative state in integers
and r128 fixed point, yet the packet carried position as `f64` —
three doubles whose 52-bit mantissa cannot even represent a Q64.64
value, reintroducing cross-platform divergence. Every field on the
wire becomes integral. Position becomes int64 absolute micrometers —
the integer twin of the `precision=double` large-world coordinate, so
there is no camera-relative origin shifting. Velocity stays i16,
scaled to `PBVH_V_MAX_PHYSICAL_DEFAULT` so it shares the predictive
BVH's units; rotation stays i16 swing-twist; a 42-byte userdata
payload carries control and state; the packet keeps its 100 bytes.
The authoritative position stays r128, and the wire is its
micrometer-scale integer projection. Clients render rather than
re-simulate, so quantization stays below perception while the exact
state remains server-side. A Lean 4 plus Plausible model is the
source of truth: a roundtrip property, a size invariant, and a
golden-vector differential the C++ must match.

## References

- Density-from-baseline note, entropy tradeoff, confirmation, and the
  spec-model repository: `DETAILS.md`
- Original record: `decisions/20260612-integral-entity-transform-wire.md`

## Related

- `rfd/2034-deterministic-cores-integer-seeded-rng`: the determinism
  doctrine this wire format follows.
- `rfd/2046-server-authoritative-simulation-deferred-rollback`: why
  clients render rather than re-simulate.
- `rfd/2049-fabric-channels-as-reliability-classes`: the channel this
  packet rides.

## Detail

{{< include DETAILS.md >}}
