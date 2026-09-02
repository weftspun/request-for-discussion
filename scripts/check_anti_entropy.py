"""Inventory and anti-entropy check over the workspace. CLAUDE.md names this check.

METHOD, AND WHY IT IS MOSTLY NOT RANDOM. CLAUDE.md rule 5: "A sampled check only sees
defects larger than ~3/n. For a FIXED population, enumerate rather than estimate."
Manifest projects, serials, blocklist rows and linkfiles are all fixed and countable,
so sampling them would be strictly worse than reading all of them. They are enumerated.

Randomness earns its place only where enumeration costs too much to run: picking which
expensive re-verification to perform. That draw uses `secrets`, so it cannot be nudged.
"""
import os, re, secrets, subprocess, sys, xml.etree.ElementTree as ET
from pathlib import Path

RFD = Path(__file__).resolve().parent.parent
ROOT = next((c for c in [RFD, *RFD.parents] if (c / ".repo").is_dir()), None)
if ROOT is None:
    print("no .repo above this checkout, so there is no workspace to check")
    raise SystemExit(0)
out, fails = [], 0

def check(name, ok, detail=""):
    global fails
    if not ok: fails += 1
    out.append(f"  {'ok  ' if ok else 'FAIL'} {name:<42} {detail}")

# --- A. manifest projects, enumerated -------------------------------------------------
man = ET.parse(ROOT/".repo/manifests/default.xml").getroot()
projects = [(p.get("name"), p.get("path")) for p in man.iter("project")]
missing = [p for _, p in projects if not (ROOT/p).is_dir()]
check("manifest paths exist on disk", not missing, f"{len(projects)} projects, missing: {missing or 'none'}")
bad = [p for _, p in projects if "_" in p or " " in p]
check("every path hyphen-only", not bad, f"offenders: {bad or 'none'}")

# --- B. serials, enumerated both directions -------------------------------------------
# PARSED INDEPENDENTLY, ON PURPOSE. check-rfd-serials.py reads this register through the
# USD API; this reads the text. Two implementations that disagree is the finding, and
# sharing one reader would retire the check while appearing to keep it.
#
# ROW FORM. The register was parallel `int[] serial` and `string[] slug`, and is now one
# prim per row with the serial in the prim name. The old shape could hold a duplicate key
# -- `[1, 1, 2]` parses -- and could lose a slug without the count changing anywhere a
# reader looked. USD refuses two siblings of one name, so the first is now impossible to
# author rather than merely checked for.
s = (RFD/"SERIALS.usda").read_text()

def _section(name):
    i = s.find(f'def Scope "{name}"')
    if i < 0:
        return ""
    j = min([x for x in (s.find('def Scope "Unused"', i + 1),
                         s.find('def Scope "Deleted"', i + 1),
                         len(s)) if x > i] or [len(s)])
    return s[i:j]

_alloc = _section("Allocated")
live = [int(x) for x in re.findall(r'def "S(\d+)"', _alloc)]
slugs = re.findall(r'custom string slug = "([^"]*)"', _alloc)
dead = [int(x) for x in re.findall(r'def "S(\d+)"', _section("Deleted"))]
dirs = sorted(d for d in os.listdir(RFD / "rfd") if re.match(r"^1\d{3}-", d))

check("every allocated row carries a slug", len(live)==len(slugs), f"{len(live)} rows / {len(slugs)} slugs")
check("no duplicate serials", len(live)==len(set(live)), f"{len(live)} rows, {len(set(live))} distinct")
check("  control: a planted duplicate row is seen",
      len([int(x) for x in re.findall(r'def "S(\d+)"', _alloc + '\n                def "S1000"\n')]) == len(live)+1)
