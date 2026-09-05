# RFD 2208: Decision-point control surface for planner-driven demos

**Decision-point control surface:** retracted 2026-09-05,
superseded by [RFD 2210](../2210-atelier-godot-web-shipping-surface/)
(with L2 fanout at [RFD 2215](../2215-one-binary-two-heads/) —
the "one binary, two heads" architecture folds this control-surface
decision into the game-head shape). The planner-surfaces-menu vs
planner-drives-actor distinction stays authoritative; it is now
described in RFD 2215 as the game-head's control loop rather than
as a standalone RFD.

**State:** abandoned
**Feature:** the planner in a player-facing demo surfaces the set
of currently-legal moves and the player picks one; the planner is
not allowed to drive the actor forward on its own
**Scope:** any browser demo where a Taskweft (RECTGTN) planner
runs the game loop for a player-controlled character; today's
concrete case is the Starforged play surface in
`7-service/service-sqlar-cas/docs/`

## Decision

The planner's per-turn output is the *decision menu*, not the
*next action*. Concretely:

1. `taskweft.wasm`'s `plan()` returns every `TwMethod` alternative
   whose guards currently pass — the natural output shape when a
   Goal has multiple ways forward. RECTGTN's `alternatives` array
   *is* the decision menu.
2. The demo renders these as buttons (slash-command shape, numeric
   hotkeys 1-9). The player picks one. That pick becomes the
   actor's next action.
3. Stochastic moves separate the choice from the roll. The player
   commits to a move; then the demo rolls, reads the outcome text
   from the fixture, and surfaces the *outcome*'s next menu. The
   player never rolls in the dark; the menu shows what the move
   can produce before they commit.
4. On outcomes that themselves branch ("on a weak hit, choose one:
   pay -1 supply, mark a debility, endure harm"), the branches
   are sub-methods with their own alternatives. A weak hit produces
   a fresh menu; the player picks the price.
5. After the player's pick and any roll, the planner re-runs on
   the resulting state to produce the next menu.

## What is banned

- An **autobattler** shape where the planner picks the next action
  and the player watches. Even if the planner picks well, the
  player has no agency, and the demo reads as a rigged cutscene.
- A **single-choice menu** shape where the planner narrows to one
  option and the button is "continue". A one-option menu is the
  autobattler with an extra click.
- **Hidden rolls** where the demo rolls before showing the menu
  and only surfaces one branch. The player must see what the move
  can produce before committing.

## Problem

A planner that returns a single next step is a natural fit for a
coordination surface (RFD 2205's fleet-domain use case — Bao
returns one Task per `creds` read). A planner that returns a
single next step for a player-facing character is an autobattler;
the player is a spectator. The Starforged play surface needed the
planner in a different role — as the *legal-moves oracle* — and
this RFD writes down which role a demo picks.

The two roles use the same planner. What changes is which layer
of the planner's output the caller consumes: the coordination
surface consumes the winning action, and the player-facing surface
consumes the menu of alternatives above it.

## Non-goals

Not a spec for the coordination surface (that is RFD 2205). Not a
spec for player-facing UX (buttons vs. cards vs. numeric hotkeys
is per-demo). Not a rule about how many alternatives a menu
carries — that is domain content.

## Related

- RFD 2205 (Taskweft in Bao) — the coordination-surface use case
  where the planner returns one action.
- RFD 2206 (video-call VRM portrait) — the visual convention the
  player-facing surface pairs with.
- Codebase: `7-service/service-sqlar-cas/docs/starforged.js` and
  `starforged-core.js` — the reference implementation.

This RFD was drafted by an AI and read by a human before it shipped.
