# RFD 2231: drop WebGPU, use Vulkan (native-only means the browser carveout is gone)

**State:** discussion
**Flight level:** L3 (strategy — retracts the WebGPU premise
across RFDs 2211/2218/2228)
**Feature:** native-only delivery (per RFD 2228) removes the
reason WebGPU was in the stack; Vulkan has decades more
production QA on all three targets and is Godot's primary
renderer
**Scope:** RFD 2211 (WebGPU-fork patch amendment retracts), RFD
2218 (ggml WebGPU backend → ggml Vulkan backend), RFD 2228
("native WebGPU" → "native Vulkan (MoltenVK on macOS)"), RFD
2230 (native module compute backend), CLAUDE.md + BLOCKLIST.md
new blocklist row

## Operator directive

Verbatim 2026-09-05: *"wait a second if we're native we can
blocklist webgpu and only use vulkan which has more quality
assurance hours in production"*, followed by *"vulkan on mac,
windows and linux has more quality assurance hours than webgpu"*.

## Why WebGPU was in the stack

WebGPU showed up because the delivery surface was `platform=web`
(RFDs 2210 / 2211 / 2218 / 2227). The browser can't call Vulkan
directly, so ggml matmul on the browser side had to go through
WebGPU or fall back to CPU-in-WASM. WebGPU-native (via Dawn or
wgpu-native) was picked for the desktop side too so both surfaces
shared one backend.

RFD 2228 dropped `platform=web`. **The browser reason is gone.**
The desktop reason (share one backend across browser + native)
only had value while both existed.

## Why Vulkan wins on each target

| target | WebGPU-native path | Vulkan path |
|---|---|---|
| Linux | Dawn/wgpu → Vulkan | Vulkan direct |
| Windows | Dawn/wgpu → D3D12 (or Vulkan) | Vulkan direct |
| macOS | Dawn/wgpu → Metal | Vulkan → MoltenVK → Metal |

Linux and Windows: Vulkan removes one translation layer. macOS:
WebGPU-native has the shorter Metal path (one hop vs MoltenVK's
two), but MoltenVK is battle-tested — shipped in Godot since
3.x, used by every Vulkan macOS game — while Dawn's macOS
backend is much newer. Godot 4's primary renderer is Vulkan-
based (`RenderingDevice` driver); using anything else means
fighting the engine.

Production-QA hours: Vulkan 1.0 shipped 2016 (~10 years);
WebGPU stable in Chrome late 2023 (~2 years). Operator confirmed
2026-09-05 that Vulkan has more QA hours on all three targets.

## What this retracts

- **RFD 2211's WebGPU-Godot-fork patch amendment.** Godot's
  shipping Vulkan renderer is the answer; no fork patch series
  needed. The base-tree pick (`entities-godot-sandbox`) stands
  unchanged.
- **RFD 2218 (ggml WebGPU backend).** Retracts as a delivery
  target; use **ggml's Vulkan backend** (present in upstream
  ggml for years, more mature than the WebGPU backend llama.cpp
  added recently). RFD 2218's approach-A (adopt llama.cpp's
  backend) still applies — the workspace inherits llama.cpp's
  Vulkan backend rather than its WebGPU one.
- **RFD 2228's "native WebGPU via Dawn/wgpu-native" wording.**
  Native delivery stays; the API changes from WebGPU to Vulkan.
  Two-heads architecture (RFD 2215) and everything else in
  2228's "what survives" section stand.
- **RFD 2230's native compute backend.** The `modules/ggml/`
  under `entities-godot-sandbox` links **ggml's Vulkan backend**
  (not WebGPU); GDExtension surface exposed to GDScript adapters
  is unchanged.

## What survives

- Native-only delivery (RFD 2228 core).
- `entities-godot-sandbox` as base tree (RFD 2211 base pick).
- `modules/ggml/` as one shared native ggml module (RFD 2230
  layering).
- GDScript adapters over the GDExtension surface (RFD 2230).
- SQLite+ZSTD model bundle on local disk (RFD 2214, rescoped).
- Godot native binary as three.js substitute (RFD 2216).
- One-binary-two-heads: interactive window + headless
  `--write-movie` capture (RFD 2215).

