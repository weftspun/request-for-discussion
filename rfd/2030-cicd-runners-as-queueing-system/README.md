# RFD 2030: Cicd runners as queueing system

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The organization shares one GitHub Actions runner pool across every
repository, observed at roughly 14–20 concurrent jobs. A single push
to the Godot fork triggers a matrix of about 20 jobs, and the slowest
of them (sanitizer and Windows builds) hold a runner for one to two
hours. Pushes arrive from fix branches, pull requests, merge commits,
reruns, and even archive repositories that carry the same workflow
files. When arrivals outpace the pool, every queued job waits behind
work that may carry no information at all. How does CI work get
admitted to the runner pool so that signal arrives quickly?

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
