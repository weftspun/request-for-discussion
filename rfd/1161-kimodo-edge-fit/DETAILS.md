# RFD 1161 details: un-abandonment rescore + un-park scope

## The 2026-08-28 abandonment paragraph, as history

RFD 1161 was abandoned on 2026-08-28 with the reasoning: "The
accelerator work is scoped to rf-detr keypoint and RFD 1157, and
this scored 14 of 25 against RFD 1157's 18." The scoring rubric
was RFD 1157's `value / difficulty / verification` frame,
25 points across three axes, and Kimodo landed below RFD 1157 on
the composite. The abandonment paragraph stays in the README as
history; nothing that cited it changes retroactively.

## The 2026-09-04 rescore, against the current landscape

Four premises of the 14/25 scoring turned out to be stale:

0. **Zoo-DETR resurrection rejected 2026-09-04.** The `detr_resnet_v1_18_bn`
   zoo entry parses clean on hailo10h but does object detection not
   keypoints; adapting it to the 133-keypoint expanded schema is 1-2
   weeks of head engineering, plus a ResNet-18 backbone loses rf-detr's
   DINOv2 pretraining floor, plus the shipped `.alls` is INT8 not INT4.
   Vision-Hailo is culled; rf-detr QAT ships CUDA-only via HERO's
   task #65.
1. **RFD 2199 (rf-detr on-device) parked 2026-09-04.** HERO's
   scaffold-first pilot analysis surfaced (a) a 4.57% BN accuracy
   delta against LN baseline when the vit_base_bn recipe was
   applied to rf-detr's encoder, and (b) a vendor-fork
   publishability constraint on the LN→BN edit. Full retrain
   never kicked. Task #64 shelved. See
   `logbook-rfd-2199-vit-base-bn-pick-provenance.md`.
2. **RFD 1157 (EditScore edge acceleration) shares the LN-axes
   wall the RFD 2199 bisect isolated.** EditScore is a LoRA over
   Qwen3-VL; the accelerated encoder path (mtmd Hailo, in
   `3-interactor/llama-cpp-npu-vision-upstream` at commit
   `5ccbf7cd3`) uses a ViT backbone with LayerNormalization
   throughout. Same `_convert_axes_to_nhwc` diagnosis applies. RFD
   1157 stays at 18/25 nominally but the on-device path is subject
   to the same un-park conditions RFD 2199 hit.
3. **RFD 1163 (rented card + on-desk accelerator) is abandoned per
   RFD 2175 (rented-compute abandonment).** The 14/25 scoring
   implicitly assumed rental was available for the DFC compile
   half. That premise is closed. Kimodo compile now runs on the
   local Fedora WSL container (`weftspun-hailo-dfc:latest`)
   the same way RFD 2199's work did.

Rescore against those three inputs, honestly:

- **value axis**: rises. Motion becomes the primary latency-
  critical Hailo-10H track that still fits without an un-park
  condition on the encoder-LN diagnosis. Kimodo's diffusion
  denoiser is a UNet-1D or transformer-1D over joint sequences;
  transformer variants hit the LN wall like everything else,
  UNet-1D variant may not. Verify at ONNX-export time before
  committing to compile.
- **difficulty axis**: unchanged from the earlier estimate. The
  sampler still needs porting from `nv-tlabs/kimodo` upstream
  into `3-interactor/kimodo-text-to-motion/server.py`; step-
  count reduction (Flow LCM style, per RFD 2136 rung 0
  precedent) still needs a distillation pass. Same weeks of
  Python/Torch work as before.
- **verification axis**: rises. `dot-claude#19` (hailo-dfc-
  compat-probe) and `dot-claude#20` (BN-vs-LN node counting)
  land the mechanical checks; the RFD 2199 bisect methodology
  (`logbook-dfc-bisect-methodology-rf-detr.md`) names where to
  look if compile fails. Kimodo lands into a compile+measure
  pipeline shape already spec'd
  (`logbook-rfd-2199-compile-measure-spec.md`).