The atelier stack after this RFD: **Godot native binary with
Vulkan (MoltenVK on macOS) renderer + Vulkan-backed ggml + one
`modules/ggml/` module + N GDScript adapters + SQLite+ZSTD model
bundle on local disk.**

## Blocklist row

Adds a WebGPU row to CLAUDE.md's blocklist table:

    | **WebGPU** as a workspace render / compute target | RFD 2228 dropped the browser delivery that made WebGPU worth having; on native, Vulkan has ~10 years of production QA vs WebGPU's ~2, is Godot 4's primary renderer, and skips a translation layer on Linux/Windows (MoltenVK's two hops on macOS are battle-tested vs Dawn's newer Metal backend); RFDs 2211's WebGPU-fork amendment + 2218 (ggml WebGPU backend) + 2228's WebGPU wording all retract by this row — see below

Blocks: `Ggml.WebGPU=ON`, Dawn/wgpu-native as a dependency,
Godot forks whose sole purpose is a WebGPU renderer, ORT-Web
+ TFJS WebGPU EPs (already covered by RFD 2216 companion
blocklist, generalises).

**Not blocked:** reading a WebGPU spec or example to understand
a Vulkan concept. WebGPU on a third-party site we don't ship
(reference docs, tutorials).

## Blast radius

Nothing in this session's arc has shipped — RFDs 2211/2218/2228
landed as doctrine, not code. The native module (RFD 2230) is
still design-phase. This retraction costs no code, only prose.

External: llama.cpp's WebGPU backend work is unaffected; the
workspace consumes llama.cpp's Vulkan backend, which is a
different upstream file.

## Verification

- **Godot Vulkan render smoke test.** `entities-godot-sandbox`
  built with default Vulkan renderer opens a window, renders a
  scene. Zero WebGPU-related dependencies in the build. Grep
  `build.log` for `webgpu` returns nothing.
- **ggml Vulkan backend smoke test.** `modules/ggml/` linked
  with `GGML_VULKAN=ON`, `GGML_WEBGPU=OFF` (blocklisted); a
  fixture prompt round-trips through Vulkan matmul.
- **macOS MoltenVK path.** Same tests on macOS — MoltenVK
  translates the Vulkan calls to Metal; smoke test confirms
  matmul output matches Windows/Linux Vulkan output within f32
  tolerance.

## Related

- RFD 2210 (L3 atelier shipping surface) — unchanged; delivery
  is one native binary per platform.
- RFD 2211 (base tree entities-godot-sandbox) — base-tree pick
  stands; WebGPU-fork patch amendment retracts.
- RFD 2214 (model bundle SQLite+ZSTD) — unchanged.
- RFD 2215 (one binary two heads) — unchanged.
- RFD 2216 (three.js blocklist) — unchanged; substitute is
  Godot native binary regardless of graphics API.
- RFD 2218 (ggml WebGPU backend) — retracted, superseded by
  this RFD; use ggml Vulkan backend.
- RFD 2228 (WebGPU native, drop platform=web) — the "native"
  half stands, the "WebGPU" half retracts.
- RFD 2229 (interchangeable-parts consolidation) — this RFD is
  itself an interchangeable-parts consolidation: two graphics
  APIs (Vulkan for engine, WebGPU for ggml) collapse to one
  (Vulkan for both).
- RFD 2230 (ggml adapters in godot-sandbox GDScript) — native
  module compute backend flips from WebGPU to Vulkan; GDScript
  adapter API unchanged.

## Operator context 2026-09-05

Verbatim, this session: *"wait a second if we're native we can
blocklist webgpu and only use vulkan which has more quality
assurance hours in production"* + *"vulkan on mac, windows and
linux has more quality assurance hours than webgpu"*.

Third API reversal in ~24 hours (WebGL2 → WebGPU per RFD 2218;
browser → native per RFD 2228; WebGPU → Vulkan per this RFD).
All three are recorded rather than tidied out because the
pattern matters: the target API keeps moving as the delivery
surface constraint changes. This RFD parks WebGPU and commits
to Vulkan on the argument that native delivery has no reason
to visit WebGPU on the way to the underlying graphics API.

This RFD was drafted by an AI and read by a human before it shipped.
