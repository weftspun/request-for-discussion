## Context

`rfd/2045-loot-action-core-loop-mvp-vertical-slice` shipped a playable
shell: a Hub where players gather, an instanced Field room for one
loot-action loop, and five hexagonal cores (Combat, Loot, Presence,
Progression, Budgeter) behind ports. That slice targets SteamVR, one
melee combo, one loot drop, four players.

The Gyre is a proposed setting: a sci-fi, gig-economy-survival MUD
where players are "Sparks" occupying disposable "Frames" on a decaying
station, working contracts to pay down a Debt Clock. The design lives
in `zone-server-h2o` issue #4 and is reproduced here, remapped onto
the existing shell's terms.

## Party composition and tone

Playtester feedback (screen name "cthulhoo," mostly GURPS in the last
15 years, D&D from 3e onward) shapes this revision. Their favorite
campaigns "feel like anime": exploration-led, with far fewer combat
encounters per session than D&D's recommended pacing, run for 2-4
players plus NPC party members.

Apply that directly:

- Party size stays 2-4. A contract board scales its harder contracts
  to whatever party size shows up, rather than assuming a fixed four.
- Rook, Splicer Jax, and other named NPCs are recruitable companions
  for a run, not just vendors. A party of 2 can take a contract sized
  for 4 by bringing one or two NPC companions instead of waiting for
  more players.
- Combat stays the minority activity. Of the nine contracts in the
  catalog below, one (Drone Decommission) is combat, and it is
  avoidable: a stealth or hacking path exists around the drones for a
  party that would rather not fight. The rest are scavenging, repair,
  hacking, delivery, and social/exploration work.
- Exploration carries the session. A room's description, its NPCs,
  and what a player finds there (a Rumor, a piece of station history,
  a side conversation) matter as much as the contract's reward. The
  Session pacing table below spends more of its 120 minutes moving
  through rooms and talking to NPCs than fighting.

## The web target and save data

The Gyre's target client is a website, not the SteamVR build `rfd/0045`
targets. Save data (Debt Clock balance, Frame state, inventory) needs
to persist per player across sessions, tied to a GitHub OAuth login.

This is new client and persistence-adapter work, not a change to the
core reducers. The Progression core (`rfd/0043`) already owns profile
and inventory commits through a port; a web/OAuth build needs a new
adapter behind that port, not a new core. The Combat, Loot, and
Budgeter cores stay unaffected: a text-based web client still issues
the same loot-request and combat-tick events the SteamVR client does,
just through a different front end.

## Mapping The Gyre onto the Hub/Field shell

- The Hub maps to The Under-Market (Splicer's Den, Exchange Plaza,
  Transit Rails) and The Commons (Cycle's End Tavern, Chapel of the
  Backup, Broadcast Row). Players gather, trade, and patch up here
  between contracts, the same role the Hub deck plays in `rfd/0045`.
- A Field instance maps to one contract run. The Tangle, the Sub-Net,
  and the Underhull each host contract-type Field rooms: a scavenge
  check, a hacking check, a short combat encounter. Each contract is
  bounded and returns the player to the Hub, matching the
  Hub-to-Field-to-Hub round trip.
- Contract rewards (chits, Encrypted Bounties, salvage) resolve
  through the loot core's existing first-touch contention.
- The Debt Clock, Frame Integrity, and inventory are profile state
  the progression core commits, the same path the MVP slice's
  inventory delta already uses.
- Only the Drone Decommission contract type uses the combat core,
  reusing the existing timed-hit validation. Every other contract
  resolves through the Loot and Progression cores alone, keeping
  combat the minority path through the content, per "Party
  composition and tone" above.

## World map and zones (room graph)

Six zones, three to four rooms each.

### The Reclamation Wards (spawn zone)

- The Decanting Floor is a freezing, sterile room filled with
  hundreds of suspended Frames. Automated robotic arms attach players
  to their new bodies.
- The Decon Vents are a mandatory exit path where players are blasted
  with harsh chemical foam before being pushed out into the station's
  general population.
- Intake Records is a small office of humming servers where a player
  can review their current Debt Clock balance and Frame warranty
  status.

### The Tangle (scavenging and gathering)

- Collapsed Aeroponics is a humid, rusted dome where modified fungal
  blooms have taken over the old air scrubbers. Players can harvest
  bio-matter here, but risk inhaling corrosive spores.
- The Filtration Sump is a dark, flooded sector where players can
  filter clean water out of the station's waste runoff.
- Scrap Canyon is a collapsed maintenance corridor, floor to ceiling
  in decades of dumped hardware, the station's best salvage and its
  least stable footing.

### The Under-Market (safe zone and hub)

