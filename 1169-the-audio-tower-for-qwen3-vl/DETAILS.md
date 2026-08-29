# RFD 1169 details: the tower, the fork gap, and the half that has no path

## Why this is the vision tower again

RFD 1157 established the shape: EditScore is a LoRA over Qwen3-VL, and
`llama-cpp-npu-vision` compiles the encoder into a HEF while decode
stays on the host. The audio proposal is the same arrangement with a
different front end.

    tower              input                       output

    vision, ViT        image, fixed edge           tokens at 4096
    audio, AuT 300M    128-bin log-mel, fixed      tokens at 4096
                       frame count

Both end in an MLP projector writing into the decoder's sequence space,
which is why one hook can serve both and why the fork's refusal to is
the thing to fix rather than a reason to look elsewhere.

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

## ASR against voice cloning, and why they are not one capability

The request names ASR, voice cloning and audio together. Two of those
have a path and one does not.

**Understanding is an encoder.** ASR, audio question-answering and
speaker identification all read a spectrogram and emit tokens. That is
the tower above, it is fixed-shape, and it compiles.

**Production is decode into a vocoder.** Voice cloning emits audio,
which means an autoregressive stage producing codec tokens and a vocoder
turning them into a waveform. RFD 1126 names that obstacle and nothing
here changes it: the sequence and its cache grow every step while a
dataflow part compiles fixed shapes. RFD 1155 abandoned Gemma 4 on the
same ground.

A speaker embedding is worth separating from both. Extracting a voice
identity from a reference clip is an encoder and would compile; using
that embedding to synthesise speech is not. So "voice cloning" splits
across the line rather than sitting on one side of it, and the half that
compiles is not the half that produces sound.

**The honest statement is that this buys ears, not a voice.**

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
