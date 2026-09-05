# RFD 2211: base tree — `entities-godot-sandbox` for the web export

**State:** discussion
**Flight level:** L2 (coordination)
**Feature:** which of the two Godot fork trees is the base for the
atelier `platform=web` export
**Scope:** `3-interactor/entities-godot-{main,sandbox}`

## Decision

**`entities-godot-sandbox` with the WebGPU-fork patch series
applied.**

Both trees are byte-identical except under `modules/sandbox/`:
`-main` tracks the vendored `godot-sandbox` subrepo pinned via
`.gitrepo`; `-sandbox` carries local sandbox-module modifications.

[RFD 2213](../2213-vrm-via-godot-sandbox-elf/) picks `modules/sandbox`
(libriscv) to load `V-Sekai/godot-vrm` as a RISC-V ELF; that path
needs the local iteration.

**Amendment 2026-09-05 (operator refinement, verbatim):** *"use the
existing webgpu godot fork. add it as a patch to our godot-entities"*.
The WebGPU-capable Godot fork (community fork with `RenderingDevice`
WebGPU backend) is applied as a patch series on top of
`entities-godot-sandbox`, not as a base-tree replacement. The
sandbox tree stays the source of truth for engine + custom modules;
WebGPU support arrives as a patch layer the manifest applies at
`repo sync` time.

**Amendment 2026-09-05 (second operator reversal):** the WebGPU-fork
patch series is now motivated by **native WebGPU rendering** (Dawn /
wgpu-native), not by browser WebGPU. Per [RFD 2228](../2228-webgpu-native-drop-platform-web/)
the atelier drops the browser export; the WebGPU-Godot fork is the
same patch set, its output target changes from Emscripten + native
fallback to native across the board. The base-tree pick
(`entities-godot-sandbox`) stands unchanged.

This unblocks [RFD 2218](../2218-ggml-webgpu-backend/) — the ggml
WebGPU backend runs against the same native `WGPUDevice` Godot's
renderer requests through Dawn, so the desktop binary gets one
WebGPU adapter, not two.

**Amendment 2026-09-05 (third reversal, retracts the WebGPU-fork
patch amendment above):** [RFD 2231](../2231-drop-webgpu-use-vulkan/)
blocklists WebGPU as a workspace render/compute target — native
delivery removes the reason WebGPU was in the stack, and Vulkan
has ~10 years of production QA vs WebGPU's ~2 with Godot's
`RenderingDevice` already Vulkan-based. The WebGPU-Godot-fork
patch series is retracted; Godot's shipping Vulkan renderer is
the answer. Base-tree pick (`entities-godot-sandbox`) still
stands unchanged — this is the third time it survives a reversal,
which is the signal it was picked for the right reason.

Pin the exact commit in `.repo/manifests/default.xml`, plus the
patch-series SHA range from the WebGPU fork. Don't track a moving
branch.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3 anchor.
- [RFD 2213](../2213-vrm-via-godot-sandbox-elf/) — why the local
  sandbox iteration matters here.

This RFD was drafted by an AI and read by a human before it shipped.
