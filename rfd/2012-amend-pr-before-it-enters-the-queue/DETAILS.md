# Details

## Context and Problem Statement

The merge queue captures a PR's head commit the moment its checks pass
and it is enqueued. While drafting the gitassembly tag MADR, a
correction was pushed to the PR branch seconds after enqueueing; the
queue had already snapshotted the earlier commit, so it merged the draft
and orphaned the fix. The correction had to land as a second PR. How
should a late fix to an in-flight PR be sequenced so it is not lost to
the queue?

## Decision Drivers

- A pushed correction must be the commit that actually merges.
- Avoid a follow-up PR that exists only to redo a missed fix.
- Keep the cost of the rule near zero for the common case (no late fix).

## Considered Options

- Push the fix and assume the queue picks up the new tip (status quo
  that failed).
- Confirm the PR is still `OPEN` after the corrective push, before
  relying on it.
- Dequeue the PR, push the fix, then re-enqueue.

## Consequences

- Good: the commit that merges is the one intended, with no orphaned
  fixes.
- Good: no redundant follow-up PRs to reapply a missed correction.
- Bad: a small habit of checking state or dequeuing adds a step when
  editing a PR that is already in flight.

## Confirmation

A late fix to an enqueued PR is preceded by a dequeue or followed by an
`OPEN` state check; the merged commit on `main` contains the fix, with
no follow-up PR that only reapplies it.

## More Information

This refines the merge queue policy
(`decisions/20260606-require-pr-and-merge-queue-on-main.md`) and is the
work-in-progress discipline the bounded steering queue
(`decisions/20260606-bounded-llm-steering-queue.md`) relies on: one
finished concern per PR, merged before the next.
