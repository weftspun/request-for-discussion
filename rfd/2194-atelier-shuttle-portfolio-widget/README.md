# RFD 2194: Atelier shuttle portfolio widget

**State:** discussion
**Feature:** sub-25s runway demo of the shuttle, 10s outro
**Scope:** `chibifire.com`, `1-transport/weftspun-studio`, RFD 2136 rung 9

## Decision

Rerender the same runway scene N times, different outfits and
identity per shot, cut in a video editor. Under 25 seconds + 10s
outro with QR + URL per RFD 2136 (gacha ladder) rung 9. Live Godot
render is fine if it produces the same shot structure.

**Anime side, text-only anchor** (near-term reachable). Dressing
from `chibifire/zenodo-ecommerce-text` +
`chibifire/kaggle-womens-ecom-clothing-reviews`, CycleGAN-styled
via RFD 0036 for anime look. Identity from
`alfredplpl/anime-with-caption-cc0` captions (BLOCKLIST.md permits
captions). OmniGen2 (RFD 2183) generates from language.

**Real-world side.** `chibifire/zenodo-second-hand-fashion-v3` (32k
CC-BY garments) direct as dressing. Identity: text → Wan-VACE or
OmniGen2 (RFD 1102 catalog) → EditScore per RFD 2193. No footage.

Motion: motion-bricks.cpp on hand-authored keyframes. FX + palette
per chibifire (RFD 2182): ribbon trails; peach, coral, blush,
cream. Music: CC0 or CC-BY. No commissioned music.

## Problem

Atelier-workshop has no shipped demonstrable artifact.

## Related

RFD 2136, RFD 2166 (Cineform), RFD 2171 (vocabulary), RFD 2183,
RFD 2186 + 2187 (parked), RFD 1102.

This RFD was drafted by an AI and read by a human before it shipped.
