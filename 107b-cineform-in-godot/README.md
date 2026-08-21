# RFD 107b: CineForm in Godot, both directions

**State:** discussion
**Feature:** CineForm video decode and encode inside Godot Engine
**Scope:** `3-interactor/godot-cineform`, `6-datasource/dataflow-coco-gemx`,
`3-interactor/pose-consensus`

## Problem

We write depth as CineForm video in Matroska. Godot cannot read it.

Godot 4 ships one video codec, Theora. Theora is 8 bit. Our depth needs 12 bits. An 8 bit
depth map has 256 steps across the body. That is 6.3 mm per step, which is about four stacked
credit cards. The renderer measures depth to better than 1 mm, so Theora throws away most of
what we made.

The corpus is 800,000 frames. We cannot hold it as loose images. Depth at 1024 by 1024 in
12 bit CineForm costs 127 MB for every 1000 frames. The same frames as 16 bit PNG cost about
ten times more.

So Godot must read CineForm, or the engine cannot see the data we produce.

## Decision

Write a GDExtension that decodes CineForm. Use the GoPro CineForm SDK. Do not use FFmpeg.

**1. The licence decides this, not the code.** GoPro publishes the CineForm SDK under
`Apache-2.0 OR MIT`. It ships both licence files. FFmpeg is LGPL-2.1 or later, and some
builds are GPL.

Godot exports link everything into one binary. LGPL then asks us to ship relinkable object
files or a separate shared library. The SDK asks for neither. Our own code carries
`Apache-2.0 OR MIT`, so the SDK matches it exactly.

`EIRTeam.FFmpeg` already decodes video in Godot and carries an MIT licence. The plugin licence
is not the problem. The FFmpeg it links is the problem.

**2. Implement `VideoStream` and `VideoStreamPlayback`.** These are the engine interfaces
that `VideoStreamPlayer` calls. A decoder behind them works in any scene with no new node
type.

**3. Carry 12 bits all the way to the texture.** This is the part that is easy to get wrong.

Godot's half float image format holds an 11 bit significand. A 12 bit code cannot survive it.
A reader who picks `FORMAT_RGBAH` because it says "float" will lose the bottom bit and see
nothing wrong. Depth must land in `FORMAT_RF`, which is 32 bit float, or stay as integer
codes in two 8 bit channels.

**4. Expose the track.** Each chunk holds two video tracks. Track 0 is depth. Track 1 is the
keypoint overlay, which carries alpha. `VideoStreamPlayer` plays one track, so the extension
must let a caller choose.

**5. Write the encoder too, in the same extension.** Godot records offline video through
`MovieWriter`. It ships a raw uncompressed AVI writer and a PNG sequence writer, and nothing
between them. Raw AVI at 1024 by 1024 costs about 3 GB for every 1000 frames.

One extension carries both directions. The SDK holds an encoder and a decoder, the licence
argument is the same for each, and splitting them would vendor the same dependency twice.

The encoder exists and lives in `3-interactor/godot-cineform`. It claims the `.cfhd`
extension, uses the SDK encoder pool so encoding runs off the render thread, and writes AVI.
The corpus remuxes to Matroska with `ffmpeg -c copy`, which copies the stream and re-encodes
nothing.

## What we measured before proposing this

The numbers come from FFmpeg 8.1.2 on the local machine. The test is 24 frames at 1024 by
1024, of a depth ramp with a 0.2 m step in it. The step is there because wavelet codecs do
their worst at edges. A smooth ramp alone flatters them.

| pixel format | bits | MB per 1000 frames | median error | worst error |
| --- | --- | --- | --- | --- |
| `gbrp12le` | 12 | 127 | 0.46 mm | 3.3 mm |
| `yuv422p10le` | 10 | 94 | 2.10 mm | 7.9 mm |

Quantisation alone costs 0.39 mm for each step at 12 bit and 1.56 mm at 10 bit. So CineForm
adds about one step of error and no more.

0.46 mm is about half the thickness of a credit card. 3.3 mm is about two stacked pennies, and
it happens only where an arm crosses a torso.

10 bit is not enough. Its 2.10 mm median is coarser than the 0.54 mm agreement we measured
between two independent renderers. It would become the largest error in the chain.

