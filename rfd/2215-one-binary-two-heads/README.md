# RFD 2215: one binary, two heads

**State:** discussion
**Flight level:** L2 (coordination)
**Feature:** one runtime serves both the marketing video (headless
capture head) and the game (interactive head)
**Scope:** native binary entrypoints for both heads, CineForm video
muxing for the capture head

## Decision

One source tree, one CI workflow, one native binary per platform
(macOS / Windows / Linux), two invocation flags:

- **Head A — game.** Native window; loads Starforged fixture
  (`starforged.sqlite`), calls `taskweft`'s planner (RFD 2205),
  surfaces the decision-point menu via a Godot Control-node VN
  layout, plays reactions on the VRM portrait via
  `Ggml.run_inference()` (RFD 2230) for motion + VRM expressions
  for face.
- **Head B — marketing video.** Headless render pass of the same
  binary. `godot --headless --write-movie shot<NN>.<container> ...`
  captures the runway scene per shot; video muxed via CineForm per
  RFD 1123 (ffmpeg blocklisted, see memory `ffmpeg-blocklisted`).

Same `.tscn` / `.tres` assets, same binary, different invocation
flag.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3
  strategic bet.
- [RFD 2216](../2216-threejs-blocklist/) — same "one runtime, not
  two" argument.
- RFD 1123 (CineForm in Godot) — Head B's encoder.

This RFD was drafted by an AI and read by a human before it shipped.
