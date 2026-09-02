# RFD 2167: Voice-clone reward-model distillation

**State:** discussion
**Feature:** distill the wavlm_cos + voxtral_wer scoring signal from
RFD 2164.3.1/.3.2 into a fast reward model usable in RL fine-tuning of
voice models. Parallels EditScore for image edits.
**Scope:** `6-datasource/anny-render-corpus`, later a dedicated model
repo for the reward LoRA.

## Problem

The 10-rank voice-clone ladder from RFD 2164.2 has a real gradient
(measured RFD 2164.3.2: identity 0.92 -> pitch-shift 0.70 -> wrong
subject 0.75 on wavlm_cos; canonical 0.07 WER -> wrong text 1.94), but
the scoring path itself is too slow to serve as an RL reward. Voxtral
inference takes 5-10s per candidate on MPS; standard RL loops want
around 10,000 rollouts per epoch, which is >24 hours per epoch just
for reward computation.

## Decision

Train a small reward model that predicts our composite score directly
from raw audio, then freeze it and use as the reward signal for RL
fine-tuning downstream voice models.

  base       Gemma-4-12B QAT Q4_0 (Apache-2.0, already local)
  training   pairwise ranking on the 150 rank pairs from RFD 2164
             (grow toward 3000 by adding SpeakingFaces subjects)
  input      (reference_audio, target_text, candidate_audio)
  output     scalar reward
  loss       Bradley-Terry on the 10-rank ladders
  latency    ~50 ms per pair on MPS after distillation

Also lands the reward-model swap parked as task #42 (EditScore
Qwen3-VL -> Gemma-4-12B): the same fine-tuned Gemma serves both image
and voice reward roles, one model instead of two.

## Related

Spine: urn:oid:1.3.6.1.4.1.66606.1.1.1173 (MaskScore).
Consumes: urn:oid:1.3.6.1.4.1.66606.1.2.2164 (voice-clone score data).

This RFD was drafted by an AI and read by a human before it shipped.