Matroska accepts CineForm. MOV accepts it too and gave identical results. We choose Matroska
because it is the open container.

## Retracted: an earlier claim that the codec was free

A first probe reported that 97% of codes returned bit exact and that the codec added 0.0 mm.
That measurement was wrong, and it was wrong in a flattering direction.

The probe clipped the depth step below the near plane. Clipping produced large flat regions.
Flat regions compress exactly, so the codec looked perfect on data that was already ruined.

The corrected probe reports 5.87% of codes exact and a median error of 0.39 mm. The lesson is
the one this workspace keeps relearning. A check that passes on broken input certifies the
defect.

## Alternatives, and why each fails

**Link FFmpeg through `EIRTeam.FFmpeg`.** This works today and needs no new code. It brings
LGPL into every export. We reject it on licence, not on quality.

**Transcode to VP9 or AV1 for Godot.** Both are open and both reach 12 bit. Both are also
generational codecs that predict frames. Our depth frames are measurements, and we want each
frame decoded on its own. Transcoding also adds a second lossy step on top of CineForm.

**Ship PNG sequences.** This keeps 16 bits and needs no decoder. It costs about ten times the
space and gives up seeking.

**Wait for Godot to add a codec.** Godot has shipped only Theora for years. We treat this as
unavailable rather than late.

## What is built, and what is not

The encoder is written. Its round trip gate runs today and passes. The test pattern holds flat fields, a hard edge and a one
pixel checker. It returns a median error of 0.00 codes and a worst error of 2.00 codes. The negative control zeroes 8 KB in the middle of the file, and the check
rejects it at 215 codes.

The extension has not been compiled. Every SDK symbol it calls was read from the published
headers rather than recalled. The README lists each one with the header it came from. Reading
a header is not linking against it, so the first build is part of the work.

The decoder is not written. This RFD proposes it.

## How this gets verified

The gate is a round trip, not a playback demo. Encode a known depth ramp. Decode it inside
Godot. Read the texture back. Compare against the source in millimetres.

Ship a negative control with it. Run the same check through an 8 bit path and assert that it
fails. A gate that only ever passes has proved nothing about the thing under test.

Record the decode cost for each frame. A decoder that misses 30 frames each second changes how
the studio uses this. So the number belongs in the result.

## The cheapest thing that could change the plan

Measure CineForm decode speed on one core before writing any Godot code. The SDK has no
hardware path. One frame at 1024 by 1024 must cost less than 33 ms to hold 30 frames each
second. If it costs more, the answer becomes a background decode thread, or still images in a
different container.

This costs an hour and needs no engine work.

## Related

RFD 1079 and RFD 107a cover the corpus this video carries. RFD 1035 makes OpenUSD the internal
format for geometry, and this RFD does the same job for rendered frames.

## What shipped, and where this RFD was wrong

Kept in place rather than rewritten, because a reader who knows which road was tried is better
off than one who only knows where it ends.

**The GDExtension route is closed.** `MovieWriter` is not exposed to GDExtension, so an
exporter has nothing to register against, and godot-cpp would have been a dependency carried
for an API that cannot be reached. What shipped is an in-engine module: `modules/cineform`
inside `entities-godot`, with the codec vendored at `thirdparty/cineform` and the muxer at
`thirdparty/libwebm`.

**So the Scope line is wrong.** `3-interactor/godot-cineform` was created, used, and deleted.
The manifest entry went with it. One repository builds this now.

**Both directions were built.** `MovieWriterCineForm` writes and `VideoStreamCineForm` reads,
verified against FFmpeg's own `cfhd` decoder rather than against each other.

**The decode budget was met with room.** The RFD asked for one frame at 1024 by 1024 under
33 ms on one core. Measured at 1920x1080, encode is 2.51 ms for each frame and the ladder puts
4K at 11.50 ms, so the background decode thread this RFD held in reserve was not needed.

**The container is Matroska, not raw CineForm.** AVI caps a file at 4 GB, which these bitrates
reach in about 56 seconds of 4K60.

**One measurement contradicts the premise, and is worth stating.** Below 4K the per frame cost
does not depend on resolution: 640x360 has 36 times fewer pixels than 4K and costs the same
16.75 ms. The limit under 4K is the window present, not the codec. This RFD assumed decode
speed would decide the design, and it did not.
