# RFD 1159: TRELLIS.2 sits exactly on the ceiling at bf16

**State:** abandoned
**Feature:** edge acceleration candidate
**Scope:** `3-interactor/trellis2-image-to-textured-mesh`

## Decision

Abandoned on 2026-08-28. The accelerator work is scoped to
rf-detr keypoint and RFD 1157, and this scored 12 of 25 against RFD 1157's 18.

Record eight bits as this model's ceiling and stop treating bf16 as
an option. Do not attempt a path through trellis2cpp: BLOCKLIST.md
settles that ggml carries no graph and the gap is structural. Any
revival exports the upstream torch model fresh.

## Problem

TRELLIS.2 is 4.0 B parameters, which is 8.0 GB at bf16 against a
device that holds 8 GB. Whether that fits depends on whether the
part means 8 GiB or 8 GB, and either way nothing remains for
activations.

A row that lands on the line is worse than one that misses. It
invites a reader to record bf16 as available and discover otherwise
during a run.

At eight bits it is 4.0 GB and the question disappears.

The graph is the harder half. `3-interactor/trellis2cpp` carries the
model as 3420 lines of hand-written ggml across 79 distinct
operators, which is the form that reaches no accelerator. What would
compile is the torch model both descend from, not the port.

## Related

BLOCKLIST.md gives the ggml row. RFD 1148 chose the runtime.
RFD 1026 gives the memory.
