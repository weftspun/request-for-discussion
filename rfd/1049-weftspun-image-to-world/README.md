# RFD 1049: Model image for weftspun_image_to_world

**State:** abandoned
**Feature:** model packaging

## Problem

This entry builds an explorable world from one image. It runs
TripoSplat for the environment, and TRELLIS.2 for the props. RFD 1026
records its own parameter count as 0, because it owns no weights.

The two halves make different things. A splat is a radiance field, and
a prop is a mesh. One output file cannot hold both well.

## Decision

Do not package this model image. Abandon this line of work.

RFD 1064 turns the roadmap toward character concepts, and away from
explorable worlds. RFD 1052 and RFD 1051, its two splat-half
dependencies, are abandoned for the same reason. Package this entry
again only if the world-building scope returns.

See `DETAILS.md` for the per-part memory and the `predict()`
interface this RFD sketched before the pivot.

## Related

RFD 1064 records the pivot this RFD yields to. RFD 1052 gave the
splat half. RFD 1038 gave the prop half, and it stays active for
character mesh generation. RFD 1053 gives the stage composition this
RFD would have used. RFD 1037 gives the convention.
