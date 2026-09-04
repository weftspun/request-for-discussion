# RFD 2194: Atelier shuttle portfolio widget

**State:** discussion
**Feature:** sub-25s runway demo of the shuttle, 10s outro
**Scope:** `chibifire.com`, `1-transport/weftspun-studio`, RFD 2136 rung 9

## Decision

Rerender the same runway scene N times, different outfits per shot,
cut in a video editor. Under 25 seconds + 10s outro with QR + URL per
RFD 2136 rung 9. Live Godot render acceptable.

**Identity: ANNY.** Same avatar every shot. Anime style is the shipped
look on every shot in the final video.

**Paired generation.** Each shot is a pair — same identity, same
garment, same pose — rendered photographic + anime-styled. Anime
half ships; photographic stays as EditScore anchor. Sources:
`chibifire/zenodo-second-hand-fashion-v3` (garments),
`alfredplpl/anime-with-caption-cc0` (style anchor),
`chibifire/zenodo-ecommerce-text` +
`chibifire/kaggle-womens-ecom-clothing-reviews` (garment
vocabulary). CycleGAN styles per BLOCKLIST.md. Generator OmniGen2
(RFD 2183); LLaDA-o pending RFD 2198. Recursive EditScore
(RFD 2193) ranks pairs, per-axis critique fed back. Output:
`chibifire/anny-runway-shots-<yyyymmdd>`. See DETAILS.

## Problem

Atelier-workshop has no shipped demonstrable artifact.

## Related

RFD 2136, RFD 2166, RFD 2171, RFD 2183, RFD 2193, RFD 2198, RFD 1102,
BLOCKLIST.md CycleGAN section.

This RFD was drafted by an AI and read by a human before it shipped.
