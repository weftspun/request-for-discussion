# RFD 2199 doc-only survey: Hailo-10H INT4, DFC compilation path, catalog fit

Task #62 in the coordinator queue. RFD 2199 scopes real 4-bit QAT with
Hailo as target hardware. Un-park directive named "compile + measure
on-catalog model" as the use case. On-device work waits on operator
firmware recovery of a stuck-bootloader USB; this survey covers the
doc-only prerequisite phase: does the hardware do INT4, does DFC produce
an INT4 HEF, does the vendor's INT4 workflow line up with the workspace's
real-QAT stance, and which RFD 1102 catalog models fit as compile targets.

## Hailo-10H hardware

INT4 is a first-class datatype on the part. Product page states
`40 | 20 TOPS (INT4 | INT8)`: 40 TOPS at INT4, 20 TOPS at INT8, 2×
throughput at INT4. Positioned by Hailo as the enabling datatype for
"immersive generative AI at the edge."

Concrete deployed example: **Qwen2-1.5B-Instruct** runs on Hailo-10H at
"Static, 4-bit symmetric, group-wise" weight quantization, with 1.2 GB
memory for weights and a 2048-token KV cache.

## DFC compilation path to INT4

Two techniques fused into the DFC Model Optimization stage produce the
INT4 HEF:

- **QuaROT**, a Hadamard rotation of weight matrices that pushes outliers
  into a rotated basis so they quantize cleanly.
- **GPTQ**, one-shot post-training quantization using approximate
  second-order information.

Both are **post-training** methods running against a trained bf16 (or
fp16) checkpoint at Model Optimization time. DFC's LLM path is
PTQ-first: the compiler takes bf16 weights and produces the INT4 HEF
without a training loop.

DFC also ships a `DFC_6_QAT_Tutorial.ipynb`, so a QAT path does exist,
separate from the LLM PTQ tools. The community forum has an open thread
titled *"DFC parser cannot parse a Tensorflow model trained with
Quantization aware training (QAT)"*, so the QAT path is functional but
has parser gotchas depending on the training framework.

**Model zoo:** `gh code-search q=int4 repo:hailo-ai/hailo_model_zoo`
returns one hit in an unrelated 3D correspondence helper. The zoo does
not currently ship any INT4-configured model; every zoo config in scope
still targets INT8. INT4 is a compiler capability, not a shipped baseline.

## Conflict with the workspace's real-QAT stance

RFD 2199 exists because the workspace's blocklist rules out precisely
what Hailo's LLM INT4 path is:

| blocklist row (CLAUDE.md)                                       | Hailo INT4 LLM path        |
| --------------------------------------------------------------- | -------------------------- |
| Post-training quantization (train-then-quantize, no QAT loop)   | **GPTQ** step in DFC       |
| Post-quantization fine-tuning (quantize-first, adapt-after)     | orthogonal, not this path  |
| bnb NF4 4-bit as a QAFT / QAT path                              | orthogonal                 |

Hailo's LLM path is the "train bf16, then GPTQ" shape the workspace
blocklists. QuaROT is a weight-rotation preprocessor to that
GPTQ step; it does not turn the pipeline into QAT. The **Hailo Model
Optimization stage as the source of INT4 weights** violates the
blocklist for the LLM case.

Three ways this can resolve:

1. **Vision model, not LLM.** The `DFC_6_QAT_Tutorial` path is available;
   pick a small ViT/CNN target, do real QAT on GPU (workspace-owned
   compute), then feed the QAT'd model to DFC as a QAT-imported model
   (not through the LLM Model Optimization path). Feasibility depends on
   DFC accepting pre-quantized weights via the QAT tutorial's flow;
   community thread shows this is not always frictionless.
2. **Operator override on the blocklist for the LLM path.** RFD-level
   decision, not this survey's call. Would treat Hailo's GPTQ+QuaROT as
   a vendor-specific carve-out on the blocklist, comparable to how
   `ggml`/GGUF is blocklisted with an exemption for a vendor's own
   on-device runtime.
3. **Fork / bypass Model Optimization.** Feed already-QAT-trained INT4
   weights into DFC downstream of Model Optimization. Undocumented in
   the sources surveyed; would require Hailo support engagement.