- The Splicer's Den is a makeshift clinic lit by harsh LED strips.
  Players spend chits here to patch their Integrity or install
  unregulated augments.
- Exchange Plaza is a crowded, noisy hub where players pick up
  bounties, trade salvaged tech, and check the current cycle's market
  prices.
- The Transit Rails are the station's rattling internal shuttle line.
  Riding it skips travel time between distant zones, for a small
  chit fare.

### The Sub-Net (the "dungeon")

- Uplink Node Alpha is a physical junction box sparking with loose
  wires. A player with the right augment can plug their Frame
  directly in.
- The Data Sea is a surreal, text-based interpretation of the
  station's intranet. Movement here is instant, but a failed hacking
  check causes direct neural feedback, damaging the player's Spark.
- The Firewall Reef is a maze of self-patching defensive subroutines
  rendered as jagged coral, the station's most valuable data and its
  most aggressive automated defenses.

### The Underhull (hazard zone)

- The Radiation Seam is a cracked section of outer hull venting the
  gas giant's ambient radiation directly into the corridor. Fast
  Integrity drain, fast salvage.
- The Drone Graveyard holds dozens of decommissioned security drones,
  some not fully decommissioned. A slow, tense room, not a rush.
- Airlock Seven is the only working route to the station's exterior.
  A short EVA contract type launches from here.

### The Commons (social zone)

- Other Sparks unwind at Cycle's End Tavern between contracts, a
  source of rumor-board side content and NPC banter.
- The Chapel of the Backup is a quiet room where Sparks who fear a
  bad resleeve pay to store a redundant memory snapshot.
- Broadcast Row is a row of dead advertising screens one enterprising
  Spark reactivated to run a pirate radio station.

## NPCs

- Splicer Jax runs The Splicer's Den, gruff, transactional, quietly
  generous to Sparks who are clearly new.
- Overseer Q-11 is the automated debt-collection voice heard at the
  start and end of every cycle, never hostile, never warm, always
  exact about numbers.
- Rook is a Tangle scavenger who trades salvage tips for a cut of
  whatever the player finds on their first trip.
- The Pirate DJ runs Broadcast Row and drops rumors about which
  zones have good salvage or heavy drone activity this cycle.

## Contract catalog

| Contract            | Zone                         | Type                                                        | Est. time | Reward                     |
| ------------------- | ---------------------------- | ----------------------------------------------------------- | --------- | -------------------------- |
| Scrub the Scrubbers | Collapsed Aeroponics         | Scavenge check                                              | 8-10 min  | Chits + bio-matter         |
| Sump Pump Repair    | The Filtration Sump          | Repair task                                                 | 10-12 min | Chits + Debt Clock dent    |
| Ghost Line          | Uplink Node Alpha → Data Sea | Hacking check                                               | 10-15 min | Chits + Encrypted Bounty   |
| Reef Breach         | The Firewall Reef            | Hard hacking check                                          | 15-20 min | Large Debt Clock dent      |
| Seam Walk           | The Radiation Seam           | Timed salvage/exploration                                   | 8-10 min  | Chits, high Integrity risk |
| Drone Decommission  | The Drone Graveyard          | Short combat, or a stealth/hacking bypass around the drones | 10-12 min | Chits + salvage parts      |
| Rail Courier        | Exchange Plaza → any zone    | Delivery                                                    | 5-8 min   | Small chits, low risk      |
| Signal Boost        | Broadcast Row                | Social/fetch                                                | 8-10 min  | Rumor unlock, small chits  |
| The Long Corridor   | Scrap Canyon → The Underhull | Pure exploration, no check required                         | 10-15 min | Station lore, a Rumor lead |

Seven of these nine contracts resolve without a fight. Drone
Decommission is the one combat-typed contract, and its stealth or
hacking bypass keeps even that one avoidable for a party that would
rather not.

## Entity and item concepts

| Item/entity        | Type            | Description                                                    | Mechanic                                                                                         |
| ------------------ | --------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Memory Drive       | Core equipment  | A heavy, metallic cylinder housing the player's consciousness. | Drops on death. Can be looted, sold, or returned by other players.                               |
| Synapse Coolant    | Consumable      | A pressurized can of foul-smelling gray gel.                   | Restores a moderate amount of Frame Integrity.                                                   |
| Encrypted Bounties | Currency / loot | Datapads filled with stolen corporate secrets.                 | Sold at the Exchange Plaza to pay down the player's debt.                                        |
| Pneumatic Riveter  | Weapon / tool   | A heavy, modified construction tool.                           | Used to pry open sealed crates, or as a slow melee weapon.                                       |
| Backup Snapshot    | Service         | A stored memory copy, purchased at the Chapel of the Backup.   | On Catastrophic Seizure, restores the Spark to its last snapshot state instead of a blank slate. |
| Radiation Tab      | Consumable      | A chalky pill that slows Integrity drain in the Underhull.     | One-time use, single Radiation Seam trip.                                                        |

