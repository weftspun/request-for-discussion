---
title: "RFD 2012: Amend a PR before it enters the merge queue, not after"
rfd: "2012"
state: abandoned
scope: CI
---

## Problem

Enqueueing a pull request marks its current head commit ready to
merge. The merge queue snapshots that head commit the instant it
enters the queue. A push made after enqueueing can race the merge and
get orphaned. A correction pushed seconds after enqueueing once merged
the earlier commit and orphaned the fix, and the fix then needed a
second PR to land.

## Decision

Do not enqueue a pull request until it is final. Enqueueing
(`gh pr merge --auto`) states that the current commit is ready to merge,
not that the branch is a parking spot for further edits. The merge queue
snapshots a PR's head commit the instant it enters the queue, so a push
made after enqueueing can race the merge and get orphaned.

If a fix is needed after a PR is already enqueued, dequeue it first
(`gh pr merge --disable-auto`), push the fix, then re-enqueue. After any
corrective push to an in-flight PR, verify the PR is still `OPEN`
(`gh pr view <n> --json state`) before assuming the new commit will
merge; a `MERGED` state means the fix was missed and needs its own PR.

This rule was learned the hard way: a correction pushed seconds after
enqueueing merged the earlier commit and orphaned the fix, which then
needed a second PR to land.

## References

- Considered options and confirmation check: `DETAILS.md`
- Original record: `decisions/20260606-amend-pr-before-it-enters-the-queue.md`

## Related

Refines `decisions/20260606-require-pr-and-merge-queue-on-main.md`;
supports `rfd/2015-bounded-llm-steering-queue/index.md`.

## Detail

{{< include DETAILS.md >}}
