# Preparing assets

Clone and install [Weftspun3DStudio](https://github.com/weftspun/weftspun-3d-studio).
Copy your assets into the `public` folder, then check the `.env`
variables point at the right location.

## Blender

Requirements: [Blender LTS](https://www.blender.org/download/lts/)
(tested with 3.6; Blender 4.0's material export did not work
correctly in the last test, so prefer 3.6 if you hit problems), and
the [Saturday06 VRM add-on](https://github.com/saturday06/VRM-Addon-for-Blender).

**Modeling traits.** Keep each trait type in its own blend file: one
for clothing, one for hair, and so on, so a file does not grow too
big to open and debug. An artist designing a trait imports the
rigged base mesh first, since it keeps the parts aligned to merge
correctly into a VRM. The app cannot adjust position, scale, or
rotation after import yet, so make those adjustments in Blender.

**Exporting.** Each trait carries its own VRM armature as its
parent, not a shared one, since some traits hold more bones than
others. The project targets VRM version 0.

![](/img/SJebjntDeT.jpg)

A batch export script writes every VRM in a blend file to a
destination folder. Set `export_path` in the script before running
it:

```python
import bpy
import os
import sys

def export_vrm(input_blend):
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(input_blend))

    view_layer_name = 'ViewLayer'
    view_layer = bpy.context.scene.view_layers.get(view_layer_name)
    if view_layer is None:
        print(f"View Layer '{view_layer_name}' not found.")
        sys.exit(1)
    bpy.context.window.view_layer = view_layer

    visible_objects = [obj for obj in bpy.context.scene.objects if obj.parent is None]

    for obj in visible_objects:
        if obj.name not in view_layer.objects:
            print(f"Object '{obj.name}' is not in view layer '{view_layer_name}'. Skipping.")
            continue

        for child in obj.children_recursive:
            if child.type != 'MESH':
                continue
            mesh = child
            if mesh.name not in view_layer.objects:
                continue

            armature = mesh.parent
            armature.data.vrm_addon_extension.spec_version = "0.0"
            filename = mesh.name + ".vrm"

            bpy.context.view_layer.objects.active = mesh
            mesh.select_set(True)

            bpy.ops.export_scene.vrm(
                filepath=os.path.join(export_path, filename),
                export_invisibles=False,
                enable_advanced_preferences=True,
                export_fb_ngon_encoding=False,
                export_only_selections=True,
                armature_object_name=obj.name
            )

if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

    export_path = "/home/user/Desktop/Exports"  # change this
    os.makedirs(export_path, exist_ok=True)

    input_blend = os.path.abspath(argv[0]) if argv else None
    if not input_blend:
        print("Error: Input .blend file not provided.")
        sys.exit(1)

    export_vrm(input_blend)
```

Run it headless: `blender -b -P scripts/blender_export.py -- blends/Waist.blend`.
Or open the Scripting tab in Blender and run it there.

![](/img/Bke-i2YPeT.jpg)

## Unity

Requirements: [UniVRM](https://github.com/vrm-c/UniVRM/).

![](/img/HkeZs2Kvla.jpg)
