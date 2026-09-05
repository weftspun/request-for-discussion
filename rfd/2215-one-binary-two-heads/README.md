# RFD 2215: one Godot `platform=web` binary, two heads

**`platform=web` delivery surface:** retracted 2026-09-05 by
[RFD 2228](../2228-webgpu-native-drop-platform-web/) — operator
reversal (verbatim): *"drop webgpu platform=web. try webgpu
native"*.

**State:** discussion
**Flight level:** L2 (coordination)
**Feature:** one runtime serves both the marketing video
(headless capture head) and the game (interactive head), which
dissolves the RFD 2194 vs 2208 conflict
**Scope:** native binary entrypoints for both heads, CineForm
video muxing for the capture head

## The surviving decision

One source tree, one CI workflow, one **native binary per
platform** (macOS / Windows / Linux), two invocation flags:

- **Head A — game.** Native window; loads Starforged fixture
  (`starforged.sqlite`), calls `taskweft`'s planner (RFD 2205),
  surfaces the decision-point menu via a Godot Control-node VN
  layout, plays reactions on the VRM portrait via
  `Ggml.run_inference()` (RFD 2230 GDExtension surface) for
  motion + VRM expressions for face.
- **Head B — marketing video.** Headless render pass of the same
  binary. `godot --headless --write-movie shot<NN>.<container>
  ...` captures the runway scene per shot; video muxed via
  CineForm per RFD 1123 (ffmpeg blocklisted, see memory
  `ffmpeg-blocklisted`).

Same `.tscn` / `.tres` assets, same binary, different
invocation flag. The video is what the game looks like when you
run it deterministically with a script over the shot list.

## Why one binary

Six merge conflicts between RFD 2194 and RFD 2208 (render surface
/ autonomy / identity pipeline / runtime footprint /
parked-vs-live / RFD-graph) all dissolve when one runtime serves
both. Two binaries is what created the conflicts in the first
place.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3
  strategic bet.
- [RFD 2216](../2216-threejs-blocklist/) — same "one runtime, not
  two" argument.
- [RFD 2228](../2228-webgpu-native-drop-platform-web/) — reversal
  that flipped delivery to native.
- [RFD 2231](../2231-drop-webgpu-use-vulkan/) — reversal that
  flipped compute/render API to Vulkan.
- RFD 1123 (CineForm in Godot) — Head B's encoder.

This RFD was drafted by an AI and read by a human before it shipped.
