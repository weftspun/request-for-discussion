# RFD 1018 details: background, plan, risk, references

## Background

The site config still names the M3 origin. The rebrand changed only
the title, so the config now claims the Weftspun name over the M3
identity.

The API reference under `Developers` copies the source. RFD 1000
forbids a copy of the source. The reference has also drifted. The
animation manager source holds 47 methods, and the document lists
26 and misses the viewport and XR work.

## Plan

The work follows this order:

1. Delete the template blog and the template page.
2. Delete the `Developers` reference. Add the code map.
3. Rewrite the `Modders` manifest guides. Delete the originals.
4. Rewrite the `General` guides and the quickstart.
5. Rewrite the history page as a short lineage note.
6. Delete the site config, the sidebars, and the package files.
7. Delete `docs/LICENSE`.

Steps 1, 2, 4, and 5 are complete. Steps 3, 6, and 7 remain open.

## Risk

The image folder holds 29 MB. The history page uses many of those
images. A rewrite of the history page must drop the unused images.

The GitHub Pages workflow named an M3 host. The workflow now runs as
a check only. It builds the app and runs the animation tests. It no
longer publishes to any host. RFD 1013 keeps Vercel as the deploy
path for the public demo.

## Static assets

`m3/static/img/` holds 40 files. Ten markdown files under `m3/docs/`
name 37 of them, under `/img/`. Three go unnamed anywhere in the
repository: `charstudio.jpg`, `overview-app.jpg`,
`overview-schema.jpg`. Delete those three now. Delete each remaining
image only when the guide rewrite that named it either drops the
image or moves to a source the reader can reach on their own.

## Misc top-level guides, beyond the original plan

The original plan named the `Modders` and `General` guides, the
quickstart, and the history page. `m3/docs/` also held nine other
top-level guides the plan did not name. Four left the tree mid-session,
outside this RFD's own work: `E2E_DGX_DEVTOOLS.md`,
`IWSDK_OPTION_A_MIGRATION_BLUEPRINT.md`, `MCP_SETUP.md`,
`quickstart.md`.

Six more are deleted now, each superseded rather than rewritten, and
none linked from any `README.md`:

| File                                     | Why deletion, not a rewrite                                                                            |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `WALLET_OWNED_ASSETS_AVATAR_APPROACH.md` | Wallet, minting, and Thirdweb; RFD 1012 abandons this line of work                                     |
| `THIRDWEB_BENEFITS_AND_UI.md`            | Same abandoned line, RFD 1012                                                                          |
| `QUICK_RECONNECT_STEPS.md`               | Manual ADB reconnect steps; `scripts/reconnect-galaxy-xr-debug.ps1` automates this now, per RFD 1099   |
| `SIMPLE_ADB_CONNECT_GUIDE.md`            | Same script supersedes this Cursor-IDE clickthrough                                                    |
| `WIRELESS_ADB_SETUP.md`                  | Same script supersedes this guide                                                                      |
| `SceneControlsIntegration.md`            | Documents merging `SceneControlsBackup.jsx`, a file that no longer exists; the merge already completed |

The remaining four are resolved too, none rewritten:

| File                                  | Disposition                                                                                                                                                                                                            |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `THREEJS_QUICK_START.md`              | Deleted. `getRendererInfo()`, `setupPostProcessing()`, and `createPositionalAudio()` do not exist in `sceneManager.js`; a build that never shipped, or shipped then shrank                                             |
| `THREEJS_WEBGPU_WEBXR_MIGRATION.md`   | Deleted. Same drift; RFD 1009 dropped its own reference to this file and gained a `DETAILS.md` with the real renderer fallback chain instead                                                                           |
| `FACE_EXPRESSION_TUNING_REFERENCE.md` | Deleted from this repo only. The live copy is the app's own `docs/FACE_EXPRESSION_TUNING_REFERENCE.md`, named directly in `xrExpressionTrackingDriver.js`'s header; a copy here would drift. RFD 1096 points to it now |
| `model-format-specification.md`       | Deleted. Confused "Open3DStudio (Weftspun3DStudio)" bridge framing for what RFD 1102 shows is one codebase under its old and new name; the real, current export fields moved into RFD 1005's `DETAILS.md`              |

## history.md's dropped Roadmap section

The pre-rewrite `history.md` carried a "Roadmap" section mixed into
the history page: real, current content (WebXR, Kimodo, moeChat and
AIRI, with working RFD links), beside two abandoned wallet items
("Connect wallet to load profiles or mint files," an external
Solana/Arweave launchpad) RFD 1012 already abandons, and a closing
link to `MONETIZATION_ROADMAP.md`, a file `weftspun-moat-protected.mdc`
names as never committed. That link pointed at a file this public
repository does not, and should not, hold. The rewrite drops the
whole Roadmap section; a history page states lineage, not a live
roadmap, and RFD 1106 already gives the public-safe open/proprietary
split this section partly restated.

## References

- M3 notice: `m3/LICENSE`
- Site config: `m3/docs/docusaurus.config.js` (if still present)
- Code map: `m3/docs/CODE_MAP.md` (to add)
- DRY policy: RFD 1000
- Attribution: `README.md`, section Third-Party Trademarks
