# Logbook: OpenBao on FoundationDB

Question: can the FoundationDB storage backend from Vault v1.14.8 be
ported to OpenBao's current interfaces, and does bao run against the
existing weftspun-fdb cluster over 6PN.

## The apparatus

OpenBao v2.6.2 (HEAD of weftspun/openbao, branch
feat/foundationdb-storage). FDB 7.3.79 C client and Go binding at
commit 0074653ee011 (headerVersion 730). Go 1.27. Fly app
weftspun-bao, shared-cpu-1x 512 MB, sjc. The cluster is weftspun-fdb
(3 machines, double redundancy, mutual TLS per RFD 2134).

## What was done

Ported `physical/foundationdb/foundationdb.go` from Vault v1.14.8
(888 lines, MPL-2.0) to 984 lines on OpenBao. Three interface changes:
added ListPage, rewrote one-shot Transaction to interactive
BeginTx/BeginReadOnlyTx, kept HA lock unchanged.

Wired into `internal/command/commands.go` as the sixth backend
(file, inmem_ha, inmem, raft, postgresql, foundationdb).

The first deploy ran a co-located single-node fdbserver for bring-up.
After init and unseal succeeded, the target moved to the existing
cluster. The single-node entrypoint stays in git history.

## What did not go as planned

**The 2019 FDB Go binding crashes on the 7.3 C client.** The binding
at cd5c9d91fad2 has a headerVersion around 520. The 7.3 C client
refuses it with error 2203 (API version not supported). Lowering
the config's api_version had no effect: the binding sets the API
version before config is read. Fix: pin the 7.3.79 binding.

**Fly's listener bind on `0.0.0.0:8200` is IPv4-only.** The fdb
machines reach bao over 6PN (IPv6 fdaa:: addresses). curl from fdb
to bao returned connection refused until the listener moved to
`[::]:8200`.

**Fly dual-mount deploy failure.** Two `[[mounts]]` blocks (bao_data
and fdb_data) prevented machine update. Collapsed to one volume with
FDB data under `/bao/data/fdb`.

**`/usr/lib/foundationdb/fdbserver` does not exist.** The deb installs
at `/usr/sbin/fdbserver`.

## The measurement

From `fly deploy` to `OpenBao server started!`: under 50 seconds
(co-located fdbserver joins cluster at ~t+18s, database created at
~t+20s, bao listening at ~t+31s). Init produced 1 key share,
threshold 1. Unseal, enable KV v2, write two secrets from the
cluster over 6PN: all succeeded on first attempt after the dual-stack
fix.
