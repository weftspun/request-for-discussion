# RFD 2227: workspace ggml models on `platform=web` + WebGPU

**Platform=web delivery surface:** retracted 2026-09-05, superseded
by [RFD 2228](../2228-webgpu-native-drop-platform-web/) — operator
reversal (verbatim): *"drop webgpu platform=web. try webgpu
native"*. The workspace ggml inventory + six-step recipe here
still apply against native WebGPU (llama.cpp's Dawn path); the
browser sizing constraint (2 GB iPad ceiling) that forced
Gemma 3 270M as first ship is lifted. A successor RFD in the 22xx
range re-scopes the inventory against native.

**State:** abandoned
**Flight level:** L2 (coordination — spans every ggml-consuming
project in the workspace)
**Feature:** the workspace has ~15 ggml consumers; a consistent
recipe for delivering any of them inside a Godot `platform=web`
export via WebGPU, ordered smallest-to-largest so we prove the
stack on the cheap model first
**Scope:** all `3-interactor/*` projects that consume ggml + the
canonical `2-contract/ggml/` (RFD 2188) + entities-godot-sandbox
web export (RFDs 2210/2211/2218) + model bundle path (RFD 2214)

## The scope

Operator directive 2026-09-05, verbatim: *"we have many many many
ggml based models. figure out how we can use them on platform=web
webgpu"* + *"you may need to pick the smallest gemma4"*.

RFD 2218 scoped ggml WebGPU for **motion-bricks-cpp specifically**.
This RFD widens the scope: **every ggml consumer in the workspace
takes the same recipe**, applied smallest-model-first so the browser
stack (WebGPU init + SQLite range-fetch + memory ceiling) is proven
on cheap ships before expensive ones commit.

## Ggml consumer inventory (as of 2026-09-05)

Grouped by size class. Sizes are approximate F32 → Q4 unless noted.

| project | model | F32 / Q4 size | current status | browser fit |
|---|---|---|---|---|
| `interactor-hailo-ugen300` | Gemma 3 270M | 1.1 GB / 135 MB | HAILO-focused; Gemma 3 270M is the smallest Gemma family member the workspace has touched | **First ship candidate** |
| `llama-cpp-npu-vision-upstream` | Gemma 4 E2B (~1.5B eff) | ~3 GB / 750 MB | measured by SIDEKICK per RFD 2199 | Second (biggest cheap Gemma); WebGPU-ready-when-2218-lands |
| `llama-cpp-npu-vision-upstream` | Gemma 4 E4B (~4B eff) | ~6 GB / 1.5 GB | fetched then reclaimed by SIDEKICK (task #94) | Third; borderline for browser page-load |
| `motion-bricks-cpp` | G1 F32 GGUF | 730 MB / 180 MB | RFD 2218 primary target | Ship alongside Gemma 3 270M — same pipeline validates both |
| `interactor-kimodo-text-to-motion` | (pinned same ggml rev as motion-bricks) | TBD | RFD 1161 | Follows motion-bricks |
| `nx-ggml` | Elixir NIF, not browser-shipped | n/a | server-side | out of scope for this RFD |
| `ggml-seethrough` | Workspace ggml fork (14+ custom backends) | n/a | RFD 2188 canonical source | Backend host, not a model consumer |
| `interactor-editscore` | EditScore-7B (Qwen3-VL) | ~14 GB / 3.5 GB | RFD 2193 anchor | Too big for browser v1 |
| `interactor-omnigen2` | OmniGen2 | ~15 GB / 3.8 GB | RFD 2183 corpus generator | Too big; server-side only |
| `interactor-voxhammer-*` | VoxHammer | TBD | Mesh repair | Server-side |
| `interactor-pixal3d-*` | Pixal3D image-to-mesh | ~4 GB / 1 GB | | Server-side |
| `interactor-trellis2-*` | TRELLIS.2 image-mesh | ~10 GB / 2.5 GB | | Server-side |
| `interactor-lladao-*` | LLaDA-o SDEdit | ~8 GB / 2 GB | RFD 2198 (execution parked) | Server-side |
| `skin-tokens-cpp` | SkinTokens | TBD | RFD 2210 rung 4 | Client possible (small) |
| `trellis2cpp` | TRELLIS.2 CPU port | ~10 GB / 2.5 GB | | Server-side |

## Smallest-first ordering, why

The browser stack has three unknowns:

1. **WebGPU adapter handoff** between Godot's `RenderingDevice` and
   ggml's backend (RFD 2211's WebGPU-fork patch series + RFD 2218's
   ggml WebGPU backend). Never done together.
2. **Model bundle range-fetch** at Q4 sizes over the ZSTD-compressed
   SQLite VFS (RFD 2214). Untested end-to-end.
3. **Browser memory ceiling** — 4 GB tablets, 2 GB iPad Safari,
   `SharedArrayBuffer` gates on cross-origin isolation. Model at
   ~150 MB is comfortable everywhere; >500 MB starts stranding
   devices.

Ship **Gemma 3 270M @ Q4 (~135 MB)** first because:

- Same GGUF format as motion-bricks-cpp (same loader path via RFD
  2214's `mb_model_load_from_memory` shape, generalised to
  `ggml_model_load_from_memory`).
- Small enough that if the browser stack collapses under it, the
  problem is definitely the stack, not the model size.
- Fits every browser + device the atelier ships to.
- Already in the workspace's HAILO project — no new fetch, no new
  provenance question.

## The recipe (applies to every ggml consumer in scope)

Once the Gemma 3 270M ship proves the stack, every ggml consumer
follows the same six steps:

1. **Q4 quantize** (QAT if the model is one we train, PTQ per RFD
   blocklist doctrine only for models we do not; almost everything
   in the workspace is somebody else's checkpoint we fetch).
2. **ZSTD-SQLite-fy** the GGUF via `build_<project>_sqlite.exs`
   (Elixir per language-preference doctrine, mirrors RFD 2223 L1
   recipe ANCHOR is drafting). Shape A (whole GGUF as one BLOB) for
   v1; Shape B (per-tensor rows) for models where the browser memory
   ceiling matters.
3. **CMakeLists `if(EMSCRIPTEN)` branch** on the consumer project,
   forcing `GGML_VULKAN/METAL/BLAS/NATIVE=OFF`, `GGML_WASM_SINGLE_FILE=ON`,
   `GGML_WEBGPU=ON` (once RFD 2218 lands the backend).
4. **`_load_from_memory` C API sibling** so the browser loader hands
   a `Uint8Array` from the SQLite blob to the model. Generalises
   RFD 2221's motion-bricks-specific pattern.
5. **Godot module wrap** at `entities-godot-sandbox/modules/<name>/`
   linking the consumer's static lib, exposing a GDScript-callable
   API. Mirrors RFD 2222's motion-bricks pattern.
6. **CI web workflow addition** compiling the module against the
   emcc toolchain per RFD 2225.

Each consumer's landing lives as its own follow-up L1 RFD (in
the 22xx range) once the Gemma 3 270M ship proves out.

## Not in scope

- **Models >2 GB Q4**: EditScore-7B, OmniGen2, TRELLIS.2, Pixal3D,
  LLaDA-o. Server-side only under this RFD; a future L2 RFD scopes
  "server-side ggml inference behind a HTTP endpoint the browser
  calls" separately.
- **nx-ggml** (Elixir NIF, BEAM-hosted) — server-side execution
  path stays server-side.
- **Non-ggml runtimes**: ONNX Runtime Web, TFJS. RFD 2216 blocklists
  three.js; extending that to "one browser inference runtime"
  belongs in a follow-up RFD if it becomes a live question.

## Verification

Smallest-first proof-of-life:

- Gemma 3 270M @ Q4 loads via SQLite range-fetch on Chrome desktop,
  first token latency measured cold + warm, paired with household-
  object equivalent per CLAUDE.md.
- Same measurement on iOS Safari 26 preview (WebGPU behind flag) —
  confirms the mobile ceiling holds.
- Same load path with a **planted broken SHA** on the SQLite blob
  errors cleanly rather than silently loading zeros (rule 2
  negative control).

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3.
- [RFD 2211](../2211-base-tree-entities-godot-sandbox/) — the
  WebGPU-fork patch series that gives Godot's renderer WebGPU.
- [RFD 2214](../2214-model-bundle-sqlite-range-fetch-zstd/) — the
  model-in-SQLite loader path this RFD generalises.
- [RFD 2218](../2218-ggml-webgpu-backend/) — the ggml WebGPU backend
  motion-bricks was the first case of; this RFD makes it universal.
- RFD 2188 (one ggml across workspace) — the canonical ggml source
  every consumer links.
- RFD 2199 (HAILO 4-bit QAT survey) — SIDEKICK's earlier work on
  Gemma 4 E2B/E4B measurements, referenced in the inventory.
- Memory: `cuda-tests-ship-to-hf` — quantized checkpoints ship as
  HF datasets, which the browser SQLite converter reads.

## Operator context 2026-09-05

Two mid-session directives (verbatim): *"we have many many many
ggml based models. figure out how we can use them on platform=web
webgpu"* + *"you may need to pick the smallest gemma4"*.

The "smallest gemma4" reading: Gemma 4 E2B is the smallest of the
Gemma 4 family we have on hand. But **Gemma 3 270M** (already in
the workspace's HAILO project) is smaller still and follows the
same recipe — this RFD picks it as the first ship, treating
Gemma 4 E2B as the second, so we prove the stack on the
cheapest-possible model before committing browser memory to a 750
MB Q4 bundle. If operator wants Gemma 4 specifically, the swap is
one line in the inventory; the recipe is unchanged.

This RFD was drafted by an AI and read by a human before it shipped.
