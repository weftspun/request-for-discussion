# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Gate: a changed source file may not climb the comment-density ladder.

Run: check_comment_ladder.py [--base HEAD] [--baseline] [--self-test]
"""

import argparse
import os
import statistics
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comment_density import density, is_source  # noqa: E402

FROZEN = ("rfd/2", "changelog/", "data/")

RUNGS = (0.05, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40)
ENTRY = 0.10
MIN_LINES = 100


def rung_of(ratio):
    """The lowest rung at or above ratio, or None if it is off the top."""
    for r in RUNGS:
        if ratio <= r + 1e-9:
            return r
    return None


def git(repo, *args):
    out = subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True)
    return out.stdout if out.returncode == 0 else None


def renames(repo, base):
    out, m = git(repo, "diff", "--name-status", "-M", base) or "", {}
    for line in out.splitlines():
        f = line.split("	")
        if len(f) == 3 and f[0].startswith("R"):
            m[f[2]] = f[1]
    return m


def at_ref(repo, ref, path, moved=None):
    text = git(repo, "show", "%s:%s" % (ref, path))
    if text is None and moved and path in moved:
        text = git(repo, "show", "%s:%s" % (ref, moved[path]))
    return text


def changed(repo, base):
    names = set()
    for args in (("diff", "--name-only", base),
                 ("diff", "--name-only", "--cached"),
                 ("ls-files", "--others", "--exclude-standard")):
        names.update((git(repo, *args) or "").split())
    return sorted(f for f in names if is_source(f) and not f.startswith(FROZEN))


def tracked(repo):
    return [f for f in (git(repo, "ls-files") or "").split()
            if is_source(f) and not f.startswith(FROZEN)]


def read(repo, path):
    try:
        with open(os.path.join(repo, path), encoding="utf8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return None


def measure(path, text):
    return density(text, os.path.splitext(path)[1])


def check(repo, base, verbose=True):
    rows, failures = [], []
    moved = renames(repo, base)
    for path in changed(repo, base):
        now = read(repo, path)
        if now is None:
            continue
        n_com, n_code, n_ratio = measure(path, now)
        if n_com + n_code < MIN_LINES:
            continue
        before = at_ref(repo, base, path, moved)
        if before is None:
            ceiling, was = ENTRY, None
        else:
            b_com, _, was = measure(path, before)
            rung = rung_of(was)
            if rung is None:
                rung = was
            # Adding a comment cannot raise density; the rung is slack for deletions.
            ceiling = rung if n_com <= b_com else min(was, rung)
        ok = n_ratio <= ceiling + 1e-9
        rows.append((ok, path, n_ratio, was, ceiling))
        if not ok:
            failures.append((path, n_ratio, ceiling, was))
    if verbose:
        if not rows:
            print("no source files changed against %s" % base)
        for ok, path, ratio, was, ceiling in rows:
            print("  %-4s %-48s %5.1f%%  was %6s  rung %4.0f%%"
                  % ("ok" if ok else "FAIL", path, ratio * 100,
                     "new" if was is None else "%.1f%%" % (was * 100), ceiling * 100))
    return len(rows), failures


def baseline(repo):
    vals = []
    for path in tracked(repo):
        text = read(repo, path)
        if text is None:
            continue
        com, code, ratio = measure(path, text)
        if com + code >= MIN_LINES:
            vals.append((ratio, path))
    if not vals:
        print("no source files of %d+ lines" % MIN_LINES)
        return 1
    vals.sort()
    only = [v for v, _ in vals]
    print("  %d files of %d+ non-blank lines" % (len(vals), MIN_LINES))
    print("  floor %.1f%% (%s)" % (only[0] * 100, vals[0][1]))
    print("  median %.1f%%   p90 %.1f%%   max %.1f%% (%s)"
          % (statistics.median(only) * 100, only[int(len(only) * 0.9)] * 100,
             only[-1] * 100, vals[-1][1]))
    for r in RUNGS:
        n = sum(1 for v in only if rung_of(v) == r)
        print("    rung %2.0f%% %-9s %d" % (r * 100, "<- entry" if r == ENTRY else "", n))
    print("    off the top         %d" % sum(1 for v in only if rung_of(v) is None))
    return 0


def _fixture(repo, name, comments, code_lines=180):
    body = "".join("# note %d\n" % i for i in range(comments))
    body += "".join("x%d = %d\n" % (i, i) for i in range(code_lines))
    with open(os.path.join(repo, name), "w", encoding="utf8") as fh:
        fh.write(body)


def _run(repo, *args):
    subprocess.run(["git", "-C", repo] + list(args), capture_output=True)


def self_test():
    """Seven controls. Four must reject known-broken input."""
    results = []
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as repo:
        _run(repo, "init", "-q")
        _run(repo, "config", "user.email", "gate@example.com")
        _run(repo, "config", "user.name", "gate")
        _fixture(repo, "a.py", 40)       # 40/220 = 18.2%, rung 20%
        _run(repo, "add", "-A")
        _run(repo, "commit", "-qm", "base")

        _fixture(repo, "a.py", 60)       # 60/240 = 25.0%, above its rung
        results.append(("a file padded past its rung is rejected",
                        any(f[0] == "a.py" for f in check(repo, "HEAD", False)[1])))

        _fixture(repo, "a.py", 43)       # 43/223 = 19.3%, inside the rung but up from 18.2%
        results.append(("a comment added inside the rung is rejected",
                        any(f[0] == "a.py" for f in check(repo, "HEAD", False)[1])))

        _fixture(repo, "a.py", 40, 220)  # 40/260 = 15.4%, code added, comments untouched
        results.append(("a file whose density falls is accepted",
                        not check(repo, "HEAD", False)[1]))

        _fixture(repo, "a.py", 40, 170)  # 40/210 = 19.0%, deletion inside the rung
        results.append(("deleting code inside the rung is accepted, comments untouched",
                        not check(repo, "HEAD", False)[1]))

        _fixture(repo, "a.py", 40, 120)  # 40/160 = 25.0%, deletion past the rung
        results.append(("deleting code past the rung is rejected, comments untouched",
                        any(f[0] == "a.py" for f in check(repo, "HEAD", False)[1])))

        _fixture(repo, "a.py", 40)
        _fixture(repo, "new.py", 40)     # new at 18.2%, entry rung is 10%
        _run(repo, "add", "-A")
        results.append(("a new file above the entry rung is rejected",
                        any(f[0] == "new.py" for f in check(repo, "HEAD", False)[1])))

        os.remove(os.path.join(repo, "new.py"))
        _fixture(repo, "ok.py", 18)      # new at 9.1%, under the entry rung
        _run(repo, "add", "-A")
        results.append(("a new file under the entry rung is accepted",
                        not check(repo, "HEAD", False)[1]))

        _fixture(repo, "twelve.py", 22)
        _run(repo, "add", "-A")
        _run(repo, "commit", "-qm", "twelve base")
        _fixture(repo, "twelve.py", 22, 120)
        results.append(("deleting code past the 12%% rung is rejected",
                        any(f[0] == "twelve.py" for f in check(repo, "HEAD", False)[1])))

    bad = sum(1 for _, got in results if not got)
    for name, got in results:
        print("  %-4s control: %s" % ("ok" if got else "FAIL", name))
    print("  %d of %d controls fired." % (len(results) - bad, len(results)))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--base", default="HEAD")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.baseline:
        return baseline(args.repo)
    if args.self_test:
        return self_test()

    n, failures = check(args.repo, args.base)
    print()
    if failures:
        for path, ratio, ceiling, was in failures:
            print("%s is %.1f%% comments, above the %.0f%% rung it %s."
                  % (path, ratio * 100, ceiling * 100,
                     "sits on" if was is not None else "enters at"))
        print("Move the reasoning into the commit message.")
        return 1
    print("%d changed source file(s) within their rung." % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
