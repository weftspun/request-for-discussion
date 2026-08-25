# RFD 1005 details: file references

- Pipeline: `docs/AVATAR_PIPELINE.md`
- Rig contract: `docs/API_AVATAR_RIG_CONTRACT.md`
- Client: `src/library/avatarPipelineCatalog.js`
- Client: `src/library/avatarPipelineExport.js`
- Export: `src/components/GLBExport.jsx`
- Export: `src/components/VRMExport.jsx`
- Export: `src/library/glbCompress.js`
- Export options: `src/library/glbExporter.js`. Real fields include
  `includeAnimations`, `includeTextures`, `optimize`, and
  `exportDate` (an ISO timestamp, set at export time). The deleted
  `m3/docs/model-format-specification.md` also claimed a
  `forWeftspun3DStudio` flag; no such field exists in the exporter,
  and its "Open3DStudio (Weftspun3DStudio)" framing described the
  same codebase under its old and new name as if bridging two
  systems. RFD 1102 gives the real Open3DStudio-to-Weftspun history.
