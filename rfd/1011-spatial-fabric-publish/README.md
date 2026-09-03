# RFD 1011: Spatial fabric publish

**State:** published
**Feature:** spatial fabric

## Decision

Add a publish flow for completed tasks.

- Publish RP1 sends the completed mesh to the spatial fabric.
- Validate OMB tier checks the GLB export against the fabric.

The flow opens the Scene Assembler in a new tab. The spatial
fabric adapter checks the manifest and the tier presets.

## Problem

A completed mesh task should reach shared worlds. The app needs a
publish path to the spatial fabric. The fabric needs a valid
manifest and a scene assembler.

## References

- Adapter: `src/library/spatialFabricAdapter.js`
- Hook: `src/hooks/useSpatialFabric.js`
- Presets: `src/library/ombExportPresets.js`
- Docs: `docs/SPATIAL_FABRIC_INTEGRATION.md`

## Related

RFD 1007 replaces the publish terminal validation with motion
validation in the Studio pipeline.
