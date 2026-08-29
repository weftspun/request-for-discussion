---
title: "RFD 2118: A baker replaces the Godot editor"
rfd: "2118"
state: discussion
scope: client build pipeline, asset delivery, engine modules
---

## Problem

The Godot editor is a build-time dependency of every client artifact, and two steps are the reason. Resource import turns `.png` into `.ctex`, `.wav` into a sample, and mesh formats into meshes under `res://.godot/imported/`, and the importers live in `editor/`. Export builds the `.pck`, and `--export-release` lives there too. A `template_release` binary reads what both produce and can run neither.

That places a GUI application in the middle of an automated pipeline. `godot-images` builds and publishes editors for Windows and Linux so that CI can call `--export-release`, and `windows-editor.zip` alone is 482 MB. The assets already arrive at runtime from `transport-asset`, so the editor is doing work for content it never sees.

## Decision

**Bake to `.tscn` in the backend.** The text scene format is documented, and `ResourceFormatLoaderText` compiles into every target, so a baker that writes `.tscn` writes a file the release template already knows how to load. The editor is one program that happens to write the same format.

**Carry textures as Basis Universal inside glTF.** Import exists to choose a GPU format ahead of time, and Basis transcodes on the device, so that step has nothing left to do. `KHR_texture_basisu` puts the texture inside the glTF and `GLTFDocument` loads it at runtime. `modules/basis_universal` and `modules/gltf` are already in `entities-godot`, and `godot-images` disables no modules on any platform.

**Run OpenUSD in the baker.** openUSD is a C++ library. `idtx-flow` calls it from an editor import plugin; the baker calls the same library server-side and emits glTF and `.tscn`. This takes USD off artists' machines and out of the engine.

**Mount the filesystem with a small C++ module in the release template.** A `PackSource` resolves `res://` against a directory or against `transport-asset`'s content-addressed chunks, registered at `MODULE_INITIALIZATION_LEVEL_CORE` because `PackedData` is core and has to be serving before anything asks for a path. It has to be a module: GDExtension initializes after the filesystem is up, so it cannot serve boot.

**Keep gameplay out of the module.** Logic stays RISC-V ELF in the sandbox, as `zone-guest-godot` and `zone-guest-middleham` already deliver it. The module is the one part of this stack no CDN can replace, so every line in it costs an engine release to change.

**Stop building the editor when the baker covers every asset class.** Until then `godot-images` keeps building it, and `--export-release` stays available as a fallback.

## References

- `entities-godot`, the engine fork and where the module lands under `modules/`; `godot-images`, the engine builds and the release that now carries templates alone
- `zone-client-godot`, a client already shipping `template_release` and no editor; `zone-guest-godot` and `zone-guest-middleham`, the sandboxed guests the logic lives in
- `transport-asset`, the content-addressed store the pack source reads; `idtx-flow`, the USD import the baker takes over

## Detail

{{< include DETAILS.md >}}
