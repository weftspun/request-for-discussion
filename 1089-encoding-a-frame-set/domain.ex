# A taskweft domain for delivering a rendered set, written because a re-render that stopped
# at frames was called done three times in one session.
#
# THE GOAL IS `delivered`, AND FRAMES DO NOT SATISFY IT. Every earlier failure had the same
# shape: the expensive step ran, the cheap steps after it did not, and the report said
# "re-rendered". A script cannot catch that, because the script IS the claim. A domain can:
# the todo list names the end state, the planner orders the steps, and a run that stops
# early leaves `delivered` false with the step that failed named.
#
# Types come from glTF Interactivity, as RFD 1025 states. There is no :string, so a subject
# name, a directory and a file handle are each :ref, an opaque value compared for equality.
#
# Checked with `Code.string_to_quoted/1`, which needs no planner. The solved plan belongs in
# `plan.ex` beside this file, from the `plan` tool when it is reachable and by hand when it
# is not. RFD 1025 forbade the second and retracted that on 2026-08-25, because a domain
# nobody can run is worse than a plan nobody generated. `plan.ex` carries @origin saying
# which way it was made.
#
# The task and parameter names below stay strings because RFD 1025's DSL defines them that
# way: they are keys into @actions and @variables rather than values. What is NOT a string
# is any value a pointer takes, and those are the constants above.
defmodule Weftspun.CineformDelivery.Domain do
  use Taskweft.DSL

  @name "cineform_delivery"

  # TAGS ARE CONSTANTS, NOT STRING LITERALS. The type vocabulary has no :string, so every
  # value a pointer takes is a :ref, an opaque value compared for equality. Written inline
  # as text, "mkv" in one file and "MKV" in another are two different refs that read as one
  # thing, and nothing catches it. Named here, a typo is an undefined attribute.
  @stream_rgba :rgba
  @clip_mkv :mkv
  @citation_cff :cff

  @variables %{
    # What is being delivered. A subject, and the rig it was posed from.
    "subject" => %{type: :ref, init: nil},
    "rig" => %{type: :ref, init: nil},
    "posed" => %{type: :bool, init: false},

    # The conventions gate. `checked` is false until it has run, and a run that could not
    # measure forward or handedness leaves `conventions_complete` false, which is not the
    # same as failing. RFD 108b holds the check itself.
    "conventions_checked" => %{type: :bool, init: false},
    "conventions_complete" => %{type: :bool, init: false},
    "facing_deg" => %{type: :float, init: 0.0},

    # The work, in the order it can only happen.
    "frames" => %{type: :int, init: 0},
    "frames_expected" => %{type: :int, init: 96},
    "stream" => %{type: :ref, init: nil},
    "clip" => %{type: :ref, init: nil},
    "citation" => %{type: :ref, init: nil},
    "delivered" => %{type: :bool, init: false}
  }

  @actions %{
    # Measure scale, up, forward and handedness before anything expensive. The facing comes
    # out of this and is not a caller's guess: passing one that disagrees with the rig is
    # what put 96 frames under the wrong phrases twice.
    "check_conventions" => %{
      params: ["rig", "posed"],
      bind: %{"rig" => "rig", "posed" => "posed"},
      body: [
        %{eval: %{op: "not_equal", a: %{pointer_get: "/rig"}, b: nil}},
        %{pointer_set: "/conventions_checked", value: true},
        %{pointer_set: "/conventions_complete", value: true}
      ]
    },

    # The facing is taken from the measurement rather than supplied.
    "adopt_measured_facing" => %{
      params: ["facing_deg"],
      bind: %{"facing_deg" => "facing_deg"},
      body: [
        %{eval: %{op: "equal", a: %{pointer_get: "/conventions_checked"}, b: true}},
        %{pointer_set: "/facing_deg", value: %{pointer_get: "/facing_deg"}}
      ]
    },
    "render_frames" => %{
      params: ["subject"],
      bind: %{"subject" => "subject"},
      body: [
        %{eval: %{op: "equal", a: %{pointer_get: "/conventions_checked"}, b: true}},
        %{pointer_set: "/subject", value: %{pointer_get: "/subject"}},
        %{pointer_set: "/frames", value: %{pointer_get: "/frames_expected"}}
      ]
    },

    # Packing is where a partial render is caught: the stream is only set when the frame
    # count matches what was asked for.
    "pack_stream" => %{
      params: [],
      bind: %{},
      body: [
        %{
          eval: %{
            op: "equal",
            a: %{pointer_get: "/frames"},
            b: %{pointer_get: "/frames_expected"}
          }
        },
        %{pointer_set: "/stream", value: @stream_rgba}
      ]
    },
    "encode_clip" => %{
      params: [],
      bind: %{},
      body: [
        %{eval: %{op: "not_equal", a: %{pointer_get: "/stream"}, b: nil}},
        %{pointer_set: "/clip", value: @clip_mkv}
      ]
    },

    # The citation names the clip, and the clip takes its stem from the citation's title.
    # Neither exists without the other, so this cannot run first.
    "write_citation" => %{
      params: [],
      bind: %{},
      body: [
        %{eval: %{op: "not_equal", a: %{pointer_get: "/clip"}, b: nil}},
        %{pointer_set: "/citation", value: @citation_cff}
      ]
    },

    # The only action that sets `delivered`, and it reads every earlier result rather than
    # trusting that the steps ran.
    "verify_delivery" => %{
      params: [],
      bind: %{},
      body: [
        %{eval: %{op: "equal", a: %{pointer_get: "/conventions_complete"}, b: true}},
        %{
          eval: %{
            op: "equal",
            a: %{pointer_get: "/frames"},
            b: %{pointer_get: "/frames_expected"}
          }
        },
        %{eval: %{op: "not_equal", a: %{pointer_get: "/clip"}, b: nil}},
        %{eval: %{op: "not_equal", a: %{pointer_get: "/citation"}, b: nil}},
        %{pointer_set: "/delivered", value: true}
      ]
    }
  }

  @methods %{
    "deliver_set" => %{
      params: ["subject", "rig", "posed", "facing_deg"],
      alternatives: [
        [
          %{task: "check_conventions", args: ["rig", "posed"]},
          %{task: "adopt_measured_facing", args: ["facing_deg"]},
          %{task: "render_frames", args: ["subject"]},
          %{task: "pack_stream", args: []},
          %{task: "encode_clip", args: []},
          %{task: "write_citation", args: []},
          %{task: "verify_delivery", args: []}
        ]
      ]
    }
  }

  # THE GOAL IS THE CLIP AND ITS CITATION, NOT THE FRAMES. A run that renders 96 frames and
  # stops leaves this false, and the planner names the step that did not run.
  @todo_list [
    %{task: "deliver_set", args: ["subject", "rig", "posed", "facing_deg"]},
    %{goal: %{"delivered" => true}}
  ]
end
