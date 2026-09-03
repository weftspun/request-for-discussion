#!/usr/bin/env python3
"""If pages/logbook.qmd states an entry count, it matches the entries on disk.

A prose count in the logbook page ("These 145 entries...") drifts silently
the moment an entry is added or removed. This gate scans logbook.qmd for
any "N entries" phrase and asserts N equals len(glob('logbook/logbook-*.md')).

Rule 3 (silent skip reads as a pass): if the page carries no such phrase,
the gate reports "ok" and names the entry count it observed so an operator
sees the number rather than a bare success.

Run --self-test for negative and positive controls.
"""
from __future__ import annotations

import glob
import os
import re
import sys
import tempfile


COUNT_RE = re.compile(r"\b(\d+)\s+entries\b")


def entries_on_disk(root: str) -> int:
    return len(glob.glob(os.path.join(root, "logbook", "logbook-*.md")))


def scan(root: str) -> tuple[int, list[int]]:
    """Return (disk_count, declared_counts)."""
    disk = entries_on_disk(root)
    qmd = os.path.join(root, "pages", "logbook.qmd")
    declared: list[int] = []
    if os.path.isfile(qmd):
        text = open(qmd, encoding="utf-8").read()
        declared = [int(m.group(1)) for m in COUNT_RE.finditer(text)]
    return disk, declared


def run(root: str) -> int:
    disk, declared = scan(root)
    if not declared:
        print(f"ok   pages/logbook.qmd declares no count; disk has {disk} entries")
        return 0
    bad = [d for d in declared if d != disk]
    if bad:
        print(f"FAIL pages/logbook.qmd declares {declared}, disk has {disk} entries")
        return 1
    print(f"ok   pages/logbook.qmd declares {declared[0]}, matches {disk} entries on disk")
    return 0


def _plant(root: str, qmd_body: str, n_entries: int) -> None:
    os.makedirs(os.path.join(root, "pages"))
    os.makedirs(os.path.join(root, "logbook"))
    open(os.path.join(root, "pages", "logbook.qmd"), "w").write(qmd_body)
    for i in range(n_entries):
        open(os.path.join(root, "logbook", f"logbook-{i:04d}.md"), "w").write("x\n")


def _self_test() -> int:
    # positive: declared matches disk
    with tempfile.TemporaryDirectory() as t:
        _plant(t, "These 3 entries...\n", 3)
        assert run(t) == 0
    # negative: declared does not match disk
    with tempfile.TemporaryDirectory() as t:
        _plant(t, "These 145 entries...\n", 26)
        assert run(t) == 1
    # silent-skip case: no phrase, but the count is still reported
    with tempfile.TemporaryDirectory() as t:
        _plant(t, "no count here.\n", 5)
        assert run(t) == 0
    print("self-test ok")
    return 0


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        return _self_test()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return run(root)


if __name__ == "__main__":
    sys.exit(main())
