# RFD 2216: Three.js blocklist

**State:** discussion
**Flight level:** L2 (coordination — closes a runtime fork)
**Feature:** three.js goes on the CLAUDE.md / BLOCKLIST.md blocklist
as an in-browser 3D runtime
**Scope:** `CLAUDE.md`, `BLOCKLIST.md`, cascade of retirements in
consumer files

## Decision

Blocklist three.js as an in-browser 3D runtime. Substitute is
**Godot as a native binary** (see [RFD 2210](../2210-atelier-godot-web-shipping-surface/)
+ [RFD 2211](../2211-base-tree-entities-godot-sandbox/) +
[RFD 2228](../2228-webgpu-native-drop-platform-web/)). Three.js
itself is MIT-licensed — the objection is not licence, it is
runtime story: the workspace ships every other 3D surface via
Godot, and a three.js path forks the scene-graph, material pipeline,
animation graph, and lighting model.

**Amendment 2026-09-05:** the earlier substitute wording named
Godot `platform=web` (Emscripten export). RFD 2228 flipped the
delivery surface to native binaries with Godot's WebGPU renderer
via Dawn/wgpu-native; the substitute is now the native binary,
not the browser export. The three.js blocklist rationale is
unchanged — the workspace ships one 3D runtime, and three.js is
still the second one it declines to ship.

## CLAUDE.md table row

    | **Three.js** as an in-browser 3D runtime                                   | JS/npm-runtime lock-in on a stack we don't fully control; the same scene ships from `entities-godot-sandbox` via `scons platform=web`; RFD 1170 already picks Godot over three.js — see below |

## BLOCKLIST.md section

    ### Three.js is blocklisted as an in-browser 3D runtime, and Godot `platform=web` is why

    Three.js itself is MIT-licensed — the objection is not licence, it
    is runtime story. The workspace ships ANNY through Godot on desktop
    and Android; a three.js path forks that story: a second scene-graph
    the avatar has to be re-authored into, a second material pipeline,
    a second animation graph, a second lighting model. Each fork is a
    place the two runtimes render the same scene differently, and each
    difference is a bug nothing reports.

    The substitute costs nothing to adopt because it already ships.
    Godot 4's `platform=web` export produces `godot.web.*.wasm` +
    `godot.web.*.js` from the same source tree that produces the
    desktop build, and the same `.tscn` / `.tres` assets load in both.
    `3-interactor/entities-godot-sandbox` is the canonical checkout
    (see RFD 2211 for the tree-choice reason). Godot's own MToon
    support and its glTF/VRM importers (via godot-vrm as a
    godot-sandbox ELF per RFD 2213) cover the three-vrm role.

    **Why this row exists now.** RFD 1170 already picks Godot over
    three.js. RFD 2210 reverses the April-2026 "Godot web dropped"
    decision for the atelier workload and puts the marketing video
    renderer (RFD 2215 Head B) and the game-loop control surface
    (RFD 2215 Head A) on one hat, and that hat is Godot `platform=web`.
    Naming three.js in a shipping demo would re-fork the runtime
    story this workspace deliberately holds to one.

    **What this costs, stated rather than discovered.**

    - `7-service/service-sqlar-cas/docs/{vrm.js,index.html}` renders
      the Starforged VRM portrait per RFD 2206; the demo moves to
      Godot `platform=web` or retires.
    - `3-interactor/motion-bricks-cpp/demo/web/app.js` renders
      motion-bricks previews; moves to Godot or retires.
    - `1-transport/usd-viewer/src/render-delegate.ts` targets THREE
      — this render delegate is gone with this entry; USD viewing
      routes through Godot's own USD importer.
    - `6-datasource/anny-render-corpus/mtoon-reference/` compared
      our MToon shades against three-vrm; comparison target moves
      to a Godot MToon renderer or retires.

    **The substitute we already own.** Godot 4.7-beta from
    `3-interactor/entities-godot-sandbox` exports to WebAssembly with
    the Godot runtime and the same `.tscn` / `.tres` assets the
    desktop build reads. RFD 2210 is the canonical form of this
    substitution for the atelier surface.

    **Carve-outs.**
    - **Vendored upstream demos are exempt.**
      `3-interactor/moge-upstream/moge/utils/gradio_3d_viewer/`,
      `3-interactor/taskweft/thirdparty/gltf/extensions/.../examples/`,
      `3-interactor/physics/thirdparty/mujoco/wasm/`, and
      `3-interactor/mujoco-mjx/wasm/` carry three.js as part of an
      upstream we track by pin; touching them is upstream's decision.
    - **A third-party viewer we do not ship is exempt.** Reading
      someone else's three.js viewer to check a glTF export is not a
      shipped artefact.

    **What the row does not cover.** It does not ban WebGL or WebGPU
    as such — Godot `platform=web` uses WebGL2 under the hood, and
    WebGPU is blocklisted separately per the standing 2026-09-05
    operator directive. This row bans the three.js runtime and the
    `@pixiv/three-vrm` plugin as our chosen renderer.

    RFDs 1022, 1023, 1073, 1149, 1170, 2206, 2161 name three.js as
    example or dependency; those are doctrine references and stay as
    records of what the choice used to be.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3
  strategic bet.
- [RFD 2215](../2215-one-binary-two-heads/) — the "one runtime, not
  two" argument that also drives this blocklist.
- RFD 1170 (cleanroom presence loop) — earlier RFD that picks Godot
  over three.js for a different workload.

This RFD was drafted by an AI and read by a human before it shipped.
