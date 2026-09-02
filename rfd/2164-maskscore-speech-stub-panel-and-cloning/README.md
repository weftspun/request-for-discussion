# RFD 2164: MaskScore Speech-stub 12-track ASR panel + 10-rank voice cloning

**State:** discussion
**Feature:** MaskScore Speech stub filled along two axes -- a panel of
diverse ASR judges (12 tracks per audio) and a 10-rank ladder of
voice-cloned candidates. Together they cover the transcript and audio
dimensions the reward model needs to score.
**Scope:** `6-datasource/anny-render-corpus`

## Decision

Sub-rungs (each a citable OID under this serial):

  .1    12-track ASR panel: parakeet, whisper, voxtral, wav2vec2,
        gemma-auto (text) + gemma-gbnf, voxtral-ipa, ipa-whisper-s/b,
        allosaurus universal/eng/rus (ipa + phone controls). See
        `emit_10track_panel.py`, `add_allosaurus_control.py`.
  .2.1  10 voice clones per audio via Qwen3-TTS-12Hz-1.7B-Base:
        identity, pitch/tempo perturbation gradient, wrong content,
        wrong subject. See `voice_clone_10rank.py`.
  .2.2  Real different-speaker reference for rank9/10 using sub_1
        SpeakingFaces clips with `x_vector_only_mode=True`.
  .3.1  Score wavlm-cos (speaker embedding) + voxtral-WER on 150
        clones. See `score_voice_clones.py`.
  .3.2  Rescore after .2.2 lands.
  .4    Emit Speech-stub parquets in ETNF three-file form.
  .5    Commit, push, HF upload, PR.

Panel judges are ordered by canonical-closeness for the transcript
axis, and cloning ranks are ordered by intended similarity to the
reference audio for the audio axis. Both feed the same MaskScore
gradient shape.

## Related

Spine: urn:oid:1.3.6.1.4.1.66606.1.1.1173 (MaskScore).

This RFD was drafted by an AI and read by a human before it shipped.
