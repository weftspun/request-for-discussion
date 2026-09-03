# RFD 2020: Pin engine to frozen godot 4 7

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The engine fork carries many feature branches (cassie, resonance
audio, native media, speech, spatial audio, the fabric modules) that
the `merge` recipe assembles onto a base. If that base tracks a moving
upstream, every assembly can shift under the patches, so a green build
one day can break the next from upstream churn alone. What base should
the feature branches and the assembly build on?

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
