## Context and problem statement

The `manuals` repo had no branch protection on `main`. Changes landed
by pushing directly or by manually merging pull requests, with no
guarantee that a PR's checks ran against the tip it was about to
join. Two PRs can each pass against an older `main` and then conflict
or break the Quarto build once both land. How should changes reach
`main` so that every merge is reviewable and tested against the tip it
will actually join?

## Decision drivers

- Every change to `main` should arrive through a pull request, not a
  direct push.
- A PR should be validated against the latest `main` before it lands.
- The team is small, so the process should add little ceremony (no
  mandatory second reviewer, no enqueue step).
- The setting should be declarative and recorded, not click-ops
  folklore.

## Considered options

- Leave `main` unprotected (status quo).
- Branch protection requiring a pull request only.
- A repository ruleset requiring a pull request plus a merge queue.
- A repository ruleset requiring a pull request plus strict required
  status checks.

## Decision outcome

Chosen option: a repository ruleset requiring a pull request plus
strict required status checks, because it keeps `main` PR-only and
tests each change against the current tip without forcing a second
reviewer or an enqueue step.

The ruleset targets the default branch with these rules:

- Block branch deletion and non-fast-forward pushes.
- Require a pull request, with `0` required approvals (review is
  allowed, not mandated).
- Require status check `prek`, with
  `strict_required_status_checks_policy` set to `true`, so a PR whose
  branch is behind `main` updates and re-runs its checks before it
  merges.

Alongside the ruleset, the repository sets `delete_branch_on_merge`, so
a merged PR's source branch is removed automatically.

### The merge method

`allow_squash_merge` and `allow_rebase_merge` are both `false`, leaving
`allow_merge_commit` as the only way a pull request can land. Auto-merge
stays enabled; with the other two off it can only produce a merge commit.

This is not a preference for more commits. A split costs CI linearly:
every commit must pass on its own, so a branch of `n` commits is `n`
verifications and not one, paid again on every push while the branch
lives. Against that a split buys understandability — review reads one
idea at a time, and `git bisect` lands on a change small enough to read
rather than on a whole feature.

The trade is real in both directions and it is decided per branch. Most
branches are one idea and should be squashed locally before the pull
request is final; the doc-gate port in `fabric#52` was collapsed from
four commits to one for exactly that reason. A split earns its keep only
when the concerns are independent, as in `fabric#54`, where a new gate
and a documentation correction had nothing to do with each other and
each passed alone.

So the question the setting answers is not how many commits a branch
should have. It is who decides, and when:

- Squashing at merge time decides for every branch, after review, and
  collapses the series that was deliberately kept along with the ones
  that were not. The author already had the cheaper option — `git rebase
-i` before marking the PR ready — and it costs the same CI either way,
  because the squashed branch is verified once as one commit.
- A squash or a rebase also gives the merge a new SHA, so the branch tip
  is not an ancestor of the default branch afterwards. The documented
  post-merge check reads exactly that, and reported three complete merges
  as unmerged in a single day.

The second could be answered by comparing trees instead of commits, and
that change is worth making anyway because history already holds squashed
merges. It does not answer the first.

### Why not a merge queue

The earlier form of this decision required a `merge_queue` rule. The
queue serializes entries and builds each against the branch tip, which
is worth its cost on a repo with enough concurrent PRs that rebasing by
hand becomes the bottleneck. This repo merges documentation changes a
few at a time, and the queue charged for capacity it never used:

- Every merge needs an explicit enqueue step, and the queue snapshots
  the PR head at enqueue time, so a late fix races the merge and can be
  orphaned.
- `gh pr merge --delete-branch` fails while a queue is enabled
  ("Cannot use `-d` or `--delete-branch` when merge queue enabled"), so
  branch cleanup has to move to the repo-level
  `delete_branch_on_merge` setting.
- The `merge_queue` rule names no CI job on its own. A ruleset carrying
  `pull_request` + `merge_queue` and no `required_status_checks` rule
  merges a PR through the queue even when every check on it failed.
  This bit two dependent repos (`taskweft/taskweft`, `taskweft/nif`).

The strict `required_status_checks` policy keeps the property the queue
was there for — a change is tested against the tip it joins — and the
enqueue discipline goes away with it.

## Consequences

- Good: `main` only changes through PRs, and a PR behind the tip
  updates and re-runs its checks before it lands.
- Good: the configuration is captured here and reproducible from the
  ruleset JSON.
- Good: merging is a single `gh pr merge` with no enqueue step and no
  dequeue-to-fix dance.
- Bad: solo edits still need a PR.
- Bad: with `0` required approvals, the rule enforces process but not
  review, so an unreviewed PR can still merge.
- Bad: strict checks re-run on update, so a burst of concurrent PRs
  costs one extra CI round per PR that falls behind, with no batching.

## Confirmation

The ruleset is active (id `17352485`). `gh api
repos/v-sekai-multiplayer-fabric/multiplayer-fabric-manuals/rulesets` lists it, a direct
push to `main` is rejected, and the rule list carries no `merge_queue`
entry:

```sh
gh api repos/<org>/<repo>/rulesets/<id> --jq '.rules[].type'
```

`gh api repos/<org>/<repo>/rulesets/<id> --jq '.rules[] | select(.type
== "required_status_checks")'` returns the rule with the expected job
names and `strict_required_status_checks_policy: true`, and a PR with a
failing check cannot merge.

`gh api repos/v-sekai-multiplayer-fabric/<repo> --jq
.delete_branch_on_merge` returns `true`, and the source branch of a
merged PR no longer exists.

## More information

The ruleset is edited with `gh api -X PUT
repos/<org>/<repo>/rulesets/<id> --input ruleset.json`. The API
replaces the whole rule array, so read the current rules first and send
back every rule to keep, not only the one being changed:

```sh
gh api repos/<org>/<repo>/rulesets/<id> --jq '.rules'
```

Job names to require come from a real PR's checks:

```sh
gh pr checks <PR-number> --repo <org>/<repo>
```

and the status-check rule takes the shape:

```json
{
  "type": "required_status_checks",
  "parameters": {
    "strict_required_status_checks_policy": true,
    "required_status_checks": [{ "context": "<job name from gh pr checks>" }]
  }
}
```

Change the policy by editing the ruleset rather than protecting the
branch through the classic branch-protection API, so the two mechanisms
do not overlap.

Apply the branch-cleanup setting declaratively:

```sh
gh api -X PATCH repos/v-sekai-multiplayer-fabric/<repo> \
  -F delete_branch_on_merge=true
```
