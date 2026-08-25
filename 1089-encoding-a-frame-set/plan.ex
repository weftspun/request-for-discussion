# The solved plan for `cineform_delivery`, WRITTEN BY HAND rather than produced by the
# planner. RFD 1025 forbade that and retracted the rule on 2026-08-25: taskweft serves
# `plan` over MCP, this desk was not reaching that host mid-task, and a domain nobody can
# run is worse than a plan nobody generated. Regenerate from the planner when it is
# reachable, and delete this note when that happens.
#
# The order below is the only order the guards permit, which is why it was writable by hand:
# each action reads what the one before it set. `verify_delivery` is last and is the only
# step that sets `delivered`, so a run that stops early leaves the goal false.
#
# Checked with `Code.string_to_quoted/1`. That is a parse and not a proof: the guards decide
# at run time, and a step order they forbid fails there.
defmodule Weftspun.CineformDelivery.Plan do
  use Taskweft.DSL

  @source "cineform_delivery"

  # How this plan was made, as a constant rather than a sentence. A reader greps for
  # @origin_hand_written and finds every plan that has not been through the planner; a
  # sentence has to be read, and the next writer phrases it differently.
  @origin_hand_written :hand_written
  @origin_generated :generated
  @origin @origin_hand_written

  @plan [
    %{task: "check_conventions", args: ["rig", "posed"]},
    %{task: "adopt_measured_facing", args: ["facing_deg"]},
    %{task: "render_frames", args: ["subject"]},
    %{task: "pack_stream", args: []},
    %{task: "encode_clip", args: []},
    %{task: "write_citation", args: []},
    %{task: "verify_delivery", args: []}
  ]
end
