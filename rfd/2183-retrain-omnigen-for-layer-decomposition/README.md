# RFD 2183: Retrain OmniGen for layer decomposition

**State:** discussion
**Feature:** replace rf-detr-Seg + LaMa with a retrained OmniGen
**Scope:** layer decomposition rung of the gacha ladder

## Decision

Retrain OmniGen (MIT-licensed unified image generator) on
multi-view renders of atelier-workshop-passed VRMs for layer
decomposition. Replaces the rf-detr-Seg + LaMa plan in RFD 1168
(See-Through blocklist substitute).

Corpus: VRMs shipped by the pipeline, rendered under
`sphere_hammersley_sequence` (per CLAUDE.md), paired as (composite
image, layered ground truth). Constructed synthetic: labels true
by construction, seed reproducible, no learned-distribution
sampling.

## Problem

LaMa is a patch inpainter; it fills a hole with pixels resembling
its surround. Layer decomposition needs semantic reconstruction of
the hidden layer (back hair behind front hair, arm behind sleeve).
Nothing behind the mask exists in the composite to copy from, so
LaMa produces a plausible surface, not a plausible back layer.
rf-detr-Seg gets the mask; LaMa cannot supply what belongs behind
it. OmniGen retrained on (composite -> layers) pairs learns the
mapping the task actually needs.

## Related

RFD 1168 (rf-detr-Seg substitute; superseded),
RFD 1173 (edit-reward corpus),
RFD 2136 (gacha ladder),
RFD 2178 (QAFT-4bit across the stack; OmniGen inherits),
RFD 1102 (task catalog; layer-decomp row points here),
CLAUDE.md blocklist row for See-Through.

This RFD was drafted by an AI and read by a human before it shipped.
