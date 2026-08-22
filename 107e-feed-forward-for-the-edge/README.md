# RFD 107e: Unroll the descent, do not replace it

**State:** discussion
**Feature:** edge deployment of the wholebody chain
**Scope:** `3-interactor/rf-detr-cpp`, `4-entities/anny-pose-retarget-work`

## Problem

RFD 107a's chain has six stages: three feed-forward graphs, and three descent
loops that an inference accelerator cannot compile.

The obstacle is control flow rather than precision. `lbfgs_polish.py` uses a
strong-Wolfe line search, a loop whose trip count depends on values, and `Loop`
and `If` are what an edge compiler refuses. Its `float64` follows from that same
file's `tolerance_grad=1e-10`, an offline target rather than an inference one.

An earlier draft answered by replacing the fit with a learned student, which
gives up the property the parametric model exists for: `soma_referee.py` states
that a parametric model cannot represent an impossible skeleton, and nothing in
a regressor's architecture forbids one.

## Decision

Unroll the descent into a fixed number of steps, keeping the forward we own.

**Clamp every step to the Kusudama cone.** `swing-twist-kusudama` gives joint
limits checked in Lean 4 against Godot, and a clamp is `Clip`, which compiles.
The unrolled graph therefore still cannot emit an unreachable pose.

**Warm-start from the previous frame**, so the step count stays small.

**Compile the backbone with `num_windows=1`.** Measured: it parses and
`num_windows=2` does not. It costs 1.35x wall-clock and needs retraining.

**Give the face camera the resolution and starve the body cameras.** One device
holds four streams at 120 fps only if they differ.

**Report the residual as a percentage of stature**, as `soma_referee` does.

See `DETAILS.md` for the rig budget, the unrolled cost, and what is unmeasured.
