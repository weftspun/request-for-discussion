# RFD 1065: Two SSH hosts only, `DGX-Local` and `DGX-Remote`

**State:** abandoned
**Scope:** `~/.ssh/config`, `~/.ssh/config-cursor`, `scripts/*-dgx-*`

## Problem

The DGX Spark shows up under more than one name across NVIDIA Sync
and an SSH client: `DGX-Local`, `DGX-Remote`, and the raw hostname
`dgx-spark.local`, which reads as a third machine if the naming
rule is not written down anywhere.

## Decision

Exactly two SSH hosts: `DGX-Local` (`dgx-spark.local`, at home) and
`DGX-Remote` (`100.93.124.59`, over Tailscale, away). `dgx-spark.local`
is not a third machine; it is `DGX-Local`'s own address, reached
through `~/.ssh/config-cursor`. An auto-guard script
(`scripts/install-dgx-ssh-guard.ps1`, checked with `npm run
dgx:guard`) restores the golden config templates when NVIDIA Sync or
the editor's own SSH settings drift, but never re-pairs NVIDIA Sync
or deletes a host itself.

See `DETAILS.md` for every repair script, what each one touches, and
the reverse-SSH setup from the DGX back to the Surface.

## Related

**Unresolved duplicate:** weftspun-3d-studio's own
`thirdparty/m3/docs/SSH_HOST_NAMES.md` covers the same topic, with
real content differences, including different SSH routes and
hostnames. Neither version is authoritative; that reconciliation is
still open. RFD 1056 gives the machine topology these two hosts fit
into.
