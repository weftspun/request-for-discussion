# RFD 2185: Flow-LCM + QAFT-nf4 combined distillation for Lumina-Image-2.0

**State:** discussion
**Feature:** produce a Lumina-Image-2.0 few-step nf4-quantized LoRA in one
training loop — sampling-trajectory compression AND quantization-loss recovery
learned together, not sequentially
**Scope:** `3-interactor/omnigen2/artifacts/lumina2-distill/`; deliverable is
one LoRA weight file that loads over `Alpha-VLLM/Lumina-Image-2.0` in nf4

## Problem

Session 2026-09-02/03 measured Lumina-Image-2.0 on the 3090:

| Config | Steps | Wall (1024²) | VRAM peak |
|---|---|---|---|
| bf16, no offload | 30 | 31.6 s | 13.19 GB |
| nf4 (bnb, transformer-only) | 30 | 33.9 s | 9.33 GB |

nf4 cuts VRAM by 3.86 GB at the cost of 2.3 seconds. It does NOT reduce
step count. Independently, a Lightning-style distill LoRA
(`qpqpqpqpqpqp/Lumina_Image_2.0_Distill_Lora`) exists in the community
but is trained against a DMD checkpoint (`heziiiii/lu2_lightning_test`)
whose loading isn't drop-in — a `noise_refiner` module in the DMD base
that vanilla Lumina2 doesn't have. Neither knob, alone, satisfies the
combined constraint the workspace actually wants: **fewer steps, smaller
weights, one artefact**.

Doing the two sequentially — distill first at bf16, then quantize to
nf4 — has a known failure mode: the quantization noise is applied AFTER
the LoRA has learned to correct for bf16 noise levels, so the LoRA does
not correct for the nf4-specific rounding error. QAT literature (QLoRA
et al.) demonstrates that co-training LoRA against a QUANTIZED base is
strictly better than fine-tuning at fp16 then quantizing.

## Decision

Combined **Flow-LCM + QAFT-nf4** training loop, one artefact:

- **Teacher:** vanilla `Alpha-VLLM/Lumina-Image-2.0` transformer in bf16,
  frozen. Runs the reference forward that defines the target sampling
  trajectory.
- **Student:** the same transformer weights loaded in nf4 via
  `bitsandbytes` (fast Q4 kernel active because `hidden_size=2304`
  is 64-aligned; measured this session at 1.13 s/step). A fresh LoRA
  (rank 32, targeting `to_q`/`to_k`/`to_v`/`to_out.0`) sits on top; only
  the LoRA trains.
- **Both share** the bf16 text encoder and VAE — those components are
  frozen in both roles, no reason to duplicate.
- **Loss:** endpoint-consistency in flow-matching parameterization.
  For sampled `(t, dt)`:

  ```
  x_t   = (1 - t)   * x_0 + t   * noise
  x_tdt = (1 - tdt) * x_0 + tdt * noise           # tdt = t + dt
  v_teacher = teacher(x_tdt, tdt)   # stopgrad
  v_student = student(x_t,   t)
  x0_teacher = x_tdt - tdt * v_teacher
  x0_student = x_t   - t   * v_student
  loss = huber(x0_student, stopgrad(x0_teacher))
  ```

  Enforces the LCM invariant "predicted endpoint should be constant
  along the flow trajectory," adapted for flow matching's velocity
  parameterization. Standard LCM's DDPM-native math doesn't apply here
  because Lumina2 predicts velocity `v`, not noise `epsilon`.

### VRAM budget (measured / estimated)

| Component | GB |
|---|---|
| Text encoder (Gemma2-2B, bf16, shared) | ~5 |
| VAE (bf16, shared) | ~0.2 |
| Teacher transformer (bf16) | 8 |
| Student transformer (nf4) | 4 |
| LoRA weights + AdamW state (rank 32) | ~0.5 |
| Activations at 512², batch 1 | ~2 |
| **Total** | **~20 GB** |

Fits 24 GB card with ~4 GB headroom. The bf16 teacher is the largest
single VRAM cost; if training OOMs, first cut is to move teacher to
`enable_model_cpu_offload()` (adds ~2× per-step penalty, still fits).

### Smoke run

- 1000 prompts (deterministic subset of `EditScore-Reward-Data/train`,
  `text_change` parked per memory `parked-language-to-vision-edit-pair`)
- LoRA rank 32, batch 1, 512², 1 epoch (~1000 steps)
- Expected wall clock: 1-3 hours
- **Success criterion:** loss monotonically decreases, no NaN. Produces
  a LoRA that reduces step count from 30 to ~8 at nf4 with acceptable
  quality vs the bf16-30-step baseline.

Not a shippable LoRA — the smoke uses random-latent `x_0` as a proxy for
real image latents. A shippable LoRA needs real image latents from the
same pipeline's VAE encoder (see "Follow-up" below).

## Verification

- **Loss curve:** written to `losses.txt` alongside the LoRA weights.
  Monotone decrease across the epoch is the smoke's pass criterion.
- **Inference gate:** after the smoke lands, load the LoRA over nf4-base
  Lumina2 and generate the same prompt/seed we measured the bf16-30-step
  baseline on. Compare visually AND with EditScore-7B (via the pilot
  harness) on a stratified n=10 prompt subset. Two axes reported side
  by side (rule 4):

  | Config | Steps | Wall | EditScore.overall |
  |---|---|---|---|
  | bf16, no LoRA (baseline) | 30 | 31.6 s | (measure) |
  | nf4, no LoRA | 30 | 33.9 s | (measure) |
  | **nf4 + this LoRA** | **8** | (measure) | (measure) |

- **Negative control (rule 2):** load a randomly-initialized LoRA of the
  same rank onto nf4 base, generate. Must produce noticeably worse
  output than the trained LoRA on the same prompt/seed. If not, the
  training loop's contribution is not distinguishable from noise.

## Related

- **RFD 2184** (sdcpp port): orthogonal — that RFD lands OmniGen2 into a
  ggml-native runtime; this RFD lands a distilled+quantized LoRA over
  vanilla Lumina2 in diffusers. Complementary if we choose to also port
  the distilled artefact through sdcpp, but neither depends on the other.
- **RFD 1173** (multimodal avatar pipeline): the presence-loop generator
  slot benefits from any speedup this LoRA delivers.
- Memory: [[parked-language-to-vision-edit-pair]] (dataset filter),
  [[three-model-vram-serialization]] (VRAM budget precedent),
  [[editscore-api-surface]] (scorer for the inference gate).

## What is NOT in this RFD

- **Shippable LoRA training on real image latents.** The smoke uses
  random `x_0` as a proxy to prove the loop mechanics. Shipping needs a
  real-image dataset (LAION-COCO, X2I2, or workspace-owned renders) plus
  ~24-hour training. Comes after the smoke lands.
- **Full LCM formulation with boundary conditions.** The smoke's loss
  is the middle piece — proper LCM adds constraints at `t=0` (student
  must be an identity) and typically uses an EMA teacher instead of the
  fixed base. Both improve convergence but aren't necessary to measure
  whether the plumbing runs.
- **Higher-rank LoRAs (128, 256).** Rank 32 for the smoke keeps
  parameter count small and training fast. Production LoRA sizing waits
  on the smoke's data.

This RFD was drafted by an AI and read by a human before it shipped.
