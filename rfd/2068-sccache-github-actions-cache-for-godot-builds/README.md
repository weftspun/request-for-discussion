# RFD 2068: Sccache github actions cache for godot builds

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The `fabric-godot-images` repo builds the Godot engine from source
inside a podman container and publishes the result to ghcr.io. A full
cold build takes 30–60 minutes. The previous CI path used
`docker/build-push-action` with `cache-from/to: type=gha`, which
cached OCI layers between runs. That action was replaced by plain
`podman build` to align with the fabric's rootless-podman +
systemd-quadlet standard. The layer cache was lost in that migration.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
