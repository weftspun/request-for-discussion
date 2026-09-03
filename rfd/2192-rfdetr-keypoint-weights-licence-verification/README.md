# RFD 2192: rfdetr keypoint weights licence verification

**State:** discussion
**Feature:** written licence terms for the separately-hosted keypoint weights
**Scope:** `RFDETRKeypointPreview`, `rf-detr-cpp` README claim

## Decision

Contact the weights publisher for written licence terms on
`rf-detr-keypoint-preview-xlarge.pth` and siblings, alongside the
download URL. If clean, correct the `rf-detr-cpp` README so its
licence claim matches the installed package. If unlicensed, add
rfdetr-keypoint to BLOCKLIST.md under the See-Through checkpoints
reasoning. Until terms are written, the weights are usable for
local investigation, not for a shipping corpus or deployed model.

## Problem

`RFDETRKeypointPreview` downloads
`rf-detr-keypoint-preview-xlarge.pth` (164 MB) from the vendor's
object storage. The rfdetr 1.9.3 package on disk is Apache-2.0
across every source (`LICENSE`, `METADATA`, per-variant `license`).
The weights are hosted separately and carry no separate licence
statement, the shape the See-Through row in BLOCKLIST.md already
addresses. `rf-detr-cpp`'s README claims "PML 1.0 for XL/2XL";
the installed package says Apache-2.0. One claim is wrong and
neither is written alongside the weights. Issue 29 closed stale.

## References

Original issue: `weftspun/request-for-discussion` issue 29;
`rf-detr-cpp` README; rfdetr 1.9.3 `LICENSE` and `METADATA`.

## Related

BLOCKLIST.md See-Through checkpoints row (precedent shape),
CLAUDE.md licence discipline, `rf-detr-cpp` project.

This RFD was drafted by an AI and read by a human before it shipped.
