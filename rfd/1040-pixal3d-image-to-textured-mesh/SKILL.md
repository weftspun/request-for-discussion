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

## It builds now, and it still does not finish

Measured on the desk, 2026-08-25, RTX 3090 (Ampere sm_86). **Stage 1 of 3 succeeds** -- sparse
structure, 12/12 steps, 22 s -- and stage 2 dies:

    NATTEN failure: CUDA runtime error: no kernel image is available for execution on the device

NATTEN appears nowhere in Pixal3D's own Python. It arrives through **NAF**, the upsampler used whenever `use_naf_upsample: True`, which
is every stage except the one that worked. `flash_attn_3` has the same problem and can be routed
around with `ATTN_BACKEND=sdpa`. NATTEN has no equivalent switch, and the missing kernel is for
sm_86, so any other Ampere card fails the same way. The options are to build `natten` for sm_86 against a `-devel` base with Ampere support
unverified, to disable NAF and label the output off-distribution, or to rent a Hopper card --
RFD 1140 covers the last of those. The config is known-good up to this point.

No GLB was produced. Vertex counts, extract VRAM and the mesh usability check **did not run and
are counted as not-run, not as passes**.

## Two failures that stopped it building at all

Both are in the repository, and either one alone stops the build at step 4 of 7.

**The Dockerfile pins a branch that does not exist.** `ARG PIXAL3D_REF=main`; upstream's default
branch is **`master`**, HEAD `cdbb2bbf`. It fails 140 s in, at step 4 of 7, before any Python is
installed:

    error: pathspec 'main' did not match any file(s) known to git

**Upstream's requirements file is no longer solvable.** `requirements-hfdemo.txt` carries an
unpinned `git+https://github.com/microsoft/MoGe.git`, which now resolves to moge 3.0.0 and wants
`flex-gemm 1.0.0`, while the same file pins the prebuilt `flex_gemm 0.0.1` wheel everything else
is built against. The result is `ResolutionImpossible`. Install MoGe afterwards with `--no-deps`
so the prebuilt wheel wins. This is the hazard CLAUDE.md's `uv` entry describes, arriving through
someone else's repository: the file was reproducible when written and is not now.

Three smaller ones follow those: `utils3d_moge`, `pipeline`, `scipy` and `matplotlib` go missing;
the `-runtime` base has no C compiler and triton JIT-compiles at import (`Failed to find C
compiler`); and `render_utils.py` imports `utils3d`, which is listed nowhere.

## A native environment is impossible here, and that is settled

Every heavy dependency publishes **linux_x86_64 wheels only** -- `natten`, `flash_attn_3`,
`cumesh`, `flex_gemm`, `o_voxel`, `nvdiffrast`, `nvdiffrec_render` -- and three of those are the
authors' own CUDA extensions with no source distribution on PyPI. Docker is the only path on
Windows. A pixi environment for this cannot be built, so do not start one.

## Cutting BRIA out, and proving it

Cutting the construction site alone leaves the class reachable from a cached config. Three cuts:

a. **delete** the `rembg_model` entry from a patched `pipeline.json`, bind-mounted over the
   cached copy at run time, leaving the HF cache untouched;
b. replace every `pipeline.rembg_model = getattr(rembg, ...)(...)` -- in `pixal3d_image_to_3d.py`,
   `trellis2_image_to_3d.py` and `trellis2_texturing.py` -- with `None`, and **raise** if a config
   still carries the key;
c. make `BiRefNet.__init__` **raise** before its `from_pretrained`, so the class is unreachable
   whatever any config says.

Then prove it twice rather than assuming the edit worked. Grep the patched config for
`bria|RMBG|briaai`: zero hits, and zero constructed components. Diff `~/.cache/huggingface/hub`
before and after: no `briaai` or `RMBG` repository appears. Add a runtime gate that calls the
constructor and **exits non-zero if it succeeds**.

`preprocess_image`'s no-alpha branch should raise rather than substituting a different matting
model, so a missing alpha channel stops the run instead of changing what it measures.

## Two more things about the environment

`worker_entry.py` sets **none** of the five environment variables upstream sets at the top of both
`app.py` and `inference.py`: `ATTN_BACKEND`, `OPENCV_IO_ENABLE_OPENEXR`, `PYTORCH_CUDA_ALLOC_CONF`,
`FLEX_GEMM_AUTOTUNE_CACHE_PATH`, `FLEX_GEMM_AUTOTUNER_VERBOSE`. `ATTN_BACKEND` is read at **module
import time** by `pixal3d/modules/attention/config.py`, so it cannot be set after importing
pixal3d.

`DETAILS.md` omits a fourth runtime weight source: **`valeoai/NAF`**, fetched via torch.hub. Its
checkpoint table is otherwise exact -- 24.045 GB, confirmed file by file.

Last: `pixal3d-image-to-textured-mesh` and `pixal3d-image-mesh-painting` are **byte-identical**
apart from `.git`, and the second one's README opens with the first one's name. Both are in
`default.xml`. One is a copy that was never re-pointed.

## Checks that mean something

Import checks belong at run time with `--gpus all`, never in a `RUN` layer. Verify the
checkpoint against the published sha256 before concluding a file is corrupt: the 1.3B
checkpoint hashes to `6d0147bb347eb61fa81c304cc68c7fd69d447e91870357a549b47e1d0fd77242`, and
it was intact every time it looked broken.
