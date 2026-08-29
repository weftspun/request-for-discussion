---
title: "RFD 2091: The Gyre as a second MUD domain"
rfd: "2091"
state: published
scope: zone-server-h2o mud/guest, mud/web
---

## Problem

`mud/guest/mud_guest.cpp` served one setting, Middleham. Middleham is a
spy-thriller MUD, with gate, market, and temple rooms. It has trust and
suspicion objectives. The starting room, the item list, and the
objective logic were all fixed to that one world. `rfd/0085` proposes a
second setting, The Gyre. `zone-server-h2o` needed a way to add it
without a second server architecture.

## Decision

`mud_boot()` reads a new `domain` CBOR field (`"middleham"` default,
`"the_gyre"` new). `MiddlehamStateMachine` keeps its name and its
existing behavior unchanged for the default domain. A `domain_` member
and three guarded branches cover the new domain: the start-room pick,
`clone_rooms()`, and `objective_complete()`. A new
`gyre_room_templates()` backs them, with two rooms, `decanting_floor`
and `splicers_den`, one exit each way, no items, and no non-player
characters (NPCs). This is the smallest possible loop (look, go, look),
not `rfd/0085`'s full room graph.

The `domain` field threads through the same chain the `objective` field
already used, ending at `POST /api/mud/command`. `mud/web/index.html`
and `mud.js` get a mode selector (Middleham or The Gyre). Each mode
keeps its own `localStorage` session ID, because the server reads a
session's domain only once, on that session's first request.

## References

- Full verification log, wire-protocol detail, and open follow-up
  items: `DETAILS.md`
- Source: `v-sekai-multiplayer-fabric/zone-server-h2o`,
  `docs/0003-the-gyre-mud-domain-and-mode-selector.md`. This RFD ports
  that file's content here. Git history in that repo still keeps the
  original file.

## Related

- `rfd/2085-the-gyre-mud-setting-on-the-loot-action-shell`: the design
  RFD this implements the smallest code-side loop for.

## Detail

{{< include DETAILS.md >}}
