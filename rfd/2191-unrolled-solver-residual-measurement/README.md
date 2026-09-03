# RFD 2191: Unrolled solver residual measurement

**State:** discussion
**Feature:** measure fixed-step Kusudama solver residual vs baselines
**Scope:** the unrolled fit RFD 1122 decided on

## Decision

Measure the residual an unrolled fit reaches after K steps, as a
percentage of stature per `soma_referee.py` convention (a
millimetre is negligible on an adult and disqualifying on a
child), against two baselines: `lbfgs_polish.py` run to convergence
(what the unroll replaces), and K swept from one upward warm-
started from the previous frame at 120 fps. Compute is trivial:
one step is 25.6k MAC against 102 GMAC for a four-view backbone,
0.0006% of the backbone. Waits on RFD 2190 (rig extrinsics
calibration): a residual against an uncalibrated `view` is in
unknown units.

## Problem

RFD 1122 (unrolled Kusudama solver) decided to unroll the descent
into a fixed number of steps with a per-step pairwise-Kusudama
clamp. Whether the residual is good enough was never measured. A
solver shipped without its residual against a baseline is a number
without a floor, which PITFALLS rule 4 refuses. Issue 28 on the
register closed stale.

## References

Original issue: `weftspun/request-for-discussion` issue 28;
`pose-consensus/python/lbfgs_polish.py` (baseline);
`pose-consensus/python/soma_referee.py` (reporting convention).

## Related

RFD 1122 (unrolled Kusudama solver), RFD 2190 (rig extrinsics
calibration; blocks this), RFD 2168 (wholebody detector retract).

This RFD was drafted by an AI and read by a human before it shipped.
