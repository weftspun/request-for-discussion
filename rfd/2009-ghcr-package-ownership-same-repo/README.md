# RFD 2009: Ghcr package ownership same repo

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The zone server binary was built by `multiplayer-fabric-baker` and
pushed to `ghcr.io/v-sekai-fire/godot-zone-double`. The zone deploy
workflow (in `multiplayer-fabric-zone`) used `--local-only` with
`docker/login-action` to pull that image, but received 403 Forbidden.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
