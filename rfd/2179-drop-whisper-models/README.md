# RFD 2179: Drop all Whisper models from the ASR panel

**State:** published
**Feature:** documentation retraction
**Scope:** RFDs 2164, 2178, 1102, 1027; CITATION.cff;
`emit_10track_panel.py`

## Decision

Drop all three Whisper models (whisper-large-v3, ipa-whisper-small, ipa-whisper-base) from the ASR panel; the panel drops from 12 tracks to 9, and Whisper is not replaced.

## Problem

RFD 2164 (Rung 1 corpus)'s 12-track panel carries whisper-large-v3, ipa-whisper-small, ipa-whisper-base. whisper-large-v3 dominates panel wall-time (several seconds each on MPS versus sub-second for Voxtral and Parakeet); the ipa-whisper variants share that latency, and the IPA slot is already served by Voxtral-IPA and Gemma-IPA. A 15-clip WER pass across the surviving text tracks (DETAILS.md) puts whisper-large-v3 at 0.339 mean, beating Parakeet (0.501) and wav2vec2 (0.571); Voxtral leads at 0.000. The reason to drop is latency, not accuracy.

## Panel after the drop

  text-track    Parakeet TDT 0.6B v3, Voxtral Mini 3B, wav2vec2,
                Gemma-4-12B auto
  IPA-track     Voxtral-IPA, Gemma-4-12B GBNF-IPA
  phone-track   allosaurus (universal + eng + rus)

Voxtral is the accuracy leader; Parakeet stays as the CC-BY-4.0 alternate.

Follow-ups: `emit_10track_panel.py` drops the whisper backends; downstream RFDs and CITATION.cff drop Whisper entries. Gemma-auto shipped empty transcripts on all 15 clips (WER 1.000); separate follow-up to fix or drop.

## Related

Retracts three rows from RFD 2164 (Rung 1 corpus); amends RFD 2178 (QAFT stack plan), three Class B rungs go.

This RFD was drafted by an AI and read by a human before it shipped.
