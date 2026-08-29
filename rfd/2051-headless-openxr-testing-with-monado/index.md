---
title: "RFD 2051: Headless OpenXR testing with Monado (null compositor + simulated HMD)"
rfd: "2051"
state: published
scope: OpenXR functional and integration test coverage
---

## Problem

The OpenXR path needs to run on Linux with no headset, both on the
workstation for iteration and inside a podman quadlet for CI. The
project had no way to reach a conformant OpenXR runtime under these
conditions.

## Decision

The OpenXR path needs to run on Linux without a headset: on the
workstation for iteration and in a podman quadlet for CI. The project
runs Monado with the null compositor and a simulated HMD, headless,
because it is a conformant OpenXR runtime that an app reaches over
the loader with no display and no device, on the workstation and
inside a quadlet. `XRT_COMPOSITOR_NULL` discards submitted frames, so
this covers the runtime, the tracking, and frame submission, with no
rendered output and no performance signal. `SIMULATED_ENABLE` supplies
a head and controllers driven programmatically. This is functional
and integration coverage; the standalone OpenXR build stays the
performance and comfort gate. `openxr_runtime_list`, and any OpenXR
app, reaches `xrCreateInstance` against the running service, and the
service log reports the null compositor and a simulated HMD.

## References

- Install recipe, the stdin-pipe caveat, and the qwerty driver:
  `DETAILS.md`
- Original record:
  `decisions/20260612-headless-openxr-testing-with-monado.md`

## Related

- `rfd/2056-systemd-quadlet-verification-queue`: the quadlet queue
  that runs this Monado smoke.

## Detail

{{< include DETAILS.md >}}
