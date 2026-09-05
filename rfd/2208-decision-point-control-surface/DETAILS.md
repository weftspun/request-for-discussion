# RFD 2208: Decision-point control surface — details

## The two roles the same planner plays

`tw_plan(domain, skip_state)` returns a sol-tree — a nested
structure whose root is the current Goal and whose leaves are
concrete actions the planner can commit to. Between root and
leaves are `TwMethod` alternatives: at any node where the domain
declares multiple decompositions, the planner enumerates the ones
whose guards pass.

Two callers, two projections of that tree:

- **Coordination caller** (RFD 2205's fleet plugin) takes the
  first leaf whose `actor == <caller cn>` and returns it as an
  assignment. The caller does not need to see alternatives; it
  needs one commitment.
- **Player-facing caller** (this RFD) takes the immediate children
  of the current Goal — the top-level alternatives — and renders
  them as a menu. When the player picks, the planner re-runs at
  the depth *below* that pick to surface the next menu.

Same tree, two projections. The tree walker on the player-facing
side stops one level shallower than on the coordination side.

## Concrete example

A Vow's opening beat surfaces the alternatives the planner
computed at the Vow's root:

    /journey   1. Undertake an Expedition  →  6-waypoint direct route
               2. Undertake an Expedition  →  8-waypoint detour
    /scene     3. Set a Scene              →  station bar (Sojourn)
    /oracle    4. Ask the Oracle           →  reveal a danger

Player picks 1 (direct route). The planner re-runs at the
Expedition's root and surfaces:

    1. Face Danger      (action-die vs. Wits, +1 supply on strong)
    2. Secure Advantage (action-die vs. Edge, +1 momentum on strong)
    3. Sojourn early    (rest at a station, +health/spirit/supply)

Player picks 1. The demo rolls action-die vs. two challenge-dice,
reads the CC-BY-4.0 outcome text from the SQLite fixture, and
surfaces the outcome's menu — which for a weak hit is:

    On a weak hit — choose one:
    1. Pay -1 supply
    2. Mark a debility
    3. Endure harm (-1 health)

Player picks 3. State updates. Planner re-runs. Next menu.

The loop is: (menu) → pick → (roll if stochastic) → (outcome
menu) → pick → state update → (next menu).

## Test hooks

`starforged-core.js` exposes the pure functions that drive the
menu: `contextMoves(scene, vow) → [{kind, act, args, label}, …]`,
`rollStarforged(stat, adds, rng)`, `applyOutcome(state, act,
outcome, args) → newState`. Each is tested in isolation under
`docs/test/` with a seeded RNG so every scenario reproduces.

## Verification

- **Negative control** (rule 2): a demo revision that quietly
  narrows the menu to one option when only one alternative's
  guards pass fails a Playwright assertion that at least one
  scene in the test scenarios surfaces ≥3 options. A degenerate
  planner passes this test only by returning a real menu.
- **Autobattler drift check.** The QA runner asserts that
  `starforged.js` contains no code path that calls `applyOutcome`
  without a preceding user event (click, key). A planted defect
  that fires `applyOutcome` on a timer fails this.
- **Roll-after-commit ordering.** A Playwright scenario asserts
  that the outcome text becomes visible only *after* the player's
  button click, never before.

## Related retractions

The autobattler shape was never shipped in this workspace; the
retirement note is on the *isekai-crossroads* reflex-executor
demo whose buttons (`arrive`, `traveler_arrived`, `wait`,
`depart`, `__night`) fired a hard-coded reflex chain. That chain
survived as fallback for non-planner scenes; the primary game
loop is planner-driven per this RFD.

This RFD was drafted by an AI and read by a human before it shipped.
