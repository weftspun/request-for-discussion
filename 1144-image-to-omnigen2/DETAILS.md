# RFD 1144 details: what loop 2 costs and what it scores

Loop 2 exercises OmniGen2 and EditScore with nothing else in the way, so its
numbers are the ones the plan layers check their quantities against. Both
`fourloops-plan.usda` and `fourloops-etnf.usda` name this file as a source.

Measured on the desk described in `logbook-fourloops-first-runs.md`, which holds
the apparatus and the runs these are lifted from.

## OmniGen2, and what four bits buys

Same input, same seed, 1024 square, 30 steps:

| precision | weights   | peak      | seconds |
| --------- | --------- | --------- | ------: |
| bf16      | 14.75 GiB | 17.14 GiB |     131 |
| NF4       | 4.33 GiB  | 6.72 GiB  |     133 |

Four bits bought memory and cost two seconds. Weights fall to 0.29 of bf16 and
peak to 0.39, while the wall time moves from 131 to 133 seconds, which is inside
the run-to-run spread and should be read as unchanged rather than as slower.

That matters for a 24 GiB desk. At bf16 the peak of 17.14 GiB leaves 6.86 GiB for
everything else in the process; at NF4 the peak of 6.72 GiB leaves 17.28. Loop 2
fits either way and loop 4 does not, which is why the plan carries both rows
rather than only the one it runs.

CLAUDE.md's generated-synthetic condition 5 decides what may be done with the
NF4 row: quantised weights produce no corpus data. So the four-bit form is a way
to fit the loop on this desk, and never a way to make data with it. RFD 1128
reaches the same place for a different model, and records that four bits bought
no speed there either.

## What EditScore costs and returns

RFD 1147 holds it. Every loop scores with EditScore and only loops 2 and 3
propose with OmniGen2, so the scorer's figures belong to the plan rather than to
this loop. `editscoreMatchingOverall`, `editscoreNonsenseOverall`,
`editscorePeakGib512` and `editscorePeakGib1024` all resolve there.
