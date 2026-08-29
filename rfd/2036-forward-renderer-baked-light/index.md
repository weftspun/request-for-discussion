---
title: "RFD 2036: Forward renderer with baked light for the mobile floor"
rfd: "2036"
state: published
scope: rendering pipeline (mobile VR floor)
---

## Problem

The mobile tile renderer rations bandwidth across file, memory, and
network IO. Deferred rendering competes for that same bandwidth. The
content slice needs predictable frame cost regardless of light count,
and deferred rendering does not give this.

## Decision

The mobile tile renderer rations bandwidth across file, memory, and
network IO, and deferred rendering competes for that bandwidth. The
slice needs predictable frame cost regardless of light count. The
project uses a simple forward renderer with baked global illumination
and light probes for static geometry, a dedicated shadow pass for
avatars, and probe lighting for dynamic entities, because the frame
cost stays predictable regardless of light count. Deferred rendering
would pressure the bandwidth the mobile tile renderer already rations.
Frame cost stays predictable, so artists place many lights without
watching the budget. Dynamic entities take lower-fidelity probe
lighting, and the renderer removes one axis the small team would
otherwise tune by hand.

## References

- Full context, considered options, and confirmation steps:
  `DETAILS.md`
- Original record: `decisions/20260611-forward-renderer-baked-light.md`

## Related

- `rfd/2035-first-party-curated-content-zone-baker-budgets`: the
  bake-time budget this renderer relies on.

## Detail

{{< include DETAILS.md >}}
