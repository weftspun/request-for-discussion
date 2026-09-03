# RFD 2180: Drop the gemma-auto ASR track (bug fixed, drop confirmed)

**State:** published
**Feature:** documentation retraction with investigation record
**Scope:** RFDs 2164, 2179; `emit_10track_panel.py`; `CITATION.cff`

## Problem

RFD 2179 flagged gemma-auto shipping empty transcripts across all 15 clips (WER 1.000, .vtt files carried only the WEBVTT header). Follow-up was fix-or-drop.

Investigation (DETAILS.md): `gemma_cli_run` used prompt "Transcribe
this audio verbatim" with `-n 200`. Gemma-4-12B heard the audio as
spoken user input, reasoned about how to respond as an AI assistant,
and expired the token budget inside chain-of-thought without reaching
the final channel. Empty output.

## Decision

Bug is fixable but the track's quality after the fix is worst in
the surviving panel. Drop the track. Fix (for the record): firmer
ASR-only prompt plus `-n 400`. 15-clip WER pass with the fix: 0.690
mean (6 exact, 3 accent-mishears, 6 still truncated mid-reasoning).
Voxtral runs the same clips at 0.000 sub-second. Gemma-auto's
several-seconds-per-clip latency plus 0.690 WER matches the
speed-plus-quality argument RFD 2179 used for Whisper.

Panel drops 9 tracks (post-2179) to 8:

  text-track   Parakeet TDT 0.6B v3, Voxtral Mini 3B, wav2vec2
  IPA-track    Voxtral-IPA, Gemma-4-12B GBNF-IPA
  phone-track  allosaurus (universal + eng + rus)

Gemma-IPA stays: the GBNF constraint pins output to IPA characters and forces short completions; neither failure mode appears on that track.

## Related

Extends RFD 2179 (Whisper drop). DETAILS.md holds the 15-clip WER
table with the fix applied and the exact prompt + argv.

This RFD was drafted by an AI and read by a human before it shipped.
