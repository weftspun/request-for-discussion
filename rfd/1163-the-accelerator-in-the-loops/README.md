# RFD 1163: The flow rents a card, the accelerator stays on the desk

**State:** ideation
**Feature:** where each half of the loop runs
**Scope:** `7-service/service-livebook`, `3-interactor/rf-detr-cpp`

## Problem

The four loops run on the desk card, and RFD 1140 recorded what that
costs: one RTX 3090 at 24 GiB, where OmniGen2 pages into shared
memory rather than failing, so the symptom is a run that stops being
fast.

The UGen300 has no place in any loop. The compile that would give it
one was killed at 30.26 GiB, Docker's ceiling and also WSL's, since
both are one virtual machine under an absent `.wslconfig`.

Renting answers the first and cannot answer the second: a pod has no
USB, so no rented card runs a HEF. The compiler needs no device at
all -- `gate_dfc_parse.py` says so in its own docstring -- and that
splits the work rather than blocking it.

## Decision

The flow runs on RunPod and the accelerator runs on the desk, and
the HEF is the only thing that crosses. RunPod takes OmniGen2 with `anny-camera-lora`, EditScore, and the
Dataflow Compiler; the desk keeps `hailortcli` and `usb/004:013`.
RFD 1140's order governs the renting: push before, tear down after,
check the tear down.

Loop 1's `detect_keypoints` goes first, because RF-DETR is the one
graph already through translate: 825 nodes, 22 operators, and the
compiler agreeing with the allowlist. EditScore is second and
bounded; `DETAILS.md` has the measurement that bounds it.

## Related

RFD 1140 rents the card. RFD 1141 says where the HEF goes. RFD 1157
holds EditScore. RFD 1143 is the loop it serves.
