# RFD 1169 details: the tower, the fork gap, and the half that has no path

## Why this is the vision tower again

RFD 1157 established the shape: EditScore is a LoRA over Qwen3-VL, and
`llama-cpp-npu-vision` compiles the encoder into a HEF while decode
stays on the host. The audio proposal is the same arrangement with a
different front end.

    tower              input                       output

    vision, ViT        image, fixed edge           tokens at 4096
    audio, AuT         128-bin log-mel, fixed      1280, needing a new
                       frame count                 projector to 4096

Both end in an MLP projector writing into the decoder's sequence space,
which is why one hook can serve both and why the fork's refusal to is
the thing to fix rather than a reason to look elsewhere. The widths
differ and the section on the checkpoint below is where that is paid
for.

## The operator question, which is the encouraging one

A Whisper-shaped encoder is two strided convolutions, a positional add,
then transformer blocks. Every operator that needs is already in
`DEVICE_OPS`:

    Conv                 the mel front end
    MatMul, Softmax      attention
    LayerNormalization   45 of them survived in rf-detr's graph
    Erf                  inside the gelu sequence, and only there
    Transpose, Slice, Concat, Add, Mul   shape plumbing

`hailo_ops.usda` records that `Erf` is accepted **only** as part of the
gelu pattern and is rejected standing alone, so an encoder using a gelu
approximation rather than the exact form is worth checking before
assuming it translates.

**The input rank is the risk worth naming, and it looks survivable.**
`_add_input_layers` refused Pixal3D four times because its inputs are a
voxel grid and a timestep rather than anything image-shaped. A log-mel
is 128 bins by a fixed frame count — a single-channel 2D array, which
is exactly the shape the parser wants. This is the one place the audio
path is structurally luckier than the 3D one.

## The fork gap, stated precisely

`tools/mtmd/clip.cpp:2834`, `clip_init_hailo`:

- refuses any `proj_type` but `PROJECTOR_TYPE_QWEN3VL`
- sets `ctx->model.modality = CLIP_MODALITY_VISION` unconditionally
- takes `max_image_edge`, `patch_size`, `spatial_merge_size`,
  `image_mean[3]`, `image_std[3]` — every parameter image-shaped

Upstream `mtmd` is already more general than this. It carries
`CLIP_MODALITY_AUDIO`, a `clip_graph_whisper_enc` builder,
`KEY_A_NUM_MEL_BINS` and `KEY_AUDIO_PROJ_TYPE`. So the work is to widen
the Hailo entry point to the modality the surrounding code already
knows about: a modality argument, mel bins and frame count where edge
and patch go, and no three-channel normalization.

**This is a change to a repository we own.** `weftspun/llama-cpp-npu-vision`
is in `default.xml` pinned at `6a27290`, forked from `hailo-ai/llama.cpp`
for exactly this kind of edit. CLAUDE.md's rule for other people's
codebases applies to the upstream part: match the density of the code
being edited and put the reasoning in the commit message.

## ASR against voice cloning, and the correction

An earlier revision of this section said voice cloning was "not in
reach" and that this buys ears and not a voice. **That was too strong,
and asking for the cloning variant is what exposed it.** Qwen publishes
one, and it is clean:

    model                            licence      params   released

    Qwen3-TTS-12Hz-1.7B-CustomVoice  Apache-2.0   1.92 B   2026-01-21
    Qwen3-TTS-12Hz-1.7B-VoiceDesign  Apache-2.0   1.92 B   2026-01-21
    Qwen3-TTS-Tokenizer-12Hz         Apache-2.0   0.17 B   2026-01-21

All ungated, all newer than Qwen3-VL-8B, and 1.92 B is 1.92 GB at eight
bits against the device's 8 GB. Nothing about availability, licensing or
memory blocks a voice.

