# Getting started with manifest files

A manifest file tells Weftspun3DStudio where to find a collection's
3D models and textures, how to group them into trait categories
(body, clothing, hair), and how those categories interact.

## Your collection's manifest.json

```json
{
  "assetsLocation": "/character-assets",
  "traitsDirectory": "/your-collection/",
  "thumbnailsDirectory": "/your-collection/",
  "format": "vrm",
  "displayScale": 1.0,
  "traits": []
}
```

Lay out the asset folder to match:

```
character-assets/
└── your-collection/
    ├── BODY/
    │   ├── female.vrm
    │   └── female.png
    ├── CLOTHING/
    │   ├── dress.vrm
    │   └── dress.png
    ├── HAIR/
    │   ├── long.vrm
    │   └── long.png
    └── icons/
        └── body.svg
```

## Adding a trait

Each entry in `traits` names a category, a culling layer, a camera
target, and a `collection` of options within it:

```json
{
  "trait": "BODY",
  "name": "Body",
  "iconSvg": "icons/body.svg",
  "cullingLayer": 0,
  "cameraTarget": { "distance": 0.75, "height": 1.35 },
  "collection": [
    {
      "id": "FEMALE",
      "name": "Female",
      "directory": "BODY/female.vrm",
      "thumbnail": "BODY/female.png"
    }
  ]
}
```

Base body sits at culling layer 0, clothing at 1, and accessories at
2 or higher. Use -1 for something that should never cull, such as
hair.

A collection option can also name a `textureCollection`,
`colorCollection`, or `decalCollection`, pointing at an entry under
the manifest's own `textureCollections`, `colorCollections`, or
`decalCollections` arrays. See
[Character traits](./manifest-files/character-traits.md) for the full field list
on each.

## Registering the collection

`public/manifest.json` lists every collection Weftspun3DStudio
loads, under `characters`. Each entry names `name`, `description`,
`portrait`, `manifest` (the path or URL to your collection's own
manifest file), and `format`:

```json
{
  "characters": [
    {
      "name": "Your Collection",
      "description": "A brief description",
      "portrait": "your-collection/portrait.png",
      "manifest": "your-collection/manifest.json",
      "format": "vrm"
    }
  ]
}
```

`public/manifest.json` also carries four optional top-level
sections, shared across every collection: `loras`
([LoRA capture](./manifest-files/vrm-to-lora.md)), `sprites`
([sprite sheets](./manifest-files/vrm-to-spritesheet.md)),
`thumbnails` ([thumbnail generation](./manifest-files/vrm-to-thumbnails.md)),
and `defaultAnimations` (shared idle, walk, and run clips, per
[Character traits](./manifest-files/character-traits.md#animationpath)).

## Common issues

A model that does not show up usually means a file path in the
manifest does not match the folder structure, or a VRM export
failed. A texture that looks wrong usually means the UV map does not
match the base mesh, or the texture is not PNG. A color that does
not apply usually means the trait's `colorCollection` id does not
match an entry in `colorCollections`.

See [Character traits](./manifest-files/character-traits.md) for the full field
reference.
