# RFD 2178 details: per-model QAFT 4-bit position

## Per-model table

Compute estimates assume the RTX 3090 (24 GB) and a QAFT fine-tune on
each model's own pretraining data or a distillation-appropriate
substitute. "Fits" = QAFT run fits 24 GB VRAM. "Overnight" = <12 h.
"Multi-day" = >36 h continuous.

| Model | Params | Upstream QAFT? | Class | QAFT compute | Notes |
| --- | ---: | :---: | :---: | --- | --- |
| Gemma-4-12B | 12B | ✓ Q4_0 GGUF (Google) | A | 0 (verbatim) | The anchor case; RFD 1027's canonical example |
| Wan-VACE | 14B | ✗ | C | Multi-day, tight | Doesn't fit 24 GB in QAFT config without heavy gradient checkpointing; parked |
| Pixal3D (image → mesh) | ~24 GB bf16 | ✗ | C | Multi-day, tight | Same 24 GB ceiling; staged inference already at peak; QAFT training doesn't fit |
| VoxHammer | 0 (no weights, RFD 1162) | n/a | n/a | 0 | Nothing to quantize |
| TRELLIS.2 | ~8B | ✗ | B | Overnight | Fits QAFT run at moderate batch |
| MoGe-3 | ~1B | ✗ | B | Hours | Small; trivial run |
| SkinTokens | ~1B | ✗ | B | Hours | Small |
| Kimodo | ~0.6B | ✗ | B | Hours | Small |
| rf-detr-Seg | ~0.2B | ✗ | B | Hours | Very small |
| LaMa (inpainting) | ~0.2B | ✗ | B | Hours | Very small |
| Qwen3-TTS-12Hz-1.7B-Base | 1.7B | ✗ | B | Overnight | Blocks RFD 2167's voice-reward distillation until done |
| Voxtral Mini 3B | 3B | ✗ | B | Overnight | Fits comfortably |
| Whisper large-v3 | 1.55B | ✗ | B | Hours | Small |
| Parakeet TDT 0.6B v3 | 0.6B | ✗ | B | Hours | Small |
| wav2vec2 large | 0.3B | ✗ | B | Hours | Small |
| ipa-whisper (small + base) | ~0.5 GB | ✗ | B | Hours | Small |
| WavLM Base+ SV | ~0.1B | ✗ | B | Minutes | Trivial |
| allosaurus (universal + 27) | ~0.03B | ✗ | B | Minutes | Trivial; per-language head |

## Sequencing

Class-B QAFT rungs, cheapest first, so each result unblocks the next:

1. **Voice-adjacent small models first** -- Qwen3-TTS-1.7B, wav2vec2,
   Parakeet, ipa-whisper. Overnight batch. Unblocks RFD 2167
   (voice-reward distillation) because both the reward LoRA base and
   the TTS candidate generation stop dominating inference cost.
2. **Segmentation + inpainting** -- rf-detr-Seg, LaMa. Hours. Small
   in the compute budget; large in the RFD 1168 layer-decomposition
   path's per-view cost.
3. **Motion + rigging** -- Kimodo, SkinTokens, MoGe-3. Hours each.
4. **Mid-tier vision + audio** -- TRELLIS.2 (~8B), Voxtral (3B),
   Whisper large-v3. Overnight runs.
5. **Class C (Wan-VACE, Pixal3D)** -- parked. Either an upstream Q4
   lands or the workspace acquires >24 GB training capacity.

## Compute cost of the plan

Rough total for Class B (all rungs 1-4): about a week of continuous
3090 wall-time if run serially. Roughly a weekend if parallelised
across a Mac (MPS QLoRA for the smallest) and the 3090 (true QAFT
for the mid-tier). CLAUDE.md's Compute constraint applies: rented
compute stays blocklisted; runs happen on the desktop machine.

## Retraction / adjustment note

RFD 2139 read "no true-QAFT 4-bit checkpoints exist upstream" as
"only Gemma runs QAFT-quantized." That reading conflated "upstream
publishes one" with "the workspace can have one." This RFD splits
those two into Class A vs Class B. Wan-VACE and Pixal3D stay in
Class C, matching RFD 2139's concern for those specific models.