## Example room description

> **[The Splicer's Den]**
>
> The air is thick with the acrid stench of burning flux and cheap
> synthetic skin. Bundles of fiber-optic cables hang from the
> ceiling, leading to a massive, heavily modified medical chair in
> the center of the room. A flickering display board flashes today's
> rates for Integrity patching and limb alignment. A half-dismantled
> Hauler Frame sits in the corner, its servos clicking in a
> repetitive, broken loop.
>
> _Exits: [North] to Exchange Plaza, [East] to The Transit Rails._
>
> _Interactables: [Splicer Jax], [Medical Vendor], [Scavenge Pile]_

## Session pacing (120 minutes)

| Phase                               | Minutes | Content                                                                                                                 |
| ----------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------- |
| Login and orientation               | 0-10    | Decanting Floor, Decon Vents, Intake Records, first look at the Debt Clock; recruit an NPC companion if under 4 players |
| Loop 1-2 (exploration and scavenge) | 10-40   | Scrub the Scrubbers, The Long Corridor, no combat, teach the loop and the setting                                       |
| Market and downtime                 | 40-55   | Exchange Plaza trades, Splicer's Den patch-up, Cycle's End Tavern rumor pickup, NPC banter                              |
| Loop 3-4 (repair and hacking)       | 55-95   | Sump Pump Repair, Ghost Line, real Integrity risk, still no required combat                                             |
| Closing set piece                   | 95-115  | Reef Breach (a hacking contract, not combat) or Drone Decommission via its stealth bypass                               |
| Wrap-up                             | 115-120 | Turn-in, Debt Clock check, Backup Snapshot purchase before logout                                                       |

A session that skips Drone Decommission entirely, or takes its
bypass, sees zero required combat encounters across the full 120
minutes. A session that takes it head-on sees exactly one.

## Smallest-loop implementation status

`zone-server-h2o` PR #5 lands the smallest real slice of this loop:
two rooms only (Decanting Floor, Splicer's Den), pure exploration, no
items or NPCs. Not the full room graph or contract catalog above;
those stay design, not yet built.

The MUD engine (`mud/guest/mud_guest.cpp`) previously served one
hardcoded setting, Middleham. The PR adds a `domain` boot field
(`"middleham"` default, `"the_gyre"` new) rather than a new engine:
`MiddlehamStateMachine` keeps its Middleham behavior unchanged for the
default domain, and a `gyre_room_templates()` table plus a
`DOMAIN_THE_GYRE` branch in the constructor, `clone_rooms()`, and
`objective_complete()` cover the new one. `mud/web/index.html`/`mud.js`
get a mode selector, one `localStorage` session id per mode.

Verified: a native (non-riscv64) link of `mud_guest.cpp` driving
`mud_boot()`/`mud_step()` through the whole Gyre loop, real narration
text, `objective_complete()` true after both rooms are visited
(`mud/guest/test/gyre_smoke_test.cpp`). The client change (mode
selector, per-domain session id, `domain` field on the wire) was
driven with real Playwright, both Chromium and Camoufox, against a
throwaway local stub, before the real spec (`mud/web/test/gyre.spec.ts`)
was written.

Not verified: a `riscv64-musl` + `libriscv` build/run of the guest
code (no cross toolchain available when this was written). No real
FDB/H2O build or deploy. `gyre.spec.ts` needs a real `MUD_BASE_URL`
deployment to go green, matching `mud.spec.ts`'s own red-first
convention; it has not run against one.

## Open questions

- How does GitHub OAuth login map to a player profile the Progression
  core already models? Whether a GitHub identity becomes the
  profile's primary key, or an added claim on an existing account
  scheme, is undecided.
- What does a web client need from the transport layer that the
  SteamVR client does not, and does it reuse the same WebTransport
  path `zone-server` already speaks, or a separate HTTP/WebSocket
  adapter for browser clients without WebTransport support?
- How do the "dice roll" mechanics for resolving risky actions
  (hacking, scavenging, and similar) work, mechanically, against the
  Combat core's existing timed-hit validation model?
- Whether the Debt Clock and Effort Pips need their own core, or fit
  inside the existing Progression and Budgeter cores, is undecided.
  Default to reusing Progression until a concrete need forces a new
  core.
- How an NPC companion occupies a party slot in the Presence core is
  undecided: a server-driven pseudo-player with its own pose/state,
  or a lighter-weight attachment to the recruiting player's own
  state. The choice affects whether a 2-player party with two NPC
  companions costs the same server resources as a 4-human party.
