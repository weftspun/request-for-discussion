# RFD 107b: CineForm in Godot, both directions

**State:** discussion
**Feature:** CineForm video decode and encode inside Godot Engine
**Scope:** `entities-godot/modules/cineform`, `6-datasource/dataflow-coco-gemx`,
`3-interactor/pose-consensus`

## Problem

We write depth as CineForm video in Matroska and Godot cannot read it. Godot 4 ships one video
codec, Theora, which is 8 bit where our depth needs 12. An 8 bit depth map has 256 steps across
the body, 6.3 mm per step, about four stacked credit cards, and the renderer measures to better
than 1 mm. The corpus is 800,000 frames, too many to hold loose: 12 bit CineForm at 1024 by 1024
costs 127 MB for every 1000 frames, and 16 bit PNG costs about ten times more.

## Decision

Decode and encode CineForm inside Godot, with the GoPro CineForm SDK and not FFmpeg.

1. **The licence decides this, not the code.** The SDK is `Apache-2.0 OR MIT`, matching our own
   code. FFmpeg is LGPL-2.1 or later, and a Godot export links into one binary, so LGPL asks for
   relinkable objects the SDK does not.
2. **Carry 12 bits all the way to the texture.** Godot's half float format holds an 11 bit
   significand, so `FORMAT_RGBAH` loses the bottom bit and looks correct. Depth lands in
   `FORMAT_RF`, or stays as integer codes in two 8 bit channels.
3. **One component, both directions.** The SDK holds an encoder and a decoder, the licence
   argument is the same for each, and splitting them would vendor one dependency twice.
4. **Expose the track.** A chunk holds two tracks, depth and the alpha-carrying keypoint overlay,
   and a caller chooses between them.
5. **Verify by round trip, with a negative control.** Encode a known ramp, decode it in Godot,
   compare the texture in millimetres, then run the same check at 8 bit and assert it fails.

See `DETAILS.md` for the licence argument, 12 bit against 10 bit, the retracted free-codec claim,
the alternatives, the interfaces, the chunk manifest, and what shipped instead of a GDExtension.

## Related

RFD 1079 and RFD 107a cover the corpus this video carries. RFD 1035 makes OpenUSD the internal
format for geometry, and this RFD does the same for rendered frames.
