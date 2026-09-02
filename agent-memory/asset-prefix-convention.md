---
name: asset-prefix-convention
description: Asset filenames under 5-repository and 6-datasource carry a typed prefix + PascalCase name
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6af7ce67-cc66-41b2-8c13-0bc4c0cb6fde
  modified: 2026-09-02T03:52:39.144Z
---

Asset files under `5-repository/` and `6-datasource/` follow the
typed-prefix + PascalCase naming convention. Prefix names the kind:

    T_   texture (png, jpg, webp, exr, tiff)
    DA_  data asset (json, yaml, toml)
    SM_  static mesh, SK_ skeletal mesh
    A_ AS_ AC_  animation
    M_ MI_ MF_ MPC_  material family
    S_ SC_  sound family
    VFX_ PS_  particle system
    BP_ EUW_ WBP_  blueprint family
    F_   fx

Followed by PascalCase name and optional variant suffix.
Example: `T_Az000_A.png`, `DA_Ladder.json`, `SM_AnnyHead_LOD0.glb`.

The convention is enforced by `scripts/check_asset_prefix.py`
in `weftspun/request-for-discussion` (added by PR #154). Three modes:

1. `--self-test` — control, 14 planted (8 good, 6 broken), fires
   both directions.
2. `--base <ref>` or file args — actual, fails on added or renamed
   assets that violate the shape. Wired as `asset-prefix` pre-commit
   hook.
3. no args — scouts, walks the workspace and reports drift as
   informational output (not a gate).

**Exclusions:** vendored trees (`thirdparty/`, `vendor/`,
`third_party/`), HF-standard filenames (`config.json`,
`adapter_config.json`, `tokenizer.json`, `preprocessor_config.json`,
`training_args.json`, `chat_template.jinja`, `vocab.json`,
`merges.txt`, `special_tokens_map.json`, `generation_config.json`),
build artifacts (`__pycache__`, `_build`, `.pixi`, `.lake`).

The prefix set matches the widely-adopted UE5 asset style guide from
Allar; the workspace uses it because it collapses to one convention
across image, mesh, sound and data assets rather than one per format.
The workspace's identifier for this rule is `asset-prefix`, not
"Allar's convention", so it does not depend on an external source's
continued availability.

Related: [[weights-live-on-huggingface]] — assets live on HF; this
rule names how the files on HF should be named.
