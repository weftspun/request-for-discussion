## Why the native tier is not affordable

The cost is not the machine. `rfd/0102` costed the deployment at 15 USD
with the native server in it.

The cost is the tier. `zone-server-h2o` adds C to a project that
already runs Elixir, CockroachDB, and Godot. C brings its own
toolchain, its own memory-safety burden, its own vendored
`thirdparty/` tree, and its own class of bug. `rfd/0095` shows where
that leads. Seventeen syscall handlers, an invented POSIX layer over a
key-value store, and a list of next failures with no end.

One person cannot carry four runtimes. The decision buys back a
runtime and pays for it in throughput.

## What carries over

The design records that describe the protocol, the state, and the game
survive the host change. They are not about libh2o.

| Record                                             | Why it survives                                                              |
| -------------------------------------------------- | ---------------------------------------------------------------------------- |
| `rfd/0046` server authority with deferred rollback | The authority model any zone server implements.                              |
| `rfd/0049` fabric channels as reliability classes  | Wire protocol, independent of what serves it.                                |
| `rfd/0050` five-second transaction limit           | Bounded operations, proven in `lean-connection-fsm`.                         |
| `rfd/0053` integral entity-transform wire          | Generated from `lean-entity-packet`.                                         |
| `rfd/0008`, `rfd/0023` WebTransport over HTTP/3    | The transport choice. Elixir speaks it.                                      |
| The hexagon cores and their Lean workspaces        | `rfd/0044` puts Lean at build time behind flat C, which an Elixir NIF calls. |

## What does not carry over

Every record scoped to the internals of the native host retires. The
work was real and the measurements were real. Neither transfers to a
BEAM process.

- The libh2o event loop and its callback discipline.
- The FoundationDB C API path, its value encoding, and its compression.
- `libriscv` as the guest engine, and the guest ABI built on it.
- eBPF and XDP in the request path.
- CBMC as a verification layer, which needs C to check.

`rfd/0117` lists all 43 retired records.

## The Gyre keeps its setting, not its host

`rfd/0085`, `rfd/0091`, and `rfd/0094` stay live. Each one names
`zone-server-h2o` as the host. Each carries an amendment naming this
record instead.

The Gyre is a MUD setting and a web client. Neither needs a native
host. `rfd/0094`'s UGC loop stays as an intent, and its libriscv
mechanism does not.

## What this record does not settle

The throughput of the Elixir server is not measured. Every number in
`data/measurements/` came off the native tier and a FoundationDB
probe. A record that states the new tier's ceiling needs a new
measurement, not an extrapolation from the old one.

`ecto_foundationdb` and `ecto-bench-tpcc` are active repositories that
exist to put Uro on FoundationDB. This decision removes their reason.
Their repository state is open.

## Related

- `rfd/2006-cockroachdb-with-mtls-role-separation`: the database this
  tier returns to.
- `rfd/2046-server-authoritative-simulation-deferred-rollback`: the
  authority model the new server implements.
- `rfd/2117-retire-the-h2o-tier-record-set`: retires the records that
  described the native tier.
