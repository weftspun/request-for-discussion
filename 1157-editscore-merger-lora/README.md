# RFD 1157: EditScore needs its own encoder, not a stock one

**State:** ideation
**Feature:** edge acceleration candidate
**Scope:** `3-interactor/editscore`

## Problem

EditScore is not a model. It is a LoRA over `Qwen3-VL-4B-Instruct`,
and `3-interactor/llama-cpp-npu-vision-upstream` accelerates that
family: a compiled encoder replaces the mmproj, decode stays on host.

The adapter holds 516 tensors. 504 are language-model layers, and
12 are `visual.deepstack_merger_list.{0,1,2}.linear_fc{1,2}`. No
`visual.blocks.*` appears, so the ViT itself is stock.

Whether that matters turns on where the compiled part ends, and
`tools/mtmd/clip.cpp:3850` answers it:

    // Hailo HEF replaces ViT + projector, so mm_* tensors are not loaded.

The projector is inside the artifact and the GGUF's `mm_*` tensors
are never read, so a stock encoder carries stock mergers and
EditScore's 12 are never applied. The failure is silent: shapes
match, the pipeline runs, and a score comes back from a model
missing the adaptation on the path that carries visual evidence
into the decoder.

## Decision

EditScore requires an encoder built with its merger LoRA merged; a
downloaded artifact is wrong in a way no shape check catches. Time
encode against decode before building it. The encoder runs once per
image; the decoder emits up to 512 tokens twice per score. This
ranks second at 18 of 25, and `value` is 2 of that 18: the easiest
candidate to accelerate, and among the least worth accelerating.

## Related

RFD 1155 ranks the other multimodal family. RFD 1131 cuts the graph.
