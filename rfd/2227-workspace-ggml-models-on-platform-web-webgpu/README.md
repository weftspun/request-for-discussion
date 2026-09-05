# RFD 2227: workspace ggml models on `platform=web` + WebGPU

**Platform=web delivery surface:** retracted 2026-09-05, superseded
by [RFD 2228](../2228-webgpu-native-drop-platform-web/) — operator
reversal (verbatim): *"drop webgpu platform=web. try webgpu
native"*.

**Gemma 3 270M as first-ship pick:** retracted 2026-09-05 by the
Gemma 3 blocklist row in `CLAUDE.md` (operator directive: *"gemma3
is blockedlisted only gemma4 is allowlisted"*). A successor RFD
scoping ggml-consumers-on-native-WebGPU picks Gemma 4 E2B (~750 MB
Q4) as first ship.

**State:** abandoned

This RFD was drafted by an AI and read by a human before it shipped.
