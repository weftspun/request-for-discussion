#!/usr/bin/env python3
"""Check that every RFD number follows the org-qualified hex rule.

RFD 1000 gives the rule. This script enforces it. Run --self-test to see each
check reject a known-bad input, because a check that passes on broken input
certifies the defect instead of catching it.

This gate owns numbering: directory names, the organization digit, serial
uniqueness, heading agreement, and ALIASES.md coverage. It used to also scan
for unmigrated decimal citations, and no longer does. That scan read the raw
bytes, so a citation an RFD wrapped over two lines never matched it: it found
3 of the 37 in the tree. `check-rfd-structure.py` reads the same citations off
a CommonMark AST and finds all of them, so the scan moved there rather than
being kept in two places at two strengths. RFD 107c records the move.
"""
import os
import re
import sys

ORG = "1"
DIR_RE = re.compile(r"^([0-9a-f]{4})-[a-z0-9-]+$")
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

    aliases = os.path.join(root, "ALIASES.md")
    if not os.path.exists(aliases):
        problems.append("ALIASES.md is missing, so old numbers do not resolve")
    else:
        with open(aliases, encoding="utf-8") as fh:
            mapped = {m.group(1) for m in re.finditer(r"RFD ([0-9a-f]{4})", fh.read())}
        # The migration was a closed set. It renumbered a contiguous range and
        # ended, so only a number inside that range can have an old number to
        # resolve. An RFD written afterwards has none, and demanding a row for
        # it would put a lookup entry that maps from nothing into the table.
        # The range is read from ALIASES.md rather than written here, because
        # the table is the record of what the migration covered.
        migrated = {n for n in mapped if n[0] == ORG}
        if not migrated:
            # An empty table would make the range empty and every check below
            # vacuous, which reads exactly like a pass.
            problems.append("ALIASES.md maps no RFD in this organization")
        else:
            last = max(migrated)
            for num in sorted(seen):
                if num <= last and num not in mapped:
                    problems.append(f"ALIASES.md has no row for RFD {num}")
    return problems


def self_test():
    import shutil
    import tempfile

    def build(tmp, **kw):
        for name, head in kw.get("extra_dirs", []):
            os.makedirs(os.path.join(tmp, name))
            with open(os.path.join(tmp, name, "README.md"), "w", encoding="utf-8") as fh:
                fh.write(head)
        d = os.path.join(tmp, kw.get("dirname", "1001-a-slug"))
        os.makedirs(d)
        with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as fh:
            fh.write(kw.get("heading", "# RFD 1001: A slug\n"))
        with open(os.path.join(tmp, "ALIASES.md"), "w", encoding="utf-8") as fh:
            fh.write(kw.get("aliases", "| RFD 0001 | RFD 1001 | x |\n"))

    cases = [
        ("a clean tree passes", {}, False),
        ("wrong organization digit", {"dirname": "2001-a-slug"}, True),
        ("decimal directory name", {"dirname": "0001-a-slug"}, True),
        ("heading disagrees with directory", {"heading": "# RFD 1002: A slug\n"}, True),
        ("ALIASES.md maps nothing in this organization",
         {"aliases": "| RFD 0009 | RFD 9999 | x |\n"}, True),
        # The pair below is the boundary. Inside the migrated range a missing
        # row is a defect. Above it there is no old number to record.
        ("a migrated number with no row",
         {"aliases": "| RFD 0009 | RFD 1009 | x |\n"}, True),
        ("a post-migration number needs no row",
         {"extra_dirs": [("1002-a-slug", "# RFD 1002: A slug\n")],
          "aliases": "| RFD 0001 | RFD 1001 | x |\n"}, False),
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
