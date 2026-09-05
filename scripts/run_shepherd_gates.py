# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Dual-track wrapper: run shepherd's gate ports alongside the python ones for parity.

Finds shepherd via `SHEPHERD_ROOT` env var, or by walking up looking for
`1-transport/transport-shepherd/mix.exs`. Skips loudly (rule 3: named skip,
not silent) when shepherd or `mix` is unavailable. When both are present,
runs `mix gates <name> --self-test` for every ported gate and prints a
per-gate result line. Non-zero exit if any gate self-test fails.

The parity this exposes is between the two implementations of the same gate,
not between the two run modes. A shepherd gate whose self-test fails is a
port bug; a shepherd gate that passes while its python twin fails on a real
diff is either measurement drift the port stated up-front or a real gap.
The one-week dual-track window (task #83) is how the operator sees both.

## Gates list

Aggregate rather than per-gate so pre-commit pays one BEAM startup instead
of seventeen; a per-gate breakdown is what this script's per-line output is.
A gate whose self-test walks synthetic text with no on-disk context is
listed with `None`; a gate whose self-test still reads the working repo's
CLAUDE.md or manifest is listed with the flag that tells it where. The
wrapper's cwd (this manuals-weftspun repo) holds both files, so `--repo .`
is the right anchor.

manifest-root's self-test creates symlink fixtures; on Windows Elixir's
File.ln_s! raises without SeCreateSymbolicLinkPrivilege. CI is Linux, so
it works there. Local Windows dual-track skips this one via `WINDOWS_SKIP`.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

IS_WINDOWS = sys.platform.startswith("win")

WINDOWS_SKIP = {"manifest-root"}

GATES = [
    ("anti-entropy", None),
    ("asset-prefix", None),
    ("blocklist-detail", None),
    ("commit-style", None),
    ("comment-density", None),
    ("comment-ladder", None),
    ("ggml-singleton", None),
    ("goal-manifests", ["--repo", "."]),
    ("logbook-count", None),
    ("manifest-root", ["--repo", "."]),
    ("no-auto", None),
    ("no-orphaned-branches", None),
    ("project-readme-length", None),
    ("rfd-canary", None),
    ("rfd-readme-present", None),
    ("rfd-state-canonical", None),
    ("tropes", None),
]


def find_shepherd():
    env = os.environ.get("SHEPHERD_ROOT")
    if env:
        p = Path(env).expanduser().resolve()
        if (p / "mix.exs").exists():
            return p
    here = Path.cwd().resolve()
    for base in [here, *here.parents]:
        cand = base / "1-transport" / "transport-shepherd"
        if (cand / "mix.exs").exists():
            return cand.resolve()
    return None


def find_mix():
    return shutil.which("mix") or shutil.which("mix.bat")


def main():
    shepherd = find_shepherd()
    if shepherd is None:
        print("shepherd SKIP: transport-shepherd not found on disk.")
        print("  set SHEPHERD_ROOT=<path>, or run inside a goal-manifest workspace where")
        print("  1-transport/transport-shepherd is placed. Skip is named, not silent.")
        return 0
    mix = find_mix()
    if mix is None:
        print("shepherd SKIP: `mix` not on PATH; Elixir toolchain unavailable.")
        print("  install Elixir locally (asdf/mise) or use `erlef/setup-beam` in CI.")
        print("  Skip is named, not silent.")
        return 0

    print(f"shepherd: {shepherd}")
    cwd = str(Path.cwd().resolve())
    fails = 0
    skipped = 0
    for gate, extra in GATES:
        if IS_WINDOWS and gate in WINDOWS_SKIP:
            print(f"  SKIP shepherd:{gate:<24} windows self-test fixture needs symlink privilege")
            skipped += 1
            continue
        args = [mix, "gates", gate]
        if extra:
            resolved = [cwd if a == "." else a for a in extra]
            args += resolved
        args.append("--self-test")
        r = subprocess.run(
            args,
            cwd=str(shepherd),
            capture_output=True,
            text=True,
            shell=False,
        )
        tail = (r.stdout.strip().splitlines() or [""])[-1][:60]
        status = "ok  " if r.returncode == 0 else "FAIL"
        print(f"  {status} shepherd:{gate:<24} {tail}")
        if r.returncode != 0:
            fails += 1

    print()
    total = len(GATES)
    ran = total - skipped
    print(f"{ran - fails} of {ran} shepherd gate self-tests fired ({skipped} windows-skipped).")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
