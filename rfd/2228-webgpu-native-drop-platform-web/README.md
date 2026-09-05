# RFD 2228: WebGPU native, drop `platform=web`

**State:** discussion
**Flight level:** L3 (strategy — reverses the platform=web premise
that RFDs 2210/2211/2218/2227 stood on)
**Feature:** the atelier ships as a **native binary with WebGPU as
its renderer**, not as a Godot `platform=web` (Emscripten) browser
export
**Scope:** RFD 2210 (L3), RFD 2211 (base tree + WebGPU fork), RFD
2218 (ggml WebGPU backend, now native), RFD 2227 (workspace ggml
consumers, now native), RFD 2214 (SQLite model bundle, now local
file rather than HTTP-Range)

## The reversal

Operator directive 2026-09-05, verbatim: *"drop webgpu
platform=web. try webgpu native"*.

The atelier no longer ships to a browser page. It ships as a native
executable per platform (`.exe` / `.app` / `.AppImage`) with **Godot's
WebGPU renderer** driving it — that is, WebGPU as the graphics API
(via Dawn or wgpu-native on the desktop side), not as the browser
delivery surface. The WebGPU-capable Godot fork that RFD 2211 named
still applies; what changes is *why* — it is the native renderer,
not the browser bridge.

## What this kills

- **Emscripten toolchain path.** No `scons platform=web`. Native
  templates only.
- **SQLite-over-HTTP-Range fetch.** RFD 2214's model bundle stays
  a SQLite file with ZSTD-compressed rows, but it lives on local
  disk next to the binary; `sqlite3_open()` on a filesystem path,
  not `sql.js` + Range GET.
- **`GGML_WASM_SINGLE_FILE=ON`** and every other emcc option in the
  motion-bricks-cpp `if(EMSCRIPTEN)` branch RFD 2212/2218 sketched.
  The branch becomes a native WebGPU build, so `GGML_WEBGPU=ON`
  against Dawn/wgpu-native rather than against Emscripten's WebGPU
  binding.
- **Browser memory ceiling** (2 GB iPad Safari, 4 GB tablets) as
  a sizing constraint on which ggml models are shippable. Native
  binaries take the host machine's memory, so RFD 2227's
  "smallest-first" ordering is no longer forced by a browser
  ceiling — it is still worth doing on stack-collapse-isolation
  grounds, but Gemma 4 E2B (~750 MB Q4) and E4B (~1.5 GB Q4) are
  now first-class options rather than borderline ones.
- **CI web-export workflow** on `entities-godot-sandbox`. Native
  export workflows (macOS / Windows / Linux) replace it.

## What survives

- **Godot as the runtime** — yes.
- **`entities-godot-sandbox` as the base tree** (RFD 2211) — yes.
  Local sandbox-module modifications still needed for the ELF path.
- **WebGPU-capable Godot fork as a patch series** on top of
  `entities-godot-sandbox` (RFD 2211 amendment) — yes, but the
  fork's value is now "native WebGPU renderer" not "browser WebGPU
  bridge". Same patches, different motivation.
- **`modules/motionbricks/`** as a native Godot module (RFD 2212)
  — yes, simpler now: one build path (native), no emcc branch.
- **godot-vrm via `godot-sandbox` RISC-V ELF** (RFD 2213) — yes,
  the ELF loads under native Godot the same way it would have
  under a browser Godot.
- **SQLite + ZSTD as the model bundle format** (RFD 2214) — yes;
  the loader path is `sqlite3_open()` against a local file. The
  ZSTD requirement (operator directive earlier this session)
  still holds because the on-disk size matters for install-time
  bundles.
- **ggml WebGPU backend** (RFD 2218) — yes, and easier: llama.cpp's
  WebGPU backend already targets native (via Dawn) as its primary,
  the browser bindings are the port. This RFD's reversal moves us
  onto llama.cpp's native path directly.
- **Three.js blocklist** (RFD 2216) — yes. The row's rationale
  needs an amendment: the substitute is "the same scene ships from
  `entities-godot-sandbox` as a native binary" rather than "via
  `scons platform=web`". Native Godot vs. three.js is still the
  same choice.

## Why this is coherent

Godot's WebGPU renderer targets both native and browser from the
same `RenderingDeviceDriverWebGPU` code path — the fork was already
"WebGPU as a rendering backend option alongside Vulkan/Metal/D3D12".
Dropping the browser export drops one output target of the same
fork, not the fork itself.

ggml's WebGPU backend (RFD 2218 approach A) inherits the same
property: `ggml-backend-webgpu.c` calls `wgpuInstanceCreateInstance`,
which resolves to Dawn on macOS/Windows/Linux native and to the
browser's `navigator.gpu` under Emscripten. Native compiles the
Dawn side, browser compiled the Emscripten side; the C code is one
file.

So the reversal costs the CI web workflow and the SQLite-over-HTTP
path, and buys back native install size, native memory ceilings,
and a simpler build matrix (three native platforms vs. one browser
+ three native fallbacks).

## What the atelier delivers now

- **Interactive game head** (RFD 2210 §"one binary two heads"): a
  native window, camera + microphone input from OS APIs, WebGPU
  render output.
- **Headless capture head** (RFD 2210 §"one binary two heads"):
  same binary invoked with `--capture` flag, writes PSD frames or
  a CineForm-encoded video (RFD 2206 amendment) for the video
  demo.

The "two heads" architecture from RFD 2215 is preserved; only the
delivery surface changes from `.html` + native fallback to native
across the board.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3 that
  named `platform=web` as the delivery surface; needs a retraction
  pointer at that section, superseded by this RFD.
- [RFD 2211](../2211-base-tree-entities-godot-sandbox/) —
  base-tree pick stands; the WebGPU-fork-patch amendment needs its
  motivation rewritten from "browser WebGPU bridge" to "native
  WebGPU renderer".
- [RFD 2214](../2214-model-bundle-sqlite-range-fetch-zstd/) —
  SQLite + ZSTD still the model bundle; loader path simplifies to
  local file `sqlite3_open()`; the range-fetch-over-HTTP section
  retracts.
- [RFD 2218](../2218-ggml-webgpu-backend/) — ggml WebGPU backend
  stands, target changes from Emscripten binding to Dawn/wgpu-
  native.
- [RFD 2227](../2227-workspace-ggml-models-on-platform-web-webgpu/)
  — the "workspace ggml on platform=web" premise dies. A
  successor RFD scoping "workspace ggml on native WebGPU" carries
  the same inventory and recipe minus the browser sizing
  constraint.
- [RFD 2216](../2216-threejs-blocklist/) — blocklist row rationale
  needs an amendment paragraph noting the substitute is now a
  native binary, not a browser export.

## Operator context 2026-09-05

Verbatim, this session: *"drop webgpu platform=web. try webgpu
native"*.

This RFD is the second reversal in ~24 hours (the first was
2026-09-04 WebGL2→WebGPU per RFD 2218). Both are recorded rather
than tidied out because the pattern matters: WebGPU is the answer;
its delivery surface (browser vs. native) is the axis that is still
moving. This RFD parks the browser side and commits to native.

This RFD was drafted by an AI and read by a human before it shipped.
