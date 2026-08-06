# RFD 0117: Text-to-image chains into Image-to-3D, one URL resolver

**State:** committed
**Scope:** the Krea 2 Turbo completed row, the Image-to-3D form,
`3DAIGC-API`'s DINOv3 adapter

## Problem

A completed `krea2_turbo_text_to_image` row offers "Use for Image to
3D," chaining straight into `trellis2_image_to_textured_mesh`. Two
regressions kept recurring: a browser fetch reading a filesystem
path (`outputs/images/...`) instead of the job's own download URL,
and a duplicate DINOv3 feature-extractor class drifting from the
shared one.

## Decision

`resolveTextToImageDownloadUrl(task)` is the one URL resolver, for
preview, download, and chain alike. No code fetches an
`outputs/images/...` path directly. The chain button fetches through
that resolver, sets the target task type to `image-to-3d`, attaches
the fetched image as a `File`, expands the Tasks panel, and scrolls
to the new-task form. A text-to-image completion never auto-loads
into the 3D viewport on its own. The T-pose and A-pose chips stay
mutually exclusive.

On the backend, `get_dinov3_encoder_layers()` is the only path to
the DINOv3 layers; `image_feature_extractor.py` holds no second
extractor class. YAML `init_params` metadata passes through
`_filter_init_params` before reaching an adapter's `__init__`. A
pip or TRELLIS.2 edit runs `verify_hf_conditioning.py`, then
`restart_services.sh`, before merge.

## Related

RFD 0038 gives the TRELLIS.2 model image this chain's target task
runs on. This RFD replaces `krea2-text-to-3d-pipeline-protected.mdc`,
listed in RFD 0112.
