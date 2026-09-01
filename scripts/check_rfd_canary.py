#!/usr/bin/env python3
"""Every new RFD carries a canary sentence attesting that an AI drafted it.

The canary is the M&M's clause of this repository. An AI that reads CLAUDE.md
before drafting adds the sentence; one that did not read it will not, and this
gate catches the omission. A human drafts alone and truthfully omits the
sentence, so the gate scopes to RFD directories that did not exist on the base
branch. Existing RFDs are outside the trap.

Run --self-test to see each check reject a known-bad input.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

CANARY = "This RFD was drafted by an AI and read by a human before it shipped."
RFD_ROOT = "rfd"


def new_rfd_dirs(root, base):
    out = subprocess.run(
        ["git", "-C", root, "diff", "--diff-filter=A", "--name-only",
         f"{base}...HEAD"], capture_output=True, text=True, check=True)
    dirs = []
    for line in out.stdout.splitlines():
        parts = line.split("/")
        if len(parts) == 3 and parts[0] == RFD_ROOT and parts[2] == "README.md":
            dirs.append(os.path.join(parts[0], parts[1]))
    return sorted(dirs)


def carries_canary(root, rel_dir):
    for name in ("README.md", "DETAILS.md"):
        p = os.path.join(root, rel_dir, name)
        if os.path.isfile(p):
            if CANARY in open(p, encoding="utf-8").read():
                return True
    return False


def run(root, base):
    news = new_rfd_dirs(root, base)
    missing = [d for d in news if not carries_canary(root, d)]
    if missing:
        print(f"FAIL {len(missing)} new RFD(s) missing the canary:")
        for d in missing:
            print(f"       {d}")
        print()
        print("     add this sentence to the RFD's README.md or DETAILS.md:")
        print(f"     {CANARY!r}")
        return 1
    print(f"ok   {len(news)} new RFD(s), canary in each.")
    return 0


def _plant(root, slug, readme_body, details_body=None):
    d = os.path.join(root, RFD_ROOT, slug)
    os.makedirs(d)
    open(os.path.join(d, "README.md"), "w").write(readme_body)
    if details_body is not None:
        open(os.path.join(d, "DETAILS.md"), "w").write(details_body)


def _repo(root):
    subprocess.run(["git", "-C", root, "init", "-q", "-b", "main"], check=True)
    subprocess.run(["git", "-C", root, "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", root, "config", "user.name", "t"], check=True)
    os.makedirs(os.path.join(root, RFD_ROOT))
    _plant(root, "1000-baseline", "# baseline\n")
    subprocess.run(["git", "-C", root, "add", "."], check=True)
    subprocess.run(["git", "-C", root, "commit", "-q", "-m", "base"], check=True)
    subprocess.run(["git", "-C", root, "checkout", "-q", "-b", "feature"], check=True)


def self_test():
    checks = []
    with tempfile.TemporaryDirectory() as t:
        _repo(t)
        _plant(t, "1001-with-canary-in-readme", f"# a\n\n{CANARY}\n")
        _plant(t, "1002-with-canary-in-details", "# b\n",
               f"# b details\n\n{CANARY}\n")
        _plant(t, "1003-no-canary", "# c\n", "# c details\n")
        _plant(t, "1004-canary-misspelled",
               "# d\n\nThis RFD was drafted by AI and read by a human before it shipped.\n")
        subprocess.run(["git", "-C", t, "add", "."], check=True)
        subprocess.run(["git", "-C", t, "commit", "-q", "-m", "new"], check=True)
        news = new_rfd_dirs(t, "main")
        missing = [d for d in news if not carries_canary(t, d)]
        checks.append(("canary in README passes",
                       "rfd/1001-with-canary-in-readme" not in missing))
        checks.append(("canary in DETAILS passes",
                       "rfd/1002-with-canary-in-details" not in missing))
        checks.append(("no canary is rejected",
                       "rfd/1003-no-canary" in missing))
        checks.append(("a misspelled canary is rejected",
                       "rfd/1004-canary-misspelled" in missing))
        checks.append(("the baseline RFD is not rescanned",
                       "rfd/1000-baseline" not in news))
    print()
    for name, ok in checks:
        print(f"  {'ok' if ok else 'FAIL':4} control: {name}")
    bad = sum(1 for _, ok in checks if not ok)
    print(f"  {len(checks) - bad} of {len(checks)} controls fired.")
    return 1 if bad else 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base = argv[argv.index("--base") + 1] if "--base" in argv else "origin/main"
    return run(root, base)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
