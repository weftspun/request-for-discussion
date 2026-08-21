# RFD 1065 details: what is what, and every repair script

## What is what

| Seen in NVIDIA Sync | SSH name (editor) | Address underneath | When    |
| ------------------- | ----------------- | ------------------ | ------- |
| DGX Sparks local    | `DGX-Local`       | `dgx-spark.local`  | At home |
| DGX Sparks remote   | `DGX-Remote`      | `100.93.124.59`    | Away    |

`DGX-Local` in the SSH config is correct; prefer Remote-SSH to
either `DGX-Local` or `DGX-Remote` directly.

If an old editor session still shows `dgx-spark.local`, that is not
a third machine, it is the address under `DGX-Local`. The editor
uses `~/.ssh/config-cursor` (the main config, plus a mapping from
`dgx-spark.local` to user `sifr`); NVIDIA Sync uses `~/.ssh/config`
directly, two hosts only.

NVIDIA Sync uses `~/.ssh/config` plus `nvsync.key`. If Sync fails
but the editor still worked before, the key on the Spark needs
reinstalling, not deleting `DGX-Local`.

## Auto-guard, keeps the layout after an update

Golden templates live in this repository's own `scripts/`
(`dgx-spark.ssh.config`, `cursor-ssh-extras.config`, and others).
The guard restores them whenever NVIDIA Sync or the editor's SSH
settings drift.

One-time install (before every `npm run dev`, and at Windows
sign-in):

```powershell
cd C:\Users\alfao\Documents\GitHub\Weftspun3DStudio
.\scripts\install-dgx-ssh-guard.ps1
```

Manual check: `npm run dgx:guard`.

The guard does not re-pair NVIDIA Sync or delete a host; it only
restores config files, strips a bad `Include` line, fixes a byte-order
mark, and resets the editor's own SSH settings. Use the repair
scripts below if auth or remote pairing actually breaks.

## Fix auth

```powershell
cd C:\Users\alfao\Documents\GitHub\Weftspun3DStudio
.\scripts\repair-dgx-auth.ps1
```

This script keeps `DGX-Local` and `DGX-Remote` in `~/.ssh/config`,
installs the NVIDIA Sync public key on the Spark (one password
prompt), and re-registers with NVIDIA Sync without wiping the SSH
config.

## Fix `DGX-Remote` only

For `knownhost: remote host not known`, when `DGX-Local` already
works. This script does not change `DGX-Local`.

```powershell
cd C:\Users\alfao\Documents\GitHub\Weftspun3DStudio
.\scripts\repair-dgx-remote.ps1
```

## Editor terminal stuck reconnecting

A stale `cursor-server` process on the Spark causes a multiplex 401
and an endless reconnect loop.

```powershell
cd C:\Users\alfao\Documents\GitHub\Weftspun3DStudio
.\scripts\fix-cursor-remote-loop.ps1
```

Quit the editor fully, run the script, reopen it, then connect
through `DGX-Local`, not `dgx-spark.local` directly.

## Other scripts

```powershell
cd C:\Users\alfao\Documents\GitHub\Weftspun3DStudio
.\scripts\repair-nvidia-sync-devices.ps1   # removes old junk device names only
.\scripts\restart-nvidia-sync.ps1          # for when the app itself will not open
```

## DGX to Surface, reverse SSH

Lets the Spark SSH into the Surface (`alfao@10.0.0.32`), for sync
scripts and file pulls.

One-time, administrator PowerShell on the Surface:

```powershell
cd C:\Users\alfao\Documents\GitHub\Weftspun3DStudio
.\scripts\install-surface-openssh-server.ps1
```

Then, in a normal PowerShell:

```powershell
.\scripts\allow-dgx-ssh-to-surface.ps1
```

This fetches or creates `~/.ssh/id_ed25519` on the Spark, adds it to
`~/.ssh/authorized_keys` on the Surface, fixes the key's file
permissions, and appends a `Host Surface-PC` block to the Spark's
own `~/.ssh/config`.

Test from the DGX:

```bash
ssh Surface-PC hostname
# or: ssh alfao@10.0.0.32
```

The Surface's LAN IP is auto-detected, Wi-Fi first; Tailscale
(`100.94.x.x`) is not used for LAN SSH unless a separate host block
is added for it.