**What was actually true is narrower: the synthesis stage does not
compile.** That is a claim about the accelerator and not about the
capability, and conflating the two is the error the earlier wording
made. Split properly:

    stage                          shape              device half?

    audio in, AuT or ASR encoder   fixed              yes
    speaker embedding from a       fixed              yes
    reference clip
    codec tokens to waveform,      fixed, feed        probably, and
    the 0.17 B tokenizer           forward            worth measuring
    text to codec tokens,          autoregressive,    no, RFD 1126
    the 1.92 B backbone            growing cache

**12 Hz is the number that makes this comfortable.** Most neural codecs
run at 25 to 75 tokens a second; this one emits twelve, so a ten-second
utterance is 120 autoregressive steps rather than several hundred. The
stage that cannot be accelerated is also the stage that needs least
accelerating, and it runs on the host exactly as Qwen3-VL's own decode
already does.

**So the corrected statement is that the accelerator buys ears, and the
host can still supply a voice.** That is a different sentence from the
one this document shipped, and the difference matters to anyone reading
it to decide whether the capability is available at all.

The 0.17 B tokenizer is the interesting unmeasured piece. If its decode
side is a feed-forward vocoder it is a small fixed-shape graph and a
plausible rung-1 candidate on its own, which would put the waveform
generation on the device while the token generation stays off it.

## Qwen3.5-Omni has no checkpoint to take a projector from

Ripping the projector from Qwen3.5-Omni was proposed on the grounds that
a retrain is happening anyway. **No official Qwen3.5-Omni exists.** The
Qwen organisation's newest Omni release is Qwen3-Omni-30B-A3B; the
Qwen3.5 line is published in other shapes, and every `Qwen3.5-Omni` name
on Hugging Face belongs to a third party rather than to Qwen. The
announcement page is a JavaScript shell that serves no text to a
fetcher, so this is what the model index says rather than what the blog
says.

That is a statement about what can be downloaded today, not a claim the
model does not exist. If it lands, the argument for taking the newer
projector stands -- a projector being retrained is a projector whose
provenance is free to change.

## The better answer for ASR is a smaller model, not a bigger tower

Searching for that checkpoint turned up three releases that change the
recommendation:

    model                        licence      audio enc       mel

    Qwen3-ASR-0.6B-hf            Apache-2.0   896, 18 layers   128
    Qwen3-ASR-1.7B-hf            Apache-2.0   1024, 24 layers  128
    Qwen3-ForcedAligner-0.6B-hf  Apache-2.0   -                 -

All three are ungated Apache-2.0 and take **128 mel bins**, exactly the
front end this proposal specified.

**The 1.7B is the one to take, and it fits.** Its parameter count is
2.04 B whole -- 4.08 GB at bf16 and 2.04 GB at eight bits against the
device's 8 GB, so unlike almost every row in RFD 1166 it does not meet
RFD 1128's four-bit question at all. Its encoder is 1024 wide over 24
layers, against the 0.6B's 896 over 18, and its decoder is 2048 rather
than 1024.

That is the better trade here. The thing this buys is transcription
quality, the smaller model saves 2 GB that nothing else is waiting for,
and both compile the same way because the encoder is the device half in
either case.

**Its age was queried, and checking inverted the concern.** The `-hf`
suffixes are June transformers conversions; the models themselves are
older. But older than what is the question that matters:

    checkpoint                  released      relative to our base

    Qwen3-Omni-30B-A3B          2025-09-20    3 weeks OLDER
    Qwen3-VL-8B                 2025-10-11    the base
    Qwen3-ASR-0.6B              2026-01-28    3.5 months newer

**The AuT tower comes out of the oldest artifact in the set**, older
than the model it would be bolted onto, while the ASR model that looked
stale is the newest thing here by a wide margin. A recency objection to
`Qwen3-ASR-0.6B` argues harder against the Omni route it was raised to
defend.

**This is arXiv:2608.12875's argument arriving in the concrete.** The
paper's finding is not "smaller is fine" but that a specialised model
ties a general one on the task it was built for, at a fraction of the
cost, and that the general model should be reserved for the class where
it genuinely leads. Transcription is the specialised task. A 0.6B ASR
model against a 300M tower extracted from a 30B mixture-of-experts is
the same trade the paper measures at 1431x, and it resolves the same
way.

