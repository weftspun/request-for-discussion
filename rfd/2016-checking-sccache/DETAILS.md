# Details

## Context and Problem Statement

Native builds route compilation through sccache
(https://github.com/mozilla/sccache) backed by a shared DigitalOcean
Spaces bucket (`chibifire-sccache`, region `tor1`), so object files are
cached across machines and CI (see
`rfd/2017-compiling-godot-engine/index.md`). The failure mode is
silent: if the `SCCACHE_*` environment is missing, the credentials are
wrong, or the region/endpoint is off, sccache quietly falls back to a
local disk cache — or records read/write errors — while the build still
succeeds. The shared-cache benefit is lost with no obvious signal. How
does someone confirm sccache is actually using the remote bucket and is
healthy?

## Decision Drivers

- A misconfigured cache degrades silently (local disk, or errored
  requests) without failing the build, so "the build worked" is not
  evidence the cache worked.
- The check should be one command, not a ritual or a log dive.
- Credentials are scoped to the `do-tor1` AWS profile, not global
  environment variables, so the check must not require exporting
  secrets.
- It should read the same on Windows (PowerShell) and WSL/Linux.

## Considered Options

- Infer from build times (implicit, unreliable, no backend visibility).
- Enable `SCCACHE_LOG=debug` and read the per-request log every build.
- Read `sccache --show-stats` and check the backend and error counters.

## Windows PowerShell wrapper

Aliases cannot carry logic, hence a function plus a `Set-Alias` shim:

```powershell
function sccheck {
    sccache --show-stats |
        Select-String -Pattern 'Compile requests|Cache hits|Cache misses|Cache .*errors|Cache location'
}
Set-Alias scc sccheck
```

The bash equivalent is `sccache --show-stats` filtered with `grep`. To
measure a single build, reset first:
`sccache --zero-stats; <build>; sccache --show-stats`.

## Consequences

- Good: one command shows the backend and health; no secrets needed,
  since stats read the running server's own counters.
- Good: works identically across shells; the PowerShell `sccheck`/`scc`
  shortcut makes it a reflex.
- Bad: the counters are per-server-session — they reset when the
  sccache server restarts or on `--zero-stats`, so they are not
  lifetime bucket totals.
- Bad: `--show-stats` alone does not prove S3 connectivity; only a
  compile (or a full build) exercises read/write. `Cache errors = 0`
  after a build is the real confirmation that auth and the endpoint are
  correct.

## Confirmation

Running `sccheck` reported `Cache location  s3, name: chibifire-sccache,
prefix: /godot/`, `Cache errors 0`, and hits accumulating during a Godot
rebuild — so the remote backend, region, and `do-tor1` credentials are
all working.

## More Information

- The non-secret `SCCACHE_*` variables (`SCCACHE_BUCKET`,
  `SCCACHE_ENDPOINT`, `SCCACHE_REGION`, `SCCACHE_S3_USE_SSL`,
  `SCCACHE_S3_KEY_PREFIX`) are set globally; credentials live in the
  `do-tor1` profile (`~/.aws/credentials`) and are applied only for the
  duration of a build, so the real AWS CLI is never shadowed.
- Per-project key prefixes keep objects from colliding in the one
  bucket (e.g. `godot` vs `idtx-flow`).
- To debug a non-zero error count, set `SCCACHE_LOG=debug` and
  `SCCACHE_ERROR_LOG` in the sccache service launcher and reinstall the
  service so the supervised server picks them up
  (`decisions/20260606-windows-background-services-nssm.md`).
