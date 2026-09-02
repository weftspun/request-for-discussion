# RFD 2168: Retract RFD 1122's bespoke wholebody detector; keep the renderer

**State:** published
**Feature:** documentation retraction
**Scope:** `rfd/1122-the-wholebody-gap`

## Problem

RFD 1122 proposed rendering ANNY to train a 104-point keypoint detector,
then deploying it. Later RFDs (1143 published, 1168 ideation, 1173
discussion) settled the deployment differently, and 1122's `discussion`
state stopped tracking reality.

## Decision

Retract the bespoke detector-training path. RFD 1122 moves to
`abandoned` alongside this document landing. What survives, by
reference into the successor RFDs:

- **Renderer-first (RFD 1122 rule 1).** ANNY is posed and photographed;
  joints come out of camera arithmetic. RFD 1143 uses this as the
  render leg of its propose loop.
- **Two-scorer discipline.** RFD 1143 committed EditScore + Referee,
  because a fit that looks right while the joints are wrong passes
  the first alone.
- **Renderer as comparison, not detector target.** RFD 1173's
  MaskScore construction scores generations by comparing renders to
  targets. No 104-point head trains on the renders.

Retracted: train a 104-point head on rendered ANNY (RFD 1168 moves
layer segmentation into the 3D latent via rf-detr-Seg), and the
wholebody-detector deployment premise (ANNY is the pose primitive
throughout, propose through score).

## Related

Retracts: urn:oid:1.3.6.1.4.1.66606.1.1.1122
Superseded by: urn:oid:1.3.6.1.4.1.66606.1.1.{1143,1168,1173}

This RFD was drafted by an AI and read by a human before it shipped.
