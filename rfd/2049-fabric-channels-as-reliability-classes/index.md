---
title: "RFD 2049: Fabric channels as reliability classes, control in payload"
rfd: "2049"
state: published
scope: fabric wire protocol (entity packet and channel layout)
---

## Problem

Transforms need unreliable, latest-wins delivery at tick rate. Sparse
control events, such as a teleport vote or a loot grab, need
reliable, exactly-once delivery instead. Mixing both on one ordered
stream lets a reliable event block the transform flow. A separate
text channel for control also needs two codecs to reason about.

## Decision

Transforms want unreliable, latest-wins delivery at tick rate; sparse
control events (a teleport vote, a loot grab) want reliable,
exactly-once delivery. Mixing both on one ordered stream lets a
reliable event head-of-line-block the transform flow, and a separate
text channel for control means two codecs to reason about. The
fabric's logical channels are the reliability classes, and the
100-byte entity packet carries everything. `FabricMultiplayerPeer`
runs one ENet host per channel, so channels are head-of-line-free:
CH_INTEREST (1) carries unreliable transforms, CH_MIGRATION (0)
carries reliable-ordered control and state. The lane is chosen with
`set_transfer_channel` plus `set_transfer_mode`; a `cmd`/`action` byte
in the payload picks the meaning within a lane. Control rides the
same packet as the transform that produced it, so a hit validates
against the exact transform and tick, atomically, with no sequence
counter or dedupe, since the transport gives exactly-once delivery
per channel. Server-to-client state (phase, grant, reject) uses the
same format under reserved global ids; a display name is a byte
field, so even names stay integral and deterministic.

## References

- Original record:
  `decisions/20260612-fabric-channels-as-reliability-classes.md`
- Confirmed by [godot#56](https://github.com/v-sekai-multiplayer-fabric/godot/pull/56)
  and a four-client `FabricMultiplayerPeer` probe

## Related

- `rfd/2003-castspell-sandbox-package-and-manifest-encoding`: cites
  this layout for its wire encoding.
- `rfd/2053-integral-entity-transform-wire`: the wire fields this
  layout carries.
