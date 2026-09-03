# RFD 1102 details: current task catalog, pipelines, retraction record

## Model catalog (Docker images, per RFD 1036)

| Task                          | Model                          | Notes                                                          |
| ----------------------------- | ------------------------------ | -------------------------------------------------------------- |
| Text/image reasoning + reward | Gemma-4-12B (QAT Q4_0)         | Shared VLM per RFD 1173; EditScore fine-tune base (RFD 1157). |
| Text/image → image            | Wan-VACE                       | ~14 GB NF4 (staged per RFD 1027).                              |
| Image → coarse mesh           | Pixal3D                        | 24 GB total, ~6.5 GB peak staged.                              |
| Mesh refinement               | VoxHammer                      | Holds no weights (RFD 1162).                                   |
| Image → mesh (fast)           | TRELLIS.2                      | ~8 GB bf16.                                                    |
| Metric depth                  | MoGe-3                         | ~1 GB.                                                         |
| Auto-rig                      | SkinTokens                     | Full GLB against ANNY skeleton.                                |
| Text → motion                 | Kimodo                         | Into SOMA pose format (78 canonical); consumed by ANNY.        |
| Mesh segmentation             | rf-detr-Seg (RFD 1168)         | Replaces P3-SAM (blocklisted, territory).                      |
| Layer decomposition           | rf-detr-Seg + LaMa inpainting  | Replaces See-Through (blocklisted, no license) per RFD 1168.   |
| Mesh retopology               | AutoRemesher, xatlas UV        | Format-adjacent tools, unchanged from prior catalog.           |

## Voice + ASR (RFD 2164)

| Task                          | Model                                      |
| ----------------------------- | ------------------------------------------ |
| Voice cloning                 | Qwen3-TTS-12Hz-1.7B-Base                   |
| ASR (canonical)               | Parakeet TDT 0.6B v3 (CC-BY-4.0)           |
| ASR panel (12 tracks)         | Parakeet, Whisper large-v3, Voxtral Mini 3B, wav2vec2, Gemma-4-12B (auto + GBNF-IPA), Voxtral-IPA, ipa-whisper (s + b), allosaurus (universal + 27 commercial-localization langs per RFD 2170) |
| Speaker embedding             | Microsoft WavLM Base+ SV                   |

## Pipeline: MaskScore corpus construction (RFD 1173)

  input      Docker container per model, /health + /predict
       |
  render     Mitsuba llvm_ad_rgb or metal_ad_rgb, sphere_hammersley
       |
  MaskScore  mask → reconstruct → score decoded outputs
       |
  parquet    3-file ZSTD per stub (root + candidates + scores),
             ETNF (no nulls, interned vocab), RFD 2165.1 schema
       |
  HF         chibifire/maskscore-rung-1-bootstrap, 5 of 8 stubs shipped
             (mesh, depth, pose, keypoints, multimodal, speech)

## Pipeline: Gacha critical path (RFD 2136)

Ten rungs, each producing an output the next rung consumes:

  0. Language prompt → image           (OmniGen2)
  1. Image → mesh                      (Pixal3D)
  2. Mesh → judged                     (EditScore)
  3. Judged → repaired                 (VoxHammer, N-attempt bound)
  4. Repaired → skinned                (SkinTokens against ANNY)
  5. Skinned → tagged                  (rf-detr-Seg + LaMa)
  6. Tagged → VRM                      (portable character)
  7. Prompt list → pool                (~50 VRMs, judged, seed-reproducible)
  8. Pool → roll button                (web page)
  9. Public                            (hosted with sponsor link)

## Retraction record

The 2026-06 draft of this RFD listed:

- DGX-hosted `3DAIGC-API` on port 7842 as the live source.
- `TaskManager.jsx` and `src/library/aiModelsCatalog.js` as the client
  half of the strangler-fig plan (RFD 1019).
- 14 task types across text-to-3D, image-to-3D, splat, world, and
  avatar categories, with per-task feature keys.
- Six models now blocklisted or abandoned: P3-SAM (territory
  restricted), TripoSplat + WorldMirror 2.0 + weftspun_image_to_world
  + LingBot-Map (RFDs 1049-1052 abandoned), Hunyuan3D-2.1 (not in
  current catalog per RFD 1027).
- Publish/RP1/OMB via MSF Map Service (RFD 1100 abandoned per RFD 2176
  Class F index).
- IWSDK Option A on SceneManager (RFD 1090 abandoned).

Retracted alongside RFD 2169 (studio-core abandonment) and RFD 2175
(rented-compute abandonment). The task shape the catalog described no
longer exists; the model set the catalog listed is the intersection
above.

## Format boundary

Internal: OpenUSD `.usda` / `.usdc` (RFD 1053 `committed`), each
stage adds a layer.
Transmission: glTF binary (asset), VRM (avatar), USDZ (archive).
Convert at the boundary only.

## Packaging

Per RFD 1036 (`committed`): plain Docker, `/health` + `/predict`,
weights at build time, two-stage Dockerfile (`contract` + `worker`),
one model per image. Target 24 GB card (local desktop GPU per
CLAUDE.md).

## Related

RFD 1004 (original AIGC catalog, historical), RFD 1094 (multi-image
routing, still current), RFD 1084 (avatar pipeline client side, still
current), RFD 1108 (XR floor anchoring, `committed`), RFD 1088
(HTTPS setup), RFD 1085 (code map), RFD 1105 (webcam avatar control).
Removed refs to abandoned RFDs 1049-1052, 1090, 1100, 1019 per RFD
2174 (open→abandoned index) and RFD 2176 (committed→terminal index).
