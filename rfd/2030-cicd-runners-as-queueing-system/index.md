---
title: "RFD 2030: CI/CD runners operate as a finite queueing system"
rfd: "2030"
state: published
scope: GitHub Actions runner pool operating discipline
---

## Problem

The organization shares one GitHub Actions runner pool, with 14 to 20
runners available at a time. A single Godot push triggers about 20
jobs, and the slowest jobs hold a runner for one to two hours.
Arrivals easily outpace the pool, so a queued job then waits behind
work that may carry no useful information at all.

## Decision

The organization shares one GitHub Actions runner pool, observed at
14 to 20 concurrent jobs, while a single Godot push triggers about 20
jobs and the slowest hold a runner for one to two hours. Arrivals
easily outpace the pool, and a queued job then waits behind work that
may carry no information at all. The project treats the pool as a
finite queueing system and bounds arrivals at the source: it runs two
or three full matrices at a time, batches fixes into fewer pushes,
cancels zero-information runs (duplicate push/PR triggers, runs on
merged or deleted refs, reruns of a known failure whose fix is not yet
on the branch), trims diagnostics to the single job that reproduces a
problem, and admits stale backlog worst-first when utilization is low.
The waste comes from how work is submitted, not from how GitHub
schedules it, so an operating discipline fixes it where a hard
concurrency cap would only block urgent work behind stale work.

## References

- Full context, decision drivers, considered options, the full
  discipline, consequences, and confirmation: `DETAILS.md`
- Original record:
  `decisions/20260611-cicd-runners-as-queueing-system.md`
- `gh run list`, `gh run view --json jobs`

## Detail

{{< include DETAILS.md >}}
