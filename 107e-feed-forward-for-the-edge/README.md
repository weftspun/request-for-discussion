# RFD 107e: The descent stages are what block the edge

**State:** discussion
**Feature:** edge deployment of the wholebody chain
**Scope:** `3-interactor/rf-detr-cpp`, `4-entities/anny-pose-retarget-work`

## Problem

RFD 107a's chain recovers a body from a picture in six stages, and the question
was whether it fits into 8 GB chunks across USB accelerators, ten available.
It does not, and memory is not the reason. The chain partitions by kind rather
than by size. Three stages are feed-forward graphs an inference part runs, and
three are descent loops and mesh operations it cannot run at any size.
`lbfgs_polish.py` solves in `float64`, and the part carries INT8.

## Decision

Replace the descent stages with a student trained on our own renders.

**Buy no inverse model.** Multi-HMR is CC-BY-NC-SA and fails twice. Sapiens is
denied already. SAM 3D Body restricts fields of use.

**Supervise from the corpus that exists.** `identities` and `pose_rotations`
are authored relations keyed to `renders`, so a regressor needs no new labels.

**Keep the 3x2 rotation.** A quaternion double-covers, a 3x3 carries a
derivable column, and both objections hold for a network output.

**Measure the cost against LBFGS.** What removing descent costs decides whether
to deploy, and a number without a baseline decides nothing.

**Measure the error correlation with the keypoint head.** One corpus trains
both, so their errors can agree, which is what ended the estimator panel.

## Related

RFD 107a gives the renderer this depends on, and carries the retraction this
decision forces. RFD 101c gives the licence gate that denied the three above.

See `DETAILS.md` for the stage table, the part, and what the student costs.
