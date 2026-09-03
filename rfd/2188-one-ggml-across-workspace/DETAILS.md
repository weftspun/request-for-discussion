# RFD 2188 details

## Discovery: HEAD dates for every ggml copy found

Measured 2026-09-03 across the workspace.

| copy | HEAD SHA | HEAD date | notes |
|---|---|---|---|
| `3-interactor/ggml-seethrough` | `3404c951` | 2026-08-29 | on branch `seethrough-metal-diag-mask-inf`, 14+ custom backends (Vulkan/Metal/CUDA/CoreML/HIP/SYCL/CANN/OpenVINO/Hexagon/OpenCL/MUSA/WebGPU/BLAS/RPC/ZenDNN/ZDNN). "NOT UPSTREAM MATERIAL" per its commit message. Chosen as base. |
| `3-interactor/trellis2cpp/ggml` | `331b9cba` | 2026-03-31 | on branch `sam3-metal-ops`. Two commits unique from ggml-seethrough HEAD: `7a466633` Metal conv\_transpose\_2d + depthwise + K/V type check; `331b9cba` Metal flash\_attn\_ext head\_dim=16 and head\_dim=56. |
| `3-interactor/nx-ggml/native/nx_ggml/third_party/ggml` | subtree, no independent history | n/a | vendored under the NIF |
| `3-interactor/rf-detr-cpp/third_party/ggml` | subtree, no independent history | n/a | vendored |
| `3-interactor/llama-cpp-npu-vision-upstream/ggml` | inside llama.cpp | 2026-09-02 | ggml lives under llama.cpp's tree, not independently rebasable. HEAD date is llama.cpp's, not ggml's. |
| `3-interactor/turboquant-godot/thirdparty/llama_cpp/ggml` | inside llama.cpp | n/a | same shape as above |
| `3-interactor/skin-tokens-cpp` | not checked out | n/a | manifest projects `skin-tokens.cpp` and `motion-bricks.cpp` did not sync to disk in this session — Phase 2 migration blocked until the sync completes |
| upstream `ggml-org/ggml` `master` | `d4716378` | 2026-08-30 | pushed to `weftspun/ggml:upstream-tracking` for future rebase base |

The user's intuition ("ggml-seethrough has the newest stuff") held: it
has the freshest independent ggml history and by far the widest
backend surface. The llama.cpp-embedded copies are newer as
llama.cpp checkouts but their ggml half sits under that project's
own git and is not a candidate for the canonical branch.

## Consolidation branch

`weftspun/ggml:weftspun-consolidated` pushed at `3404c951`
(ggml-seethrough HEAD, unmodified). The manifest points at that
branch name so a rebase moves the tip forward without a manifest
edit.

## Cherry-pick skipped commits

Cherry-picked onto `weftspun-consolidated` from `trellis2cpp/ggml`:

| commit | subject | outcome |
|---|---|---|
| `7a466633` | Metal conv\_transpose\_2d, depthwise conv\_2d, K/V flash\_attn\_ext type check | **SKIPPED**: conflicts in `src/ggml-metal/ggml-metal-device.h`, `src/ggml-metal/ggml-metal-ops.cpp`, `src/ggml-metal/ggml-metal.metal`. The Metal backend has moved substantially between the 2026-03-31 base and the 2026-08-29 tip; the change wants hand-porting against the newer op registration. |
| `331b9cba` | Metal flash\_attn\_ext head\_dim=16 and head\_dim=56 | **SKIPPED**: dependent on `7a466633`. |

Both live on `weftspun/ggml:sam3-metal-ops`, so nothing is lost —
the Phase 2 skin-tokens.cpp / motion-bricks.cpp migration owns the
hand-port because those consumers are what asked for the shapes.

## Compatibility test matrix

Phase 2 walks this per-consumer. Not run in Phase 1.

| consumer | manifest path | current ggml source | Phase 2 migration owner |
|---|---|---|---|
| `skin-tokens.cpp` | `3-interactor/skin-tokens-cpp` | its own | this RFD's follow-up PR |
| `motion-bricks.cpp` | `3-interactor/motion-bricks-cpp` | its own | ditto |
| `rf-detr-cpp` | `3-interactor/rf-detr-cpp` | `third_party/ggml` subtree | rf-detr keypoint pipeline owner |
| `nx-ggml` | `3-interactor/nx-ggml` | `native/nx_ggml/third_party/ggml` subtree | nx-ggml NIF owner |
| `llama-cpp-npu-vision-upstream` | `3-interactor/llama-cpp-npu-vision-upstream` | ggml under llama.cpp | vendor-runtime exempt (CLAUDE.md ggml row) — no migration |
| `turboquant-godot` | `3-interactor/turboquant-godot` | ggml under llama.cpp | vendor-runtime exempt — no migration |

## Phase 1 landing PRs

- `weftspun/ggml`: pushed `weftspun-consolidated` and
  `upstream-tracking` branches. No PR — direct branch push.
- `weftspun/request-for-discussion`: this RFD, S2188 in
  `SERIALS-vsekai-fabric.usda`, `scripts/check_ggml_singleton.py`,
  hook wiring in `.pre-commit-config.yaml`.
- `weftspun/weftspun-keypoint`: manifest change collapsing the two
  conflicting `<project name="ggml">` entries into one pointing at
  `weftspun-consolidated` under `2-contract/ggml`.

## Phase 1 non-goals

- `skin-tokens.cpp` proof-of-pattern migration deferred: the
  manifest projects did not check out in this session. Named and
  counted per CLAUDE.md rule 3 — a silent skip would have read as a
  pass.
- No consumer's CMake was edited in Phase 1.
- No build was verified in Phase 1.
