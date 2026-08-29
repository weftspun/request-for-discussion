---
title: "RFD 2021: Require pull requests on main"
rfd: "2021"
state: published
scope: repo branch protection and CI gating
---

## Problem

`main` had no branch protection. Pushes landed directly on the
branch. Pull requests merged with no guarantee that their checks ran
against the tip they were about to join.

## Decision

The repository applies a ruleset on the default branch that blocks
direct pushes and branch deletion, requires a pull request (with zero
mandatory approvals), and requires the real CI jobs to pass with a
strict up-to-date policy, so a PR rebases onto the current tip before
it merges. The repository also enables automatic deletion of a merged
pull request's source branch, so merged feature branches do not pile
up.

A merge produces a merge commit. Squash and rebase merging are both
disabled on the repository, so the commits a pull request was reviewed
as are the commits that land, and the branch tip stays reachable from
the default branch afterwards.

Squash the branch by hand where squashing is right. A split is not
free: every commit has to pass CI on its own, so a series of `n` costs
`n` verifications rather than one, and that cost is paid on every push
for the life of the branch. Most branches are one idea and should
arrive as one commit, squashed locally before the pull request is
final.

Keep a split only where the concerns are genuinely independent, and
then it buys understandability the collapse cannot: review reads one
idea at a time, and `git bisect` lands on a change small enough to
hold in the head. That is a judgement about the branch, made by the
person who wrote it.

The setting is about who makes that judgement and when. A squash at
merge time makes it for every branch, after review, and collapses the
series that was deliberately kept along with the ones that were not.
Rebase merging keeps the split but rewrites every SHA, so it breaks
reachability the same way a squash does.

Reachability is what the post-merge check reads. `git log
origin/main..<branch>` reports a correct merge as unmerged whenever the
tip was rewritten, and it did so on three complete merges in one day.
A check that is red on every correct merge is one nobody reads.

A merge queue is not part of the policy. The strict
`required_status_checks` policy covers the same ground at this volume
of changes, without the enqueue step, the snapshot races, and the rules
the queue needed around branch deletion and late fixes.

## References

- Full context, options, consequences, and confirmation: `DETAILS.md`
- Original record:
  `decisions/20260606-require-pr-and-merge-queue-on-main.md`
- `gh api repos/v-sekai-multiplayer-fabric/multiplayer-fabric-manuals/rulesets` (ruleset
  id `17352485`)

## Detail

{{< include DETAILS.md >}}
