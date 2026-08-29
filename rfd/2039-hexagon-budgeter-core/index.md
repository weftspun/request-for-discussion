---
title: "RFD 2039: Budgeter hexagon — core, ports, and adapters"
rfd: "2039"
state: published
scope: budgeter hexagon (proof of concept)
---

## Problem

The content slice needs graceful degradation under load on the
mobile floor. Quality knobs, such as avatar level-of-detail and voice
radius, must adjust per frame so the player stays inside the
experience during a burst. The budgeter had no structure that could
measure the device and adjust these knobs.

## Decision

The slice needs graceful degradation under load on the mobile floor,
dialing quality knobs per frame so the player stays inside the
experience during a burst. The project structures the budgeter as a
hexagon. The core is a constraint solver that maps on-device
measurements to knob settings, such as avatar level-of-detail,
interpolation against extrapolation, voice radius, and audio sample
quality, as a pure reducer. It dials the knobs every frame, never
overrules itself, and never dictates how the artists work. The driving
port `measurement_source` carries frame time, thermals, and entity
counts. The driven port `knob_sink` carries the settings the runtime
applies. `feat/module-open-telemetry` feeds `measurement_source`, the
engine runtime applies `knob_sink`, and a fixture adapter replays a
load spike for CI. As a hundred extra players land in the hub, the
budgeter degrades gracefully so the player stays inside the
experience. The solve runs against a recorded spike in CI with no
device, and the budgeter stays advisory, so it never overrules the
artists.

## References

- Original record: `decisions/20260611-hexagon-budgeter-core.md`
- `feat/module-open-telemetry`

## Related

- `rfd/2028-hexagonal-core-ports-adapters`: the core/ports/adapters
  convention this hexagon follows.
