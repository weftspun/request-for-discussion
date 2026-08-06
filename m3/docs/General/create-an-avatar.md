# Create an avatar

Weftspun3DStudio builds an avatar in three ways:

- Select from preloaded assets.
- Drag and drop your own 3D models and textures.
- Generate an avatar from a manifest file.

## Select traits

Pick from the assets the app loads, and mix them to build a style,
the way other character creators work.

![](/img/v2zJEiy.gif)

To create your own preloaded asset configuration, read the manifest
file documentation under `Modders/manifest-files/`.

## Drag and drop your own assets

Upload files in VRM format. Weftspun3DStudio also overwrites a
trait's texture the same way: select the trait, then drag an image
file into the browser window. Click the target category first. The
image needs a UV layout that matches the base mesh.

## Generate from a manifest

Weftspun3DStudio assembles and exports a VRM from a JSON manifest
naming each trait. This path suits a batch of VRM files sharing one
trait structure, not a one-off avatar edit. See
`Modders/manifest-files/overview.md` for the schema, and
`Modders/getting-started.md` for the walkthrough.
