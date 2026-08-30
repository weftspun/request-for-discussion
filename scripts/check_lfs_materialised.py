#!/usr/bin/env python3
"""Gate: an LFS-tracked file left as a pointer instead of its content, which a
path-existence check passes. Classified on the LFS preamble, not on size. Reasoning in
logbook-rfd1171-gemma-first-rerank.md.

    python scripts/check_lfs_materialised.py [<workspace>] [--self-test]
"""
from __future__ import annotations

import fnmatch
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

POINTER_MAGIC = b"version https://git-lfs.github.com/spec/v1"


def lfs_patterns(repo: Path) -> list[str]:
    ga = repo / ".gitattributes"
    if not ga.is_file():
        return []
    pats = []
    for line in ga.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "filter=lfs" in line:
            pats.append(line.split()[0])
    return pats


def is_pointer(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            return f.read(len(POINTER_MAGIC)) == POINTER_MAGIC
    except OSError:
        return False


def scan(repo: Path) -> tuple[int, list[Path]]:
    pats = lfs_patterns(repo)
    if not pats:
        return 0, []
    tracked, pointers = 0, []
    for f in repo.rglob("*"):
        if not f.is_file() or ".git" in f.parts:
            continue
        if not any(fnmatch.fnmatch(f.name, p) for p in pats):
            continue
        tracked += 1
        if is_pointer(f):
            pointers.append(f)
    return tracked, pointers


def workspace_repos(root: Path) -> list[Path]:
    man = ET.parse(root / ".repo" / "manifests" / "default.xml").getroot()
    return [root / p.get("path") for p in man.iter("project")]


def self_test() -> int:
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td)
        (repo / ".gitattributes").write_text("*.parquet filter=lfs diff=lfs merge=lfs -text\n")

        (repo / "real.parquet").write_bytes(b"PAR1" + b"\0" * 200)
        tracked, ptrs = scan(repo)
        assert tracked == 1 and not ptrs, f"clean input flagged: {ptrs}"

        # Negative control: without it this gate could pass on every input forever.
        (repo / "pointer.parquet").write_bytes(
            POINTER_MAGIC + b"\noid sha256:00\nsize 1220080\n")
        tracked, ptrs = scan(repo)
        assert tracked == 2 and [p.name for p in ptrs] == ["pointer.parquet"], \
            f"planted pointer not caught: {ptrs}"

        (repo / "tiny.parquet").write_bytes(b"PAR1")
        _, ptrs = scan(repo)
        assert [p.name for p in ptrs] == ["pointer.parquet"], f"size used as proxy: {ptrs}"

        (repo / "notes.txt").write_bytes(POINTER_MAGIC)
        tracked, _ = scan(repo)
        assert tracked == 3, f"untracked file entered the population: {tracked}"

    print("self-test ok: pointer caught, small file spared, untracked file excluded")
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    args = [a for a in argv if not a.startswith("-")]
    if len(args) > 1:
        print(__doc__)
        return 2

    start = Path(args[0]).resolve() if args else Path(__file__).resolve().parent.parent
    root = next((c for c in [start, *start.parents] if (c / ".repo").is_dir()), None)
    if root is None:
        print("no .repo above this checkout, so there is no workspace to check")
        return 0

    total, offenders, scanned = 0, [], 0
    for repo in workspace_repos(root):
        if not repo.is_dir():
            continue
        scanned += 1
        n, ptrs = scan(repo)
        total += n
        offenders += [p.relative_to(root).as_posix() for p in ptrs]

    if offenders:
        print(f"FAIL {len(offenders)} of {total} LFS-tracked files are still pointers:")
        for o in offenders[:20]:
            print(f"       {o}")
        if len(offenders) > 20:
            print(f"       ... and {len(offenders) - 20} more")
        print("\n     fix: git lfs pull, in each checkout above")
        return 1

    print(f"ok   {total} LFS-tracked files across {scanned} checkouts, all materialised")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
