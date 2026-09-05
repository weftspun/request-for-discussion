# RFD 2214: model bundle as ZSTD-compressed SQLite range-fetched from the browser

**Range-fetch-from-browser half:** retracted 2026-09-05 by
[RFD 2228](../2228-webgpu-native-drop-platform-web/) — operator
reversal (verbatim): *"drop webgpu platform=web. try webgpu
native"*. The atelier drops the browser export, so `sql.js`,
`Accept-Ranges: bytes`, and the decompressing browser VFS are all
out.

**What survives (the live decision):** the model bundle is a
**ZSTD-compressed SQLite file on local disk**, next to the native
binary. Loader is `sqlite3_open()` on the filesystem path; the
GDExtension surface RFD 2230 defines (`Ggml.load_model()`) reads
it. Two schema shapes:

- **Shape A** (v1): whole GGUF as one BLOB in
  `model_weights(id, gguf)`. Simplest ship path.
- **Shape B** (v2, if measurement asks for it): one row per
  tensor, `tensors(name, shape, dtype, offset, blob)`. Enables
  never-fully-resident-in-memory models on constrained hosts.

ZSTD-compress at the SQLite-page level per the standing
2026-09-05 operator directive on the SQLite range-query shape.
A non-ZSTD `model.sqlite` fails whatever gate lands to enforce it.

**Where the file lives:** in the native binary's install
directory (`godot/data/models/<name>.zstd.sqlite`) or under
`$XDG_DATA_HOME/atelier/models/`. Cross-origin fetch and the H2O
edge-CDN pattern (RFD 1077) go away with the browser retraction —
downloads happen at install time via whatever release channel
ships the binary.

**State:** discussion
**Flight level:** L2 (coordination)

## Related

- [RFD 2228](../2228-webgpu-native-drop-platform-web/) — the
  reversal that retracted the browser half.
- [RFD 2229](../2229-interchangeable-parts-consolidation/) — the
  SQLite+ZSTD bundle format is the shared model-delivery
  interface across ggml consumers.
- [RFD 2230](../2230-ggml-adapters-in-godot-sandbox/) — the
  `Ggml.load_model()` GDExtension surface that consumes the
  bundle.
- [RFD 2231](../2231-drop-webgpu-use-vulkan/) — the reversal
  that dropped WebGPU; unrelated to this RFD's storage question
  but part of the same session's cleanup.

This RFD was drafted by an AI and read by a human before it shipped.
