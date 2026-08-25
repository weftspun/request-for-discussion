# RFD 1073: A billboard gallery of the RFD 1064 dataset, in one USD stage

**State:** prediscussion
**Scope:** RFD 1064's dataset, `apps/usd_viewer_app/`

## Problem

RFD 1064's dataset holds about 15,000 anime images and captions, on
disk, unused until step 1 writes a `problem.ex` per row. Nothing
shows what the dataset actually contains today. A person cannot see
it without writing code to open a parquet shard.

## Decision

Wrap every dataset image as a flat billboard card, per the technique
this session already verified: a textured quad, alpha cutout, no
mesh generation needed. Compose every card into one USD stage, each
holding its image and caption as metadata. Serve that stage from
`usd_viewer_app/`, the companion app already built this session.

Scale honestly against the clock. One shard, of 42, proves the
mechanism first: extract, downscale, author, package, verify it
opens, verify it renders. Every later shard runs the same script.
See `DETAILS.md` for the exact scope shipped today, the file-size
reasoning, and what running the remaining 41 shards needs.

## Related

RFD 1064 gives the dataset this RFD displays. RFD 1053 makes USD the
internal format, and this RFD is the deliberate, scoped exception:
a preview stage, in a companion app, not the main studio client.
RFD 1062 gives the Fly.io toplevel this RFD's app first deployed
beside. RFD 1076 moves that companion app to its own deploy target
entirely (`apps/usd_viewer_app/`), reached through a
`GallerySource` port, and gives the `usd-viewer` patch's real,
current form. RFD 1077 decides Tigris, not `versitygw`, as the
object storage the still-open fetch path in `DETAILS.md` targets.
