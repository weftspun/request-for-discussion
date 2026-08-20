# RFD 0123 details: the licence, the interfaces, and the 12 bit path

## The licence argument in full

Four projects matter here. Three were checked against the GitHub API rather than recalled.

| project | licence | role |
| --- | --- | --- |
| `gopro/cineform-sdk` | Apache-2.0 OR MIT | the codec we propose to vendor |
| `godotengine/godot` | MIT | the engine |
| `EIRTeam/EIRTeam.FFmpeg` | MIT | an existing Godot video plugin |
| FFmpeg | LGPL-2.1 or later, GPL in some builds | what that plugin links |

The SDK entry is better than the GitHub API reports. The API returns Apache-2.0, because it
names one licence. The repository holds both `LICENSE-APACHE` and `LICENSE-MIT`, so the SDK is
dual licensed. That is the same `Apache-2.0 OR MIT` we apply to our own code.

Read the repository, not the API field. The API picks one licence and a dual licence has two.

The plugin licence and the dependency licence are different things. `EIRTeam.FFmpeg` is MIT
and it links FFmpeg. A reader who checks only the plugin sees MIT and stops. The terms that
reach a shipped game come from FFmpeg.

This is the same mistake the workspace already recorded about ControlNets. A base model can be
Apache-2.0 while its control weights are not. So read the licence of the part that does the
work. Here that part is FFmpeg.

LGPL-2.1 asks that a user can replace the library. A Godot export is one binary with
everything linked in. Meeting the condition means shipping relinkable object files or moving
FFmpeg to a shared library the user can swap. Both are possible. Both add a step to every
release, forever.

Apache-2.0 asks for attribution and a patent grant. It adds nothing to the release process.

## What CineForm is, and why it suits depth

CineForm is a wavelet codec. Each frame is complete on its own, so there are no predicted
frames and no group of pictures. Seeking to frame 41,000 costs one frame of work.

That property is why it fits a corpus. A training loader reads frames in whatever order the
sampler asks for. A codec that predicts frames turns a random read into a decode of everything
since the last keyframe.

The codec reaches 12 bits for each channel. It also carries alpha in `gbrap12le`, which is
what the keypoint overlay track needs.

## The pixel formats FFmpeg 8.1.2 offers for `cfhd`

    yuv422p10le    10 bit, chroma at half width
    gbrp12le       12 bit planar RGB
    gbrap12le      12 bit planar RGB with alpha

Depth goes in `gbrp12le`, with the same code written to all three planes. The codec then sees
no colour detail and spends no bits on it.

Depth could go in `yuv422p10le` luma alone, and chroma subsampling would not touch it. It is
still 10 bit, and the table in the README rules that out on precision.

## The trap in the texture path

Godot image formats that hold more than 8 bits for each channel are these.

    FORMAT_RH, FORMAT_RGH, FORMAT_RGBAH     16 bit half float
    FORMAT_RF, FORMAT_RGF, FORMAT_RGBAF     32 bit float

A half float has an 11 bit significand. A 12 bit integer code needs 12. So a 12 bit code
cannot round trip through any of the half formats.

The failure is quiet. The image loads, the depth map looks correct, and the bottom bit is
gone. Nothing raises and no test that only checks the picture will notice.

Two ways through, and the choice belongs in the implementation review.

**32 bit float.** `FORMAT_RF` holds one channel and every 12 bit code exactly. It costs 4
bytes for each pixel on the GPU.

**Two 8 bit channels.** Split the code into a high byte and a low nibble. `FORMAT_RG8` costs
2 bytes for each pixel. The shader recombines them. This keeps memory down and moves the risk
into shader code that must be tested.

## The interfaces to implement

Godot calls into two classes.

`VideoStream` describes the file. It reads the path and creates a playback object.

`VideoStreamPlayback` does the work. These are the virtual methods, read from godot-cpp's
`extension_api-4-5.json` rather than recalled.

    void _play()
    void _stop()
    bool _is_playing()
    void _set_paused(bool paused)
    bool _is_paused()
    float _get_length()
    float _get_playback_position()
    void _seek(float time)
    void _update(float delta)
    Texture2D _get_texture()
    int _get_channels()
    int _get_mix_rate()
    void _set_audio_track(int idx)

