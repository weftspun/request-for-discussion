---
title: "RFD 2054: MCP runtime bridge for deployed builds"
rfd: "2054"
state: published
scope: MCP inspection of deployed (non-editor) builds
---

## Problem

The Godot MCP addon is an editor plugin. It drives the editor over
its `EditorInterface`, and the editor does not run inside a deployed
build. Debugging a deployed build, such as a headless zone server, a
mobile client, or an OpenXR app, needs the same inspection with no
editor present.

## Decision

The Godot MCP addon is an editor plugin, so it drives the editor over
its `EditorInterface`. Debugging a deployed build — a headless zone
server, a mobile client, an OpenXR app — needs the same inspection
against the running game, where there is no editor. A runtime
autoload (`mcp_runtime.gd`) serves the same MCP from inside the
running game, injecting the live `SceneTree` where the editor plugin
injects the editor. An MCP client reaches it over `adb forward` (or
any port forward). Scene, node, property, `call_method`, `run_script`,
`get_render_info`, and a runtime-capable `screenshot` operate on the
running game; editor-only commands return an error. The contribution
lands upstream as `vsekai-godot-mcp#1`. A deployed OpenXR build
becomes inspectable and drivable from the workstation: frame stats,
the live scene tree, and arbitrary GDScript against the running game.
Under XR, `screenshot` reads the flat Window viewport, which stays
black because the rendered frames go to the XR compositor's per-eye
swapchain and that is not host-readable; `get_render_info` and
`run_script` cover XR diagnostics instead. Over `adb forward`,
`get_render_info` returns 13 draw calls and 46476 primitives from the
running OpenXR app, and `run_script` reads the live client state.

## References

- Original record:
  `decisions/20260612-mcp-runtime-bridge-deployed-builds.md`
- Upstream PR:
  `https://github.com/v-sekai-multiplayer-fabric/vsekai-godot-mcp/pull/1`

## Related

- `rfd/2031-content-build-merged-double-precision-mcp`: the editor MCP
  this runtime bridge extends to deployed builds.
