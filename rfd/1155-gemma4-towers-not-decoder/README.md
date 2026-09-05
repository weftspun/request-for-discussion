# RFD 1155: Gemma 4 reaches the device as towers, not as a decoder

Abandoned on 2026-08-28. The accelerator work is scoped to rf-detr
keypoint and RFD 1157. Gemma 4 ranked last at 4 of 25 against that
model's 18, scoring zero on shape, reference and clear at once, and
the gap is a reference implementation.
`3-interactor/llama-cpp-npu-vision-upstream` compiles an encoder for
Qwen3-VL and nothing else, and RFD 1157's model sits on that family.
One encoder serves both, where Gemma 4 needs its own with no
precedent. Qwen3-VL-4B is also comfortable at eight bits, so it
never meets the four-bit question.

**State:** abandoned

This RFD was drafted by an AI and read by a human before it shipped.
