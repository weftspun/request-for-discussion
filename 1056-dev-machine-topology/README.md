# RFD 1056: Dev machine topology, and the two-machine sync rule

**State:** published
**Scope:** an editor workstation, a CUDA-capable GPU host, `scripts/sync-*`

## Problem

Two machines, an editor workstation and a headless GPU host, each
hold a copy of this repository, synced by `scp`, not by git.
Reading `logs/remote-log.txt`, planning a headset test, or resolving
a sync conflict all need to know which machine owns `src/` at any
given moment. Nothing about this split needs one specific machine or
headset; RFD 1077 gives the real requirement, a CUDA GPU and a
WebXR browser. This RFD's own examples name a Windows Surface, an
NVIDIA DGX Spark, and a Galaxy XR headset, this team's own reference
pair and test device.

## Decision

One rule: one machine owns `src/` at a time. Normal development and
headset testing run on the editor workstation, which also runs the
Vite dev server (`https://<workstation-LAN-IP>:3000`); the headset
always targets that LAN IP, never `localhost` on itself. The GPU
host is reached over a VPN mesh (Tailscale), mostly headless, for
SSH, `3DAIGC-API` inference, and builds. `scripts/sync-changes-to-dgx.ps1`
and `sync-changes-to-pc.sh` push incrementally in one direction at a
time; a `.sync-lock-dgx` file mid-sync means stop, not force.

See `DETAILS.md` for the machine-role table, the log-reading fields,
the file-ownership table, and the full sync command reference.

## Related

RFD 1077 gives the general hardware requirement this RFD's own
Surface/DGX pair is one example of. RFD 1058 gives the HTTPS
certificate setup this topology's headset access depends on. RFD
1065 gives the two SSH host names this RFD also names.
weftspun-3d-studio's own `thirdparty/m3/docs/DEV_MACHINE_TOPOLOGY.md`
holds the same content, byte-identical, as of this writing.
