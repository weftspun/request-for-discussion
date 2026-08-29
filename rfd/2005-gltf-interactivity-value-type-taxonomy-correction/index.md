---
title: "RFD 2005: gltf_interactivity's value types: primitive, ref, and custom"
rfd: "2005"
state: discussion
scope: zone-server-h2o CastSpell
---

## Problem

RFD 2001 item 5 described `gltf_interactivity`'s value types as a
two-way split: primitive types and `ref` types. The vendored
`gltf_interactivity` specification actually defines three value-type
categories, not two. This mismatch left CastSpell's bitpacked struct
design without a correct taxonomy to implement against.

## Decision

`gltf_interactivity`'s vendored specification defines three value-type
categories, not the two-way primitive/`ref` split `RFD 2001` item 5
first described: primitive types (`bool`, `float`, the `float2`/`3`/`4`
vectors and matrices, `int`), `ref` (an opaque reference, null by
default), and `custom` (a signature that defers all type semantics to
an extension). `zone-server-h2o` implements only the first two today;
CastSpell's bitpacked struct gives a primitive field its value inline
and a `ref` field a slotmap handle. Leave `custom` unimplemented, not
rejected, until a CastSpell parameter needs an extension-defined type.

## References

- Full taxonomy detail and verification: `DETAILS.md`
- `taskweft/thirdparty/gltf_interactivity/01_core_concepts.md`,
  `03_extending_gltf.md`

## Related

`rfd/2001-zonefabric-roadmap-vs-mas-bandwidth-fps/index.md` (item 5),
`rfd/2003-castspell-sandbox-package-and-manifest-encoding/index.md`

## Detail

{{< include DETAILS.md >}}
