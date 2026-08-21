# RFD 1024: Model packaging convention

**State:** discussion
**Feature:** model packaging

## Problem

The DGX API ran each model through its own adapter. Each adapter
carried its own weight loader, its own CUDA pin, and its own output
writer. There is no DGX now, and none of those adapters run anywhere.

This RFD first selected Replicate Cog. Cog is a good package format,
and it targets one host. RFD 1037 now runs the worker on this box's
own 4090 first, plain Docker, no rental. vast.ai stays priced for
later, the same plain-Docker shape once this box is not enough.

## Decision

Package each model as a plain Docker image that serves HTTP.

No Cog. Cog wraps a `Predictor` class and builds an image around it,
and that image expects Replicate's own runtime. Neither this box's
own worker nor a vast.ai instance needs that. Each one starts a
container and maps a port, and nothing more.

Each model gets a folder under `decisions/`, and each folder holds
this RFD, a `Dockerfile`, a `server.py`, and a `test_input.json`.

Name the folder for its model, and never for a package format. A
format is a decision this RFD already changed once. A folder name
that carries one goes stale on the next change.

See `DETAILS.md` for the target hardware, the packaging rules, the
two-stage Dockerfile, the file list, the composite-model convention,
and which folders are not converted yet.

## Related

RFD 1010 lists the models. RFD 101a gives the memory. RFD 101b gives
the GPU tier. RFD 1025 gives the composite convention. RFD 1035 gives
the asset format. RFD 101c gates the license.
