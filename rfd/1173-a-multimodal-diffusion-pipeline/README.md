# RFD 1173: A multimodal avatar pipeline

**State:** discussion
**Feature:** omni-modal MaskScore construction and real-time avatar
**Scope:** Gemma-4-12B, Wan-VACE, MaskScore, Pixal3D/VoxHammer, EditScore

## Problem

A real-time avatar needs a text+image reasoning core that doubles as
the reward model for its own outputs. The audio path is separate per
RFD 1170. EditScore is functionally complete in the NAND-gate sense:
every generation task reduces to an edit, so one reward covers every
modality.

## Decision

Gemma-4-12B (QAT Q4_0, Apache-2.0) is the shared VLM: it serves both
the avatar's text+image reasoning path and, as EditScore's fine-tune
base (RFD 1157), the reward model that scores its own generations.
Wan-VACE fills the image-generation slot Gemma leaves open. Audio
arrives from RFD 1170's presence loop.

    vlm         Gemma-4-12B (QAT Q4_0)      Apache 2.0   text + image → text
    image gen   Wan-VACE                    Apache 2.0   text/image → image
    3D stage    Pixal3D → VoxHammer         Apache 2.0   image → mesh
    audio in    Qwen3-ASR-1.7B              Apache 2.0   waveform → text (RFD 1170)
    audio out   Qwen3-TTS-12Hz-CustomVoice  Apache 2.0   text → waveform (RFD 1170)
    scoring     MaskScore + EditScore       n/a          self-supervised reward

MaskScore constructs edit triples by masking, reconstructing, and
scoring decoded outputs. The reward model RL fine-tunes generators via EditScore.

Reasoning-core swap 2026-09-02: earlier drafts named Qwen3-VL; RFD
2169 walked that back to Gemma-4-12B. VRAM budget in
[DETAILS.md](DETAILS.md); the eight dataset stubs in
[MASKSCORE.md](MASKSCORE.md).

## Related

RFD 1157, RFD 1166, RFD 1169, RFD 1170, RFD 1171, RFD 1172, RFD 2169.