Composite lands above 14/25 on the current landscape. Not asked to
pin a specific number; the honest read is that Kimodo is now the
best remaining latency-critical Hailo-10H candidate that has both
the size envelope and a licence-clean shipping path.

## Un-park scope

Sequenced work items, with ownership:

1. **HERO**: upstream sampler port. `nv-tlabs/kimodo` → 
   `3-interactor/kimodo-text-to-motion/server.py`. Currently
   `_run_upstream()` raises `NotImplementedError`. Weeks of Python
   / Torch work. HERO has capacity while blocked on ANCHOR's corpus
   render. Kimodo-SOMA checkpoint (NVIDIA Open Model License,
   commercial-friendly) is the ship variant.
2. **SIDEKICK**: ONNX export of the denoiser + text encoder from
   the ported sampler. Standard `torch.onnx.export` with
   `dynamo=False` per the RFD 2199 rewind's export-toolchain
   lesson.
3. **SIDEKICK**: LN-vs-BN probe via `dot-claude#20`. Names whether
   the denoiser's Norm layers trigger the `_convert_axes_to_nhwc`
   wall. Reports BN nodes seen vs LN nodes for the recipe check.
4. **SIDEKICK**: sampler step-count reduction. Flow-LCM style
   distillation adapter, per RFD 2136 rung 0's OmniGen2 precedent.
   Cuts N from default (50-100) to the ~20 steps × 5 ms latency
   slice.
5. **SIDEKICK**: DFC compile + on-device measure per
   `logbook-rfd-2199-compile-measure-spec.md`'s pipeline shape.
   HAILO USB firmware 5.3.2 already recovered; hardware side is
   live.

## Acceptance criteria

- LN-vs-BN probe returns green on the ported ONNX
  (`BN > 0, LN == 0` in the denoiser body, or same-error-different-path
  documented so it is a known recipe failure rather than a probe
  failure).
- **Latency floor: 20 sampling steps × 5 ms per step = 100 ms per
  inference** on Hailo-10H INT4. Fits RFD 1170's sub-500 ms budget
  alongside ASR (Parakeet TDT, ~100 ms slice) and TTS (Qwen3-TTS,
  ~100-200 ms slice) with headroom.
- Motion validation (RFD 1007) still passes on the reduced-step
  output. A faster sampler that fails the floor-contact or
  joint-limit check has moved the failure rather than removed it.
- Output shape unchanged: SOMA canonical × `duration × fps` frames,
  so ANNY downstream consumes without a schema change. **Joint count
  needs verification against upstream release notes.** RFD 1102 +
  RFD 1173 + RFD 2162 consistently document 78 canonical joints;
  HERO's upstream recon reports 77 (a `somaskel77` breaking change
  in the `nv-tlabs/kimodo` release notes 2026-03-19). Discrepancy
  matters because ANCHOR's wholebody133 schema keys on the exact
  joint count. Resolve at sampler-port time (HERO's task item 1)
  by reading the actual `.npz` output shape from a
  `Kimodo-SOMA` inference and back-porting the correct number to
  RFD 1102 + RFD 1173 + RFD 2162 in a follow-up PR.

## What re-triggers a second abandonment

If any of these lands, RFD 1161 gets abandoned again with a
retraction pointer to whichever entry names the reason:

- LN-vs-BN probe surfaces an LN-axes wall in Kimodo's denoiser
  that no BN swap resolves (same failure class as RFD 2199's
  fork-encoder-LN option, and the same recipe-swap accuracy delta
  the RFD 2199 park cited).
- Step-count reduction below the 20-step floor requires an
  accuracy sacrifice that fails RFD 1007's motion validation.
- Sampler port from `nv-tlabs/kimodo` takes long enough that the
  operator picks a different latency-critical track instead
  (VAD, TTS variant, or something the RFD 1170 loop names later).

This RFD was drafted by an AI and read by a human before it shipped.