So the two routes are not competing, they answer different questions:

    want                                   route

    transcription, alignment, captions     Qwen3-ASR-0.6B, standalone
    audio inside the VLM's reasoning --    the AuT tower, a new
    "what is the tone of this clip,        projector to 4096, and a
    given the image"                       LoRA on Qwen3-VL

**The first costs a download and the second costs a training run.**
Nothing yet says the second is needed, and RFD 1168's ordering rule says
find out with the first.

## The checkpoint: licence clean, but the projector does not transfer

**The licence is usable.** Qwen3-Omni-30B-A3B, in all three variants, is
**Apache-2.0**. The Hugging Face API reports `license: other` while
`license_name` and the card badge both say `apache-2.0`, which is
metadata noise rather than a second licence -- worth recording because
`other` is the value that should always be chased rather than assumed.

**There is no standalone AuT checkpoint.** Only the three 30B-A3B
variants are published, so obtaining a 300M tower means extracting it
from a 30B mixture-of-experts download.

**AND THE PROJECTOR TARGETS THE WRONG WIDTH.**

    model                  text hidden   audio hidden   audio layers

    Qwen3-Omni-30B-A3B        2048          1280            32
    Qwen3-VL-8B               4096          none            none
    Qwen3-ASR-0.6B            1024           896            18

The proposal was stated as log-mel into "the same 4096 sequence space".
4096 is right for Qwen3-VL-8B's decoder and **wrong for every projector
that exists**: Qwen3-Omni's AuT writes into 2048 and the ASR model's
into 1024, because those are the decoders they were trained inside.

So the transfer splits in two. The **encoder** carries over, and it is
the part that would compile. The **projector does not**, and a new MLP
into 4096 has to be trained with a LoRA teaching Qwen3-VL to read it.

**That is exactly EditScore's arrangement.** RFD 1157 records EditScore
as a LoRA over Qwen3-VL holding 516 tensors, 12 of them at
`deepstack_merger_list` -- the projector adaptation -- with the ViT left
stock. An audio LoRA is the same object with an audio tower behind it,
which is a reason to think the arrangement works and not a reason to
think the training is free.

`PROJECTOR_TYPE_QWEN3A`'s `conv2d_1/2/3` are worth noting separately:
QWEN2A uses `conv1d`, QWEN3A uses **2D** convolutions, direct evidence
that the log-mel is handled as a single-channel image and support for
the input-rank argument above.

## The fixed window, which is unresolved

Audio is variable length and the compiler is not. Whisper answers this
by padding every clip to 30 seconds, which is a fixed shape bought with
wasted compute on short utterances.

Nothing here has decided the window, and the choice is a real trade:

- a long window wastes the device on short utterances, and most
  utterances are short
- a short window forces chunking, and chunking across a sentence
  boundary is where transcription errors concentrate

This wants measuring against the actual utterance length distribution
before a number is picked, and no such distribution has been collected.

## What to measure, cheapest first

Following RFD 1168's ordering rule and the stratification argument in
arXiv:2608.12875 — climb only as far as the answer requires:

1. **Export a stock Whisper-family encoder to ONNX at a fixed window**
   and run `gate_onnx_device.py` against it. No fork change, no device,
   and it answers the operator question outright.
2. **Translate it with `gate_dfc_parse.py`.** This is where the input
   rank claim above is confirmed or refused, and it is the step that
   stopped Pixal3D.
3. **Only then widen `clip_init_hailo`**, because the fork change is
   pointless if the graph does not translate.

Steps 1 and 2 need no audio corpus and no AuT checkpoint. They test the
architecture rather than the model, which is the same reason RFD 1168
starts with a one-hot constant.

## What this does not claim

It does not claim the 300M AuT checkpoint is available under a licence
this workspace can use. That has not been checked, and RFD 1166 records
what happens when a row is scored without reading its weights.

It does not claim parity with Gemma 4. Gemma 4 was wanted for language,
vision and sound in one model; this is three towers around one decoder,
which is a different arrangement that happens to answer the same need.
