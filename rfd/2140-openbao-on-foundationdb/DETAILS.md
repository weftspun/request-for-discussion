# RFD 2140 details: the interface port and the deploy

## The three interface changes

OpenBao's `physical.Backend` diverged from Vault's after v1.14.x.
The port rewrites three sites.

**ListPage.** Vault's `List(prefix)` returned all keys. OpenBao added
`ListPage(ctx, prefix, after, limit)` to the interface. The FDB
implementation uses a range query with `after` as a begin-selector
offset and `limit` as the range option.

**Interactive transactions.** Vault used a one-shot
`Transaction([]*TxnEntry)`. OpenBao replaced it with `BeginTx` and
`BeginReadOnlyTx`, each returning a `physical.Transaction` carrying
Put/Get/Delete/List/ListPage/Commit/Rollback. The FDB port calls
`db.CreateTransaction()` and wraps the result in a struct that tracks
committed/readonly state and returns the canonical error sentinels
(`ErrTransactionReadOnly`, `ErrTransactionAlreadyCommitted`,
`ErrTransactionCommitFailure`). PostgreSQL's `transaction.go` was the
reference for the shape.

**Backend registry.** `internal/command/commands.go` gains one import
and one map entry (`"foundationdb": physFDB.NewFDBBackend`), wired the
same way file, inmem, raft, and postgresql are.

## The binding version

The FDB Go binding hardcodes a `headerVersion` that must match or
exceed the C client's API version. The 2019 binding
(`cd5c9d91fad2`, headerVersion around 520) crashed at startup with
error 2203 against the FDB 7.3 C client. The 7.3.79 binding
(`0074653ee011`, `headerVersion := 730`) resolved it. The Go pseudo-
version is `v0.0.0-20260715201227-0074653ee011`.

## The deploy

Fly app `weftspun-bao`, region sjc, `shared-cpu-1x`, 512 MB.
Dockerfile.fdb is a two-stage build: Go 1.27 on bookworm compiles
with the `foundationdb` build tag and CGO, then a slim runtime image
installs the FDB client library deb (not the server).

The bao machine connects to the existing weftspun-fdb cluster (3
machines, double redundancy, mutual TLS per RFD 2134) over Fly 6PN.
It presents its own TLS client certificate (`fdb-bao.chibifire.com`)
and verifies the cluster with the same rule the cluster uses.

Listener binds `[::]:8200` (dual-stack) so the machine is reachable
over 6PN from other apps in the org.

Storage: `auto_stop_machines = "suspend"`, `min_machines_running = 1`.

## What the co-located fdbserver was, and why it moved

The first deploy ran a single-node fdbserver inside the bao machine
on the same volume. That worked for initialization but carried no
redundancy, no backup, and no TLS. Moving to the cluster gives all
three for free. The co-located entrypoint and the single-node config
are kept in the repository's git history.

## What the anchor creds cover

Two KV v2 paths carry the FDB cluster's identity material:

`secret/fdb/tls-anchor` — the CA certificate (base64 PEM), the
cluster ID, and the verify-peers rule.

`secret/fdb/blobstore` — the Tigris S3 credentials used by the FDB
backup agents (AWS key pair, endpoint, region, bucket name).

Both were written from a weftspun-fdb machine over 6PN, where the
Fly secrets are available as environment variables.
