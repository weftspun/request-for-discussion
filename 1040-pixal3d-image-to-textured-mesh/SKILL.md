---
name: pixal3d-image-to-textured-mesh
description: Build and run the Pixal3D image-to-3D worker without rediscovering its eighteen packaging gaps. Use when standing up the container, when an install step reports success and installs nothing, or when a run fails inside a diffusion step with an error that names the wrong cause.
---

# Pixal3D, as a procedure rather than a discovery

RFD 1040 records what is wrong with the packaging. This is what to do about it. The two are
separate on purpose: the RFD is the measurement, and a measurement does not tell you the
order to do things in.

Every gap below was found by running the thing and reading the error. None was found by
reading the Dockerfile, because each one reports success or reports a cause that is not the
cause.

## The rule that generates most of this

**Upstream's pins are the ones that count. Ours are the ones that break it.**

Pixal3D's `requirements.txt` names no torch, no safetensors, no `huggingface_hub` and no
`usd-core`. RFD 1040's Dockerfile invented all four, and three of them are why it does not
work: `huggingface_hub==0.26.2` contradicts `transformers==4.57.3` and stops the build at
pip; `torch==2.5.1` brings triton 3.1.0, which FlexGEMM cannot call; `safetensors==0.4.5`
cannot open the 1.3B checkpoint. Prefer a solver with a lockfile over a hand-written pin,
and where two upstreams disagree, follow the one whose code runs.

## Order matters, and here is the order

1. **Modern pip and setuptools, before anything else.** With `--no-build-isolation` and pip
   22, every PEP 621 project installs as `UNKNOWN-0.0.0`, and since they share that name each
   install uninstalls the previous one. Nothing errors and the layers look right.
2. **Toolchain**: `build-essential ninja-build git python3-dev libeigen3-dev cmake`, plus
   `CPLUS_INCLUDE_PATH=/usr/include/eigen3`. The base uses python3.10 even though it installs
   3.11, so the headers must be 3.10's.
3. **torch 2.6.0 + torchvision 0.21.0** from the cu124 index, before compiling anything.
   Extensions link against the libtorch present at build time.
4. **The four extensions**, `TORCH_CUDA_ARCH_LIST=8.6` for a 3090: CuMesh, FlexGEMM,
   o-voxel from TRELLIS.2's subdirectory, nvdiffrast v0.4.0 and nvdiffrec's `renderutils`
   branch. `o_voxel.postprocess` imports `nvdiffrast.torch` at module load.
5. **natten, with its CUDA library**: `NATTEN_CUDA_ARCH=8.6 NATTEN_N_WORKERS=8 pip install
   --force-reinstall --no-deps natten==0.21.0 --no-build-isolation`. Thirty minutes, and not
   optional. `--no-deps` stops it replacing torch.
6. **einops**, which BiRefNet's remote code imports where no dependency list can see it.

## Errors that name the wrong cause

| what it says | what it is |
| --- | --- |
| `401 Repository Not Found for ckpts/ss_flow_...` | safetensors too old. `pipelines/base.py` swallows the real exception and retries the path as a Hugging Face repo id |
| `Successfully installed UNKNOWN-0.0.0` | pip cannot parse the metadata; this install also removed the last one |
| `undefined symbol: ...torchInternalAssertFail...RKSs` | torch changed after the extension was compiled |
| `Autotuner.__init__() takes 13 ... 14 were given` | triton is older than FlexGEMM's `triton>=3.2.0` |
| `Can't run CUTLASS FNA; NATTEN was not built with libnatten` | natten installed without `NATTEN_CUDA_ARCH`; it imports and has no kernels |
| `RuntimeError: 0 active drivers` | a GPU-requiring import ran during `docker build`, which has no device |

## Running it

`--fov` is **radians**. Passing 40 means 2292 degrees. For a 40 degree render, pass 0.698.

Never let it construct the background remover on a rendered input. `pipeline.json` names
`briaai/RMBG-2.0`, which is gated and non-commercial and on the blocklist, and the pipeline
builds it in `from_pretrained` before it looks at the image -- so an alpha channel does not
avoid it. A render's matte is exact, so no matting model belongs on that path at all.

`ATTN_BACKEND=sdpa`, because flash-attn is not installed and upstream defaults to it.

## Checks that mean something

Import checks belong at run time with `--gpus all`, never in a `RUN` layer. Verify the
checkpoint against the published sha256 before concluding a file is corrupt: the 1.3B
checkpoint hashes to `6d0147bb347eb61fa81c304cc68c7fd69d447e91870357a549b47e1d0fd77242`, and
it was intact every time it looked broken.
