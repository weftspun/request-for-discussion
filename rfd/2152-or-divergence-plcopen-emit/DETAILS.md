# DETAILS: OR-divergence emit in PLCopen SFC

## The PLCopen XML shape

IEC 61131-3 SFC's OR-divergence is a *simultaneous divergence* whose
outgoing transitions have mutually exclusive receptivities. In
PLCopen TC6 XML the shape is:

    <step localId="10" name="find">...</step>
    <transition localId="11">
      <connectionPointIn refLocalId="10"/>
      <connectionPointOut refLocalId="20"/>
      <condition><inline><FBD>... pickup_from_table branch's guard ...</FBD></inline></condition>
    </transition>
    <transition localId="12">
      <connectionPointIn refLocalId="10"/>
      <connectionPointOut refLocalId="21"/>
      <condition><inline><FBD>... unstack branch's guard ...</FBD></inline></condition>
    </transition>
    <step localId="20" name="pickup_from_table">...</step>
    <step localId="21" name="unstack">...</step>
    ... each branch's tail ...
    <transition localId="30">
      <connectionPointIn refLocalId="last_of_pickup"/>
      <connectionPointOut refLocalId="40"/>
    </transition>
    <transition localId="31">
      <connectionPointIn refLocalId="last_of_unstack"/>
      <connectionPointOut refLocalId="40"/>
    </transition>
    <step localId="40" name="mark_done">...</step>

Two things distinguish OR-divergence from AND-divergence in the XML:

1. `AndDivergence` in the compact form emits *one* transition with
   multiple `connectionPointOut` elements (fires all branches at once).
   OR-divergence emits *N* transitions, each with its own guard and
   its own single successor.
2. The convergence side: `AndConvergence` emits one transition with
   multiple `connectionPointIn`s (fires when all branches complete).
   `OrConvergence` emits N transitions each with a single
   `connectionPointIn`, all pointing at the same merged step.

FBD inline bodies apply as everywhere else per RFD 2150 (ST and LD
blocklisted).

## The mutually-exclusive-receptivity gate

An OR-divergence whose branch receptivities are not mutually
exclusive is a design defect: two branches fire at once, the SFC
enters a state IEC 60848 does not specify, and the runtime's
behaviour is implementation-defined. RFD 2149's Lean analyser flags
this as a concurrent pair (the two branch steps co-occur in some
reachable marking). The emitter reads that flag on the source
compact GRAFCET before emitting; if any pair of branches from the
same OR block appears, `emit/1` refuses with a pointer at the pair.

**This turns the analyser from advisory into a load-time gate**, which
is what RFD 2149 promised. RFD 2152 lands the interlock the promise
implied.

## Multi-step branches

A branch with more than one step (`|> A → B → C |<`) needs a linear
sub-chain per branch, and only the *last* step of the sub-chain
connects to the OR-convergence. The stage 1 emitter refuses
multi-step branches; stage 2 admits them once the walker in
`lib/taskweft/openplc/plcopen.ex` can nest, mirroring what
`Taskweft.Grafcet.lower/1`'s OR block tracking already does.

## Interaction with the HTN lower

`Taskweft.Grafcet.lower/1` already synthesises `m_choose_after_<parent>`
methods with per-branch checks for OR blocks (RFD 2148 stage 1). The
PLCopen emitter reads the *source* compact GRAFCET, not the lowered
HTN, so this RFD does not touch `lower/1`. The two lower directions
(HTN and PLCopen) stay independent, each with its own staging.

## Verification

- `blocks_get_or.grafcet.jsonld` under `test/fixtures/grafcet/`
  emits an SFC with two mutually exclusive transitions out of `find`,
  two convergence transitions into `mark_done`, and no `<ST>` /
  `<LD>` / `<IL>` bodies (the BLOCKLIST rows still hold).
- A hand-authored non-exclusive fixture is refused by the emitter
  with the offending pair cited.
- The emitted XML validates against the PLCopen TC6 schema.

## Staging within this RFD

| stage | scope |
|---|---|
| 1 | single-step branches, mutually exclusive receptivities, `|>` and `|<` markers, blocks_world's `get` fixture |
| 2 | multi-step branches (linear sub-chains between markers) |
| 3 | nested OR blocks (`|>` inside `|>`) |
| 4 | mixed OR + AND divergence in the same chart |

The staging matches RFD 2148's own; each stage ships with its own
round-trip test in `test/taskweft/openplc/plcopen_test.exs` and its
own refusal control (a chart that would need the *next* stage fails
with a pointer at that stage).
