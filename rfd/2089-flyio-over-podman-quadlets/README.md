# RFD 2089: Flyio over podman quadlets

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

`rfd/0061` chose podman quadlets under systemd on self-hosted Fedora
44 hosts over both Fly.io and the earlier Harvester HCI plan,
provisioned by the `infra` repo's OpenTofu. Seven quadlet repos were
created for this: `zone-backend-quadlet`, `cockroach-crdb-quadlet`,
`zone-server-quadlet`, `zone-baker-quadlet`, `restic-backup-quadlet`,
`gha-runner-quadlet`, and `sccache-cache-quadlet`, each with an
`install.sh` and a real `.container` unit. All seven last received a
push on 2026-06-13.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
