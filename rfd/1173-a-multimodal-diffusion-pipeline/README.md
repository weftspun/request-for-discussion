# RFD 1173: A multimodal avatar pipeline

**State:** discussion
**Feature:** omni-modal MaskScore construction and real-time avatar
**Scope:** Qwen3-Omni, MaskScore, Pixal3D/VoxHammer, EditScore

## Problem

A real-time avatar demo (Gemma Avatar architecture, 9k+ robots)
needs sub-500ms first-packet latency with text + image + audio.
MaskScore (self-supervised edit scoring) needs a model that handles
all three modalities to construct training data. One model for both.

EditScore is functionally complete in the NAND-gate sense: every
generation task reduces to an edit. One reward covers every modality.

## Decision

Qwen3-Omni for everything. 30B MoE (3B active), Apache 2.0,
234ms first-packet latency, streaming talker with voice cloning.
Handles text, image, audio, and video natively — constructs
MaskScore data and serves the avatar demo with one model.

    thinker     Qwen3-Omni thinker         Apache 2.0   text + image + audio + video
    talker      Qwen3-Omni talker          Apache 2.0   voice-cloning speech
    3D stage    Pixal3D → VoxHammer        Apache 2.0   image → mesh
    scoring     MaskScore + EditScore      —             self-supervised reward

MaskScore constructs edit triples by masking, reconstructing, and
scoring on decoded outputs. The reward model RL fine-tunes the
same Qwen3-Omni that serves deployment.

VRAM budget, sweep results, and the LLaDA retraction are in
[DETAILS.md](DETAILS.md). The seven MaskScore dataset stubs are in
[MASKSCORE.md](MASKSCORE.md).

## Related

RFD 1172, RFD 1166, RFD 1170.
