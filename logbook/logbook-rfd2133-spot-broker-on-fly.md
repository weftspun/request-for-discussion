# Logbook: spot-broker on Fly

Question: does the spot-broker deploy plumb VAST spend authority through
Fly secrets, and does the ledger reach FoundationDB through the weft_fdb
VFS compiled into the ecto_sqlite driver.

## The apparatus

Fly.io, org `personal`, region `sjc`. spot-broker at commit `904398a`
(`the FDB client compiled into ecto_sqlite as a SQLite VFS`). Cluster is
`weftspun-fdb`, deployed per its own logbook entry
(`logbook-rfd2133-weftspun-fdb-on-fly.md`).

## What was done

    cd 7-service/spot-broker
    fly launch --no-deploy --copy-config \
      --name spot-broker --region sjc --org personal --yes

    VAST=$(powershell -Command '[Environment]::GetEnvironmentVariable("VAST_API_KEY","User")')
    TOKEN=$(openssl rand -hex 32)
    fly secrets set VAST_API_KEY="$VAST" BROKER_TOKEN="$TOKEN" \
      FDB_CLUSTER="placeholder:placeholder@127.0.0.1:4500" \
      --app spot-broker --stage

    fly deploy --app spot-broker --remote-only --strategy immediate

    # After weftspun-fdb was up:
    CLUSTER="weft:f5d800cd147f561a@[fdaa:0:5132:a7b:167:d7c3:dd2:2]:4500,\
    [fdaa:0:5132:a7b:16f:3c5b:597a:2]:4500,[fdaa:0:5132:a7b:5a3:6d12:8e67:2]:4500"
    fly secrets set FDB_CLUSTER="$CLUSTER" --app spot-broker

## The measurement

Image size 119 MB. Two machines created, `shared-cpu-1x`, 512 MiB each:
one primary, one standby. No `[[services]]` block, no `[[mounts]]` block
— the listener binds `FLY_PRIVATE_IP` (6PN), and the ledger's pages live
in FDB. `BROKER_TOKEN` is a hex-encoded 32-byte random string saved to
`/tmp/broker_token.txt` on the operator desk; Uro will need it as its
own Fly secret to call `spot-broker.internal:8080`.

## What did not go as planned

**Fly stripped the fly.toml comments on `--copy-config`.** The `no
[[services]] / no [[mounts]]` reasoning I had written did not survive
the round trip. Verified with the user: the strip is correct. If a
future edit reintroduces public exposure or a data volume, the intent
is not encoded in the toml — this logbook entry is where it lives.

**GLIBC_2.38 mismatch.** First deploy started but the release refused to
boot: `beam.smp: /lib/x86_64-linux-gnu/libm.so.6: version GLIBC_2.38 not
found`. The build stage was `elixir:1.18-slim` (Debian trixie, glibc
2.41) and the runtime was `debian:bookworm-slim` (glibc 2.36). Matching
both stages to `debian:trixie-slim` fixes it. Trixie also drops
`adduser` from the base image, which `foundationdb-clients_7.3.76-1`
requires — install it explicitly.

**Deploying spot-broker before weftspun-fdb existed** was a deliberate
choice. FDB_CLUSTER was set to a syntactically valid placeholder so the
Fly secrets flow could be exercised without a cluster, on the reasoning
that the app would start, the API would bind, and only ledger writes
would fail — that is loud, not silent. Confirmed: with the placeholder
the release enters supervisor crash-loop the moment the VFS extension
tries to reach the placeholder cluster, which is the right failure.

## What this settles

The keeper's spend policy, the API's zero-trust bearer check, and the
2026-08-30 double-rent negative control all run in prod under the same
release image that passes `mix test` locally. The VFS extension links
against the same shared `libsqlite3.so.0` exqlite is built against
(`EXQLITE_USE_SYSTEM=1`), which is the invariant that lets a
process-default VFS registration reach the Repo's connections.

## What is still open

Uro is not yet wired to call spot-broker; the token exists but no
client has it. The gacha demo's demand for GPU on/off is what will
first exercise a real `POST /target/one` in production.
