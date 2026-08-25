# RFD 1140: Rented GPUs on RunPod

**State:** discussion
**Feature:** rented compute
**Scope:** work that does not fit the desk card

## Problem

The desk card is one RTX 3090 with 24 GiB. An OmniGen2 LoRA trains
here at 256 square in 22 minutes for 200 steps, and does not finish
one step in twelve minutes at 512 square. Neither run reports an
error. Windows pages into shared memory instead of failing, so the
only symptom is a run that stops being fast. Pixal3D dies one stage
short of geometry, because NATTEN has no sm_86 kernel and every
stage after the first reaches it.

Renting fixes both. It also loses whatever is not in a git
repository when the pod goes away, and it bills while it waits.

## Decision

Rented GPU work runs on RunPod. Push before renting, tear down after
use, and check the tear down.

The API is REST at `rest.runpod.io/v1` with a bearer token. GraphQL
is retired and answers 403. A key that answers 401 is stale rather
than absent. The CLI reads a `[default]` profile, not a bare
top-level `apikey`.

Prefer batch over a pod when the work is a queue of independent
items. A camera sweep is that shape. A pod bills while it waits for
an instruction; a batch does not.

## References

See `SKILL.md` for the order, and `DETAILS.md` for the measurements.

## Related

RFD 1040 packages the worker that needs a Hopper card.
