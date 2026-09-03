# RFD 1027: GPU tier per model

**State:** committed
**Feature:** capacity planning

## Decision

Size each model on its own. The question is which GPU tier one model
needs, and not whether a set of models co-resides.

Two numbers decide the tier: the weights RFD 1026 gives per model,
and the activation peak, which depends on the resolution and the
batch size.

Every model in the catalog reaches a 24 GB card. The workspace
standardizes on **QAFT 4-bit** as the default weights format where
upstream ships one (Gemma-4-12B QAT Q4_0 is the canonical example
and reasoning core per RFD 2169). Models without a QAFT release run
at published precision (bf16) with staged loading. See `DETAILS.md`.

Committed 2026-09-02: 24-GB tier and QAFT-first rule settled.
CLAUDE.md retracted Condition 5 the same day (precision is not a
corpus hazard), so quantised weights are permitted for corpus
generation, not only inference.

## Problem

This RFD first asked whether every model fits one device at once. It
summed 116.45 GB against a 128 GB DGX Spark, found about 10 GB of
headroom, and called the margin too small.

That question came from hardware this project does not have. CLAUDE.md
now names the local desktop GPU as the only compute; each model runs
in its own container per RFD 1036, so two never compete for one
device. The old finding was an artifact.

## Related

RFD 1025 gives the arithmetic. RFD 1026 gives the memory per model.
RFD 1036 gives the packaging that sets the tier.
