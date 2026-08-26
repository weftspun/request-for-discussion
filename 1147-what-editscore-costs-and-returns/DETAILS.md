# RFD 1147 details: the scorer's cost and its scale

Measured on the desk described in `logbook-fourloops-first-runs.md`, which holds
the apparatus these figures come from. The entry says how the runs were made and
this file says what they returned; re-running them needs the entry.

## What it returns when the instruction matched

| scale max | consistency | a second axis | overall |
| --------: | ----------: | ------------: | ------: |
|      10.0 |         9.2 |           2.0 |    4.29 |

The overall figure is 4.29 out of 10.0, and the spread behind it is the reason
to carry both. Consistency scored 9.2 while the second axis scored 2.0, so a
scorer reporting only the overall would say "middling" about a result that is
excellent on one axis and poor on another. Which axis failed is the actionable
half, and the overall alone discards it.

**The negative control.** A nonsense instruction returns 0.0 overall. That is
what makes 4.29 a measurement rather than an impression: a scorer that cannot
return 0.0 for nonsense is not discriminating, and every score it gives is
consistent with it having read nothing. `editscoreNonsenseOverall = 0.0` in
`fourloops-plan.usda` carries that control beside the quantity it validates.

## What it costs

| configuration  | peak       | seconds  |
| -------------- | ---------- | -------- |
| NF4, 512 x 512 | 6.7506 GiB | 28 to 36 |
| NF4, 1024 x 1024 | 8.6 GiB  |          |

6.7506 GiB is measured; the plan rounds it to 6.75 in `editscorePeakGib512`, and
carries 8.6 as `editscorePeakGib1024`.

The seconds are a range rather than a median, and deliberately. The run-to-run
spread at 512 is wider than the gap between the two OmniGen2 precisions RFD 1144
reports, so a single figure would imply a resolution these runs do not support.

## Why this lives in its own document

Every loop in `fourloops-plan.usda` names EditScore as its `score` stage, and
loop 1 pairs it with the Referee because an image scorer and a body scorer
answer different questions. A figure that four loops depend on belongs beside
none of them in particular.

It was in RFD 1144 first, on the reasoning that loop 2 is the smallest loop
exercising the scorer and so its numbers were the plan's. That reasoning holds
for OmniGen2, which loops 2 and 3 use and loops 1 and 4 do not. It does not hold
for a stage all four share.
