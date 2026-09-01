#!/usr/bin/env python3
"""Gate: no merged PR's head branch is left as an orphan on the remote.

`delete_branch_on_merge` handles the common case; this gate is the backstop for
a branch pushed to after its PR merged. A branch with commits ahead of the
default is not treated as an orphan, because someone kept working.

Run --self-test.
"""
from __future__ import annotations

import json
import subprocess
import sys

EXCLUDED = frozenset({"main", "gh-pages"})
DEFAULT_REPO = "weftspun/request-for-discussion"


def is_orphan(branch, merged, opened, ahead, excluded=EXCLUDED):
    if branch in excluded:
        return False
    if branch not in merged:
        return False
    if branch in opened:
        return False
    if ahead > 0:
        return False
    return True


def remote_branches(repo):
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}/branches", "--paginate",
         "--jq", ".[].name"],
        capture_output=True, text=True, check=True)
    return [b for b in out.stdout.splitlines() if b]


def pr_heads(repo, state):
    out = subprocess.run(
        ["gh", "pr", "list", "--repo", repo, "--state", state,
         "--limit", "500", "--json", "headRefName"],
        capture_output=True, text=True, check=True)
    return {p["headRefName"] for p in json.loads(out.stdout)}


def ahead_of(repo, base, branch):
    out = subprocess.run(
        ["gh", "api",
         f"repos/{repo}/compare/{base}...{branch}", "--jq", ".ahead_by"],
        capture_output=True, text=True, check=True)
    return int(out.stdout.strip() or "0")


def run(repo, base):
    branches = remote_branches(repo)
    merged = pr_heads(repo, "merged")
    opened = pr_heads(repo, "open")
    orphans = []
    for b in sorted(branches):
        if b in EXCLUDED or b not in merged or b in opened:
            continue
        ahead = ahead_of(repo, base, b)
        if is_orphan(b, merged, opened, ahead):
            orphans.append(b)
    if orphans:
        print(f"FAIL {len(orphans)} merged PR(s) with an orphaned head branch:")
        for b in orphans:
            print(f"       {b}")
        print()
        print("     delete each with: git push origin --delete <branch>")
        return 1
    print(f"ok   {len(branches)} branch(es), no orphans.")
    return 0


def self_test():
    ex = frozenset({"main"})
    m = {"x", "y", "z", "main"}
    o = {"y"}
    checks = [
        ("a merged branch with no open PR and no ahead commits is an orphan",
         is_orphan("x", m, o, 0, ex) is True),
        ("a merged branch reopened as an open PR is not an orphan",
         is_orphan("y", m, o, 0, ex) is False),
        ("a merged branch with commits ahead of main is not an orphan",
         is_orphan("z", m, o, 5, ex) is False),
        ("a branch with no PR at all is not an orphan",
         is_orphan("n", set(), set(), 0, ex) is False),
        ("main is never an orphan",
         is_orphan("main", m, o, 0, ex) is False),
        ("an open-only branch is not an orphan",
         is_orphan("y", set(), o, 0, ex) is False),
    ]
    print()
    for name, ok in checks:
        print(f"  {'ok' if ok else 'FAIL':4} control: {name}")
    bad = sum(1 for _, ok in checks if not ok)
    print(f"  {len(checks) - bad} of {len(checks)} controls fired.")
    return 1 if bad else 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    repo = argv[argv.index("--repo") + 1] if "--repo" in argv else DEFAULT_REPO
    base = argv[argv.index("--base") + 1] if "--base" in argv else "main"
    return run(repo, base)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
