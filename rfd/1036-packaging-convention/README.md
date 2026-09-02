# RFD 1036: Model packaging convention

**State:** committed
**Feature:** model packaging

## Problem

The DGX API ran each model through its own adapter, each with its
own weight loader, CUDA pin, and output writer. There is no DGX now.
This RFD first selected Cog; `DETAILS.md` records why it was withdrawn.

## Decision

Package each model as a plain Docker image that serves HTTP.

No Cog. Cog wraps a `Predictor` class and builds an image around it,
and that image expects Replicate's own runtime. The local worker
starts a container and maps a port, and nothing more.

Each model gets a folder under `decisions/`, and each folder holds
this RFD, a `Dockerfile`, a `server.py`, and a `test_input.json`.

Name the folder for its model, and never for a package format. A
format is a decision this RFD already changed once. A folder name
that carries one goes stale on the next change.

See `DETAILS.md` for target, rules, the two-stage Dockerfile, files,
composites, and unconverted folders.

Committed 2026-09-02: the convention has been in force for months;
CLAUDE.md closes compute (local desktop GPU only; RunPod/Vast.ai
blocklisted). Earlier rental-target framing retracted in DETAILS.md.

## Related

RFD 1016 lists the models. RFD 1026 gives the memory. RFD 1027 the
GPU tier. RFD 1037 the composite convention. RFD 1053 the asset
format. RFD 1028 gates the license.
