# RFD 1030: See-Through component models

**State:** published
**Feature:** layer decomposition

## Decision

Name each component here. Record its base model, its role, and its
memory.

See `DETAILS.md` for the component table, the two runtimes, and why
bf16 is the ceiling while GGUF is the floor.

**WITHDRAWN 2026-08-29 as a deployment plan, kept as a component map.**
RFD 1166 dropped See-Through from the candidate ranking on licensing:
the checkpoints named below state no licence, and the depth component
derives from an OpenRAIL++-M model. The table remains accurate about
what the project is made of and is no longer a plan to run it.

## Problem

The `seethrough_layer_decomposition` entry names one task. The task
runs nine models. One catalog row hides that fact.

## Related

RFD 1006 records the layer decomposition design. RFD 1019 selects the
same ggml runtime for the Elixir core. RFD 1026 carries the single
catalog row that this RFD breaks down.
