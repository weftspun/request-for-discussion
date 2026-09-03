# RFD 2194: Runway demo as a live-avatar portfolio widget

**State:** discussion
**Feature:** two live-avatar loop widgets on the portfolio
**Scope:** `chibifire.com`, `1-transport/weftspun-studio`, RFD 2136 rung 9

## Decision

Two sub-25-second loop widgets showing the shuttle (portable VRM
per RFD 2171 vocabulary), rendered live in Godot or browser,
screen-recorded for shareable clips.

**Anime side, text-only anchor** (near-term reachable). Dressing
from `chibifire/zenodo-ecommerce-text` +
`chibifire/kaggle-womens-ecom-clothing-reviews`, CycleGAN-styled
via RFD 0036 for anime look. Identity from
`alfredplpl/anime-with-caption-cc0` captions (BLOCKLIST.md permits
captions, blocks images). OmniGen2 (RFD 2183) generates from
language, no visual anime corpus needed.

**Real-world side.** `chibifire/zenodo-second-hand-fashion-v3`
(32k CC-BY garments) direct as dressing; identity blocked on
photorealistic-face licence-clean corpus not yet acquired.

Motion: motion-bricks.cpp (RFD 1102 catalog) on hand-authored
keyframes. FX + palette per chibifire (RFD 2182 operator): ribbon
trails on limb motion; peach, coral, blush, cream. Music: CC0 or
CC-BY. No commissioned music, no licensed footage. 10-second outro:
QR + URL per rung 9.

## Problem

Atelier-workshop has no shipped demonstrable artifact. Gist
8c64c9f6 (fire + lito) committed to two demos.

## Related

RFD 2136, RFD 2166 (Cineform bundle), RFD 2171 (vocabulary),
RFD 2183, RFD 2186 + 2187 (parked), RFD 1102.

This RFD was drafted by an AI and read by a human before it shipped.
