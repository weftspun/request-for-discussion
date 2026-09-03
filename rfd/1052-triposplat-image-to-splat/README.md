# RFD 1052: Model image for triposplat_image_to_splat

**State:** abandoned
**Feature:** model packaging

## Decision

Do not package this model image. Abandon this line of work.

RFD 1064 turns the roadmap toward character concepts, and away from
single-photo scene reconstruction. RFD 1051, its multi-photo sibling,
and RFD 1049, its would-be caller, are abandoned for the same reason.

See `DETAILS.md` for the model's memory and the `predict()`
interface this RFD sketched before the pivot.

## Problem

TripoSplat turns one photo into a Gaussian splat. It is the
single-photo path, and RFD 1051 is the multi-photo path.

It is also half of RFD 1049, which builds an explorable world. That
makes it two callers with different needs from one model image.

## Related

RFD 1064 records the pivot this RFD yields to. RFD 1051 was the
multi-photo path. RFD 1049 would have mounted these weights.
RFD 1009 records the viewport that would have loaded the result.
