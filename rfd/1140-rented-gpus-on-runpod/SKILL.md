---
name: rented-gpus-on-runpod
description: Rent a GPU on RunPod, run work that does not fit the desk card, and tear it down. Use when a run pages instead of failing, when a kernel is missing for the desk architecture, when the API returns 401 or 403, or when the work is a queue of independent items and a pod would bill while it waits.
---

# RunPod, as a procedure rather than a discovery

RFD 1140 records why renting is needed and what the measurements were. This is the order to
do things in. Every step below came from running it and reading the error.

## Before you rent anything

**Push first.** Anything not in a git repository goes with the machine. This is CLAUDE.md's
rule and it is not advisory: the pod's disk is gone when the pod is gone, and a result that
existed only there did not happen. Check `repo status` for uncommitted work, and check for
files in directories no manifest names, because `repo status` cannot see those.

**Know what you are renting for.** Two shapes need different things:

- A *training run* or a *build* needs a pod: one machine, held, with a filesystem.
- A *sweep* is a queue of independent items and wants **batch**. A pod bills while it waits
  for the next instruction. A batch does not.

## Credentials

The CLI reads `~/.runpod/config.toml` and looks for a **profile section**:

    [default]
    api_key = "rpa_..."

A bare top-level `apikey = "rpa_..."` parses as valid TOML and is invisible to the CLI, which
reports `missing default profile` while the key sits in the file. That is the first thing to
check, because it looks like a missing credential and is not one.

Verify with `runpod config --check`. That only proves the file parses. To prove the key
*works*, call the API:

    GET https://rest.runpod.io/v1/pods      Authorization: Bearer <key>

- **200** — the key is good.
- **401** — the key is stale, not absent. Rotate it; do not re-enter the same one.
- **403 from `api.runpod.io/graphql`** — GraphQL is retired. Use REST.

Read the key from 1Password with `op read` rather than pasting it into a shell that keeps
history. `op` must be signed in first; `op whoami` reports `account is not signed in` when it
is not, and that error looks nothing like an authentication failure downstream.

## Choosing a card

Match the card to the wall you hit, not to the biggest number:

- **Out of VRAM, silently.** On Windows the driver pages into shared memory rather than
  raising, so the symptom is slowness, not an exception. Measure seconds per step before and
  after; a step that takes five times longer than the step before it has not fitted.
- **Missing kernel.** `no kernel image is available for execution on the device` names an
  architecture mismatch. NATTEN and `flash_attn_3` both want sm_90; the desk card is sm_86.
  A bigger Ampere card does not fix this and a Hopper card does.

## Running

Bring the environment, not the packages. A pixi manifest or a container is reproducible; a
sequence of `pip install` commands typed into a pod is gone with the pod and was never
reviewed.

Log to a mounted volume or push results as they are produced. A run whose only record is the
pod's stdout has one copy, on the machine you are about to delete.

## Tearing down

Tear down, then **check the tear down**. `GET /v1/pods` must come back without the pod. A pod
believed stopped and still billing is the failure this step exists to catch, and it is
detected by reading the list rather than by remembering having clicked stop.

Then check the balance moved by roughly what you expected. A large gap either way is worth
understanding before the next run rather than at the end of the month.

## What this does not cover

Cost estimation per card, spot versus on-demand, and network volumes. None of those has been
measured here, and a procedure that guesses at them would read as though they had been.
