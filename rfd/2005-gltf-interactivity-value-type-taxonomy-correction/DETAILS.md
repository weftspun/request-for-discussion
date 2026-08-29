## Summary

`rfd/2001-zonefabric-roadmap-vs-mas-bandwidth-fps/index.md`, item 5, described
`gltf_interactivity`'s value-type system as a two-way split: primitive
types versus `ref`. The real specification, vendored at
`taskweft/thirdparty/gltf_interactivity/`, defines three signature
categories, not two. This RFD corrects the record and states which
category `zone-server-h2o` actually implements.

## Background

`taskweft/thirdparty/gltf_interactivity/01_core_concepts.md` defines
the value socket types this way. The scalar types are:

- `bool`, a boolean value.
- `float`, a double precision IEEE-754 floating-point scalar value.
- `int`, a two's complement 32-bit signed integer scalar value.
- `ref`, an opaque reference value.

The vector types are `float2`, `float3`, and `float4`. The matrix
types are `float2x2`, `float3x3`, and `float4x4`.

Custom variable defaults follow the same table. `bool` defaults to
false. The float, vector, and matrix types default to NaN. `int`
defaults to zero. `ref` defaults to a null reference.

`taskweft/thirdparty/gltf_interactivity/03_extending_gltf.md` adds a
third category on top of this list. A signature's value must be one
of the value types this specification defines, or `custom`. An
extension must provide the custom type semantics when a signature is
`custom`. That extension also defines a custom variable's own `value`
property.

## Motivation

`zone-server-h2o` cites this specification as its source vocabulary
for CastSpell's own value-versus-handle split, per RFD 2001 item 5. A
reader who trusts that citation needs it to describe the real
specification correctly, not a simplified version of it. Recording the
`custom` category here also settles, in advance, whether a future
CastSpell parameter needs it.

## Proposal

State the taxonomy as three categories, matching the specification
directly:

1. Primitive value types are `bool`, `float`, `float2`, `float3`,
   `float4`, `float2x2`, `float3x3`, `float4x4`, and `int`. Each
   carries its value directly.
2. `ref` is an opaque reference value, with a null reference as its
   default. The specification does not define what a `ref` points to.
   The node or extension that produces it defines that instead.
3. `custom` is a signature value that defers all type semantics,
   including a variable's own `value` property, to an extension the
   signature names.

`zone-server-h2o` implements only the first two categories today.
CastSpell's bitpacked struct layout (`rfd/0001`, item 4's cross
reference to `rfd/2003-castspell-sandbox-package-and-manifest-encoding/index.md`)
gives a primitive field its value inline, and a `ref` field a slotmap
handle from `RFD 2017 (slotmap-entity-storage)`. Nothing in the
current CastSpell design needs `custom`. Every value a CastSpell
effect reads or writes today, position, velocity, health, and an
entity handle, already fits a primitive or a `ref`.

Leave `custom` unimplemented, not rejected. A future CastSpell
parameter might need an extension-defined type: a texture handle, a
material reference, or a similar non-numeric, non-entity value. Such a
parameter would need its own extension declaration first. That matches
the specification's own "an additional extension" requirement, and
must happen before this project's struct layout could carry it.

## Recommendation and next steps

1. Correct `rfd/2001-zonefabric-roadmap-vs-mas-bandwidth-fps/index.md`, item
   5, to cite this RFD instead of restating the (incomplete) two-way
   split inline.
2. When a future CastSpell parameter needs a `custom`-signature value,
   design its extension and its struct representation as a follow-up
   to this RFD, not as a silent addition to the primitive/`ref` split.

## Deferred work and verification

No question stays open here. One item is deferred, which is a
different thing, because nothing blocks on the answer.

Deferred: no current CastSpell parameter needs `custom`. The decision
waits on a parameter that needs it. Revisit this RFD when one appears,
and decide the extension and the struct representation at that time.

Verification: re-read
`taskweft/thirdparty/gltf_interactivity/01_core_concepts.md` and
`03_extending_gltf.md` directly to confirm the three-category taxonomy
still holds. `taskweft/taskweft` is a project outside this org, and
its vendored copy can move independently of this RFD.
