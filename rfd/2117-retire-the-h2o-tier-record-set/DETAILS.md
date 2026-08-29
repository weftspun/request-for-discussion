## Counts

| Set                               | Count |
| --------------------------------- | ----- |
| RFDs before this decision         | 105   |
| Retired to the archive            | 43    |
| Live after this decision          | 62    |
| Live, plus `rfd/0116`, `rfd/0117` | 64    |

## The native zone tier, 12 records

| RFD    | Subject                                     |
| ------ | ------------------------------------------- |
| `0001` | Zonefabric roadmap and PERT order           |
| `0003` | CastSpell sandbox package format            |
| `0004` | CastSpell embeds libgodot                   |
| `0010` | Client transport handshake, gateway cycle 1 |
| `0072` | Actor-lite worker pool                      |
| `0076` | Macaroon with eBPF and XDP                  |
| `0077` | PERT critical path                          |
| `0078` | plausible-witness-dag feature ablation      |
| `0080` | Slotmap entity storage                      |
| `0082` | Zonefabric scaling benchmark                |
| `0083` | Replace FabricZone with zone-server-h2o     |
| `0086` | Defer NoGod.lean gossip authority           |
| `0088` | picoquic and picotls over h2o's own QUIC    |

## FoundationDB, 7 records

CockroachDB replaces it, so `rfd/0006` returns to force.

| RFD    | Subject                                     |
| ------ | ------------------------------------------- |
| `0002` | taskweft value narrowing in FDB encoding    |
| `0073` | Async FDB callback chain on the libh2o loop |
| `0074` | Binary value encoding for FDB values        |
| `0075` | FoundationDB over CockroachDB               |
| `0084` | zstd compression for batched FDB values     |
| `0097` | Pubsub in userspace, FDB keeps the log      |
| `0103` | Uro on ecto_foundationdb                    |

## The libriscv guest runtime, 5 records

The Gyre survives. Its runtime does not.

| RFD    | Subject                                     |
| ------ | ------------------------------------------- |
| `0037` | Generated behavior as sandboxed RISC-V      |
| `0079` | Sandboxed Godot via raw libriscv            |
| `0092` | ReBAC gates libriscv guest access           |
| `0095` | Two guest classes, a domain ABI, Bubblewrap |
| `0096` | Guest transport on Fly, measured            |

## Measurements taken on the retired tier, 5 records

Each number was measured against libh2o and FoundationDB. The
measurement stands as history. It guides nothing on the new tier.

| RFD    | Subject                            |
| ------ | ---------------------------------- |
| `0098` | The rollback snapshot budget       |
| `0100` | 256 kbps per client, 47 concurrent |
| `0101` | zstd delta on the wire             |
| `0102` | The whole deployment on 15 USD     |
| `0104` | Hypothesis, 1000 concurrent users  |

## Records whose subject is an archived repository, 8 records

| RFD    | Subject                                   | Archived repository       |
| ------ | ----------------------------------------- | ------------------------- |
| `0014` | Recursive art-game loop, prediscussion    | `friends-art-game-loop`   |
| `0027` | Umbrella package installs every component | `fabric-platform-central` |
| `0047` | webtransportd out-of-process adapter      | no such repository exists |
| `0056` | Verification smokes as a quadlet queue    | `fabric-container-verify` |
| `0057` | Repository map of the loot-action slice   | `godot-loop-slice`        |
| `0058` | WebTransport on one persistent stream     | follows `rfd/0047`        |
| `0065` | fabric-platform-central packaging         | `fabric-platform-central` |
| `0069` | Defer the loot-slice hardening scope      | `godot-loop-slice`        |
| `0070` | Loop-slice telemetry to the collector     | `godot-loop-slice`        |
| `0081` | Three-layer verification with CBMC        | `zone-server-h2o`         |
| `0087` | Avatar IK with Align.lean over mink       | `zone-server-h2o`         |
| `0093` | taskweft relations to linear automata     | `zone-server-h2o` ReBAC   |

## The four that stay, and why

YAGNI keeps a record when a live consumer needs it now.

- `rfd/0005` glTF interactivity value types. `datasource-flow`
  and `datasource-flow-project` are live repositories, and this
  record describes their taxonomy.
- `rfd/0007` Godot double-precision `template_release`. The scope names
  an archived repository, and `zone-client-godot`, `zone-baker`, and
  `rfd/0031`'s merged authoring build all need double precision.
- `rfd/0045` Loot-action core-loop MVP. The record of what the game
  loop is. `rfd/0085`'s Gyre sits on this shell.
- `rfd/0067` Release tag progression. The scope names an archived
  repository, and `rfd/0090`'s live Burrito release of `uro` uses the
  convention.

## Inbound citations

53 citations in surviving files name a retired record. 16 name a full
path and become links into the archive. The rest name a bare number and
stay as citations, which follows `rfd/0106`.

`data/measurements/README.md` opens with "Measurements: rfd/0096
through rfd/0103". Both records are retired. The parquet files stay in
the manuals repository, and whether the measurement data follows its
records into the archive is open.

## Related

- `rfd/2071-yagni-times-structure-to-need`: the rule this applies.
- `rfd/2106-split-the-archive-into-its-own-repo`: the method and the
  destination.
