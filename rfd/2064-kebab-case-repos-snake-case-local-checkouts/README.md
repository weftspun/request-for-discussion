# RFD 2064: Kebab case repos snake case local checkouts

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

Repositories across our orgs grew inconsistent names. The loot-action
slice under `v-sekai-multiplayer-fabric` mixed kebab-case
(`combat-core`, `loot-core`) with snake_case (`entity_packet`), and
the `sinew-mocap` org carried `mount_drift` and `vr_bridge` alongside
kebab-case peers. We want one repo-naming convention so clones, links,
and code search stay predictable.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
