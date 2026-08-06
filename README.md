# RFD Index

This repository holds Request-for-Discussion documents, across every
weftspun project, one shared numbering space. It follows the Oxide
RFD style.

Each RFD is a reference design. It records a decision and points to
the canonical documentation, in whichever project's own repository
holds the code. It does not restate the documentation. See the STE
policy below for the writing rules.

RFD 0000 through RFD 0078 moved here from
[weftspun/weftspun-3d-studio](https://github.com/weftspun/weftspun-3d-studio)'s
own `decisions/`, per that project's own RFD convention already
naming this repository's shape. `git log` on each RFD's own files
carries its original history forward.

## Index

| RFD  | Reference design                                      | State          |
| ---- | ----------------------------------------------------- | -------------- |
| 0000 | Conventions (RFD style, STE, DRY)                     | published      |
| 0001 | App shell and routing                                 | published      |
| 0002 | Studio pipeline graph                                 | published      |
| 0003 | Task Manager job lifecycle                            | published      |
| 0004 | AIGC task catalog                                     | published      |
| 0005 | Avatar and VRM pipeline                               | published      |
| 0006 | Layer decomposition (See-Through)                     | discussion     |
| 0007 | Motion validation (Kimodo)                            | discussion     |
| 0008 | Appearance trait extraction and remix                 | discussion     |
| 0009 | Viewport and scene rendering                          | published      |
| 0010 | WebXR and IWSDK lab                                   | published      |
| 0011 | Spatial fabric publish                                | published      |
| 0012 | Wallet, minting, and x402                             | abandoned      |
| 0013 | Public demo deploy                                    | published      |
| 0014 | Batch processing                                      | published      |
| 0015 | Phygital passport                                     | abandoned      |
| 0016 | Deep learning model inventory                         | published      |
| 0017 | Fork rebrand to Weftspun                              | published      |
| 0018 | M3 documentation removal                              | discussion     |
| 0019 | Strangler fig studio core                             | published      |
| 0020 | CockroachDB persistence                               | published      |
| 0021 | Shared HRR library                                    | published      |
| 0022 | Hexagonal client                                      | published      |
| 0023 | Ports and adapters with headless CMS style            | published      |
| 0025 | Model memory arithmetic                               | published      |
| 0026 | bf16 memory per model                                 | published      |
| 0027 | GPU residency budget                                  | published      |
| 0028 | Model license gate                                    | published      |
| 0029 | FOSS model replacements                               | published      |
| 0030 | See-Through component models                          | published      |
| 0031 | Geometry refinement and alpha wrap                    | discussion     |
| 0033 | Geometric algorithms in the catalog                   | published      |
| 0034 | Krea memory cross-check                               | published      |
| 0035 | Legacy model identifiers                              | published      |
| 0036 | Model packaging convention                            | discussion     |
| 0037 | Composite models as taskweft domains                  | discussion     |
| 0038 | Model image for trellis2_image_to_textured_mesh       | discussion     |
| 0039 | Model image for trellis2_image_mesh_painting          | discussion     |
| 0040 | Model image for pixal3d_image_to_textured_mesh        | discussion     |
| 0041 | Model image for p3sam_mesh_segmentation               | discussion     |
| 0042 | Model image for krea2_turbo_text_to_image             | discussion     |
| 0043 | Model image for qwen_q4_k_m_image_edit                | discussion     |
| 0044 | Model image for seethrough_layer_decomposition        | discussion     |
| 0045 | Model image for kimodo_text_to_motion                 | discussion     |
| 0046 | Model image for skintokens_auto_rig                   | discussion     |
| 0047 | Model image for voxhammer_text_mesh_editing           | discussion     |
| 0048 | Model image for voxhammer_image_mesh_editing          | discussion     |
| 0049 | Model image for weftspun_image_to_world               | abandoned      |
| 0050 | Model image for lingbot_map_environment_scan          | abandoned      |
| 0051 | Model image for worldmirror2_reconstruct              | abandoned      |
| 0052 | Model image for triposplat_image_to_splat             | abandoned      |
| 0053 | OpenUSD as the internal format                        | discussion     |
| 0054 | The planner inside the studio core                    | published      |
| 0055 | BEAM workers, local first                             | discussion     |
| 0056 | Develop in a dev container                            | discussion     |
| 0057 | Open work                                             | published      |
| 0058 | Zero trust networking                                 | discussion     |
| 0059 | Continuous integration, in one step                   | published      |
| 0060 | A thirdparty/ reset                                   | discussion     |
| 0061 | GLB upload prep moves to idtx_core, later             | discussion     |
| 0062 | A Fly.io toplevel, and the 4090 as a worker node      | discussion     |
| 0063 | STE enforcement moves to the plugin                   | discussion     |
| 0064 | Character Concept Generator                           | pre-discussion |
| 0065 | Taskweft domain schema in essential tuple normal form | discussion     |
| 0066 | Differential Mamba for caption encoding               | abandoned      |
| 0067 | CockroachDB, reranked against FoundationDB            | published      |
| 0070 | Keep options open                                     | published      |
| 0073 | A billboard gallery of the RFD 0064 dataset           | discussion     |
| 0074 | A caption label over each billboard card              | moved          |
| 0075 | GitHub OAuth login, gated on weftspun org membership  | prediscussion  |
| 0076 | usd_viewer_app, its own app, reached through a port   | prediscussion  |
| 0077 | An H2O edge, not yet a CDN                            | prediscussion  |
| 0078 | An H2O/FoundationDB game-state server                 | moved          |
| 0079 | AppSignal observability, and versitygw's removal      | published      |
| 0080 | What the three Fly deploys cost                       | published      |
| 0082 | A companion APK relays face weights past Chrome's gap | discussion     |
| 0083 | The API avatar rig export contract                    | committed      |
| 0084 | The avatar pipeline, image to downloaded VRM          | published      |
| 0085 | A code map, not a copied API reference                | published      |
| 0086 | Dev machine topology, and the Surface/DGX sync rule   | published      |
| 0087 | MindLink, a write-as-you-go memory protocol           | abandoned      |
| 0088 | HTTPS for local WebXR development                     | published      |
| 0089 | HY-World 2.0, a quality path beside the fast one      | discussion     |
| 0090 | IWSDK, a separate `/xr` lab, Galaxy XR as source of truth | abandoned  |
| 0091 | A local IWSDK fork, linked, not published             | abandoned      |
| 0092 | Kimodo backend integration                            | committed      |
| 0093 | Loot assets, fetched, never committed                 | published      |
| 0094 | Multiple photos, routed by count, not by user choice  | committed      |
| 0095 | A voice XR path, beside Task Manager, same backend    | published      |
| 0096 | OpenXR face tracking, native and web, on Android XR   | discussion     |
| 0098 | Two deploy modes, one build that fails on a secret leak | published    |
| 0099 | One cheat sheet, every operator command                | published      |
| 0100 | Publishing to the Open Metaverse Browser's spatial fabric | abandoned  |
| 0101 | Two SSH hosts only, `DGX-Local` and `DGX-Remote`      | abandoned      |
| 0102 | The supported 3DAIGC task catalog, one live source    | published      |
| 0103 | Loot assets from a CDN, not a full clone, on Vercel   | published      |
| 0104 | Uploaded VRM, rotate the scene root, never the hips   | committed      |
| 0105 | Webcam avatar control, off during WebXR               | published      |
| 0106 | The open/proprietary boundary, in public words        | published      |
| 0107 | The world package format, splats plus optional props  | published      |
| 0108 | Floor-anchor in both AR and VR, opaque sky only in VR | committed      |
| 0109 | Payment rails and the phygital registry, not the moat | abandoned      |
| 0110 | RepoResident, a file-based operating harness          | committed      |
| 0111 | The 3DAIGC-API reference, not restated here           | committed      |
| 0112 | The Cursor rules, kept in the open                    | discussion     |
| 0113 | Image preview stays 250px, expand modal stays separate | committed      |
| 0114 | App chrome layout invariants                          | committed      |
| 0115 | VRM animation playback, one mixer, normalized bones   | committed      |
| 0116 | Tasks panel, Clear unloads the model                  | committed      |
| 0117 | Text-to-image chains into Image-to-3D                 | committed      |
| 0118 | XR embody, view toggle, and Move stay input           | committed      |
| 0119 | Target hardware stays generic                          | discussion     |
| 0120 | Split apps/ into their own repos                       | committed      |

## DRY policy

The repository keeps one source of truth for each design.

- The README describes the feature surface.
- The docs/ tree holds the detailed designs and roadmaps.
- The src/ tree implements the behavior.
- This directory records the durable decisions only.

An RFD points to the source. It does not copy the source.
An RFD that restates a document will drift. It must instead link the
document. When a design changes, update the source first. Then update
the RFD to point at the new source.

## STE policy

Each RFD uses ASD-STE100 Simplified Technical English. The rules:

- One sentence per instruction.
- Keep sentences under 25 words.
- Use active voice.
- Do not use marketing adjectives.
- Do not use phrasal verbs.
- Do not use semicolons or em dashes in prose.
- Name one thing by one name.

The repository enforces this with the `simplified-technical-english`
Claude Code plugin (`fire/claude-ste-plugin`), not a repo-local
script. Its `Stop` hook lints each reply as it is written and asks
for a rewrite on a violation. RFD 0063 records the move and why no
CI step or pre-commit hook duplicates it.
