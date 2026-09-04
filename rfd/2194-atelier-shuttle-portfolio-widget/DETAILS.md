# Atelier shuttle portfolio widget — paired-generation pipeline

## The pair as the unit

Each shot in the shuttle demo is generated as a **pair**: the same
ANNY identity, the same garment from
`chibifire/zenodo-second-hand-fashion-v3`, the same pose, rendered
twice — once photographic and once anime-styled. Identity is fixed
within a pair; it may vary across pairs (different ANNY variants,
different accessories) to give the shuttle shot-to-shot diversity.

The final video ships the anime half of each accepted pair.
The photographic half stays in the output dataset as (a) provenance
of what the anime render is styled from, and (b) EditScore's
identity-fidelity anchor for the ranking step.

## Sources

**Garments.** `chibifire/zenodo-second-hand-fashion-v3`, 32k CC-BY
used-clothing photos. Drives the photographic half directly and,
via CycleGAN style transfer, the anime half. Row key from that
dataset is carried into every output row so a downstream reader can
trace a shot back to its source garment.

**Anime-style anchor.** `alfredplpl/anime-with-caption-cc0` captions
carry the anime style prompt. BLOCKLIST.md permits the captions
(images blocked, captions permitted). `chibifire/zenodo-ecommerce-text`
and `chibifire/kaggle-womens-ecom-clothing-reviews` supply garment
vocabulary so the anime render names its clothing coherently rather
than emitting garment noise.

**Anime style — via generator prompt, not CycleGAN.** Earlier draft
proposed CycleGAN for photographic-to-anime style transfer. That
path is not executable: the workspace has no licence-clean anime
image corpus to train CycleGAN's photo→anime direction on
(BLOCKLIST.md's CycleGAN section states this explicitly, and
`alfredplpl/anime-with-caption-cc0` is captions-only per the
BLOCKLIST row). Anime style now comes from the generator itself:
the anime half of each pair is generated with an `in anime style`
prompt appended to the caption; the photographic half uses the
caption without the anime prefix. Same generator, same identity,
same garment — only the style token differs.

**Generator-provenance check: parked 2026-09-04.** Un-park conditions
are documented in the operator's memory file; the check does not
happen at execution time. Apache-2.0 weights are taken at face
value for this demo's purpose.

## Generator

**OmniGen2** per RFD 2183 as the current default. Both halves of the
pair use the same generator to hold identity constant. LLaDA-o
replaces OmniGen2 if RFD 2198's pairs-20 sweep confirms the 4-step
sweet spot beats OmniGen2 at comparable wall-clock — at that point
this DETAILS gets a swap.

## Ranking: recursive EditScore

Per shot, one round is:

1. **Generate.** Produce K paired candidates for the shot's garment.
2. **Score.** Each pair gets a composite from three axes:
   - **Identity fidelity across the pair.** Same ANNY in both halves.
     EditScore compares the photographic half against the anime half
     as its own critique.
   - **Garment fidelity.** Photographic half against the source
     dataset row.
   - **Anime-style match.** Anime half against the caption prompt.
3. **Feed back.** Top-N pairs stay. EditScore's per-axis critique
   becomes conditioning for the next round's generation, so weak
   pairs get pointed feedback instead of blind resampling.
4. **Terminate.** Top-1 composite plateau or a compute-budget cap
   per shot. Whichever hits first.

Recursion depth expected 2-4 rounds per shot at K=4 candidates
(rough sizing; the first shot calibrates).

## Output HF dataset

**Repo:** `chibifire/anny-runway-shots-<yyyymmdd>`.

**Row shape** per RFD 2196 (wide row, images as
`struct<bytes, path>`, row groups ≤ 300 MB):

| column | type | notes |
|---|---|---|
| `garment_row_key` | string | source key from zenodo-second-hand-fashion-v3 |
| `caption` | string | prompt used, from alfredplpl-with-caption-cc0 |
| `generator` | string | `omnigen2` or `lladao` |
| `steps` | int32 | step count used |
| `editscore_composite` | float64 | final round's top-1 composite |
| `editscore_identity` | float64 | per-axis: identity fidelity |
| `editscore_garment` | float64 | per-axis: garment fidelity |
| `editscore_style` | float64 | per-axis: anime-style match |
| `rounds` | int32 | how many refinement rounds this pair took |
| `image_photographic` | struct<bytes, path> | the pair's photo half |
| `image_anime` | struct<bytes, path> | the pair's anime half |

One row per accepted pair. Rejected candidates from the recursion do
not ship; they were the fuel for the top-1 that survives.

## Runway assembly

Motion: `3-interactor/motion-bricks-cpp` on hand-authored keyframes.
FX: ribbon trails. Palette per chibifire (RFD 2182): peach, coral,
blush, cream. Music: CC0 or CC-BY. No commissioned music.

Shot count sizing: at 25 s of runway + ~2 s per shot beat, plan for
10-14 accepted pairs in the output dataset. Not every dataset row is
a shot; the video editor picks the strongest ones.

## Owner and dependencies

**Owner:** CUDA (gpu-experimenter). Generation, ranking, upload all
GPU-bound.

**Blocking:** RFD 2198 pairs-20 (in flight) pins the generator choice
between OmniGen2 and LLaDA-o. Not strictly blocking — CUDA can start
with OmniGen2 and swap if the sweep says so.

**Not blocking:** the RFD 0036 reference this document used to
carry has been replaced with the direct BLOCKLIST.md CycleGAN
pointer.

## Execution parked 2026-09-04 (spec unchanged)

The paired-generation spec above stays as authored. Execution is
parked on sizing: LLaDA-o at 16-step SDEdit (the chosen generator,
per the swap decision below) needs ~264 s per edit sharded on
3090+4090; K=4 candidates × 3 rounds × 12 shots × 264 s = ~158 h
GPU wall. Not shippable in that shape.

Un-park requires one of:
- LLaDA-o at ~5x speedup or better (distillation, step-count
  reduction below 16 that holds quality, sub-quadratic candidate
  reduction, or batching across GPUs somehow)
- Smaller scope re-approval (K=2 or rounds=2 or shots<12)
- Different generator with acceptable quality at shippable wall

Memory `rfd-2194-parked-on-sizing` (operator's) carries the full
un-park condition list.

## Generator swap decision (2026-09-04)

**LLaDA-o at 16-step SDEdit replaces OmniGen2 as the default
generator when execution un-parks.** Decided from
`logbook-lladao-n20-held-out-sweep`: n=20 held-out on shard 90
gives 17/20 wins over OmniGen2's 3.36 mean (85%), mean 5.972,
median 6.573. Clears the 80% gating threshold in RFD 2198.

The swap triggers PR #274 condition 4 (LLaDA-o provenance-check
un-park) but the check itself is deferred with the execution;
LLaDA-o card + training-corpus documentation for anime-styled
outputs is owed on un-park, not now.
