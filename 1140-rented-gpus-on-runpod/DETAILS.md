# RFD 1140 details: the measurements behind renting

Every number here was taken on the desk on 2026-08-25: Windows 11, one RTX 3090, 24 GiB,
Ampere sm_86. A second card, a 4090, is present and off.

## The training wall, and why it does not raise

An OmniGen2 LoRA, rank 8, attention-only, bf16, gradient checkpointing, 8-bit AdamW, batch 1
with 8 accumulation steps, on 95 records:

| resolution | result |
| --- | --- |
| 512 square | **no optimizer step in twelve minutes**, card at 24.3 GiB of 24.5 |
| 256 square | **200 steps in 22 minutes**, 13.1 s/step early, 6.62 s/step averaged, 24.0 GiB |

Loss fell from 0.196 at step 1 to 0.111 at step 200. The checkpoint carries 886 tensors of
which **304 are LoRA**.

Neither run raised. That is the whole reason this is written down: on Windows the WDDM driver
pages into shared system memory rather than returning an allocation failure, so a run that
does not fit does not stop, it slows. Twelve minutes with no completed step and no error is
what "out of memory" looks like here.

The arithmetic behind it: the frozen transformer is **14.76 GiB** in bf16, and `train.py:255`
puts Qwen2.5-VL-3B on the same device in bf16 as well, roughly 7 GiB, to encode prompts of
about thirty tokens. That is close to 22 GiB before a single activation. Getting the text
encoder off the card, or precomputing its embeddings, is worth about 7 GiB and is the first
thing to try before renting for resolution alone.

The same failure appeared twice more in one session, which is why the guard exists:

- **TaylorSeer at inference.** Upstream claims up to 2x. It ran over eight minutes against
  103 s for the row before it, and was killed. The card sat at 24.2 GiB throughout.
- **Two pipelines at once.** Two bf16 OmniGen2 processes want 14.76 GiB each. `osqueryi`
  showed them starting two seconds apart; both paged, and a 131 s row took 27 minutes. About
  12x, with no error from either process.

`ladder_camera_obedience.py` now refuses to start when the card already holds more than
2 GiB, because refusing is cheaper than diagnosing this a fourth time.

## The kernel wall

Pixal3D builds and runs after five packaging fixes, and **stage 1 of 3 succeeds** — sparse
structure, 12/12 steps, 22 s. Stage 2 dies:

    NATTEN failure: CUDA runtime error: no kernel image is available for execution on the device

NATTEN appears nowhere in Pixal3D's own Python. It arrives through **NAF**, the upsampler used
whenever `use_naf_upsample: True`, which is every stage except the one that worked.
`flash_attn_3` has the same problem and was routed around with `ATTN_BACKEND=sdpa`; NATTEN has
no such switch. This is not a configuration slip and a larger Ampere card does not fix it.

RFD 1040 holds the packaging detail.

## The API

| call | result |
| --- | --- |
| `POST api.runpod.io/graphql` | **403** — retired |
| `GET rest.runpod.io/v1/pods` with a bearer token | **401** — key stale |
| `runpod config --check` with a bare top-level `apikey` | `missing default profile` |

The last of those is the trap. The key was present in `~/.runpod/config.toml`, 50 characters,
correct prefix, and the CLI could not see it because it was not under a `[default]` section.
The message names a missing profile and reads as a missing credential.

## The REST surface, read from its own spec

`GET https://rest.runpod.io/v1/openapi.json` with a bearer token returns 23 paths. The ones
that matter:

    /pods            get, post          /endpoints                  get, post
    /pods/{id}       get, patch, delete /endpoints/{id}             get, patch, delete
    /pods/{id}/stop  post               /endpoints/{id}/update      post
    /pods/{id}/start post               /billing/pods               get
    /pods/{id}/reset post               /billing/endpoints          get

Two things follow. There is **no `/gputypes`**: card selection is a field on `POST /pods`, so
the CLI or the console is where you discover what is available, not the REST API. And
`/endpoints` is the serverless surface, which is the batch path -- it answered 200 with **0
items**, so nothing is configured here yet.

`/billing/pods` and `/billing/endpoints` are how the tear-down check is done without trusting
memory. A pod believed stopped shows up in the first of those.

Measured 2026-08-25: key read from 1Password, `GET /pods` returned **200** with **0 running
pods**, so nothing was billing.

## `desiredStatus` states an intention, and `runtime` reports a fact

Measured 2026-08-26, renting twice. `GET /pods/{id}` returned `desiredStatus: RUNNING`
throughout, on a pod whose container never started. The field that answers whether anything
is running lives in GraphQL:

    query { pod(input:{podId:"..."}) { runtime { uptimeInSeconds ports { ... } } } }

`runtime: null` means no container, and a pod bills in that state exactly as it bills in any
other. The REST view looked healthy for the six minutes it took to notice.

The cause was the image. `nvidia/cuda:12.5.1-devel-ubuntu24.04` carries no RunPod agent, so
their SSH proxy answered `container not found` and nothing ever populated `runtime`. An
official image — `runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404`, 10.6 GB compressed —
started normally. A custom `dockerStartCmd` that installs `sshd` does not substitute for the
agent.

    pod              image                    outcome        billed
    nbqs85lbqfjupb   nvidia/cuda:12.5.1       never started  ~$0.03
    rdhfp7fycqbvsd   runpod/pytorch:1.0.2     started        ~$0.05

Two smaller facts from the same session. The proxy rejects a session without a PTY, so
`ssh -tt` is mandatory and its absence reads as `Your SSH client doesn't support PTY`.
And `POST /pods` answers **500 "There are no instances currently available"** when a
GPU list, a cloud type and a volume cannot be satisfied together; widening the GPU list and
dropping to `COMMUNITY` placed it.

Teardown was verified through both surfaces rather than one: `DELETE /pods/{id}` returned
204, then REST `GET /pods` and GraphQL `myself { pods networkVolumes clientBalance }` each
reported zero. Total for the session was **$0.079**, read as a balance difference.

## What is not measured here

Batch API throughput and pricing, spot versus on-demand, and network volumes. The batch path
is recommended in the RFD on the shape of the work — a queue of independent items against a
pod that bills while idle — and not on a measurement taken here. When one is taken it belongs
in this file, next to the others.
