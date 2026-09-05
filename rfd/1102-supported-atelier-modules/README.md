# RFD 1102: The supported task catalog, one live source

**State:** committed
**Scope:** RFDs 1036 (packaging), 1173 (pipeline), 2136 (gacha ladder), 2188 (one ggml across workspace), 2210 (atelier surface), 2230 (ggml adapters)

## Decision

Every module in the atelier catalog runs on **ggml** (RFD 2188).
Weights ship as GGUF, quantised to Q4. The set of Docker images
this workspace ships per RFD 1036 (plain HTTP, `/health` +
`/predict`, weights at build time, one model per image) runs on
the local desktop GPU per CLAUDE.md via ggml's Vulkan backend
(RFD 2231's substitute), and feeds the two pipelines the workspace
operates:

- **MaskScore corpus construction** (RFD 1173): eight stubs across
  mesh/depth/pose/keypoints/multimodal/speech/text/video. Five
  shipped on HF (RFD 2164 speech + Rung 1 walking skeleton).
- **The gacha critical path** (RFD 2136): ten-rung ladder from a
  language prompt to a public roll-button-dispensed VRM.

Consumer projects wrap the shared `2-contract/ggml/` runtime; the
native `modules/ggml/` module (RFD 2230) exposes a GDExtension
surface (`Ggml.load_model`, `Ggml.run_inference`, `Ggml.load_lora`)
consumed by per-model GDScript adapter files loaded under Godot's
script sandbox.

`DETAILS.md` carries the current per-task table (with per-model
GGUF sizes and port-needed flags), the six-step migration recipe,
the two pipeline diagrams, and the packaging pointer.

## Related

RFD 1036 (Docker packaging), RFD 1053 (OpenUSD internal + glTF/VRM
at edge), RFD 1027 (GPU tier), RFD 1173 (multimodal pipeline),
RFD 2136 (gacha ladder), RFD 2164 (Speech stub shipped), RFD 2188
(one ggml across workspace), RFD 2210 (atelier native shipping
surface), RFD 2214 (model bundle SQLite+ZSTD), RFD 2229
(interchangeable-parts consolidation), RFD 2230 (ggml adapters in
godot-sandbox), RFD 2231 (Vulkan renderer).
