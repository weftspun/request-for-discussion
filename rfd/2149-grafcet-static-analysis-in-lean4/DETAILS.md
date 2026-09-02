# DETAILS: GRAFCET static analysis in Lean 4

## Two analyses now, one later

AGRAFE's tool ships three: structural (step reachability), structural
(pairwise concurrency), and abstract interpretation of variable
domains. This RFD closes the first two and stages the third.

**Reachability.** The set of step ids that appear in some marking
reachable from the initial marking by simultaneous-firing IEC 60848
semantics. Implemented as a fuel-bounded BFS through the firing graph
in `SFC.reachableSteps`. Fuel is a parameter; a real deployment
supplies `2 ^ |steps|` as the state-space upper bound.

**Pairwise concurrency.** The set of `(a, b)` step-id pairs (ordered
by name to avoid duplicates) that co-occur in some reachable marking.
`SFC.concurrentPairs`. This is what surfaces an OR-divergence with
non-exclusive receptivities: the two branches show up as a concurrent
pair, which is a chart bug the author should see.

**Abstract interpretation.** Variable domain analysis over internal
variables. Staged; the SFC types carry the fields (`Step.storedTarget`,
receptivity `V.<var>` atoms), the analysis itself is empty. Landing
this needs either a Lean port of an Apron-style domain library
(interval, octagon, polyhedron) or a Z3 bridge; neither is a taskweft
gate today, so the RFD closes on structural analysis and leaves the
abstract-interpretation stage on the roadmap.

## Firing semantics

`Receptivity` has three constructors: `trueR`, `stepActive`, `andR`.
That covers the compact GRAFCET DSL's supported receptivity fragment
(AND of step-activity atoms). `V.<var>` atoms are conservatively
`true` in the current firing predicate; a sound over-approximation
for reachability (a step reachable under unrestricted variables is
reachable under any restriction). Abstract interpretation replaces
this with a real domain check.

`SFC.fire` is simultaneous-firing IEC 60848: every enabled transition
fires at once, sources come out of the marking, targets go in. The
result is `eraseDups`ed because the union may put a step in twice
(one transition adds it, another already had it there).

## Why Lean

Two reasons over "just port to Elixir".

**Proof.** The port opens the door to proving `reachableSteps` sound
and complete against the semantics: `s ∈ SFC.reachableSteps sfc` iff
there is a firing sequence from the initial marking that puts `s` in
some marking. Those theorems land in `Theorems.lean`; they are the
value-add over the Java tool, which asserts them rather than proving
them.

**C ABI, no runtime.** Lean 4 compiles to C, links as a static or
shared library, and imposes no runtime BEAM or JVM. That is the
minimum interface a NIF can pull; the fully-linked NIF is one
`.so`/`.dylib` and has no Apron and no Z3 in its transitive closure.

## The C ABI

`c_src/grafcet_static.h`:

    char *grafcet_static_analyse(const char *sfc_json);
    void  grafcet_static_free(char *buf);

Ownership: caller frees. The reply is a null-terminated UTF-8 JSON
string. Success shape:

    {"reachable": ["init", "find", "pickup_from_table",
                   "unstack", "mark_done"],
     "concurrent_pairs": [["pickup_from_table", "unstack"]]}

Error shape:

    {"error": "reason"}

The stub returns `{"error":"stub","reason":"...","see":"rfd 2144"}`
until the Lean-produced shared library replaces it.

## Elixir NIF

Modelled on `3-interactor/taskweft-nmm-personas/c_src/weft_bus_nif.cpp`
and `7-service/spot-broker/c_src/store_bus_nif.cpp`. Loads
`libgrafcet_static.dylib`, calls `grafcet_static_analyse`, hands the
JSON string back as an Elixir binary. Runs on a dirty CPU scheduler
because the BFS is CPU-bound and unbounded in the fuel argument.

Exposed at `Taskweft.Grafcet.Static.analyse/1` in the taskweft
project; called from the loader when a `.grafcet.jsonld` document
lands, so a chart with an unreachable step or an unintended
concurrent pair refuses to load.

## Repo manifest

`taskweft-grafcet-static` is a first-class checkout, listed in
`.repo/manifests/default.xml` at `3-interactor/taskweft-grafcet-static`
alongside `taskweft` and `taskweft-nmm-personas`. Remote is
`weftspun`. The three sit on the interactor side of the hexagon per
CLAUDE.md's "one live goal manifest" rule.

## Verification

- `lake build` in `3-interactor/taskweft-grafcet-static` builds the
  Lean library and the smoke-test executable.
- `./.lake/build/bin/grafcet_static` runs the blocks_get_or fixture
  (RFD 2148's OR-divergence worked example) and prints:

      reachable: [init, find, pickup_from_table, unstack, mark_done]
      concurrent pairs: [(pickup_from_table, unstack)]

  The concurrent pair correctly flags that the two OR branches share
  the same receptivity; an author-visible symptom of a chart where
  the AGRAFE tool would say "not mutually exclusive".
- When the Lean-produced shared library lands, the Elixir NIF's
  `analyse/1` returns the same JSON, wired into taskweft's loader
  gate.

## Staging table

| construct | state |
|---|---|
| Reachability | landed in Lean, real C body wired via Lean `@[export]` |
| Pairwise concurrency | landed in Lean, real C body wired |
| Elixir NIF | `Taskweft.Grafcet.Static.analyse/1` wired, 2/2 tests green |
| Abstract interpretation | typed in the SFC, analysis empty; needs a Lean interval/octagon domain or a Z3 bridge |
| Soundness theorems | `Theorems.lean` empty; next stage |
| Loader gate | not wired; needs a `Taskweft.JSONLD.Loader` hook after the compact GRAFCET parse |

## Unaffected by RFD 2150's FBD-target pivot

RFD 2150 changed the *emitter's target* from PLCopen SFC to PLCopen
FBD (state machine encoded as SR flip-flops). This analyser reads the
*compact GRAFCET input* to the emitter, not its output, so nothing
here changes. Reachability and pairwise concurrency are graph queries
on the SFC step/transition structure carried in the input JSON-LD;
that structure is unchanged by whatever the emitter ships downstream.

A separate analyser reading the FBD output (to catch defects
introduced during the FBD encoding; a mis-wired reset input, a
missing first-scan latch) is a follow-on. This one stays authoritative
for the input side.
