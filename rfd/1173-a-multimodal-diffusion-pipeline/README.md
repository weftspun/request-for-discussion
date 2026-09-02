# RFD 1173: A multimodal avatar pipeline

**State:** discussion
**Feature:** omni-modal MaskScore construction and real-time avatar
**Scope:** Qwen3-VL, Wan-VACE, MaskScore, Pixal3D/VoxHammer, EditScore

## Problem

A real-time avatar needs a text+image reasoning core that doubles as
the reward model for its own outputs. The audio path is separate per
RFD 1170. EditScore is functionally complete in the NAND-gate sense:
every generation task reduces to an edit, so one reward covers every
modality.

## Decision

Qwen3-VL is the shared VLM: it serves both the avatar's text+image
reasoning path and, as EditScore's own base with a LoRA (RFD 1157),
the reward model that scores its own generations. Wan-VACE fills the
image-generation slot Qwen3-VL leaves open. Audio arrives from RFD
1170's presence loop.

    vlm         Qwen3-VL                    Apache 2.0   text + image → text
    image gen   Wan-VACE                    Apache 2.0   text/image → image
    3D stage    Pixal3D → VoxHammer         Apache 2.0   image → mesh
    audio in    Qwen3-ASR-1.7B              Apache 2.0   waveform → text (RFD 1170)
    audio out   Qwen3-TTS-12Hz-CustomVoice  Apache 2.0   text → waveform (RFD 1170)
    scoring     MaskScore + EditScore       n/a          self-supervised reward

MaskScore constructs edit triples by masking, reconstructing, and
scoring on decoded outputs. The reward model RL fine-tunes the
generators via EditScore.

VRAM budget, sweep results, and the LLaDA retraction are in
[DETAILS.md](DETAILS.md). The eight MaskScore dataset stubs are in
[MASKSCORE.md](MASKSCORE.md).

## Related

RFD 1157, RFD 1166, RFD 1169, RFD 1170, RFD 1171, RFD 1172.
