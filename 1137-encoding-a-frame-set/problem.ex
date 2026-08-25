# The problem this domain is run against: one subject, its rig, and the facing measured off
# that rig rather than assumed.
#
# `@source` names the domain and the overrides are only the variables this run decides.
# Everything else keeps the domain's own init, which is what makes a problem readable: the
# diff between a run and the domain is the run.
defmodule Weftspun.CineformDelivery.Problem do
  use Taskweft.DSL

  @source "cineform_delivery"

  # The subject and the rig this run names, as constants for the same reason the domain's
  # are: they are :ref values, compared for equality, and a misspelt one would simply never
  # match.
  @subject_anny_rest_pose :anny_rest_pose
  @rig_rest_skel_npz :rest_skel_npz

  @variables %{
    "subject" => %{type: :ref, init: @subject_anny_rest_pose},
    "rig" => %{type: :ref, init: @rig_rest_skel_npz},
    # False here, and true for a fitted subject. A posed rig has its gaze and feet away from
    # the chest, which is a stance and not a defect, so only the witness-agreement check is
    # relaxed. Scale, up and the two mirror witnesses still run.
    "posed" => %{type: :bool, init: false},
    # 270.0 is ANNY at rest, measured two ways that agree to 0.0 degrees. A fitted subject
    # carries its own: 345.9 for the hv_1 fit, 72.7 for the hv_2 fit.
    "facing_deg" => %{type: :float, init: 270.0},
    "frames_expected" => %{type: :int, init: 96}
  }

  @todo_list [
    %{task: "deliver_set", args: ["subject", "rig", "posed", "facing_deg"]},
    %{goal: %{"delivered" => true}}
  ]
end
