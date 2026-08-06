# Optimize avatars

Hand-optimizing a VRM model takes time. The Optimizer page reduces
an avatar's draw calls and file size instead, through drag and drop:

- Merge textures into one image atlas. A transparent texture merges
  into a separate atlas from an opaque one.
- Merge skinned meshes together.

The Optimizer page reports the current skinned-mesh and
texture-material count, so you can weigh the options before
committing.

![Optimizer panel](/img/r1EneCsip.png)

Merging to one shader, either MToon or Standard, cuts draw calls and
file size the most. Keeping both shaders costs more space, but keeps
the closest likeness to a model built with both.

![Texture atlas comparison](/img/rkH3-CjjT.png)

See `src/pages/Optimizer.jsx` and `src/library/textureOptimizer.js`
for the atlas-size defaults and the merge logic.
