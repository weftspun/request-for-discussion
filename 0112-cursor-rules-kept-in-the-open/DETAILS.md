# RFD 0112 details: the per-file table

Three buckets. A **guard** rule blocks a regression in a feature an
existing RFD already designs. A **process** rule runs the agent's
own workflow and matches no RFD, since it names no product decision.
A **restates** rule repeats a decision an RFD already states, in
more raw or more dated words.

## Guard rules, and the RFD each one guards

| File | Guards | RFD |
| ---- | ------ | --- |
| `app-chrome-layout-protected.mdc` | header, task bar, side rails | 0001 |
| `collapsed-rail-icons.mdc` | side-rail icon symmetry | 0001 |
| `sidebar-z-index.mdc` | panel stacking order | 0001 |
| `tasks-panel-ui-protected.mdc` | Tasks panel collapse and Clear | 0003 |
| `vrm-animation-protected.mdc` | Mixamo presets, Kimodo playback | 0005 |
| `vrm-upload-protected.mdc` | VRM upload passthrough | 0005 |
| `weftspun3d-vrm-animation-playback.mdc` | Mixamo playback invariants | 0005 |
| `krea2-text-to-3d-pipeline-protected.mdc` | Krea 2 to Image-to-3D chain | 0042 |
| `lingbot-env-scan-orientation-protected.mdc` | env-scan client load | 0050 |
| `facekeeper-black-screen.mdc` | Android XR Face Bridge screen | 0096 |
| `spatial-fabric-rp1-protected.mdc` | spatial-fabric publish | 0100 |
| `xr-avatar-view-locomotion-protected.mdc` | XR embody, third-person, Move | 0090 |
| `xr-floor-anchor-protected.mdc` | XR floor anchoring | 0010, 0108 |
| `image-preview-sizing-protected.mdc` | Preview vs Expand panel sizes | 0113 |
| `spark-msf-xr-url-separation.mdc` | Scene Assembler vs XR Voice URLs | 0095, 0099 |
| `xr-strategy.mdc` | Face Bridge and Character Studio XR architecture | 0010, 0082, 0096, 0108 |

RFD 0113 is new; it wrote up `image-preview-sizing-protected.mdc`'s
invariant, since no earlier RFD held it.
`spark-msf-xr-url-separation.mdc`'s port table already lives in RFD
0099's own port table and RFD 0095's proxy step; nothing here
needed a new RFD. `xr-strategy.mdc` splits three ways: its Face
Bridge section restates RFD 0082 and RFD 0096, its VR/AR and
floor-anchor section restates RFD 0010 and RFD 0108, and its
"Broader Character Studio WebXR Strategy" roadmap section (the
WebXR Face Tracking API, moeChat/AIRI, multi-user spectator) stays
without an RFD, on purpose, since RFD 0070 opens no RFD for a build
this project has not committed to.

## Process rules

No product decision to point at. Each one runs the agent's own
workflow: `3daigc-character-studio-workflow.mdc` (redirect stub),
`3daigc-weftspun3dstudio-workflow.mdc`, `agent-continuity-startup.mdc`
(RFD 0110's own RepoResident harness), `agent-run-instructions.mdc`,
`core.mdc`, `dgx-sync-reminder.mdc`, `graphify.mdc`, `lock-it-in.mdc`,
`mcp-workspace.mdc`, `memory-bank.mdc`,
`new-scripts-ops-cheatsheet.mdc`, `no-guess-use-data.mdc`,
`pitch-deck-sync-protected.mdc`, `remember-this-retention.mdc`,
`remote-log-first.mdc`, `security-local-only.mdc`,
`solid-skills.mdc`, `surface-sync-reminder.mdc`,
`terse-debug-ops.mdc`.

## Restates

`weftspun-moat-protected.mdc` restates RFD 0106. RFD 0106 states the
open and proprietary split, in public words, with no revenue figure.
This file states the same split for the agent's own use, and it
names the revenue mechanisms behind each proprietary layer. This
repository keeps both, by RFD 0112's own decision above.
