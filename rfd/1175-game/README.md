# RFD 1175: game

**State:** discussion
**Flight level:** L3

## Decision

There is one demo: the game. A player opens a native window on the
operator's desktop, plays the Starforged decision-point VN with a
VRM portrait as the interlocutor, and a planner supplies the legal
moves at each decision point.

The "video" is the same game invoked with `--headless
--write-movie` and a script that walks a shot list. Same source
tree, same binary, same `.tscn` / `.tres` assets. Whatever gets
posted as a marketing video is the game recorded; not a second
deliverable.

Encoder is CineForm (ffmpeg blocklisted, see memory
[[ffmpeg-blocklisted]]).

## Scope

Godot as the runtime, Vulkan as the renderer, ggml for inference,
CineForm for the encoder. Implementation lands as commits in the
respective code repos when the work is done.

This RFD was drafted by an AI and read by a human before it shipped.
