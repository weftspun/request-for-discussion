#!/usr/bin/env python3
"""Trope density did not rise. Same shape as check_comment_ladder.py: a
changed prose file may not gain trope hits per non-blank line beyond what it
already had.

The tells are the ones the prose-detrope subagent removes most often — the
list is deliberately narrow, because a wide scanner false-positives on
legitimate prose and teaches the writer to route around the gate rather
than to think. Each tell has a rationale so a later reader can revise the
list rather than deleting a rule they no longer understand.

Scope: `rfd/*/README.md`, `rfd/*/DETAILS.md`, `logbook/*.md`. Working
agreements (`CLAUDE.md`, `BLOCKLIST.md`, `PITFALLS.md`, `KEYPOINTS.md`) are
out — they carry retractions and named tells verbatim; a gate on them
would catch itself.

    python scripts/check_tropes.py                              # report only
    python scripts/check_tropes.py --base origin/main           # fail on rise
    python scripts/check_tropes.py --self-test
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# One regex per tell, chosen from the subagent's own report language.
TELLS = {
    # An em-dash between clauses is the highest-signal AI-writing tell.
    # A range dash inside a word (day 12–14) is a hyphen-minus and does
    # not match; the required whitespace on both sides is deliberate.
    "em_dash_join": re.compile(r"\s[-—][-—]?\s"),
    # A comma-separated triad that opens with "in three ways", "for two
    # reasons", "on four counts" and similar is the counting-announcement.
    "counting_announcement": re.compile(
        r"\b(in|for|on)\s+(two|three|four|five|six)\s+(ways|reasons|counts|things|senses)\b",
        re.I,
    ),
    # Reasoning-leak: "the reason X is Y is that", "the whole point is that",
    # "what makes X ... is". These are the sentences the subagent tightens
    # into "X because Y" or "X: Y".
    "reasoning_leak": re.compile(
        r"\b(the reason .+? is that|the whole point .+? is that|what makes .+? is)\b",
        re.I,
    ),
    # "the X that Y" as a pompous copula for "X Y": "the check that proves"
    # rather than "the check proves". Narrowly scoped by the "is what" tail
    # that reliably marks it.
    "pompous_copula": re.compile(r"\b(is|are)\s+what\s+(makes|proves|shows|says)\b", re.I),
    # Absolutist intensifiers in soft contexts. "exact" attached to a window
    # or a moment is almost always dropped by the subagent.
    "exact_window": re.compile(r"\bthe exact (window|moment|shape|line|point|reason|failure)\b", re.I),
}

FILE_PATTERNS = (
    re.compile(r"^rfd/[^/]+/(README|DETAILS)\.md$"),
    re.compile(r"^logbook/.+\.md$"),
)


def in_scope(path: str) -> bool:
    p = path.replace("\\", "/")
    return any(pat.match(p) for pat in FILE_PATTERNS)


def count_tropes(text: str) -> tuple[int, dict[str, int]]:
    # Strip fenced code blocks: SVG viewBox strings and other pass-through
    # content are not prose and must not fire the tells.
    text_no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    per = {name: len(rx.findall(text_no_code)) for name, rx in TELLS.items()}
    return sum(per.values()), per


def non_blank_lines(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def density(text: str) -> float:
    n = non_blank_lines(text)
    hits, _ = count_tropes(text)
    return (100.0 * hits / n) if n else 0.0


def git_show(ref: str, path: str) -> str | None:
    out = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return out.stdout if out.returncode == 0 else None


def changed_files(base: str) -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=True,
    )
    return [p for p in out.stdout.splitlines() if in_scope(p)]


def gate(base: str) -> int:
    changed = changed_files(base)
    if not changed:
        print("0 changed prose file(s) in scope.")
        return 0

    fails = 0
    for path in changed:
        full = os.path.join(ROOT, path)
        if not os.path.isfile(full):
            continue
        after = open(full, encoding="utf-8").read()
        before = git_show(base, path) or ""
        d_now = density(after)
        d_was = density(before)
        if d_now > d_was + 0.001:
            hits, per = count_tropes(after)
            top = ", ".join(f"{k}={v}" for k, v in per.items() if v)
            print(f"  FAIL {path}  {d_now:.2f}% was {d_was:.2f}%  ({hits} hits: {top})")
            fails += 1
        else:
            print(f"  ok   {path}  {d_now:.2f}% was {d_was:.2f}%")
    print(f"{fails} of {len(changed)} scoped file(s) rose above their prior density.")
    return 1 if fails else 0


def report() -> int:
    scanned = 0
    for dirpath, _, filenames in os.walk(os.path.join(ROOT, "rfd")):
        for name in filenames:
            if name in ("README.md", "DETAILS.md"):
                rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
                d = density(open(os.path.join(dirpath, name), encoding="utf-8").read())
                if d > 0:
                    print(f"  {d:5.2f}%  {rel}")
                scanned += 1
    for name in sorted(os.listdir(os.path.join(ROOT, "logbook"))):
        if name.endswith(".md"):
            rel = os.path.join("logbook", name)
            d = density(open(os.path.join(ROOT, rel), encoding="utf-8").read())
            if d > 0:
                print(f"  {d:5.2f}%  {rel}")
            scanned += 1
    print(f"{scanned} scoped file(s) scanned.")
    return 0


def self_test() -> int:
    controls = [
        ("em-dash between clauses", "The gate ran — every control fired.", "em_dash_join", 1),
        ("hyphen range unchanged", "The window is day 11-14.", "em_dash_join", 0),
        ("counting announcement", "It shapes the checks in three ways.", "counting_announcement", 1),
        ("prose that mentions three ways", "Three ways lead there.", "counting_announcement", 0),
        ("reasoning leak", "The reason it holds is that quorum tolerates one down.", "reasoning_leak", 1),
        ("pompous copula", "The second check is what proves the restart.", "pompous_copula", 1),
        ("plain because", "The second check proves the restart because a stale write would fail.", "pompous_copula", 0),
        ("exact window", "That is the exact window in which a shard can stall.", "exact_window", 1),
    ]
    fails = 0
    for label, text, tell, expected in controls:
        _, per = count_tropes(text)
        got = per[tell]
        if got != expected:
            print(f"  FAIL {label}: {tell} expected {expected}, got {got}")
            fails += 1
    if fails:
        print(f"{fails} of {len(controls)} controls failed")
        return 1
    print(f"ok   {len(controls)} of {len(controls)} controls fired in both directions")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", help="git ref to compare against (fail on density rise)")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.base:
        return gate(a.base)
    return report()


if __name__ == "__main__":
    sys.exit(main())
