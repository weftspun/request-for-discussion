# RFD 1152: Background removal for photographic corpora

**State:** published
**Feature:** background removal

## Problem

See-Through decomposes a character into semantic layers, and the union of its
nineteen part masks is an obvious foreground matte. It is already in the
manifest, already loaded, and on most frames it produces a clean cutout.

It is the wrong instrument for a photographic corpus, for a structural reason
rather than a quality one. A union of semantic classes can only keep what it can
name, and the model is trained on anime characters. Measured on a cosplay
photograph, a Santa hat scored -8.38 on `headwear` -- a confident negative, not a
borderline miss -- so the union placed a real garment in the background and
deleted it. No threshold recovers it; at a threshold low enough to matter the
union grows from 0.50 to 0.56 of the frame while `headwear` stays empty.

The same measurement showed the clothing classes fire on body region rather than
on cloth: a nude torso is labelled `topwear`, and mask-derived coverage reads
0.81 to 0.93 on images that are largely bare skin.

## Decision

Background removal uses a photo-trained dichotomous matting model, not a union of
semantic part masks. `ZhengPeng7/BiRefNet_HR-matting` is the default. It has no
vocabulary to fall outside of, so it cannot lose a garment for not knowing what
the garment is.

See-Through is retained for what transfers -- geometry -- and not for what does
not -- semantics. Its part masks may be used as regions, never as labels for what
covers what.

## Related

RFD 1006 covers layer decomposition. RFD 1153 covers how the resulting mattes are
judged. RFD 1030 records the See-Through components.
