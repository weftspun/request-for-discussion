# DETAILS: GRAFCET as taskweft's authoring surface

## The compact profile

Every construct is a 60848 element under a short local name, expanded
by JSON-LD `@context` to the AGRAFE IRIs so the same file round-trips
into their model without a second document.

Steps are entries in an ordered `S` array; position implies a `Link`
to the next entry unless a divergence intervenes. Sigils at position
zero mark the step kind: `""` or omitted = `Step`, `^` = `InitialStep`,
`%` = `MacroStep`, `#` = `EnclosingStep`. Divergence markers are their
own entries: `&>` opens an `AndDivergence` to the named siblings,
`&<` closes an `AndConvergence` from the named steps into the next
entry; `|>` / `|<` are the OR forms; `!>` is a `ForcingOrder` writing
another chart's marking. Per step: `[name, when, do, t]`; `when` is
the transition's `Receptivity` (boolean expression over `X.<step>`
step activities and `V.<var>` internal variables), `do` is a stored
`Action` (assignment or emit), `t` is the transition's time delay.

The reference file, `.github/plans/weftspun-build.grafcet.jsonld`, is
13 lines of `S` against the 38 lines of hand-authored HTN it lowers to.

## The mapping table, in full

Every taskweft feature lands on one 60848 construct. Nothing on the
right extends the standard.

| taskweft feature | IEC 60848 construct |
|---|---|
| boolean state flag | step activity `X_i` or internal boolean |
| action's `pointer/set` on a flag | `Step` with `stored` action |
| guard `math/eq` over a flag | `Receptivity` on the upstream transition |
| sequential subtasks | `Link` chain |
| fan-in / fan-out | AND-convergence / AND-divergence |
| `duration: "PT1H"` on an action | `timeDelayed` receptivity `t/X_i/1h` |
| single-alternative skip-if-done method | subsumed by step activity |
| parameterised action, finite static domain | grounded via `MacroStep` template with `for` field |
| parameterised action, domain known at plan time | internal variables + dispatch pattern |
| method with N receptivity-selected alternatives | `OrDivergence` with N exclusive receptivities |
| method with N search-selected alternatives | `ForcingOrder` rewinds the sub-chart on downstream failure |
| task-network goal | `InitialStep` marking + terminal `EnclosingStep` |
| HTN decomposition hierarchy | `MacroStep` per method |
| ETNF tuple state, ref into `capabilities` | interned integer id in an internal variable |
| plan trace with bindings | firing trace with timestamps |

The **grounding-scale gate** in `Taskweft.Grafcet` refuses any lowering
that would produce more than N ground steps for a `%macro`-with-`for`;
the author moves it to the dispatch-variable pattern instead. This is
what keeps "no HTN feature lost" from turning into "unreadable chart".

## Round-trip semantics

`raise(lower(g)) == g` when `g` is canonical; `lower(raise(h))` is
idempotent for any well-formed `h`. Canonicalisation drops
transitively-redundant guards: the reference HTN gates `a_oracle` on
`/done/lake` although `ingest`, `embedder`, and `slat` each already
gate on `lake`. The compact form drops those inherited receptivities;
the second pass is a fixed point. `mix test test/taskweft/grafcet_test.exs`
under `3-interactor/taskweft` passes 4/4, exercising both directions.

## Transport: `2-contract/bus` + CBOR + zstd

Stdio JSON is **blocklisted** for the Elixir↔Python wire when the
peer is a language-external library (nmm2 here). The workspace's
canonical transport is `2-contract/bus`'s DYNAMIC byte-slice command
bus (iceoryx2 shared memory, 8-byte request-id envelope). Python
reuses `weft_harness.Bus`'s `serve` loop verbatim; Elixir speaks the
same wire through a new NIF at
`3-interactor/taskweft-nmm-personas/c_src/weft_bus_nif.cpp`, modelled
on `spot_broker/c_src/store_bus_nif.cpp` + `bus/proof/command_publisher.cpp`.

The bus caps at 128 KiB per message. The projected 128-agent nmm2
obs is 1,233,911 bytes as JSON, 433,346 as CBOR, and **4,821 bytes
as CBOR+zstd**; 250× smaller than JSON, well under the ceiling. Both
sides speak the same envelope: 1-byte tag (`Z` = zstd-compressed CBOR,
`C` = plain CBOR) followed by the body. Python uses `cbor2` + `zstandard`;
Elixir uses `:cbor` + `:ezstd`.

An obs that outgrows even zstd should move to a Snapshot pub/sub on
its own service, coordinated by the command bus. The bus README's
own recommendation for bulk payloads. Not needed yet.

## Continuous-time scheduling

Personas run in real time, not turn-based. Two independent wall-clock
loops via `TaskweftNmmPersonas.Scheduler`:
`:timer.send_interval(persona_period_ms, :persona_tick)` refreshes
each agent's latest intended action into an ETS mailbox at
`--persona-hz` Hz; a second timer at `--env-hz` reads the latest
fragments and steps the env. Only the last intended action per agent
between env steps is submitted. Both rates are fixed integer Hz. No
elastic scheduling.

