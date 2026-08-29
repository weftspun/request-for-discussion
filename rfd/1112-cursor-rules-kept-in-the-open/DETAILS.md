# RFD 1112 details: the per-file table

Three buckets. A **guard** rule blocks a regression in a feature an
existing RFD already designs. A **process** rule runs the agent's
own workflow and matches no RFD, since it names no product decision.
A **restates** rule repeats a decision an RFD already states, in
more raw or more dated words.

All 16 guard rules are now converted. See "Converted and deleted"
below for where each one went.

## Converted and deleted

Each row already went through: the RFD named now holds the design,
and `rules/` no longer holds the file.

| File                                                                                 | Converted into                                                                                                                                                                                                                                                                                                                                 |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `app-chrome-layout-protected.mdc`, `collapsed-rail-icons.mdc`, `sidebar-z-index.mdc` | RFD 1114 (new)                                                                                                                                                                                                                                                                                                                                 |
| `image-preview-sizing-protected.mdc`                                                 | RFD 1113 (new)                                                                                                                                                                                                                                                                                                                                 |
| `vrm-animation-protected.mdc`, `weftspun3d-vrm-animation-playback.mdc`               | RFD 1115 (new, merged; the two files were near-duplicates)                                                                                                                                                                                                                                                                                     |
| `vrm-upload-protected.mdc`                                                           | RFD 1104 (already covered)                                                                                                                                                                                                                                                                                                                     |
| `spark-msf-xr-url-separation.mdc`                                                    | RFD 1099's port table, RFD 1095's proxy step (already covered)                                                                                                                                                                                                                                                                                 |
| `facekeeper-black-screen.mdc`                                                        | RFD 1082's DETAILS.md, a new section (extended, not new)                                                                                                                                                                                                                                                                                       |
| `xr-strategy.mdc`                                                                    | its Face Bridge section into RFD 1082 and RFD 1096; its VR/AR and floor-anchor section into RFD 1010 and RFD 1108; its "Broader Character Studio WebXR Strategy" roadmap (the WebXR Face Tracking API, moeChat/AIRI, multi-user spectator) into nothing, on purpose, since RFD 1070 opens no RFD for a build this project has not committed to |
| `tasks-panel-ui-protected.mdc`                                                       | RFD 1116 (new; RFD 1003 covers the job lifecycle, not this toolbar)                                                                                                                                                                                                                                                                            |
| `krea2-text-to-3d-pipeline-protected.mdc`                                            | RFD 1117 (new; RFD 1042 covers model packaging, not this chain)                                                                                                                                                                                                                                                                                |
| `lingbot-env-scan-orientation-protected.mdc`                                         | RFD 1107's DETAILS.md, a new section (extended, not new)                                                                                                                                                                                                                                                                                       |
| `spatial-fabric-rp1-protected.mdc`                                                   | RFD 1100's DETAILS.md, a new closing note (extended, not new); RFD 1099 already covered the raw-`.msf` rule                                                                                                                                                                                                                                    |
| `xr-floor-anchor-protected.mdc`                                                      | RFD 1107's DETAILS.md, a new section (extended, not new; RFD 1108 covers single-model floor placement, not the world-layer bounds computation this rule guarded)                                                                                                                                                                               |
| `xr-avatar-view-locomotion-protected.mdc`                                            | RFD 1118 (new; RFD 1090 is the abandoned IWSDK lab, a different XR path)                                                                                                                                                                                                                                                                       |

## Process rules

No product decision to point at. Each one runs the agent's own
workflow: `3daigc-character-studio-workflow.mdc` (redirect stub),
`3daigc-weftspun3dstudio-workflow.mdc`, `agent-continuity-startup.mdc`
(RFD 1110's own RepoResident harness), `agent-run-instructions.mdc`,
`core.mdc`, `dgx-sync-reminder.mdc`, `graphify.mdc`, `lock-it-in.mdc`,
`mcp-workspace.mdc`, `memory-bank.mdc`,
`new-scripts-ops-cheatsheet.mdc`, `no-guess-use-data.mdc`,
`pitch-deck-sync-protected.mdc`, `remember-this-retention.mdc`,
`remote-log-first.mdc`, `security-local-only.mdc`,
`solid-skills.mdc`, `surface-sync-reminder.mdc`,
`terse-debug-ops.mdc`.

## Restates

`weftspun-moat-protected.mdc` restates RFD 1106. RFD 1106 states the
open and proprietary split, in public words, with no revenue figure.
This file states the same split for the agent's own use, and it
names the revenue mechanisms behind each proprietary layer. This
repository keeps both, by RFD 1112's own decision above.
