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

## Cherry-pick skipped commits, then re-resolved

Cherry-picked onto `weftspun-consolidated` from `sam3-metal-ops`:

| commit | subject | first outcome | resolution |
|---|---|---|---|
| `7a466633` | Metal conv\_transpose\_2d, depthwise conv\_2d, K/V flash\_attn\_ext type check, WIN\_PART / WIN\_UNPART on Metal | **SKIPPED**: conflicts in ggml-metal-device.h, ggml-metal-ops.cpp, ggml-metal.metal | **DROPPED after re-verification**. Per-intent verdicts below |
| `331b9cba` | Metal flash\_attn\_ext head\_dim=16 and head\_dim=56 | **SKIPPED**: dependent on `7a466633`, and first pass claimed the template mechanism was restructured | **PORTED** as PR https://github.com/weftspun/ggml/pull/1 |

### 7a466633 per-intent verdicts

| intent | verdict | evidence |
|---|---|---|
| conv\_transpose\_2d on Metal | verified covered | consolidated has identical (f32\_f32, f16\_f32) template pair at ggml-metal.metal:5508. Algorithm differs (threadgroup shared-sum reduction on consolidated) but the surface and dtype coverage match |
| depthwise conv\_2d (CONV\_2D\_DW) | verified covered with more | consolidated has kernel\_conv\_2d\_dw templated over TK (_f32\_f32, _f16\_f32) plus a tiled variant with the same coverage. sam3's plain kernel\_conv\_2d\_dw\_f32 is a strict subset |
| flash\_attn\_ext K/V type check | verified covered | identical assertion `op->src[1]->type == op->src[2]->type` at ggml-metal-ops.cpp:2721 |
| WIN\_PART / WIN\_UNPART on Metal | genuinely missing, deferred | sam3 added Metal kernels; consolidated has these ops only in the CPU backend (ggml-cpu.c:2019-2023). No consumer in the workspace uses SAM3-style windowed attention today. CPU fallback correct. Port when a consumer needs it |

### 331b9cba resolution

The first close-out claimed the template mechanism had been restructured and dk16/dk56 could not be added. That was wrong. The template shape on consolidated matches sam3 exactly; adding two head-dim slots was a mechanical change once the vec dispatch was ruled out.

PR https://github.com/weftspun/ggml/pull/1 adds 16 template instantiations (dk16, dk56 × 8 K/V dtypes) plus 2 entries in the head-size whitelist in supports_op. Vec templates omitted because `ggml_metal_op_flash_attn_ext_use_vec` gates on `ne00 % 32 == 0`, which excludes 16 and 56.

The `sam3-metal-ops` branch stays for archaeology.

### Correction the record keeps

The first close-out was too fast. Two claims failed the same test: "the newer surface restructured the target" was said without reading whether the restructure actually broke the port. The re-investigation kept the same three intents already-covered verdicts, added the WIN\_PART/WIN\_UNPART deferral (which the first pass called "not clearly needed" without evidence), and reversed the dk16/dk56 verdict from "not portable" to "portable with 18 lines." The verdicts moved because they were re-measured; the retraction stays here rather than being tidied out.

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
