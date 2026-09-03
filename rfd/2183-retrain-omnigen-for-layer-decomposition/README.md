# RFD 2183: Retrain OmniGen for layer decomposition

**State:** discussion
**Feature:** replace rf-detr-Seg + LaMa with a retrained OmniGen
**Scope:** layer decomposition rung of the gacha ladder

## Decision

Layer decomposition is done by retraining OmniGen (MIT-licensed
unified image generator) on multi-view renders of VRMs that passed
the atelier-workshop's quality gate, replacing the rf-detr-Seg +
LaMa inpainting plan in RFD 1168 (layer-decomposition substitute).

Corpus: VRMs shipped by the pipeline, rendered under
`sphere_hammersley_sequence` (per CLAUDE.md), paired as (composite
image, layered ground truth). Constructed synthetic under
CLAUDE.md's data-hygiene clause: labels true by construction, seed
reproducible, no learned-distribution sampling. Fits the four
generated-data conditions vacuously (this is not generated data);
sits alongside real held-out illustration validation.

## Problem

RFD 1168 (See-Through blocklist recovery) substituted rf-detr-Seg
+ LaMa for See-Through, which is blocklisted (no license). LaMa is
a patch inpainter: it fills a hole with pixels resembling its
surround. Layer decomposition needs semantic reconstruction of the
hidden layer (back hair behind front hair, arm behind sleeve, torso
behind cloth). Nothing behind the mask exists in the composite to
copy from, so LaMa produces a plausible surface, not a plausible
back layer. rf-detr-Seg gets the mask; LaMa cannot supply the
content that belongs behind it.

OmniGen is unified image generation with instruction conditioning;
retrained on (composite → layers) pairs from our own pipeline, it
learns the mapping the task actually needs.

## Related

RFD 1168 (rf-detr-Seg + LaMa substitute; this RFD supersedes it),
RFD 1173 (edit-reward corpus), RFD 2136 (gacha ladder),
RFD 2178 (QAFT-4bit across the stack; OmniGen inherits),
RFD 1102 (task catalog; layer-decomposition row updates to point
here), CLAUDE.md blocklist row for See-Through.

This RFD was drafted by an AI and read by a human before it shipped.
