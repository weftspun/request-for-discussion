# RFD 2194: Runway demo as a live-avatar portfolio widget

**State:** discussion
**Feature:** two live-avatar loop widgets on the portfolio
**Scope:** `chibifire.com` landing, `1-transport/weftspun-studio`, RFD 2136 rung 9

## Decision

Ship two sub-25-second loop widgets showing the shuttle (portable
VRM per RFD 2171 vocabulary), rendered live in Godot or browser,
screen-recorded for shareable clips. Anime demo first (near-term
reachable); real-world fashion demo second (blocked on
photorealistic identity corpus).

Shared: dressing anchor is `chibifire/zenodo-second-hand-fashion-v3`
(32k CC-BY garments), direct for real-world and CycleGAN-style-
transferred for anime (BSD-2, per RFD 0036). Motion:
motion-bricks.cpp (RFD 1102 catalog) on hand-authored keyframes.
FX: scale-punch on VRM plus UI, purple palette, particle bursts on
pose changes. Music: CC0 or CC-BY only. No commissioned music, no
licensed dance footage.

Per-demo split: identity anchor. Anime uses RFD 2187's sources;
real-world needs a photorealistic-face licence-clean corpus not
yet acquired. 10-second outro carries QR plus URL per RFD 2136
(gacha ladder) rung 9.

## Problem

The atelier-workshop has no shipped demonstrable artifact. Gacha
ladder rung 9 needs a concrete destination. Gist 8c64c9f6 (fire +
lito) committed: "Let's do both real world feminine fashion and
slightly more anime demos." Reference clip (MiraLunaMocha, glowing
purple, scale-punch) is a live widget, not a video edit.

## Related

RFD 2136 (gacha ladder rung 9), RFD 2166 (Cineform bundle), RFD
2171 (atelier-workshop vocabulary), RFD 2183 (layer-decomp
pipeline), RFD 2186 + 2187 (dressing + identity overlays, both
parked), RFD 1102 (task catalog).

This RFD was drafted by an AI and read by a human before it shipped.
