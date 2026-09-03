# RFD 1157: EditScore needs its own encoder, not a stock one

**State:** ideation
**Feature:** edge acceleration candidate
**Scope:** `3-interactor/editscore`

## Decision

EditScore requires an encoder built with its merger LoRA merged; a
downloaded artifact is wrong in a way no shape check catches. Time
encode against decode first: RFD 1163 measures a score at 28-36 s
against a 163 s round, and the encoder is a fraction of that. This
ranks second at 18 of 25 with `value` 2 of the 18.

## Problem

EditScore is not a model. It is a LoRA over Qwen3-VL, and
`3-interactor/llama-cpp-npu-vision-upstream` accelerates that family:
a compiled encoder replaces the mmproj, decode stays on host. The
deployed size is the 8B, at 6.75 GiB NF4 in `weft_score.py`. Four
bits fit 8 GB and eight land on the ceiling, so this meets RFD 1128
after all.

The adapter holds 516 tensors at either size: 504 language-model
layers and 12 at `deepstack_merger_list.{0,1,2}.linear_fc{1,2}`,
with no `visual.blocks.*`, so the ViT is stock.

Whether that matters turns on where the compiled part ends, and
`tools/mtmd/clip.cpp:3850` answers it:

    // Hailo HEF replaces ViT + projector, so mm_* tensors are not loaded.

The projector is inside the artifact and the GGUF's `mm_*` tensors
are never read, so a stock encoder carries stock mergers and
EditScore's 12 are never applied. The failure is silent: a score
comes back from a model missing that adaptation.

## Related

RFD 1155 ranks the other family. RFD 1163 places both.
