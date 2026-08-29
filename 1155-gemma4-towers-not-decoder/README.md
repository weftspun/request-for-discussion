# RFD 1155: Gemma 4 reaches the device as towers, not as a decoder

**State:** abandoned
**Feature:** edge acceleration candidate
**Scope:** `3-interactor/gemma4-composer`

## Problem

Gemma 4 is wanted for language, vision and sound in one model. At
12 B it is 6.60 GB at four bits and does not fit at any other
precision, so it inherits RFD 1128's open question.

Two things stop it that memory does not see. The checked-out
artifact is GGUF, which carries no graph, so nothing converts. And
autoregressive decode grows its sequence and cache every token while
a dataflow part compiles fixed shapes, which is the obstacle RFD
1126 names: control flow rather than precision.

## Decision

Abandoned on 2026-08-28. The accelerator work is scoped to rf-detr
keypoint and RFD 1157. Gemma 4 ranked last at 4 of 25 against that
model's 18, scoring zero on shape, reference and clear at once, and
the gap is a reference implementation.
`3-interactor/llama-cpp-npu-vision-upstream` compiles an encoder for
Qwen3-VL and nothing else, and RFD 1157's model sits on that family.
One encoder serves both, where Gemma 4 needs its own with no
precedent. Qwen3-VL-4B is also comfortable at eight bits, so it
never meets the four-bit question.

What Qwen3-VL does not carry is sound. If audio is a requirement it
does not replace Gemma 4, and no Hailo reference for an audio model
is known here. If Gemma 4 returns, plan the towers and not the
decoder.

## Related

RFD 1157 holds the family that has a path. RFD 1126 names the
obstacle. RFD 1131 cuts the graph.
