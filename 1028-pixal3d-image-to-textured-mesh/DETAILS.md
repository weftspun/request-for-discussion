# RFD 1028 details: the Docker test, measurement, format, interface, downloads

## Tested in Docker

The `contract` stage carries the server and `usd-core`, and no model.
`WEFTSPUN_STUB=1` makes `/predict` answer with the real shape.

    docker build --target contract -t weftspun/pixal3d:contract .
    docker run --rm -p 8000:8000 weftspun/pixal3d:contract

Measured on a machine with no NVIDIA device:

- `/health` answers `{"status":"ok","ready":true,"stub":true}`.
- `/predict` answers with `glb`, `layer`, `seed`, and `stub`.
- A resolution of 999 answers 400, and names the field.

Two faults came out of that run, and neither one was visible on
inspection.

`usd-core` alone reads no glTF. The layer first added the GLB as a
`references` arc, and USD could not resolve it:

    Cannot determine file format for @output.glb@

The layer records the GLB as an asset attribute now. A glTF file
format plugin would make the arc work, and this image carries none.

`test_input.json` first wrapped the body in `"input"`, which is the
RunPod shape. An HTTP body is the request, thus every field read as
missing and the server answered 422.

## The measurement

Seven checkpoints, 24.045 GB on disk. Every file is fp16 or bf16, and
both hold one parameter in 2 bytes, thus the count is 12.02 B.

| Checkpoint                           |          Size | Stage            |
| ------------------------------------ | ------------: | ---------------- |
| slat_flow_img2shape_dit_1_3B_1024    |      5.547 GB | shape 1024       |
| slat_flow_img2shape_dit_1_3B_512     |      5.547 GB | shape 512        |
| slat_flow_imgshape2tex_dit_1_3B_1024 |      5.547 GB | texture 1024     |
| ss_flow_img_dit_1_3B_64              |      5.360 GB | sparse structure |
| shape_dec_next_dc_f16c32             |      0.948 GB | shape decode     |
| tex_dec_next_dc_f16c32               |      0.948 GB | texture decode   |
| ss_dec_conv3d_16l8                   |      0.148 GB | structure decode |
| **total**                            | **24.045 GB** |                  |

The file names say `1_3B`, and each DiT file is 5.5 GB. At 2 bytes per
parameter that is 2.77 B, and not 1.3 B. The measured size is the
fact this RFD records. The name may count the transformer alone, and
leave out an encoder the file also carries.

## Prefer bf16

The four DiTs ship bf16, and the three decoders ship fp16. Take bf16
wherever a checkpoint offers both.

The two formats cost the same memory, thus this is not a budget
choice. bf16 carries the wider exponent range, and a diffusion cascade
that overflows in one stage feeds the fault to the next.

The decoders ship fp16 only. No choice exists there yet.

## The cascade never needs one resident set

Three stages run in order, and each frees before the next loads.
`--low_vram` makes that explicit, and it drops the peak from 24.045 GB
to about 6.5 GB, which is one DiT plus a decoder.

Keep `low_vram` on. An RTX 4090 holds 24 GB, thus a 6.5 GB peak leaves
room for the activations. That card costs about 0.35 to 0.37 US
dollars per hour on demand, and 0.13 interruptible.

## Measured: the image does not build, and did not run

`SKILL.md` beside this file carries what to do about it: the order the
steps go in, and the errors that name the wrong cause. This section is
the measurement, and that one is the procedure.

Recorded on 2026-08-22, from four attempts on a desktop RTX 3090 with
Docker 29.7.2 and the NVIDIA container toolkit. Every claim below is
what a command returned, not a reading of the file.

**The pins conflict, so `docker build` stops at the pip step.**
`transformers==4.57.3` requires `huggingface-hub<1.0,>=0.34.0`, and the
same line pins `huggingface_hub==0.26.2`. pip reports
`ResolutionImpossible`. Upstream's `requirements.txt` does not pin
`huggingface_hub` at all, so that pin is this file's own, added for
`snapshot_download`, and the comment above it saying the block mirrors
upstream is wrong about that line. Built here with `0.35.3`.

**The base environment is absent.** Upstream's README has four
installation steps and this Dockerfile implements one and a half.

| upstream step        | here                                          |
| -------------------- | --------------------------------------------- |
| TRELLIS.2 base       | absent                                        |
| `requirements.txt`   | inlined as pins                               |
| natten               | no `NATTEN_CUDA_ARCH`, no build isolation off |
| `utils3d` wheel      | absent                                        |

Step 1 is where `cumesh`, `flex_gemm` and `o_voxel` come from: three
CUDA extensions built from source, none on PyPI. With the pin fixed,
the image builds and then fails at `import cumesh`.

**So the 6.5 GB peak below is upstream's number, not ours.** It cannot
be a local measurement, because nothing has run here. The same holds
for anything else in this file that reads as observed behaviour of the
container. What is measured is the image size: 74.5 GB on disk,
32.9 GB of content, built with `PIXAL3D_REF=cdbb2bb`.

**`ARG PIXAL3D_REF=master` contradicts its own comment**, which says
"Pin the commit: master moves, and a moved master changes the mesh
with no build change to show for it". A default of `master` is exactly
the thing that comment forbids.

**`ATTN_BACKEND` defaults to `flash_attn`** in upstream's
`inference.py`, and flash-attn is never installed. The run needs
`ATTN_BACKEND=sdpa` in the environment.

## The interface

| Input      | Type  | Default |
| ---------- | ----- | ------- |
| image      | Path  | none    |
| seed       | int   | 42      |
| fov        | float | -1.0    |
| resolution | int   | -1      |
| low_vram   | bool  | true    |

`fov` of -1.0 lets MoGe estimate the field of view. The output is not
one file. RFD 1035 makes USD the internal format, thus `predict()`
returns a layer beside the GLB.

## Three repositories download at build time

`TencentARC/Pixal3D` is 24.045 GB. `Ruicheng/moge-2-vitl` estimates
the field of view. `camenduru/dinov3-vitl16-pretrain-lvd1689m` is the
conditioning encoder, and all four stages read it.

A cold start that downloads 24 GB is a cold start that times out.
An instance is rented by the hour, thus that time is paid for.

## What this corrects

- The license is MIT, and not unknown. RFD 101c gates on that, and
  Pixal3D clears the gate.
- The count is 12.02 B, and not unknown. RFD 101a carried one of two
  unknown rows for this model.
- The backbone is TRELLIS.2, per the upstream README. RFD 1026
  packages TRELLIS.2, thus these two model images share a lineage.
