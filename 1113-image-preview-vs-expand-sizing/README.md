# RFD 1113: Image preview stays 250px, the expand modal stays separate

**State:** committed
**Scope:** `src/components/expandedImagePreview.css`,
`ImagePanelPreview.{css,jsx}`, `TextureExtractor.css`

## Problem

An in-panel image preview (a Krea task-row thumbnail, or a Texture
Extractor grid tile) and its click-to-expand modal share one visual
job, showing the same image larger. A single CSS variable once
served both, so a fix to one size regressed the other. The user
confirmed the current split on 2026-06-30, per
`rules/image-preview-sizing-protected.mdc`.

## Decision

Two variables, two jobs, never merged. `--panel-image-preview-height`
holds the in-panel size, at `250px`. Krea's task-row thumbnail and
the Texture Extractor's `.texture-preview` grid tile both use it.
`--expand-modal-image-preview-max-height` holds the click-to-expand
size, at `min(80vh, 512px)`. The expand modal and the Texture
Extractor's `.texture-details-preview img` both use it. Both
variables live in `expandedImagePreview.css` only; no other file
redefines either one.

The in-panel preview does not grow on hover. It expands only on a
click, into the modal. A change to one context's size, without an
explicit user request naming both, must not touch the other
context's variable.

## Related

RFD 1000 gives the DRY policy this split rule follows: one token,
one owner, one file. RFD 1112 lists this rule among `rules/`'s guard
rules, and points here for the design it protects.