Our streams carry no audio. The audio calls return zero and no mixer runs.

`_get_texture` is where the format choice above becomes visible to every consumer.

## Retracted: the interface does not drift across minor releases

A first draft of this RFD warned that the video interface changes between Godot 4 minor
releases. It told the reader to pin the engine version for that reason.

That is not true, and it was written from memory rather than measured. The virtual methods of
`VideoStream`, `VideoStreamPlayback` and `MovieWriter` are identical in
`extension_api-4-3.json` and `extension_api-4-5.json`. Every signature matches.

Pin the engine version anyway, because GDExtension has an ABI and a build for one version is
not automatically loadable by another. Pin it for the ABI, which is the real reason, and not
for an interface churn that the two files show does not exist.

## Two tracks, one file

Each chunk is one Matroska file with two video tracks.

    track 0    depth, gbrp12le, 12 bit
    track 1    keypoint overlay, gbrap12le, 12 bit with alpha

`VideoStreamPlayer` plays one track. The extension exposes a track index so a scene can open
the same file twice and show both.

The overlay colours follow the OKHSL scheme described below, so a viewer reads layer identity
from hue without a legend.

## The colour scheme the overlay carries

Each keypoint takes a hue from the See-Through layer it drives. The 24 layer names come from
`seethrough-torch/training/configs/finetune_layerdiff_iter2.yaml`.

    hue                which See-Through layer the joint drives
    hue plus or minus 6 degrees    which joint inside that layer
    lightness          position along the chain inside the layer
    shape              filled if unoccluded, hollow if the surface is in front

OKHSL rather than HSL, because HSL lightness is not perceptual. At one fixed HSL lightness the
yellows glare and the blues sink. A reader then sees brightness differences that mean nothing,
and misses the lightness differences that carry chain position.

An earlier draft spread all 104 hues by the golden angle to make neighbours distinct. That is
the wrong goal. It scattered the five joints of one hand across the whole wheel, so nothing in
the picture said they belong to one garment region.

ANNY drives 9 of the 24 layers. The other 15 have no bone at all. The legend lists them greyed
rather than leaving them out. A category that is simply absent reads as a category that does
not exist, and RFD 0121 records why that gap matters.

## What the chunk manifest must carry

Quantisation is linear between a near plane and a far plane. Those two numbers invert it. A
chunk without them is a picture, not a measurement.

    near_m, far_m          the depth band, in metres
    bits                   12
    pix_fmt                gbrp12le
    codec, encoder_version the codec and the FFmpeg build that wrote it
    frame_first, frame_count
    camera                 view matrix, field of view, width, height
    seed                   the render seed, because Mitsuba reproduces from it
    anny_version, git_sha

The render seed is not decoration. We measured that the same seed returns a bit identical
image and a different seed changes every body pixel. So the seed is what makes the corpus
reproducible, and the constructed synthetic rule asks for exactly that.

## How decode speed gets measured

Measure before building. The SDK has no hardware path, so decode runs on the CPU.

Decode 200 frames at 1024 by 1024 from a written chunk. Report milliseconds for each frame on
one core, and again with the thread count the SDK offers. State the number of cores used.

30 frames each second allows 33 ms for each frame. Report the result against that figure
rather than in isolation, because a number with no baseline is not a measurement.

If one core cannot hold the rate, the answer is a decode thread that runs ahead of playback.
That is ordinary work. It is better to know before the extension exists.

## Risks

**The SDK is quiet.** `gopro/cineform-sdk` has few contributors and slow traffic. Vendor it at
a pinned commit and record the hash. Do not track a moving branch.

**Windows and Linux both matter.** The desk is Windows and the pods are Linux. Build both from
the start, because a decoder that works on one is half a decoder.

**FFmpeg writes the files and the SDK reads them.** Two implementations of one format will
disagree somewhere. The round trip gate must run against files written by FFmpeg, not against
files the SDK wrote itself. A codec checked only against its own output has been checked
against nothing.
