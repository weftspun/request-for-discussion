---
title: "RFD 2125: An interactor in another process, and the transport layer that reaches it"
rfd: "2125"
state: discussion
scope: how a RunPod Serverless worker reaches an interactor that holds a model
---

## Problem

`contract-command` says an interactor is a command in and reply bytes out, and
`transport-runpod` supplies one to `rp_worker_run` as a `weft_interactor_t`. The interactor is
therefore linked into the worker binary and called on the job thread.

That is right when an interactor is a function. It is wrong when it holds a model. The
see-through pipeline loads about 14 GB of weights, and linking it into the worker puts three
costs in the wrong place. The load happens inside the process that answers HTTP, so
scale-from-zero pays for it before the first job-take. A job that kills the pipeline takes the
worker's job loop with it, and RunPod records a dead worker rather than a failed job. And two
model processes cannot share one endpoint, because there is one worker binary.

`contract-bus` already has the shape that fixes this. `weft/loop.hpp` is a command loop over
iceoryx2: an interactor subscribes, answers, and publishes on a reply service. What it does not
have is a caller. The only code that ever sent it a command was its own proof program.

## Decision

**The transport layer supplies a bus round trip where it used to supply a function.**
`include/runpod/bus_ask.h` publishes the command, waits for the reply carrying its own request
id, and returns those bytes. It has the signature of `weft_interactor_t::ask`, so
`rp_worker_run` is unchanged above it and there is one job loop rather than two.

The interactor is then an operating-system process, and the three costs move. Weights load once
at start, before any job is taken. A pipeline that dies leaves the worker alive to answer the
job with an error. And the two are separately replaceable, which is what makes an A/B possible
at all.

**Correlation is by request id, and a reply that does not match is dropped.** A bus is
asynchronous, so a reply to a job the worker already gave up on can arrive while it holds the
next one. Answering with it would be a wrong answer rather than a missing one, which is worse.
The id is the 8 bytes `weft/command.hpp` already puts in front of every message, and it is
seeded from the clock so a restarted worker does not reuse ids the interactor is still
answering.

**A dead bus and a slow interactor are different, and the worker treats them differently.** A
send that fails means the interactor is unreachable, so the worker answers the job and asks to
wind down: a worker that cannot reach its interactor is useless and should be replaced. A
deadline that passes means the interactor may still be working, so the worker answers that job
and takes the next one.

**Neither is answered with silence.** `rp_worker_run` posts whatever comes back as the job's
output, so an empty reply would tell a caller nothing about which failure happened. Both are
answered with a reply that names the failure.

## What this does not decide

**One interactor per machine.** `weft/command.hpp` names one command service, so two
interactors on one host would both receive every command and race to answer. Two interactors
therefore mean two containers, which is what `service-see-through` records.

**The bus is unproven on Linux.** `contract-bus`'s command loop has run on Windows against
iceoryx2 v0.9.3 and nowhere else, and `src/port_iox2.cpp` has not run at all. `proof/` covers
the correlation, the deadline and the malformed shapes against canned messages, which is
everything except the bus.

## References

- `contract-bus`, `weft/loop.hpp`: the server half this is the caller for
- `contract-command`, `weft/interactor.h`: the shape `bus_ask` wears
- RFD 2126: the two interactors this was built to compare
