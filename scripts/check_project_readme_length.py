"""Every manifest project's README.md first non-blank line is <= 144 characters.

The first line of a README is the tagline a reader sees before scrolling. A repo
tagline is small on purpose: it forces the writer to pick what the project is,
not to hedge. 144 characters is the budget.

Silently skips projects with no README.md; reports the count so the skip does
not read as a pass (CLAUDE.md rule 3). Matches the pattern of check_anti_entropy's
existing "every README <= 40 lines" check over RFDs.

    python scripts/check_project_readme_length.py
    python scripts/check_project_readme_length.py --self-test
"""
import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
RFD = HERE.parent
ROOT = next((c for c in [RFD, *RFD.parents] if (c / ".repo").is_dir()), None)
LIMIT = 144

# The first line of a fork's README is upstream's, not ours. Exempted here rather than
# rewritten upstream. Grows when a new fork lands.
FORK_EXEMPT = {
    "3-interactor/datasource-flow",
    "3-interactor/idtx-flow",
}


def first_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.rstrip()
    return ""


def gate(root: Path) -> int:
    man = ET.parse(root / ".repo/manifests/default.xml").getroot()
    projects = [(p.get("name"), p.get("path")) for p in man.iter("project")]
    have, missing, exempt, over = [], [], [], []
    for _name, path in projects:
        if path in FORK_EXEMPT:
            exempt.append(path)
            continue
        rd = root / path / "README.md"
        if not rd.is_file():
            missing.append(path)
            continue
        have.append(path)
        line = first_line(rd.read_text(encoding="utf-8", errors="replace"))
        if len(line) > LIMIT:
            over.append((path, len(line)))
    for path, ln in over:
        print(f"  FAIL {path}/README.md  first line {ln} chars > {LIMIT}")
    print(f"  {len(have)} projects with README.md, {len(missing)} without, {len(exempt)} fork-exempt.")
    print(f"{len(over)} of {len(have)} first lines over {LIMIT} chars.")
    return 1 if over else 0


def self_test() -> int:
    long_body = "x" * 143
    controls = [
        ("short heading", "# short\n\nbody", True),
        ("blank then short", "\n\n# short heading after blanks\n", True),
        ("exactly 144", "#" + " " + "x" * 142, True),
        ("145 chars", "#" + " " + "x" * 143, False),
        ("blank then long", "\n\n" + "x" * 200 + "\n", False),
        ("only whitespace", "   \n\n\t\n", True),
        ("long line 2, short line 1", "# ok\n\n" + long_body + long_body, True),
    ]
    fails = 0
    for label, text, expected_pass in controls:
        line = first_line(text)
        got_pass = len(line) <= LIMIT
        if got_pass != expected_pass:
            print(f"  FAIL {label}: got {'pass' if got_pass else 'fail'}, expected {'pass' if expected_pass else 'fail'} (line len {len(line)})")
            fails += 1
    if fails:
        print(f"{fails} of {len(controls)} controls failed")
        return 1
    print(f"ok   {len(controls)} of {len(controls)} controls fired in both directions")
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if ROOT is None:
        print("no .repo above this checkout, so there is no workspace to check")
        return 0
    return gate(ROOT)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
