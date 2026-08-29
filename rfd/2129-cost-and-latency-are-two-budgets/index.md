---
title: "RFD 2129: Cost and latency are two budgets in seconds, ratcheted against variance"
rfd: "2129"
state: discussion
scope: how a service records what it costs and how long it takes
---

## Problem

Cost is reduced by batching. Latency is reduced by not batching. The two pull in opposite
directions, so a single number that claims to measure "performance" hides which one was spent.
A change that batches and is reported as faster is reporting the wrong axis, and a latency win
bought by shrinking a batch is a cost regression nobody priced.

A worse failure is available, and this project committed it. Budgets were recorded for the
see-through service before any engine existed: 1.195 seconds of latency and 0.184 seconds of
cost, measured on a live endpoint where every job was answered by the settings gate or by a
missing-weights error. Those were floors on a path that decomposed nothing. The gate was green,
the numbers were precise, and they measured the absence of the work. `CLAUDE.md` already names
this failure: a check that reports is worse than no check, because it reads as coverage.

## Decision

**Two budgets, in SI seconds, never netted against each other.** `seconds/seconds.json` holds
`latency_seconds` and `cost_seconds`. `seconds/ratchet.py` refuses to trade one for the other:
a halved cost does not license a slower job. Seconds because the ledger's unit is the SI second
and a git timestamp is in seconds, so nothing is a conversion anybody has to trust.

**A floor may go down or hold. It may never go up.**

**The comparison is against variance, not against a point.** A single measurement fluctuates,
so a floor set from one run fails on noise and then gets switched off, which is worse than
having no gate. Each floor keeps its sample. The comparison is in log space, because a duration
is positive and right-skewed, and the floor moves only when the difference clears two standard
errors of the difference. The same threshold applies in both directions, so the gate is no
easier to please than to trip, and a run inside the noise leaves the floor exactly where it was.

**A floor is set by the first measurement of a system that works, and not before.** This is the
correction to the failure above, and it is Gall's law read the right way round: a ratchet starts
from a simple system that works. Until one exists there is nothing to ratchet, and an empty
floor is the honest record. Both budgets are empty today, and `working` records what they will
be measured against: upstream's pipeline, its weights on the network volume, one 1280-pixel
image in, a layered PSD with nine named layers out, 171.26 seconds on an RTX 4090 by the
program's own clock.

**A timing comes from the program that did the work.** Never from a clock kept elsewhere. This
project has read a normally-progressing run as hung, killed it twice, and reported a
super-linear blow-up that did not exist.

**A floor is replaced when what it measures changes, not added to.** When an engine lands, the
numbers above are deleted rather than kept beside the new ones. A gate carried across a
replacement is a test that only passes for the thing that was removed.

## References

- `CLAUDE.md`, "Checks": a check that reports is worse than no check
- Gall's law: a complex system that works evolved from a simple system that worked
