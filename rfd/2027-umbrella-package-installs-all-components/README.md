# RFD 2027: Umbrella package installs all components

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

A project ships as several components, each with its own install
entry. The sinew mocap stack publishes one scoop manifest and one
Homebrew formula per app (`sinew-tui`, `sinew-vr-bridge`,
`sinew-viewer`), and the zone backend runs several services
(cockroach, redis, uro, nextjs, caddy). A person who wants the whole
set runs one install command per component and needs to know every
component name. How does a person install or run the full set in one
step?

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
