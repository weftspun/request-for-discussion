# RFD 2166: MaskScore Cineform MKV bundle per RFD 1137

**State:** discussion
**Feature:** one Cineform MKV per edit bundling the video frames,
audio, and the 12-track WebVTT ASR panel, produced through the
service-cineform pair per RFD 1137.
**Scope:** `6-datasource/anny-render-corpus`, `7-service/service-cineform`,
`3-interactor/interactor-cineform`, `1-transport/transport-cineform-tui`

Shelved 2026-09-02: no encoding time budget this cycle to build the
video-delivery bundle; resume when local capacity frees.

## Problem

RFD 1173's deliverable rule requires a video-ready asset with a .cff
title alongside. The Rung 1.5 corpus emits USDZ animation and per-view
PNGs; neither is a reviewable clip. RFD 1137 specifies the pair that
produces one MKV per frame-set.

## Decision

Follow RFD 1137's SKILL.md verbatim: build the encoder + display, run
the bus, encode one clip per edit at 8 fps with matte + card. Filename
comes from the citation's title, lowercased with non-word runs
hyphenated: `anny-mask-score-<edit>.mkv` + matching `.cff`.

The 12-track transcripts from RFD 1173.2164.1 become S_TEXT/WEBVTT
subtitle tracks in the MKV, one per judge, tagged with LANGUAGE
metadata (auto detect per Whisper for text tracks; ipa/phn-* for
phoneme tracks).

## Related

Spine: urn:oid:1.3.6.1.4.1.66606.1.1.1173 (MaskScore).
Follows: urn:oid:1.3.6.1.4.1.66606.1.1.1137 (frame set clip
encoding).

This RFD was drafted by an AI and read by a human before it shipped.
