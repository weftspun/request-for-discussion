# RFD 1173: A multimodal avatar pipeline

**State:** discussion
**Feature:** omni-modal MaskScore construction and real-time avatar
**Scope:** Qwen3-Omni, Wan-VACE, MaskScore, Pixal3D/VoxHammer, EditScore

## Problem

A real-time avatar demo (Gemma Avatar architecture, 9k+ robots)
needs sub-500ms first-packet latency with text + image + audio.
MaskScore (self-supervised edit scoring) needs models that handle
all modalities to construct training data.

EditScore is functionally complete in the NAND-gate sense: every
generation task reduces to an edit. One reward covers every modality.

## Decision

Qwen3-Omni for understanding, text, and speech. Wan-VACE for image
generation and editing. Qwen3-Omni outputs text and audio only; it
does not generate images.

    thinker     Qwen3-Omni thinker         Apache 2.0   text + image + audio + video → text
    talker      Qwen3-Omni talker          Apache 2.0   voice-cloning speech
    image gen   Wan-VACE                   Apache 2.0   text/image → image
    3D stage    Pixal3D → VoxHammer        Apache 2.0   image → mesh
    scoring     MaskScore + EditScore      n/a           self-supervised reward

MaskScore constructs edit triples by masking, reconstructing, and
scoring on decoded outputs. The reward model RL fine-tunes the
generators via EditScore.

VRAM budget, sweep results, and the LLaDA retraction are in
[DETAILS.md](DETAILS.md). The eight MaskScore dataset stubs are in
[MASKSCORE.md](MASKSCORE.md).

## Related

RFD 1172, RFD 1166, RFD 1170.