`persona_hz >= 10` is a hard contract; the Scheduler raises
`ArgumentError` below it. Effective rates are recorded per episode
and per trace row (`wall_us` monotonic timestamp).

Measured on a live 128-agent nmm2 episode, target 30/10 Hz:

    persona 26.14 Hz (target 30), env 8.2 Hz (target 10), 1.951s

BEAM `send_interval` jitters ~10-20% under real work; target above
the floor with headroom, not at it. Three `mix test` cases guard this:
one asserts effective persona rate ≥10 Hz on a real episode, one
asserts the Scheduler refuses `persona_hz < 10`, one exercises the
MaskScore row shape.

## MaskScore row shape

One row per (persona, episode, dimension). Field names track the
EditScore schema in RFD 1173's MASKSCORE.md verbatim:

| field | meaning |
|---|---|
| `key` | `nmm2_{persona}_seed{S}_ep{N}_{hash}`; stable, dedup-safe |
| `instruction` | "play Neural MMO 2 as a {persona} persona for N ticks" |
| `input_state` | `seed={S}` |
| `conditioning_image` | null |
| `output_traces` | list of per-tick JSONL shard paths |
| `scores` | `[survival_fraction, avg_health_norm]` |
| `task_type` | `survive` |
| `dimension` | `instruction_following` / `consistency` / `overall` |

Scores are populated by game-native reductions of the trace itself,
not by Mitsuba render-and-compare. The RFD 1173 metric doesn't apply
to a text-shaped game; the schema stays faithful (same fields, same
three dimensions), the *content* of `scores` is the domain-specific
reduction. A future generator that produces game-shaped outputs would
plug directly into the same schema.

## The three personas

Each persona is one `.grafcet.jsonld` file under `personas/`. Steps
resolve to Elixir dispatch functions in
`lib/taskweft_nmm_personas/persona.ex` that consume the current
observation, mutate persona memory, and return an action fragment.

| persona | step chain |
|---|---|
| forager | sense → seek_water → gather_food → wander → end_turn |
| hunter | sense → heal_or_flee → seek_target → attack_or_move → end_turn |
| trader | sense → sell_surplus → buy_cheap → wander → end_turn |

Persona differentiation lives entirely in the step list. Adding a
persona is one new `*.grafcet.jsonld` file plus (if it introduces new
step names) new entries in the dispatch table.

## The higher-level constructs are in scope

Scope of the DSL is whatever taskweft's HTN can express. Every
construct taskweft uses today rounds-trips through the lowering
compiler; anything else stays out of the DSL.

taskweft's HTN uses parameterised actions (`params: [:block]`),
methods with N alternatives selected by `check` clauses, method
decomposition, and task-network goals. Those land on the following
60848 constructs, staged by build order:

1. `|>` / `|<` (`OrDivergence` / `OrConvergence`) for a method with N
   receptivity-selected alternatives. **Implemented.** Round-trip
   test in `taskweft/test/taskweft/grafcet_test.exs` exercises a
   two-alternative fixture.
2. `%macro` (`MacroStep`) for method decomposition and parameter
   grounding over a finite static domain. Staged next.
3. `#enclosing` (`EnclosingStep`) for a task-network goal or a
   macro-scoped sub-plan. Staged after `%macro`.
4. `!>` (`ForcingOrder`) for HTN backtracking on downstream failure
   of a chosen alternative. Staged last; harder to make round-trip
   idempotent because the rewound branch can be authored two ways.

Each staged construct ships with its own round-trip test and its own
worked fixture. The grounding-scale gate applies to `%macro` with
`for`.

## What is deliberately not here

1. RL training. Personas are hand-authored SFCs; the traces populate
  a reward-model dataset, they do not train the personas.
2. A wall-clock scheduler that varies the persona rate at runtime. The
  contract is stable Hz, no jitter.
3. Bulk-payload transport. Obs stays under 128 KiB via CBOR+zstd; a
  Snapshot pub/sub is the next-step answer if that budget is ever
  exceeded.

## Verification

1. `mix test` in `3-interactor/taskweft/`; 4/4, the compact GRAFCET
  round-trip on `weftspun-build.grafcet.jsonld` and canonicalisation
  on `weftspun-build.domain.jsonld`.
2. `mix test` in `3-interactor/taskweft-nmm-personas/`; 3/3, the
  MaskScore row count, the persona rate floor, the Scheduler refusal.
3. Live episode over `2-contract/bus` with real 128-agent nmm2:
  `ep0 seed42: persona 26.14 Hz (target 30), env 8.2 Hz (target 10),
  1.951s` and `9 MaskScore rows -> traces/maskscore.jsonl`.
4. The traces are `traces/maskscore.jsonl` + `traces/maskscore.parquet`
  (parquet via duckdb reading the JSONL sibling; no pyarrow dep).
