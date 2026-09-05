# RFD 2214: model bundle as ZSTD-compressed SQLite range-fetched from the browser

**State:** discussion
**Flight level:** L2 (coordination)
**Feature:** how the motion-bricks model (180 MB Q4 GGUF) reaches the
browser without shipping in the WASM binary or as a monolithic
initial download
**Scope:** `service-sqlar-cas/docs/` demo pattern extended, new
`mb_model_load_from_memory` C API on `motion-bricks-cpp`

## Decision

Store the motion-bricks G1 model in a SQLite file, ZSTD-compressed
per the standing operator directive 2026-09-05 for the
range-fetch shape. Serve with `Accept-Ranges: bytes`; `sql.js` in
the browser reads pages on demand via a decompressing VFS.

Two schema shapes:

- **Shape A** (recommended for v1): whole GGUF as one BLOB in
  `model_weights(id, gguf)`. Loader change: new C API
  `mb_model_load_from_memory(bytes, size, options, **model, error)`
  on `motion-bricks-cpp`. Simplest ship path.
- **Shape B** (v2): one row per tensor,
  `tensors(name, shape, dtype, offset, blob)`. Range queries stream
  only tensors the inference graph touches per plan. Enables
  never-fully-resident-in-memory models on 4 GB tablets. Bigger
  design change; needs `mb_model_load_from_tensor_provider(...)`
  API and an inference-order-vs-page-locality study.

Both shapes ZSTD-compress at the SQLite-page level; the same
decompressing VFS handles either schema.

## Compression is not optional

The standing 2026-09-05 operator directive is explicit: **our
SQLite range-query shape requires ZSTD compression**. This RFD
inherits that requirement. A non-ZSTD `model.sqlite` fails a
prek/CI gate at the point that gate lands.

## Where the SQLite file lives

- **v1**: `res://model.sqlite` bundled in the Godot export.
  Same-origin fetch. Export inflates by the file's compressed size
  (Q4 GGUF ZSTD-compressed: measurement pending; expected
  ~120–150 MB).
- **v2**: `https://cdn.chibifire.com/models/motionbricks/g1-q4.
  zstd.sqlite` per RFD 1077's H2O edge-CDN pattern. Cross-origin
  fetch (CORS). Export stays small; multiple exports share one
  asset.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3.
- [RFD 2212](../2212-motion-bricks-as-native-godot-module/) — the
  Godot module that calls the new load API.
- RFD 1077 (H2O edge-CDN) — the v2 hosting pattern.
- `service-sqlar-cas/docs/fixtures/{persona,starforged}.sqlite` —
  the demonstrated in-workspace pattern this RFD extends.

This RFD was drafted by an AI and read by a human before it shipped.