## Catalog-model fitness for compile target

Per RFD 1102 + MPS's earlier candidate list (rf-detr-Seg, MoGe-3;
MobileNetV3-Small was flagged as off-catalog). Fit against the survey
findings:

| model         | modality  | ~params      | INT4 path                                      | verdict for RFD 2199 spike                             |
| ------------- | --------- | -----------: | ---------------------------------------------- | ------------------------------------------------------ |
| rf-detr-Seg   | vision    | ~30-100 M    | `DFC_6_QAT_Tutorial` (real QAT on GPU → HEF)   | **Best fit.** On-catalog, vision, small enough to iterate. |
| MoGe-3        | depth     | ~300 M-1 B   | same QAT path in principle; arch support unproven | **Second candidate.** Larger; DFC arch support to verify. |
| Qwen2-1.5B    | LLM       | 1.5 B        | DFC LLM path (QuaROT+GPTQ, blocklisted)         | **Blocked** on real-QAT stance without operator override.  |

`rf-detr-Seg` is the recommendation for the first spike: on-catalog,
vision, small enough to iterate on the QAT loop, and takes DFC's
QAT-tutorial path rather than the blocklisted LLM PTQ path.

## What this survey does not cover

- Whether the `DFC_6_QAT_Tutorial` accepts a QAT-trained checkpoint
  produced outside its own harness (e.g., from a workspace-owned QAT
  loop using torchao's `Int4WeightOnlyQuantizer` with STE backward). The
  community forum thread suggests the parser is picky; needs a
  local-with-DFC-installed check.
- Actual INT4 accuracy vs bf16 baseline on `rf-detr-Seg` (or any
  workspace model). Hailo's blog claim of "1-2 points" is against their
  own LLM benchmarks, not our vision models.
- Hailo-10H **USB variant** vs the M.2 module. Product page's 40|20 TOPS
  figure is for the module; the USB device this session's HAILO owns
  under `usb-hailo-npu` is presumably the same silicon but was not
  cross-referenced in the survey. Firmware recovery is the pending
  precondition anyway.
- Currently-shipped mtmd Hailo path precision, checked locally in
  `weftspun/llama-cpp-npu-vision-upstream` at `d75e441df`
  (`tools/mtmd/hailo/hailo_encoder.cpp`): the encoder sets only the
  **output binding** to `HAILO_FORMAT_TYPE_FLOAT32` and touches nothing
  about internal precision. Whether the HEF runs at INT4 or INT8
  internally is a DFC-time decision baked into the HEF, invisible to the
  runtime. Currently only Qwen3-VL is wired up on this backend.

## Reproducer

External sources surveyed 2026-09-04:
- `hailo.ai/products/hailo-10h/` for the datatype claims (40 | 20 TOPS INT4 | INT8).
- `hailo.ai/blog/bringing-generative-ai-to-the-edge-llm-on-hailo-10h/` for QuaROT + GPTQ + the Qwen2-1.5B example.
- `community.hailo.ai/t/dfc-parser-cannot-parse-a-tensorflow-model-trained-with-quantization-aware-training-qat/138` for the QAT parser gotcha.
- `github.com/hailo-ai/hailo_model_zoo` (code search `int4`, 1 hit unrelated), no shipped INT4 zoo baselines.

Local sources:
- `3-interactor/llama-cpp-npu-vision-upstream/docs/multimodal-hailo.md`.
- `3-interactor/llama-cpp-npu-vision-upstream/tools/mtmd/hailo/hailo_encoder.{cpp,hpp}` at `d75e441df`.

## Recommendation to the coordinator

Proceed with RFD 2199 on-device work targeting **rf-detr-Seg** as the
first compile-and-measure model, via DFC's QAT-tutorial path fed by a
workspace-owned QAT loop. Defer the LLM INT4 case (Qwen2-1.5B or
larger) until either an operator override on the PTQ blocklist lands,
or a bypass of DFC's Model Optimization stage becomes available. Both
routes are RFD-level decisions.

Un-park precondition for on-device work stays with operator: USB in
stuck bootloader per CUDA's earlier probe, recoverable by admin
PowerShell + `hailo_usb_loader.exe fw-update` + physical cable cycle.
