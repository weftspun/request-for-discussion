# RFD 1170: A cleanroom presence loop, and which components swap

**State:** ideation
**Feature:** people present to each other
**Scope:** `3-interactor/anny`, `3-interactor/llama-cpp-npu-vision-upstream`

## Decision

Study it, take nothing, rebuild from the components it names — cheap,
because **every component is separately licensed and clean; only the
glue is unlicensed.**

    their stage        licence      ours

    silero-VAD         MIT          keep
    parakeet-tdt-1.1b  CC-BY-4.0    Qwen3-ASR-1.7B, Apache-2.0
    gemma-4-31B, API   Apache-2.0   Qwen3-VL-8B, local
    Qwen3-TTS 12Hz     Apache-2.0   already ours
    TalkingHead        MIT          keep, or ANNY through Godot
    three.js           MIT          Godot, with Mitsuba as oracle

**Their TTS choice is ours, independently** — the same
`Qwen3-TTS-12Hz-1.7B-CustomVoice` RFD 1166 seated at 4 the same day.

**Two stages swap for reasons already held here.** Parakeet is
licence-clean but has no compiled path, while RFD 1169 puts Qwen3-ASR's
encoder inside `DEVICE_OPS`. Gemma 4 is Apache-2.0 — RFD 1155 abandoned
it on shape, not licence — but 31 B does not fit 8 GB and a hosted API
cannot be a corpus source. **The lip-sync is the part we lack**, and
`DETAILS.md` carries what TalkingHead does and what is unknown.

## Problem

`victor/gemma-avatar` runs the loop this workspace wants — speak, be
understood, be answered by a lip-syncing face — and states **no
licence**. Its integration code cannot be taken.

## Related

RFD 1169 supplies the ear and the voice. RFD 1155 abandoned Gemma 4.
