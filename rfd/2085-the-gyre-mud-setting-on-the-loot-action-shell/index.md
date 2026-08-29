---
title: "RFD 2085: The Gyre — a MUD setting on the loot-action core-loop shell"
rfd: "2085"
state: discussion
scope: zone-server-h2o game content, web client
---

Players awaken as "Sparks" — digitized human consciousnesses legally owned by a defunct hyper-corporation. They are currently downloaded into "Frames," which are cheap, mass-produced synthetic worker chassis. Abandoned on The Gyre, a massive, slowly failing ring-station orbiting a toxic gas giant, players must survive cycle by cycle. They take on grueling localized contracts, scavenge for parts to prevent their Frames from seizing up, and try to buy their digital freedom from the station's automated debt-collection algorithms.

## Decision

The Gyre is content for a game and is not a new game architecture.

We defined a loop with two areas: a Hub area and a Field area.
Players start in the Hub area. They travel to a Field area to do one
task. Then they return to the Hub area.

In The Gyre, two Hub locations stand in for the Hub area: the
Under-Market and the Commons. Each contract stands in for a Field
task. A contract is one of these: a scavenge run, a hack run, an
exploration run, or (sometimes) a short combat run.

We also defined five core systems: Budgeter, Combat, Loot,
Presence, and Progression. These five core systems stay as they are.
The Gyre adds new content on top of them: rooms, non-player characters
(NPCs), items, and a story frame called the Debt Clock.

Players explore more than they fight. Combat
happens less often than in a typical Dungeons & Dragons session. A
party has 2 to 4 players. If a
party has fewer than 4 players, NPC companions can fill the empty
spots.

## References

- Room graph, NPCs, contract catalog, item table, session pacing,
  party/tone detail, implementation status, and open questions:
  `DETAILS.md`
- Implementation: `zone-server-h2o`

## Related

- `rfd/2045-loot-action-core-loop-mvp-vertical-slice`: defines the
  Hub/Field loop and the five core systems that The Gyre reuses.
- `rfd/2028-hexagonal-core-ports-adapters`,
  `rfd/2043-hexagon-progression-core`: describe the shape a future
  web/OAuth save adapter would follow.

## Detail

{{< include DETAILS.md >}}
