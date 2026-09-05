# RFD 2214: model bundle as ZSTD-compressed SQLite on local disk

**State:** discussion
**Flight level:** L2 (coordination)
**Feature:** how a ggml model file (e.g. 180 MB Q4 GGUF) reaches the
native binary at runtime
**Scope:** `2-contract/ggml`, `modules/ggml/` GDExtension loader,
per-consumer adapter files

## Decision

Ship the model in a ZSTD-compressed SQLite file on local disk, next
to the native binary. Loader is `sqlite3_open()` on the filesystem
path; the GDExtension surface RFD 2230 defines (`Ggml.load_model()`)
reads it and hands bytes to ggml. Two schema shapes:

- **Shape A** (v1): whole GGUF as one BLOB in `model_weights(id, gguf)`.
  Simplest ship path.
- **Shape B** (v2, if measurement asks for it): one row per tensor,
  `tensors(name, shape, dtype, offset, blob)`. Enables never-fully-
  resident-in-memory models on constrained hosts.

ZSTD-compress at the SQLite-page level. A gate lands to enforce it.

Files live in the native binary's install directory
(`godot/data/models/<name>.zstd.sqlite`) or under
`$XDG_DATA_HOME/atelier/models/`; downloaded at install time via the
release channel that ships the binary.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3.
- [RFD 2229](../2229-interchangeable-parts-consolidation/) — the
  SQLite+ZSTD bundle format is the shared model-delivery interface
  across ggml consumers.
- [RFD 2230](../2230-ggml-adapters-in-godot-sandbox/) — the
  `Ggml.load_model()` GDExtension surface that consumes the bundle.

This RFD was drafted by an AI and read by a human before it shipped.
