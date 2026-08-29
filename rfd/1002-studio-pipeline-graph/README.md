# RFD 1002: Studio pipeline graph

**State:** published
**Feature:** Studio pipeline

## Problem

A user wants to go from a text prompt to an animatable asset.
The steps are sequential. Each step needs a status and a result.

## Decision

Model the pipeline as a locked node graph. Each node is one stage.
Each edge is a dependency. The graph has two views: a flow graph
and a kanban board.

Stages, in order: Prompt, Image, Layers, Mesh, Rig, Motion, Export.

Runnable kinds, in order: text_to_image, layer_decomposition,
image_to_3d, auto_rigging, motion_validation.

The data model stays pure. The executor runs the nodes. Old saved
projects migrate to the new template. Migration inserts missing
stages.

See `DETAILS.md` for file references.

## Related

RFD 1003 defines the job lifecycle. RFD 1006 defines layer
decomposition. RFD 1007 defines motion validation. RFD 1008 defines
appearance remix.
