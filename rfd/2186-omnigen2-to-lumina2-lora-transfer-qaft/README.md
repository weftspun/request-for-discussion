# RFD 2186: Transfer OmniGen2's image-edit capability into a Lumina2 LoRA via QAFT-4bit

**State:** discussion, feasibility probe scoped
**Feature:** move OmniGen2's slow-but-image-edit-capable behaviour into
Lumina2's fast-but-text-to-image-only runtime, via distillation loss on
paired (source, instruction, OmniGen2-edit) triples, LoRA on nf4-quantized
Lumina2 base
**Scope:** `3-interactor/omnigen2/artifacts/lumina2-distill/o2_teacher/`;
deliverable is a Lumina2 LoRA that turns Lumina2 into an image editor

## Problem

Measured this session:

| Model | Task | Wall (1024²) |
|---|---|---|
| OmniGen2 (image edit native, bf16 + sequential offload) | source + instruction → edit | ~12 min |
| Lumina2 bf16 | text prompt → image | 31.6 s |
| Lumina2 nf4 (RFD 2185 base) | text prompt → image | 33.9 s |
| Lumina2 nf4 + Flow-LCM LoRA (RFD 2185 output) | text prompt → image, 8 steps | 11.3 s |

**OmniGen2 is 65× slower than Lumina2** for the workspace's actual need
(image editing per MaskScore's methodology). Both are Lumina2-family
architectures (verified in this session — OmniGen2 imports
`block_lumina2` primitives), so a distillation from teacher to student
inside the same family is at least architecturally plausible.

The workspace has none of the obvious speedup paths open:
- FLUX.1-Kontext (fast edit model) — CLAUDE.md blocklists it (licence)
- Qwen-Image-Edit — CLAUDE.md blocklists it (corrupts under quantisation)
- calcuis's OmniGen2 GGUF — ComfyUI-only, days of integration
- stable-diffusion.cpp port of OmniGen2 (RFD 2184) — days, and even
  ported the DiT still runs iterative diffusion; no reason to expect
  <60 s per 1024² edit

**Load-bearing question this RFD asks the probe to answer:** can a
Lumina2+LoRA distilled against OmniGen2 outputs learn image-editing
capability *at all*? Lumina2 has no image-input path in its
architecture; a LoRA on Q/K/V/O may not have the capacity to add a
new conditioning modality. Only measurement can tell.

## Decision

Two-stage feasibility probe. **Do not** commit to a full training run
until stage 2 shows a signal.

### Stage 1: OmniGen2 teacher-edit generation

Pre-generate a small cache of `(source, instruction, teacher_edit)`
triples using OmniGen2 as teacher on real sources from
`EditScore-Reward-Data`'s shard 00.

- **n = 10 triples** (probe only — see "What is NOT in this RFD")
- Sources: stratified across the 10 non-parked task_types the pilot
  already uses (`background`, `color_alter`, `material_alter`,
  `motion_change`, `ps_human`, `style`, `subject_add`, `subject_remove`,
  `subject_replace`, `tone_transfer`)
- Written to `artifacts/lumina2-distill/o2_teacher/*.png` alongside a
  `triples.parquet` recording (source_path, instruction, teacher_path,
  task_type, seed)
- Wall clock: ~10 × 12 min = **~2 hours** at OmniGen2's measured
  bf16-offload speed

### Stage 2: Lumina2+LoRA training on the teacher cache

- **Teacher:** cached triples from Stage 1 (no OmniGen2 loaded during
  training — VRAM budget wouldn't fit both)
- **Student:** Lumina2 nf4 (bnb `load_in_4bit`) + LoRA rank 64
  (higher rank than RFD 2185's 32 because we're adding a NEW capability,
  not merely accelerating an existing one)
- **Loss framing:** SDEdit-shaped image editing
  - VAE-encode source → source_latent
  - Add flow-matching noise at t=0.5 to source_latent → x_0.5
  - Student's LoRA-modified Lumina2 denoises from x_0.5 conditioned on
    instruction
  - MSE loss between student's denoised latent and
    VAE-encode(teacher_edit)
- **Epochs:** 10 (n=10 triples × 10 = 100 gradient steps — enough to
  see loss trend, not enough to converge)
- Wall clock: ~30 min

### Stage 3: Score gate (per rule 4, baseline in the same table)

Per memory `pq-only-single-image-blocklisted`: pairwise EditScore only,
never PQ-only. For each of the 10 triples, generate the edit with each
of three configs and score:

| Config | Steps | Expected wall | Expected EditScore.overall |
|---|---|---|---|
| OmniGen2 (teacher) | 50 | 12 min | (measure — this IS the reference) |
| Lumina2 nf4 + this LoRA (student) | 8 | ~15 s | (measure — the gate) |
| Lumina2 nf4 NO LoRA baseline | 8 | ~11 s | (measure — negative control per rule 2) |

**Pass criterion:** student's mean `overall` reaches ≥ 50% of teacher's,
AND the student meaningfully outperforms the no-LoRA control. If yes,
capability transfer is possible in principle and warrants a full
training run (~n=1000+ triples, ~2-10 days GPU). If no, this direction
is closed and RFD 2184's sdcpp port remains the OmniGen2 speedup plan.

## Verification

- Stage 1 counts triples generated vs 10 targeted (rule 3 — silent
  skip is a fail). Any generation failure names the task_type + source.
- Stage 2 emits a loss curve to `losses.txt`. Monotone decrease over
  100 steps is the plumbing check.
- Stage 3 reports the three-row table above. A CI that crosses the
  teacher's mean is written as "student not distinguishable from
  teacher within noise" — good if the teacher was strong.

## Related

- **RFD 2184** (sdcpp OmniGen2 port): the parallel speedup path.
  Complementary; either can land without the other.
- **RFD 2185** (Flow-LCM + QAFT-nf4 for Lumina2): established the
  training mechanism (nf4 base + LoRA + distillation loss) this RFD
  extends to a different loss objective (image-edit distillation
  instead of endpoint consistency).
- Memory: [[editscore-api-surface]], [[pq-only-single-image-blocklisted]],
  [[three-model-vram-serialization]].

## What is NOT in this RFD

- **The full training run.** n=10 is a plumbing probe. A shippable
  LoRA needs n=1000+ real triples, careful sampling of instruction
  types, and boundary conditions at the SDEdit noise level. Comes
  after the probe passes.
- **Higher-rank LoRAs (128, 256) or added text-encoder-cross-attention
  LoRAs.** The probe tests rank 64 on Q/K/V/O only; if the LoRA
  demonstrates capacity limitations we widen later.
- **Multi-image conditioning** (in-context generation, OmniGen2's
  other capability): the probe scopes to single-source edits only.

This RFD was drafted by an AI and read by a human before it shipped.
