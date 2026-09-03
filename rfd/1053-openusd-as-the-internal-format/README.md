# RFD 1053: OpenUSD as the internal format

**State:** committed
**Feature:** asset interchange

## Decision

OpenUSD is the internal format. Every stage reads a stage and writes a
layer. glTF, VRM, and KHR avatar stay the transmission formats, and
the pipeline converts to them at the edge.

USD is to this pipeline what `.blend` is to Blender. It is the working
file, and it never reaches a browser.

See `DETAILS.md` for why layers beat a flat mesh format, the
internal/transmission boundary, the shared runtime, and what every
model image must return.

Committed 2026-09-02: CLAUDE.md ratifies the choice as a hard
constraint (OpenUSD `.usda` for text-editable, ZStandard parquet for
bulk; zip and gzip banned; usdz exempt). RFD 2169 abandoned the
Elixir studio core; the `fabric-stage-runtime` Hex package still
ships OpenUSD to every consumer.

## Problem

Each pipeline stage reads a GLB and writes a GLB. A rig stage rewrites
the whole file to add bones. A texture stage rewrites it again.

Every rewrite loses what came before. glTF holds one flat result, thus
a stage cannot add an opinion without erasing the previous author.
When a mesh is wrong, no record says which stage made it wrong.

## Related

RFD 1036 gives the model image convention. `fabric-stage-runtime`
(Hex) links this runtime to every stage. RFD 1002 records the
pipeline stages that become layers.
