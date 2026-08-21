# Old numbers

Every RFD that existed at the migration changed number. The old number was
decimal and named a document in another organization as well. The new number
starts with the organization digit 1. RFD 1000 gives the rule.

Git history and pull request titles keep the old numbers. This table is how a
reader resolves them. It is a lookup and not a repair.

The migration was a closed set. An RFD written after it has no old number and
therefore no row here. RFD 107b is the last number the table covers, and
`check-rfd-numbers.py` reads that boundary out of the table rather than
holding a copy of it.

| old      | new      | slug                                            |
| -------- | -------- | ----------------------------------------------- |
| RFD 0000 | RFD 1000 | conventions                                     |
| RFD 0001 | RFD 1001 | app-shell-and-routing                           |
| RFD 0002 | RFD 1002 | studio-pipeline-graph                           |
| RFD 0003 | RFD 1003 | task-manager-job-lifecycle                      |
| RFD 0004 | RFD 1004 | aigc-task-catalog                               |
| RFD 0005 | RFD 1005 | avatar-and-vrm-pipeline                         |
| RFD 0006 | RFD 1006 | layer-decomposition-see-through                 |
| RFD 0007 | RFD 1007 | motion-validation-kimodo                        |
| RFD 0008 | RFD 1008 | appearance-trait-extraction-and-remix           |
| RFD 0009 | RFD 1009 | viewport-and-scene-rendering                    |
| RFD 0010 | RFD 100a | webxr-and-iwsdk-lab                             |
| RFD 0011 | RFD 100b | spatial-fabric-publish                          |
| RFD 0012 | RFD 100c | wallet-minting-and-x402                         |
| RFD 0013 | RFD 100d | public-demo-deploy                              |
| RFD 0014 | RFD 100e | batch-processing                                |
| RFD 0015 | RFD 100f | phygital-passport                               |
| RFD 0016 | RFD 1010 | deep-learning-model-inventory                   |
| RFD 0017 | RFD 1011 | fork-rebrand-to-weftspun                        |
| RFD 0018 | RFD 1012 | m3-documentation-removal                        |
| RFD 0019 | RFD 1013 | strangler-fig-studio-core                       |
| RFD 0020 | RFD 1014 | cockroachdb-persistence                         |
| RFD 0021 | RFD 1015 | shared-hrr-library                              |
| RFD 0022 | RFD 1016 | hexagonal-client                                |
| RFD 0023 | RFD 1017 | ports-and-adapters-with-headless-cms-style      |
| RFD 0024 | RFD 1018 | (directory deleted before the migration)        |
| RFD 0025 | RFD 1019 | model-memory-arithmetic                         |
| RFD 0026 | RFD 101a | bf16-memory-per-model                           |
| RFD 0027 | RFD 101b | gpu-residency-budget                            |
| RFD 0028 | RFD 101c | model-license-gate                              |
| RFD 0029 | RFD 101d | foss-model-replacements                         |
| RFD 0030 | RFD 101e | seethrough-component-models                     |
| RFD 0031 | RFD 101f | geometry-refinement-and-alpha-wrap              |
| RFD 0032 | RFD 1020 | (directory deleted before the migration)        |
| RFD 0033 | RFD 1021 | geometric-algorithms                            |
| RFD 0034 | RFD 1022 | krea-memory-cross-check                         |
| RFD 0035 | RFD 1023 | legacy-model-identifiers                        |
| RFD 0036 | RFD 1024 | packaging-convention                            |
| RFD 0037 | RFD 1025 | composite-models-as-taskweft-domains            |
| RFD 0038 | RFD 1026 | trellis2-image-to-textured-mesh                 |
| RFD 0039 | RFD 1027 | trellis2-image-mesh-painting                    |
| RFD 0040 | RFD 1028 | pixal3d-image-to-textured-mesh                  |
| RFD 0041 | RFD 1029 | p3sam-mesh-segmentation                         |
| RFD 0042 | RFD 102a | krea2-turbo-text-to-image                       |
| RFD 0043 | RFD 102b | qwen-image-edit                                 |
| RFD 0044 | RFD 102c | seethrough-layer-decomposition                  |
| RFD 0045 | RFD 102d | kimodo-text-to-motion                           |
| RFD 0046 | RFD 102e | skintokens-auto-rig                             |
| RFD 0047 | RFD 102f | voxhammer-text-mesh-editing                     |
| RFD 0048 | RFD 1030 | voxhammer-image-mesh-editing                    |
| RFD 0049 | RFD 1031 | weftspun-image-to-world                         |
| RFD 0050 | RFD 1032 | lingbot-map-environment-scan                    |
| RFD 0051 | RFD 1033 | worldmirror2-reconstruct                        |
| RFD 0052 | RFD 1034 | triposplat-image-to-splat                       |
| RFD 0053 | RFD 1035 | openusd-as-the-internal-format                  |
| RFD 0054 | RFD 1036 | headless-cms-on-taskweft                        |
| RFD 0055 | RFD 1037 | beam-workers-local-first                        |
| RFD 0056 | RFD 1038 | develop-in-a-dev-container                      |
| RFD 0057 | RFD 1039 | open-work                                       |
| RFD 0058 | RFD 103a | zero-trust-networking                           |
| RFD 0059 | RFD 103b | continuous-integration                          |
| RFD 0060 | RFD 103c | thirdparty-reset                                |
| RFD 0061 | RFD 103d | glb-upload-prep-via-idtx-core                   |
| RFD 0062 | RFD 103e | flyio-toplevel-4090-worker-split                |
| RFD 0063 | RFD 103f | ste-enforcement-moves-to-the-plugin             |
| RFD 0064 | RFD 1040 | character-concept-generator                     |
| RFD 0065 | RFD 1041 | taskweft-domain-schema-in-etnf                  |
| RFD 0066 | RFD 1042 | differential-mamba-for-caption-encoding         |
| RFD 0067 | RFD 1043 | cockroachdb-reranked-against-foundationdb       |
| RFD 0068 | RFD 1044 | (directory deleted before the migration)        |
| RFD 0069 | RFD 1045 | (directory deleted before the migration)        |
| RFD 0070 | RFD 1046 | keep-options-open                               |
| RFD 0071 | RFD 1047 | (directory deleted before the migration)        |
| RFD 0072 | RFD 1048 | (directory deleted before the migration)        |
| RFD 0073 | RFD 1049 | dataset-billboard-gallery                       |
| RFD 0074 | RFD 104a | 3d-billboard-labels                             |
| RFD 0075 | RFD 104b | github-oauth-admin-login                        |
| RFD 0076 | RFD 104c | usd-viewer-app-build-integration                |
| RFD 0077 | RFD 104d | h2o-edge-cdn                                    |
| RFD 0078 | RFD 104e | h2o-fdb-game-state-server                       |
| RFD 0079 | RFD 104f | appsignal-observability                         |
| RFD 0080 | RFD 1050 | fly-deploy-cost                                 |
| RFD 0082 | RFD 1052 | android-studio-ai-brief                         |
| RFD 0083 | RFD 1053 | api-avatar-rig-contract                         |
| RFD 0084 | RFD 1054 | avatar-pipeline                                 |
| RFD 0085 | RFD 1055 | code-map                                        |
| RFD 0086 | RFD 1056 | dev-machine-topology                            |
| RFD 0087 | RFD 1057 | gemini                                          |
| RFD 0088 | RFD 1058 | https-setup                                     |
| RFD 0089 | RFD 1059 | hyworld-image-to-world-scope                    |
| RFD 0090 | RFD 105a | iwsdk-integration                               |
| RFD 0091 | RFD 105b | iwsdk-local-fork                                |
| RFD 0092 | RFD 105c | kimodo-backend-integration                      |
| RFD 0093 | RFD 105d | loot-assets-setup                               |
| RFD 0094 | RFD 105e | multi-image-splat-roadmap                       |
| RFD 0095 | RFD 105f | nvidia-xr-ai-integration                        |
| RFD 0096 | RFD 1060 | openxr-face-tracking-android-xr                 |
| RFD 0098 | RFD 1062 | public-deploy                                   |
| RFD 0099 | RFD 1063 | scripts-cheatsheet                              |
| RFD 0100 | RFD 1064 | spatial-fabric-integration                      |
| RFD 0101 | RFD 1065 | ssh-host-names                                  |
| RFD 0102 | RFD 1066 | supported-3daigc-modules                        |
| RFD 0103 | RFD 1067 | vercel-loot-assets                              |
| RFD 0104 | RFD 1068 | vrm-upload-display-export                       |
| RFD 0105 | RFD 1069 | webcam-avatar-control                           |
| RFD 0106 | RFD 106a | weftspun-moat-overview                          |
| RFD 0107 | RFD 106b | world-package                                   |
| RFD 0108 | RFD 106c | xr-mode-floor-anchoring-and-backgrounds         |
| RFD 0109 | RFD 106d | moat-payment-rails-and-phygital-registry        |
| RFD 0110 | RFD 106e | reporesident-agent-harness                      |
| RFD 0111 | RFD 106f | 3daigc-api-reference-not-restated               |
| RFD 0112 | RFD 1070 | cursor-rules-kept-in-the-open                   |
| RFD 0113 | RFD 1071 | image-preview-vs-expand-sizing                  |
| RFD 0114 | RFD 1072 | app-chrome-layout-invariants                    |
| RFD 0115 | RFD 1073 | vrm-animation-playback-invariants               |
| RFD 0116 | RFD 1074 | tasks-panel-clear-and-collapse                  |
| RFD 0117 | RFD 1075 | text-to-image-to-3d-chain                       |
| RFD 0118 | RFD 1076 | xr-embody-locomotion-and-menu                   |
| RFD 0119 | RFD 1077 | generic-hardware-not-dgx-or-android-xr-specific |
| RFD 0120 | RFD 1078 | split-apps-into-own-repos                       |
| RFD 0121 | RFD 1079 | layers-from-geometry-and-the-missing-categories |
| RFD 0122 | RFD 107a | the-wholebody-gap                               |
| RFD 0123 | RFD 107b | cineform-in-godot                               |

116 RFDs, plus 6 numbers whose directory was deleted before
the migration and which older RFDs still cite.
