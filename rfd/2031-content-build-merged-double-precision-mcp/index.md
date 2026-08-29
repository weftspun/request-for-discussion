---
title: "RFD 2031: Content creation in a single merged double-precision build via the editor MCP"
rfd: "2031"
state: published
scope: content authoring build and editor MCP
---

## Problem

Content creation needs the full engine, every `feat/*` capability, at
double precision. The team can budget only one such build for the
content slice. The pipeline also needs to avoid a Blender dependency,
and a content tool needs a way to drive the editor directly.

## Decision

Content creation needs the full engine, every `feat/*` capability at
double precision, without Blender, and the team budgets a single such
build for the slice. The project produces one Godot build by merging
all `feat/*` branches with the `merge` tool at `precision=double`, and
drives content creation through the `vsekai-godot-mcp` editor server,
where the Godot editor is the MCP server over streamable-HTTP, because
one merged build covers authoring and the MCP lets a content tool
drive the editor directly. The pipeline uses no Blender. One merged
double-precision build covers content authoring for the slice, a
content tool drives the editor through the MCP, and the pipeline
carries no Blender dependency.

## References

- Original record:
  `decisions/20260611-content-build-merged-double-precision-mcp.md`
- `vsekai-godot-mcp` editor server
- `rfd/2007-godot-double-precision-template-release-for-zone`

## Related

- `rfd/2029-cassie-desktop-curvenet-authoring`: the same no-Blender
  authoring path.
