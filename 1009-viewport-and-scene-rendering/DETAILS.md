# RFD 1009 details: the renderer fallback chain

This replaces the reference this RFD once made to
`docs/THREEJS_WEBGPU_WEBXR_MIGRATION.md`. That guide, and its
companion `THREEJS_QUICK_START.md`, described a `getRendererInfo()`
method, a `setupPostProcessing()` call with SSAO, Bloom, and FXAA
toggles, and a `createPositionalAudio()` spatial-audio helper. None
of the three exist in `sceneManager.js`. `EffectComposer` appears
only in `screenshotManager.js`, for a screenshot render pass, not a
live post-processing pipeline. Both guides drifted from a build that
never shipped, or shipped then shrank; deleted, not rewritten.

## The renderer fallback chain

`SceneManager.initialize()` calls `createViewportRenderer()`, which
returns a WebGPU renderer, a WebGPU-support flag, and a type string,
when the browser and GPU support it. `this.rendererType` takes that
value: `'webgpu'`, `'webgl'`, or `'software'`, falling back in that
order when a step fails. `initialize()` returns `rendererType`
alongside `scene`, `camera`, `renderer`, and `controls`, so a caller
can read which tier is active.

## What the old migration doc got right

The VR camera offset and the AR pass-through transparency it
described are real, current behavior. RFD 106c gives the exact
wrapper math and the reference-space priority, more precisely than
the old guide did.
