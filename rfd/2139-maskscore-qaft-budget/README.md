# RFD 2139: MaskScore QAFT and extraction budget

**State:** discussion
**Feature:** QAFT quantization and dataset extraction for MaskScore
**Scope:** Qwen3-Omni, OmniGen2, Pixal3D, VoxHammer, MoGe-3, Vast.ai budget

## Problem

The MaskScore extraction pipeline (RFD 1173) needs seven models
co-resident on GPU. At published precision (bf16), VoxHammer
alone requires 40 GB. QAFT to NF4 is required before extraction
can begin. Condition 5 permits this: QAFT makes NF4 the published
precision.

## Decision

QAFT all seven pipeline models to NF4. Fork each upstream model
on HF. Cache pipeline latents in a satellite table for
pretraining.

### Architecture: forked base with QAFT checkpoint

Each upstream model is forked to chibifire/ on HF. The fork
stores:

1. the original bf16 weights (upstream copy, for provenance)
2. the QAFT'd NF4 checkpoint (merged, the working base)
3. future adaptations as LoRAs on the NF4 base

QAFT produces a merged NF4 checkpoint, not a LoRA. The NF4
checkpoint is the new base. Only post-QAFT work (RL, domain
adaptation) is stored as LoRA adapters against it.

### Models to QAFT

| model                         | params | bf16    | NF4 est. | where        | HF fork              |
|-------------------------------|--------|---------|-----------|--------------|-----------------------|
| Qwen3-Omni thinker (30B MoE) | ~30B   | ~30 GB  | ~9.3 GB   | Vast.ai A100 | chibifire/qwen3-omni  |
| Qwen3-Omni talker             | ~10B   | ~10 GB  | ~2.5 GB   | Vast.ai A100 | (same repo)           |
| OmniGen2                      | ~5B    | ~10 GB  | ~3.1 GB   | Vast.ai A100 | chibifire/omnigen2    |
| Pixal3D (8 subs)              | ~4B    | ~8 GB   | ~2.5 GB   | Vast.ai A100 | chibifire/pixal3d     |
| VoxHammer                     | TBD    | 40 GB+  | TBD       | Vast.ai A100 | chibifire/voxhammer   |
| MoGe-3 (ViT-L)               | ~300M  | ~600 MB | ~190 MB   | local Mac    | chibifire/moge3       |
| ANNY inverter                 | small  | small   | skip      | n/a          | n/a                   |

ANNY is a small vertex correspondence fitter; Mitsuba 3 is a
physics-based renderer. Neither needs QAFT.

### Extraction ladder (Gall's Law)

Each rung proves the next is worth building.

| rung | trials | rows   | GPUs             | est. hours | est. cost | proves                               |
|------|--------|--------|------------------|------------|-----------|--------------------------------------|
| -1   | 0      | 0      | 1x A100 80GB     | ~8         | ~$12      | QAFT all models to NF4               |
| 0    | 1      | 8      | 1x A100          | minutes    | ~$0.03    | extraction script runs, 8 stubs emit |
| 1    | 13     | ~104   | same             | ~15 min    | ~$0.38    | all 13 task types construct          |
| 2    | 130    | ~1040  | same             | ~2 hr      | ~$3       | scoring separates good from bad      |
| 3    | 390    | ~3120  | same             | ~6 hr      | ~$9       | usable bench set                     |
| 4    | 12k    | ~97k   | 9x RTX 3090      | ~8 hr      | ~$14      | reward-train complete                |
| 5    | 14k    | ~210k  | 18x RTX 3090     | ~8 hr      | ~$29      | all three datasets complete          |

### Cached latent satellite

The main dataset tuple stays (face_image, depth, keypoints, pose,
waveform). A satellite table caches the pipeline latents per ETNF
(derivable columns go in their own relation):

    maskscore_latents/
      pixal3d_slat.parquet
      omnigen2_latent.parquet
      qwen3_embed.parquet

Each satellite records the QAFT base version that produced it.
The latents support pretraining the reward model before RL,
where recomputing them on every batch is wasteful.

### Cost summary

| line item                              | cost           |
|----------------------------------------|----------------|
| QAFT all models to NF4 (rung -1)      | ~$12           |
| MoGe-3 QAFT                           | $0 (local Mac) |
| Rungs 0 through 3 (same A100 session)  | ~$13           |
| Rung 4 (9x RTX 3090 spot, 8 hr)       | ~$14           |
| Rung 5 (18x RTX 3090 spot, 8 hr)      | ~$29           |
| **Total**                              | **~$68**       |

### Vast.ai tear-down discipline

Per the working agreements: commit and push before tear down,
then double-check the tear down. The extraction script pushes
parquet to HF after each batch, so a torn-down machine loses
at most one batch, not the full run.

### HF artifacts

| artifact                         | type    | purpose                        |
|----------------------------------|---------|--------------------------------|
| chibifire/qwen3-omni             | model   | bf16 + QAFT NF4 base          |
| chibifire/omnigen2               | model   | bf16 + QAFT NF4 base          |
| chibifire/pixal3d                | model   | bf16 + QAFT NF4 base          |
| chibifire/voxhammer              | model   | bf16 + QAFT NF4 base          |
| chibifire/moge3                  | model   | bf16 + QAFT NF4 base          |
| chibifire/maskscore-bench        | dataset | evaluation (~2890 rows)        |
| chibifire/maskscore-reward-train | dataset | reward model training (~97k)   |
| chibifire/maskscore-rl-train     | dataset | RL training (~110k)            |

### What is NOT in this budget

* SpeakingFaces download (already on local compute)
* The reward model training itself (rung 5 produces data, not a model)

## Related

RFD 1173 (the pipeline design), RFD 1143 (keypoints to ANNY).
