# RFD 2194: Atelier shuttle portfolio widget

**Atelier shuttle portfolio widget:** retracted 2026-09-05,
superseded by [RFD 2210](../2210-atelier-godot-web-shipping-surface/)
(with L2 fanout at [RFD 2211](../2211-base-tree-entities-godot-sandbox/)
/ [2212](../2212-motion-bricks-as-native-godot-module/)
/ [2213](../2213-vrm-via-godot-sandbox-elf/)
/ [2214](../2214-model-bundle-sqlite-range-fetch-zstd/)
/ [2215](../2215-one-binary-two-heads/)
/ [2216](../2216-threejs-blocklist/)). RFD 2210 §"What this RFD
retracts" carries the argument. The upstream paired photo/anime
corpus pipeline stays parked-on-sizing (2026-09-04 execution park
survives); RFD 2210 redirects where its output flows (Godot
resources for the Head B headless capture pass), it does not
un-park generation.

**State:** abandoned
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
`alfredplpl/anime-with-caption-cc0` (style anchor, captions only per
BLOCKLIST.md), `chibifire/zenodo-ecommerce-text` +
`chibifire/kaggle-womens-ecom-clothing-reviews` (garment
vocabulary). Anime style comes from the generator via prompt
(`in anime style` + caption), not from a post-hoc CycleGAN pass —
the workspace has no licence-clean anime image corpus to train
CycleGAN's photo→anime direction on. Generator OmniGen2 (RFD 2183);
LLaDA-o pending RFD 2198. Recursive EditScore
(RFD 2193) ranks pairs, per-axis critique fed back. Output:
`chibifire/anny-runway-shots-<yyyymmdd>`. See DETAILS.

## Problem

Atelier-workshop has no shipped demonstrable artifact.

## Related

RFD 2136, RFD 2166, RFD 2171, RFD 2183, RFD 2193, RFD 2198, RFD 1102,
BLOCKLIST.md CycleGAN section.

This RFD was drafted by an AI and read by a human before it shipped.
