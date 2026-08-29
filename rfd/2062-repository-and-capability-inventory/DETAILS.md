## Context and problem statement

The landing page used to carry the full repository list, a
capability-to-branch table, and a prose description of the deployment
target. Those facts already have homes — each capability rides a
decision and an engine branch, the deployment target is a decision,
the two-org split is a decision — so the landing page was a second
copy that drifted every time one of those decisions changed. This
record is the one place that owns the org-wide inventory; the landing
page links here instead of restating it, and decided facts
(deployment, org split, per-capability status) stay in their own
decisions.

The narrower vertical-slice repository map
(`rfd/2057-vertical-slice-repository-map`) indexes only the
loot-action slice; this inventory is the full
[`v-sekai-multiplayer-fabric`](https://github.com/v-sekai-multiplayer-fabric)
org plus the repos still on
[`V-Sekai-fire`](https://github.com/V-Sekai-fire).

## Decision outcome

This page is the canonical inventory. Each capability maps to the
engine feature branch in
[fabric-godot-core](https://github.com/v-sekai-multiplayer-fabric/fabric-godot-core)
that implements it; the Tier column follows the feature classification
(`rfd/2018-feature-classification-poc-baseline-stretch`).

Names here are the current names, per `rfd/2064-kebab-case-repos-snake-case-local-checkouts`.
GitHub keeps a redirect after a rename, so an older name in an earlier
record still resolves; `rfd/0105`'s `DETAILS.md` maps the old names to
these.

### Counts

| Set                                   | Count |
| ------------------------------------- | ----- |
| Repos in `v-sekai-multiplayer-fabric` | 75    |
| Active                                | 51    |
| Archived                              | 24    |

### Capabilities and where they live

| Capability                                                                            | Tier             | Engine branch                                                                        | Supporting repos                                                                                                                                                                   | Status                                                                                |
| ------------------------------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Native video playback                                                                 | Baseline         | `feat/native-media` (MediaFoundation, GStreamer)                                     | [native-media-test](https://github.com/v-sekai-multiplayer-fabric/native-media-test); `vulkan-video-godot` is archived by `rfd/0105`                                               | Working; builds on Windows and Linux.                                                 |
| Networking transport (WebTransport / HTTP/3, `rfd/2023-webtransport-http3-transport`) | Baseline         | `feat/module-http3` (picoquic + web/wasm backends)                                   | [lean-http3-queue](https://github.com/v-sekai-multiplayer-fabric/lean-http3-queue); the server side moves to `zone-server-h2o` per `rfd/0083`                                      | Working; `WebTransportPeer`/`QUICClient`/`QUICServer`, demos, Lean termination proof. |
| Scene baking via OpenUSD                                                              | Baseline         | —                                                                                    | [zone-baker](https://github.com/v-sekai-multiplayer-fabric/zone-baker), [idtx-flow](https://github.com/v-sekai-multiplayer-fabric/idtx-flow); `openusd-fabric` is archived         | Working; USD schema, Blender export hooks, scene validation, headless export.         |
| Spatial audio (HRTF + audio probes, `rfd/2022-spatial-audio-patched-resonance-audio`) | Baseline         | `feat/spatial-audio-server`, `feat/module-resonance-audio` (patched Resonance Audio) | [sponza-godot-audio](https://github.com/v-sekai-multiplayer-fabric/sponza-godot-audio)                                                                                             | Working; demo and benchmark scene.                                                    |
| Speech                                                                                | Baseline         | `feat/module-speech`                                                                 | —                                                                                                                                                                                  | Working.                                                                              |
| Pen stroke creation (codename cassie)                                                 | Proof of concept | `feat/module-cassie`                                                                 | [vsekai-materialx](https://github.com/v-sekai-multiplayer-fabric/vsekai-materialx), [materialx-shaders-lean](https://github.com/v-sekai-multiplayer-fabric/materialx-shaders-lean) | Pen stroke creation is solid; patch surface creation is buggy (loses about 90%).      |
| Multiplayer presence (tracker orbs)                                                   | Proof of concept | `feat/module-xr-grid`                                                                | [xr-grid](https://github.com/v-sekai-multiplayer-fabric/xr-grid)                                                                                                                   | Proposed; head and hand pose orbs sent over low-level WebTransport.                   |

### Repositories — `v-sekai-multiplayer-fabric`

#### Engine and client

| Repo                                                                                                             | Purpose                                                                                             |
| ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [fabric-godot-core](https://github.com/v-sekai-multiplayer-fabric/fabric-godot-core)                             | V-Sekai fork of the Godot engine, one `feat/*` branch per topic, on the frozen base of `rfd/0020`.  |
| [fabric-godot-assembly](https://github.com/v-sekai-multiplayer-fabric/fabric-godot-assembly)                     | `gitassembly` recipe and driver that composes the engine from its feature branches, per `rfd/0019`. |
| [godot-images](https://github.com/v-sekai-multiplayer-fabric/godot-images)                                       | Engine builds: editor (baker) and `template_release`. Publishes to GHCR.                            |
| [zone-client-godot](https://github.com/v-sekai-multiplayer-fabric/zone-client-godot)                             | Godot web and WASM client build for the zone host.                                                  |
| [zone-baker](https://github.com/v-sekai-multiplayer-fabric/zone-baker)                                           | Minimal headless Godot project that validates and exports VSK assets.                               |
| [godot-sandbox-gdscript-compiler](https://github.com/v-sekai-multiplayer-fabric/godot-sandbox-gdscript-compiler) | GDScript-to-sandbox compiler for the engine's `module_sandbox`.                                     |
| [godot-sandbox-programs](https://github.com/v-sekai-multiplayer-fabric/godot-sandbox-programs)                   | RISC-V programs run inside `module_sandbox` (fork).                                                 |
| [native-media-test](https://github.com/v-sekai-multiplayer-fabric/native-media-test)                             | Godot project exercising the engine's native media backend (private).                               |

#### Transport layers

`rfd/0111` puts the input that triggers an interactor on side 1. `rfd/0123`
adds a second implementation of the WebTransport contract, so the role word
no longer identifies one repository and the language qualifies each name.

| Repo                                                                                               | Purpose                                                                                        |
| -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| [transport-gateway-c](https://github.com/v-sekai-multiplayer-fabric/transport-gateway-c)           | Control streams over picoquic. Carries player traffic. Renamed from `transport-gateway`.       |
| [transport-ingest-c](https://github.com/v-sekai-multiplayer-fabric/transport-ingest-c)             | Player input datagrams over picoquic. Carries player traffic. Renamed from `transport-ingest`. |
| [transport-gateway-python](https://github.com/v-sekai-multiplayer-fabric/transport-gateway-python) | The same control streams on `pywebtransport`, for interoperability. Carries no player traffic. |
| [transport-ingest-python](https://github.com/v-sekai-multiplayer-fabric/transport-ingest-python)   | The same datagrams on `pywebtransport`, for interoperability. Carries no player traffic.       |
| [transport-fanout](https://github.com/v-sekai-multiplayer-fabric/transport-fanout)                 | Egress: interest-filtered fan-out, driven by the zone tick rather than an arriving packet.     |
| [transport-asset](https://github.com/v-sekai-multiplayer-fabric/transport-asset)                   | Content-addressed chunks, served to whoever is allowed to ask.                                 |

The Python pair produces agreement or disagreement with the C pair rather
than traffic. `rfd/0123` has the three disagreements it found before it
carried a byte.

#### Zone host and its guests

`rfd/0094` makes the zone host the host of the minimum UGC game loop.
Guests arrive as CDN-delivered riscv64 ELFs. `rfd/0095` splits them
into two guest classes and gives each the runtime that suits it.

| Repo                                                                                       | Purpose                                                                             |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| [zone-guest-middleham](https://github.com/v-sekai-multiplayer-fabric/zone-guest-middleham) | Game-logic guest: MUD state machine and sandbox orchestrator. Loads first.          |
| [zone-guest-gyre](https://github.com/v-sekai-multiplayer-fabric/zone-guest-gyre)           | Presentation guest: the web and SlugHorn MUD client, per `rfd/0085` and `rfd/0091`. |
| [zone-guest-godot](https://github.com/v-sekai-multiplayer-fabric/zone-guest-godot)         | Godot rv64 under `rvlinux`. The stress test of the same capability table.           |
| [mujoco-riscv64](https://github.com/v-sekai-multiplayer-fabric/mujoco-riscv64)             | riscv64 Linux build of MuJoCo with libriscv host bindings.                          |

`zone-server-h2o`, the host itself, is archived on GitHub while
`rfd/0094` and `rfd/0095` carry it in scope. `rfd/0105` records that
inconsistency as open.

#### Backend, data, and observability

| Repo                                                                                                 | Purpose                                                                            |
| ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [zone-backend](https://github.com/v-sekai-multiplayer-fabric/zone-backend)                           | URO: Phoenix and Elixir backend for identity, the zone directory, and the planner. |
| [ecto_foundationdb](https://github.com/v-sekai-multiplayer-fabric/ecto_foundationdb)                 | FoundationDB adapter for Ecto (fork). The store Uro uses, per `rfd/0103`.          |
| [ecto-bench-tpcc](https://github.com/v-sekai-multiplayer-fabric/ecto-bench-tpcc)                     | TPC-C-style benchmark harness for any Ecto adapter.                                |
| [lean-duckdb](https://github.com/v-sekai-multiplayer-fabric/lean-duckdb)                             | Lean 4 and DuckDB FFI for Parquet and CSV dataset I/O.                             |
| [fabric-game-observability](https://github.com/v-sekai-multiplayer-fabric/fabric-game-observability) | VictoriaMetrics, VictoriaLogs, Tempo, and the OTEL Collector on Fly.io.            |

#### Hexagon cores

`rfd/0028` sets the core, ports, and adapters shape. `rfd/0057` makes
these the canonical proven reference, so the playable slice transcribes
them rather than importing them. A reference repo needs no recent push.

| Repo                                                                                         | Purpose                                                                                 |
| -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [loot](https://github.com/v-sekai-multiplayer-fabric/loot)                                   | Loot hexagon: Lean core plus a `lean-slang` SPIR-V kernel (`rfd/0041`).                 |
| [combat](https://github.com/v-sekai-multiplayer-fabric/combat)                               | Combat hexagon: the combo, invulnerability, and damage reducer (`rfd/0040`).            |
| [progression](https://github.com/v-sekai-multiplayer-fabric/progression)                     | Progression hexagon: profile and inventory rules, the commit valve (`rfd/0043`).        |
| [lean-loot-core](https://github.com/v-sekai-multiplayer-fabric/lean-loot-core)               | Standalone Lean 4 workspace for the loot core.                                          |
| [lean-combat-core](https://github.com/v-sekai-multiplayer-fabric/lean-combat-core)           | Standalone Lean 4 workspace for the combat core.                                        |
| [lean-progression-core](https://github.com/v-sekai-multiplayer-fabric/lean-progression-core) | Standalone Lean 4 workspace for the progression core.                                   |
| [lean-shared-core](https://github.com/v-sekai-multiplayer-fabric/lean-shared-core)           | Shared primitive types every core builds on.                                            |
| [lean-rebac-core](https://github.com/v-sekai-multiplayer-fabric/lean-rebac-core)             | ReBAC authorization core. Generates the host's `rebac.{c,h}`, per `rfd/0092`.           |
| [lean-entity-packet](https://github.com/v-sekai-multiplayer-fabric/lean-entity-packet)       | Source of truth for the 100-byte entity packet, per `rfd/0053`.                         |
| [lean-fabric-protocol](https://github.com/v-sekai-multiplayer-fabric/lean-fabric-protocol)   | Saturation, waypoint bounds, and the abyssal SLA.                                       |
| [lean-connection-fsm](https://github.com/v-sekai-multiplayer-fabric/lean-connection-fsm)     | Connection FSM soundness and the 5 s limit of `rfd/0050`.                               |
| [lean-http3-queue](https://github.com/v-sekai-multiplayer-fabric/lean-http3-queue)           | Transport concurrency: a size-honest inbound queue and a starvation-free loop.          |
| [lean-spatial-oracle](https://github.com/v-sekai-multiplayer-fabric/lean-spatial-oracle)     | Predictive spatial oracle: ghost expansion and SAH proofs, emitting `predictive_bvh.h`. |
| [lean-interest-mgmt](https://github.com/v-sekai-multiplayer-fabric/lean-interest-mgmt)       | Authority interest and solve order: who sees whom, and sequencing.                      |
| [lean-humanoid-rom](https://github.com/v-sekai-multiplayer-fabric/lean-humanoid-rom)         | Humanoid range of motion and IK constraints: Kusudama, muscle, prismatic.               |
| [swing-twist-kusudama](https://github.com/v-sekai-multiplayer-fabric/swing-twist-kusudama)   | Lean and Plausible sim of `SwingTwistIK3D` with Kusudama limits.                        |

#### Rendering, shaders, and USD

| Repo                                                                                           | Purpose                                                                                                      |
| ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [godot-toon-shaders](https://github.com/v-sekai-multiplayer-fabric/godot-toon-shaders)         | Godot toon shader ports and a shared parameter map (MToon 0.x / MToon10, planned SCSS and lilToon).          |
| [vsekai-materialx](https://github.com/v-sekai-multiplayer-fabric/vsekai-materialx)             | PBR/NPR/Slug as MaterialX nodes compiled to Slang; ThorVG-to-Slug vectorization, differentiable via SlangPy. |
| [materialx-shaders-lean](https://github.com/v-sekai-multiplayer-fabric/materialx-shaders-lean) | Lean 4 formalization of PBR, NPR, and vector shaders under MaterialX.                                        |
| [MaterialX](https://github.com/v-sekai-multiplayer-fabric/MaterialX)                           | The MaterialX material-exchange standard (fork).                                                             |
| [idtx-flow](https://github.com/v-sekai-multiplayer-fabric/idtx-flow)                           | Godot plugin importing USD via openUSD (fork).                                                               |
| [sponza-godot-audio](https://github.com/v-sekai-multiplayer-fabric/sponza-godot-audio)         | Sponza demo and audio benchmark for Godot 4.                                                                 |

#### Content flow and authoring

| Repo                                                                                                       | Purpose                                                                 |
| ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [fabric-flow-adapters](https://github.com/v-sekai-multiplayer-fabric/fabric-flow-adapters)                 | glTF-interactivity flow adapters, per `rfd/0005`.                       |
| [fabric-flow-adapters-project](https://github.com/v-sekai-multiplayer-fabric/fabric-flow-adapters-project) | Godot project that exercises the flow adapters.                         |
| [fabric-stage-runtime](https://github.com/v-sekai-multiplayer-fabric/fabric-stage-runtime)                 | Stage runtime for authored content.                                     |
| [vsekai-godot-mcp](https://github.com/v-sekai-multiplayer-fabric/vsekai-godot-mcp)                         | In-editor MCP server addon for Godot, the authoring path of `rfd/0031`. |
| [blender-mcp](https://github.com/v-sekai-multiplayer-fabric/blender-mcp)                                   | MCP server for Blender.                                                 |
| [vrm-game-project](https://github.com/v-sekai-multiplayer-fabric/vrm-game-project)                         | VRM game project (private).                                             |
| [xr-grid](https://github.com/v-sekai-multiplayer-fabric/xr-grid)                                           | VR interaction tool (fork).                                             |
| [gait-classification](https://github.com/v-sekai-multiplayer-fabric/gait-classification)                   | WEAR HAR with gait and biomechanics: a single-limb inertial pipeline.   |

#### Docs

| Repo                                                                                                   | Purpose                                                                                              |
| ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| [multiplayer-fabric-manuals](https://github.com/v-sekai-multiplayer-fabric/multiplayer-fabric-manuals) | This Quarto site.                                                                                    |
| [multiplayer-fabric-archive](https://github.com/v-sekai-multiplayer-fabric/multiplayer-fabric-archive) | Retired records: rejected and superseded MADRs, and superseded RFDs. Plain Markdown, per `rfd/0106`. |

#### Archived

Every repo below is tombstoned, not deleted. The history stays
reachable. The Basis column names the decision that retired it.

| Repo                                                                                                 | Basis                                                           |
| ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [zone-server](https://github.com/v-sekai-multiplayer-fabric/zone-server)                             | Godot zone server, replaced per `rfd/0083`.                     |
| [zone-server-h2o](https://github.com/v-sekai-multiplayer-fabric/zone-server-h2o)                     | Archive state is an open inconsistency; see `rfd/0105`.         |
| [zone-client](https://github.com/v-sekai-multiplayer-fabric/zone-client)                             | Superseded by `zone-client-godot`.                              |
| [godot-loop-slice](https://github.com/v-sekai-multiplayer-fabric/godot-loop-slice)                   | The loot-action slice, parked per `rfd/0069`.                   |
| [fabric-godot-packaging](https://github.com/v-sekai-multiplayer-fabric/fabric-godot-packaging)       | Native packaging for the parked slice.                          |
| [infra](https://github.com/v-sekai-multiplayer-fabric/infra)                                         | OpenTofu for the quadlet hosts, archived per `rfd/0089`.        |
| [zone-backend-quadlet](https://github.com/v-sekai-multiplayer-fabric/zone-backend-quadlet)           | `rfd/0089`.                                                     |
| [zone-server-quadlet](https://github.com/v-sekai-multiplayer-fabric/zone-server-quadlet)             | `rfd/0089`.                                                     |
| [zone-baker-quadlet](https://github.com/v-sekai-multiplayer-fabric/zone-baker-quadlet)               | `rfd/0089`.                                                     |
| [cockroach-crdb-quadlet](https://github.com/v-sekai-multiplayer-fabric/cockroach-crdb-quadlet)       | `rfd/0089`, and CockroachDB is dropped per `rfd/0075`.          |
| [restic-backup-quadlet](https://github.com/v-sekai-multiplayer-fabric/restic-backup-quadlet)         | `rfd/0089`.                                                     |
| [gha-runner-quadlet](https://github.com/v-sekai-multiplayer-fabric/gha-runner-quadlet)               | `rfd/0089`.                                                     |
| [sccache-cache-quadlet](https://github.com/v-sekai-multiplayer-fabric/sccache-cache-quadlet)         | `rfd/0089`.                                                     |
| [linux-base-image](https://github.com/v-sekai-multiplayer-fabric/linux-base-image)                   | Base qcow2 for the retired self-hosted VM images.               |
| [fabric-container-verify](https://github.com/v-sekai-multiplayer-fabric/fabric-container-verify)     | `rfd/0105`.                                                     |
| [fabric-casync-central](https://github.com/v-sekai-multiplayer-fabric/fabric-casync-central)         | `rfd/0105`.                                                     |
| [fabric-scoop-central](https://github.com/v-sekai-multiplayer-fabric/fabric-scoop-central)           | `rfd/0105`.                                                     |
| [fabric-platform-central](https://github.com/v-sekai-multiplayer-fabric/fabric-platform-central)     | `rfd/0105`.                                                     |
| [vulkan-video-godot](https://github.com/v-sekai-multiplayer-fabric/vulkan-video-godot)               | `rfd/0105`. Empty.                                              |
| [steamdeck](https://github.com/v-sekai-multiplayer-fabric/steamdeck)                                 | `rfd/0105`. Empty.                                              |
| [openusd-fabric](https://github.com/v-sekai-multiplayer-fabric/openusd-fabric)                       | OpenUSD pipeline across Blender, Godot, Hydra, Unity.           |
| [sandbox-gdextension-godot](https://github.com/v-sekai-multiplayer-fabric/sandbox-gdextension-godot) | Earlier GDExtension sandbox approach.                           |
| [tropes-action](https://github.com/v-sekai-multiplayer-fabric/tropes-action)                         | The tropes check now runs in-repo as `scripts/check_tropes.sh`. |
| [friends-art-game-loop](https://github.com/v-sekai-multiplayer-fabric/friends-art-game-loop)         | Local-first art-game loop experiment.                           |

### Moved to `V-Sekai-archive`

These three left this org and are archived under a third org. Links in
earlier records still resolve through the redirect.

| Repo                                                                                    | Purpose                                                      |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [lean-predictive-bvh](https://github.com/V-Sekai-archive/lean-predictive-bvh)           | Earlier Predictive BVH workspace. See `lean-spatial-oracle`. |
| [viser](https://github.com/V-Sekai-archive/viser)                                       | Web-based 3D visualization in Python (fork).                 |
| [usd-converter-for-vrchat](https://github.com/V-Sekai-archive/usd-converter-for-vrchat) | VRChat-to-VRM 1.0 converter UPM (fork).                      |

### Still on `V-Sekai-fire` (not yet migrated)

These repos remain the source of truth under the older org; see the
[two-org split decision](https://github.com/v-sekai-multiplayer-fabric/multiplayer-fabric-archive/blob/main/_archive/decisions/20260606-org-split-v-sekai-multiplayer-fabric.md),
now in `multiplayer-fabric-archive`.
Links in the decisions and changelog that point at them are correct
and still resolve.

| Repo                                                                                                       | Purpose                                                             |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| [multiplayer-fabric](https://github.com/V-Sekai-fire/multiplayer-fabric)                                   | Umbrella monorepo registering the V-Sekai-fire repos as submodules. |
| [multiplayer-fabric-gateway](https://github.com/V-Sekai-fire/multiplayer-fabric-gateway)                   | Elixir WebTransport gateway on UDP 443.                             |
| [multiplayer-fabric-zone-console](https://github.com/V-Sekai-fire/multiplayer-fabric-zone-console)         | Operator console for zone health and shard rotations.               |
| [multiplayer-fabric-webtransport](https://github.com/V-Sekai-fire/multiplayer-fabric-webtransport)         | Elixir bindings for the Rust wtransport library.                    |
| [multiplayer-fabric-taskweft](https://github.com/V-Sekai-fire/multiplayer-fabric-taskweft)                 | Re-entrant temporal HTN planner and ReBAC engine.                   |
| [multiplayer-fabric-humanoid-project](https://github.com/V-Sekai-fire/multiplayer-fabric-humanoid-project) | Humanoid avatars and animations (`mire.vrm` test avatar).           |
| [aria-storage](https://github.com/V-Sekai-fire/aria-storage)                                               | casync/desync chunked content-addressable storage.                  |
| [elixir-turboquant-llm](https://github.com/V-Sekai-fire/elixir-turboquant-llm)                             | Quantized LLM inference NIF (Elixir / llama.cpp).                   |
| [multiplayer-fabric-cycle-tests](https://github.com/V-Sekai-fire/multiplayer-fabric-cycle-tests)           | Maglev cycle smoke tests, one per cycle.                            |

## Consequences

- One page owns the inventory, so a repo or capability change lands in
  one place.
- The landing page asserts only durable orientation and links here, so
  it no longer drifts when the deployment target, org split, or a
  capability status changes.
- This inventory still needs hand maintenance; the gain is a single
  source of truth, not zero maintenance.
- The service-images section is gone. Every repo it listed is archived
  by `rfd/0089`, which supersedes `rfd/0061`'s quadlet deployment.