check("no retired serial reused", not (set(live)&set(dead)), f"retired: {dead}")
check("every directory registered", all(int(d[:4]) in live for d in dirs), f"{len(dirs)} dirs")
check("every serial has a directory", all(any(d.startswith(f"{n}-") for d in dirs) for n in live))
check("slug matches directory name", all(f"{n}-{sl}" in dirs for n,sl in zip(live,slugs)),
      f"mismatches: {[f'{n}-{sl}' for n,sl in zip(live,slugs) if f'{n}-{sl}' not in dirs] or 'none'}")

# --- C. blocklist rows vs sections, enumerated ----------------------------------------
cl = (RFD/"CLAUDE.md").read_text(); bl = (RFD/"BLOCKLIST.md").read_text()
rows = [l for l in cl.splitlines() if l.startswith("|") and "see below" in l.lower()]
secs = [l for l in bl.splitlines() if l.startswith("### ")]
check("blocklist rows == sections", len(rows)==len(secs), f"{len(rows)} rows / {len(secs)} sections")
check("  control: counter finds a planted row", 
      len([l for l in (cl+"\n| planted | See Below |").splitlines() if l.startswith("|") and "see below" in l.lower()]) == len(rows)+1,
      "case-insensitive match verified against a planted row")

# --- D. linkfiles, enumerated ----------------------------------------------------------
links = [(lf.get("src"), lf.get("dest"), p.get("path"))
         for p in man.iter("project") for lf in p.iter("linkfile")]
broken = [d for src, d, pp in links if not (ROOT/d).exists()]
check("every linkfile resolves", not broken, f"{len(links)} links, broken: {broken or 'none'}")

# --- E. README line bound, enumerated over all RFDs ------------------------------------
limit = 40
over = [d for d in dirs if (RFD/"rfd"/d/"README.md").is_file()
        and len((RFD/"rfd"/d/"README.md").read_text().splitlines()) > limit]
check(f"every README <= {limit} lines", not over, f"{len(dirs)} READMEs, over: {over or 'none'}")

# --- F. shuffled full pass over the expensive checks -----------------------------------
# A SHUFFLE RATHER THAN A DRAW, AND THE DIFFERENCE IS COVERAGE. The first version of this
# used `secrets.randbelow` three times, which samples WITH REPLACEMENT: one run drew three
# picks and got two distinct checks, and nothing bounds how long an item can go unvisited.
# A shuffled full pass visits every item exactly once, so coverage is total and the only
# thing randomised is the order -- which still surfaces anything order-dependent.
#
# Enumerating rather than sampling is also what CLAUDE.md rule 5 asks for: this population
# is fixed and countable, so a sample would see only defects larger than about 3/n while
# costing nearly as much.
EXPENSIVE = ["check_fourloops_plan", "check_fourloops_etnf", "check_rfd1122_plan",
             "check_usd_valid", "check_pen_66606", "check_blocklist_detail",
             "check_goal_manifests", "check-rfd-structure",
             ("check_comment_ladder", ("--self-test",)),
             ("check_pr_description", ("--self-test",)),
             ("check_rfd_canary", ("--self-test",)),
             ("check_no_orphaned_branches", ("--self-test",)),
             ("check_project_readme_length", ("--self-test",))]
order = list(EXPENSIVE)
secrets.SystemRandom().shuffle(order)
out.append("")
out.append(f"  shuffled full pass, {len(order)} of {len(EXPENSIVE)} (every item, random order):")
for item in order:
    name, extra = item if isinstance(item, tuple) else (item, ())
    r = subprocess.run([sys.executable, str(RFD/"scripts"/f"{name}.py"), *extra],
                       capture_output=True, text=True, cwd=RFD)
    tail = (r.stdout.strip().splitlines() or [""])[-1][:58]
    check(f"  {name}", r.returncode == 0, tail)
seen = set(order)
check("shuffle covered every item", seen == set(EXPENSIVE),
      f"{len(seen)}/{len(EXPENSIVE)} distinct, repeats: {len(order)-len(seen)}")

print("\n".join(out))
print(f"\n  enumerated checks: {len(out)-2} run, {fails} failed")
sys.exit(1 if fails else 0)
