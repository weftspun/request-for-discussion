# RFD 1175: video and game demo

**State:** discussion
**Flight level:** L3

## Decision

One native binary produces both demos:

- **Game demo (interactive).** A native window on the operator's
  desktop opens the Starforged decision-point VN. The player IS
  the caller; the VRM portrait is the interlocutor; a planner
  supplies the legal moves for each decision point.
- **Video demo (headless capture).** The same binary run as
  `--headless --write-movie` captures the scene per shot; the
  encoder is CineForm (ffmpeg blocklisted, see memory
  [[ffmpeg-blocklisted]]).

Same source tree, same binary, same `.tscn` / `.tres` assets, one
invocation flag distinguishes the heads. The video is what the
game looks like when you run it deterministically over a shot list.

## Scope

Godot as the runtime, Vulkan as the renderer, ggml for inference,
CineForm for the encoder. Concrete implementation lands as commits
in the respective repos when the work is done, not as forward-
looking RFDs.

This RFD was drafted by an AI and read by a human before it shipped.
