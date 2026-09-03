# RFD 2188: One GGML across the workspace

**State:** discussion
**Feature:** a single canonical GGML source tree the whole workspace consumes
**Scope:** every C/C++ project in `3-interactor` that links a tensor runtime

## Decision

`weftspun/ggml` is the one canonical GGML source in this workspace.
Every consumer references it through the manifest; vendored copies
are deleted; a prek gate refuses any new consumer that brings its own.

Manifest points at branch `weftspun-consolidated`, seeded from
`ggml-seethrough` HEAD (`3404c951`, 2026-08-29) — the richest tip,
carrying 14+ custom backends. `upstream-tracking` branch was pushed
at `ggml-org/ggml master` (2026-08-30) as a future rebase base.

Placed at `2-contract/ggml`: the tensor runtime is a contract every
interactor consumes. There is no `0-shared` hexagon side.

## Problem

Discovery found six divergent copies, two with conflicting-SHA
manifest entries under the same project name (drift alive at the
moment of writing). See DETAILS.md for the table and the
skipped-cherry-pick list.

Phase 1 lands the framework: canonical repo, manifest change,
singleton gate, RFD. Phase 2 migrates the remaining consumers one
PR at a time, resolving the two Metal cherry-pick conflicts by hand
against the newer backend surface.

## Related

RFD 1000 (hexagon-side placement rule), RFD 1102 (task catalog
gacha pipeline consumes ggml through skin-tokens.cpp and
motion-bricks.cpp), CLAUDE.md's ggml/GGUF blocklist row (the vendor's
own runtime is exempt — this RFD is that exemption's canonical form).

This RFD was drafted by an AI and read by a human before it shipped.
