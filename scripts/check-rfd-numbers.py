#!/usr/bin/env python3
"""Check that every RFD number follows the org-qualified hex rule.

RFD 1000 gives the rule. This script enforces it. Run --self-test to see each
check reject a known-bad input, because a check that passes on broken input
certifies the defect instead of catching it.
"""
import os
import re
import sys

ORG = "1"
DIR_RE = re.compile(r"^([0-9a-f]{4})-[a-z0-9-]+$")
# An old number always began with 0. No organization digit is 0, so a leading
# zero is what tells an unmigrated citation apart from a valid new one.
OLD_CITE_RE = re.compile(r"\bRFD (0\d{3})\b")
HEAD_RE = re.compile(r"^# RFD ([0-9a-f]{4}):")


def rfd_dirs(root):
    return sorted(
        d for d in os.listdir(root)
        if os.path.isdir(os.path.join(root, d)) and not d.startswith(".")
        and re.match(r"^[0-9a-zA-Z]{4}-", d)
    )


def check(root):
    problems = []
    dirs = rfd_dirs(root)
    if not dirs:
        problems.append("no RFD directories found, which is never correct here")

    seen = {}
    for d in dirs:
        m = DIR_RE.match(d)
        if not m:
            problems.append(f"{d}: name is not four lower-case hex digits and a slug")
            continue
        num = m.group(1)
        if num[0] != ORG:
            problems.append(f"{d}: organization digit is {num[0]}, not {ORG}")
        if num in seen:
            problems.append(f"{d}: serial {num} is already used by {seen[num]}")
        seen[num] = d

        readme = os.path.join(root, d, "README.md")
        if not os.path.exists(readme):
            problems.append(f"{d}: has no README.md")
            continue
        with open(readme, encoding="utf-8", errors="ignore") as fh:
            first = fh.readline().rstrip("\n")
        h = HEAD_RE.match(first)
        if not h:
            problems.append(f"{d}: first line is not '# RFD <num>: title', it is {first!r}")
        elif h.group(1) != num:
            problems.append(f"{d}: heading says {h.group(1)}, directory says {num}")

    # A decimal citation is an unmigrated reference. They are prose, not links,
    # so nothing else would ever report them.
    me = os.path.abspath(__file__)
    for cur, dirs_, files in os.walk(root):
        parts = cur.split(os.sep)
        if ".git" in parts or "__pycache__" in parts:
            continue
        for f in files:
            # ALIASES.md holds old numbers on purpose, and this script holds
            # them in its own negative-control fixtures.
            if f == "ALIASES.md" or os.path.abspath(os.path.join(cur, f)) == me:
                continue
            p = os.path.join(cur, f)
            try:
                with open(p, encoding="utf-8", errors="ignore") as fh:
                    body = fh.read()
            except OSError:
                continue
            for m in OLD_CITE_RE.finditer(body):
                problems.append(f"{p}: cites RFD {m.group(1)} in the old decimal form")

    aliases = os.path.join(root, "ALIASES.md")
    if not os.path.exists(aliases):
        problems.append("ALIASES.md is missing, so old numbers do not resolve")
    else:
        with open(aliases, encoding="utf-8") as fh:
            mapped = {m.group(1) for m in re.finditer(r"RFD ([0-9a-f]{4})", fh.read())}
        for num in sorted(seen):
            if num not in mapped:
                problems.append(f"ALIASES.md has no row for RFD {num}")
    return problems


def self_test():
    import shutil
    import tempfile

    def build(tmp, **kw):
        d = os.path.join(tmp, kw.get("dirname", "1001-a-slug"))
        os.makedirs(d)
        with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as fh:
            fh.write(kw.get("heading", "# RFD 1001: A slug\n"))
        with open(os.path.join(tmp, "ALIASES.md"), "w", encoding="utf-8") as fh:
            fh.write(kw.get("aliases", "| RFD 1001 | x |\n"))
        if "extra" in kw:
            with open(os.path.join(tmp, "note.md"), "w", encoding="utf-8") as fh:
                fh.write(kw["extra"])

    cases = [
        ("a clean tree passes", {}, False),
        ("wrong organization digit", {"dirname": "2001-a-slug"}, True),
        ("decimal directory name", {"dirname": "0001-a-slug"}, True),
        ("heading disagrees with directory", {"heading": "# RFD 1002: A slug\n"}, True),
        ("an unmigrated decimal citation", {"extra": "see RFD 0021 for this\n"}, True),
        ("ALIASES.md missing the row", {"aliases": "| RFD 9999 | x |\n"}, True),
    ]
    ok = True
    for name, kw, should_fail in cases:
        tmp = tempfile.mkdtemp()
        try:
            build(tmp, **kw)
            failed = bool(check(tmp))
            mark = "ok " if failed == should_fail else "BAD"
            if failed != should_fail:
                ok = False
            verb = "rejected" if failed else "accepted"
            print(f"  {mark} {name}: {verb}")
        finally:
            shutil.rmtree(tmp)
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        print("self-test: each known-bad input must be rejected")
        sys.exit(self_test())
    found = check(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for line in found:
        print(line)
    print(f"{len(found)} problems")
    sys.exit(1 if found else 0)
