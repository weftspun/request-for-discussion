---
title: "RFD 2042: Presence hexagon — wrapping the existing presence stack"
rfd: "2042"
state: published
scope: presence hexagon (proof of concept)
---

## Problem

Remote-avatar presence is already decided in depth, through the orb
demo, the marker decision, and the body-model decision. The loop
needs presence behind ports, the same way the other cores sit behind
ports. Presence had no such structure yet, and redeciding its
representation was not needed.

## Decision

Remote-avatar presence is already decided in depth: head and hand orbs
(the orb demo), human-readable markers (the marker decision), and a
ghostly partial body (the body-model decision). The loop needs
presence behind ports like the other cores, without redeciding the
representation. The project wraps the existing presence stack as a
thin hexagon. The core interpolates remote head and hand poses between
updates and keeps the visual hand separate from the logical combat
hand, as a pure reducer. The driving port `pose_source` carries remote
head and hand pose orbs. The driven port `avatar_sink` carries
interpolated transforms for the rig. `feat/module-xr-grid` feeds
`pose_source` over WebTransport and drives the flatscreen path, and a
fixture adapter replays a recorded pose stream. The marker and body
representation follow the existing presence decisions, so this
hexagon carries no new look. This is the thinnest hexagon, foldable into
Combat after the gate, and the pose channel rides its own stream, so a
stalled input packet does not delay presence. The core replays a
recorded pose stream to interpolated transforms, with no network.

## References

- Original record: `decisions/20260611-hexagon-presence-core.md`

## Related

- `rfd/2040-hexagon-combat-core`: the hexagon this one may fold into
  after the gate.
