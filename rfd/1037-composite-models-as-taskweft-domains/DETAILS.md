# RFD 1037 details: the shape, type rules, the solved plan, replanning, the five

## The shape

A domain is a module with `use Taskweft.DSL` and module attributes.

| Attribute    | Holds                                          |
| ------------ | ---------------------------------------------- |
| `@name`      | The domain name.                               |
| `@variables` | A map of `name => %{type:, init:}`. The state. |
| `@actions`   | Primitives. `params`, `bind`, and `body`.      |
| `@methods`   | Compound tasks. `params` and `alternatives`.   |
| `@todo_list` | The goal. A call, a `goal`, or a `multigoal`.  |

A body step is `%{eval: %{…}}` for a guard, or
`%{pointer_set: "/p", value: v}` for an effect. A guard reads state
with `%{pointer_get: "/p"}`.

A problem is a second module. It sets `@source` to the domain name,
it overrides the `@variables` keys it cares about, and it carries its
own `@todo_list`.

## Type rules that catch a writer out

`type` is mandatory on each variable, and the vocabulary comes from
glTF Interactivity. There is no `:string` type. A stage name, a file
handle, and a format are each `:ref`, which is an opaque value
compared for equality.

There is no `:enum` type either. A named class is capability data, and
it belongs in the top-level `capabilities` key.

## The solved plan is a file

Call `plan` once, and write the result to `plan.ex` beside the domain.
The model image then reads that file, and a cold start needs no planner
and no network.

Write it in the same DSL, and not as JSON. One language across the
domain, the problem, and the plan means one formatter and one parse
check.

Regenerate `plan.ex` when the domain changes, and never edit it by
hand. A hand-edited plan can hold a step order the guards forbid,
which is the failure this whole RFD exists to stop.

**RETRACTED, 2026-08-25: a plan may be written by hand.** The paragraph
above stays as written because it names a real hazard. The rule it drew
from that hazard is withdrawn.

What the rule cost was measured the first time it was applied. A domain
for the CineForm delivery, RFD 1137, was written and checked with
`Code.string_to_quoted/1`, and then no plan could be produced, because
the planner serves over MCP at a host this desk was not going to reach
mid-task. The domain sat unusable beside a skill that told a reader to
run it. A rule that turns a reachable deliverable into an unreachable
one costs more than the defect it prevents.

So a hand-written `plan.ex` is permitted until a pattern appears across
enough domains to encode generically. What does not change is the
checking: the plan is real Elixir and must parse, the domain's guards
still hold at run time, and a hand-written plan that violates one fails
there rather than passing quietly. Say in the file which way it was
made, and regenerate from the planner once it is reachable.

## Replanning is the payoff

`plan` takes `plan_json` and `fail_step`. A caller that loses a stage
replans from that step, and it keeps the work before it.

That is the reason a composite is a domain. A script cannot do it.

## The five composites

| Model id                       | Networks | RFD  |
| ------------------------------ | -------: | ---- |
| seethrough_layer_decomposition |        9 | 0044 |
| weftspun_image_to_world        |        2 | 0049 |
| lingbot_map_environment_scan   |        2 | 0050 |
| voxhammer_text_mesh_editing    |        2 | 0047 |
| voxhammer_image_mesh_editing   |        2 | 0048 |

Each domain lives with its model, and not here. RFD 1000 keeps one
source per design. The See-Through pair in
`0044-seethrough-layer-decomposition/` is the worked example,
because it is the largest of the five.
