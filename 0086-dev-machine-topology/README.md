# RFD 0086: Dev machine topology, and the Surface/DGX sync rule

**State:** published
**Scope:** the Surface workstation, the DGX Spark, `scripts/sync-*`

## Problem

Two machines, a Windows Surface and a headless NVIDIA DGX Spark,
each hold a copy of this repository, synced by `scp`, not by git.
Reading `logs/remote-log.txt`, planning a Galaxy XR test, or
resolving a sync conflict all need to know which machine owns
`src/` at any given moment, and confusing "the DGX" with "the PC" in
a log misreads which browser actually sent a line.

## Decision

One rule: one machine owns `src/` at a time. Normal development and
Galaxy XR testing run on the Surface, which also runs the Vite dev
server (`https://<Surface-LAN-IP>:3000`); the headset always targets
that LAN IP, never `localhost` on itself. The DGX is reached over
NVIDIA Sync (Tailscale) as user `sifr`, mostly headless, for SSH,
`3DAIGC-API` inference, and builds. `scripts/sync-changes-to-dgx.ps1`
and `sync-changes-to-pc.sh` push incrementally in one direction at a
time; a `.sync-lock-dgx` file mid-sync means stop, not force.

See `DETAILS.md` for the machine-role table, the log-reading fields,
the file-ownership table, and the full sync command reference.

## Related

**Duplicate, byte-identical:** weftspun-3d-studio's own
`thirdparty/m3/docs/DEV_MACHINE_TOPOLOGY.md` holds the same content
today. RFD 0088 gives the HTTPS certificate setup this topology's
headset access depends on. RFD 0101 gives the two SSH host names
this RFD also names.
