# RFD 2083: Zone server h2o replaces godot fabriczone

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The production zone server (`zone-server`, deployed as
`multiplayer-fabric-zone` on Fly.io) is a boot scaffold today —
OpenTelemetry init only, no WebTransport listener, no game logic
(`project/main.gd`'s own `TODO(cycle-5)` comment). The real
entity/simulation engine,
`FabricZone`/`FabricZoneJournal`/`FabricMMOGZone`, exists as a working
Godot C++ module in `V-Sekai-fire/multiplayer-fabric-build`
(`godot/modules/multiplayer_fabric/`) but has never been wired into a

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
