# RFD 2141: FDB TLS rotation without data loss

**State:** prediscussion
**Feature:** rotate the private CA and all leaf certificates on the live cluster
**Scope:** weftspun-fdb (3 machines, double), weftspun-bao (FDB client)

## Decision

A three-phase rolling rotation using FDB's automatic TLS certificate
refresh. The cluster stays available and data stays intact at every
step; each phase is gated on `fdbcli status` reporting healthy.

**Phase 1 (dual-CA trust).** Generate a new CA with the RFD 2134
profile. Set `FDB_TLS_CA_B64` to old + new CAs concatenated. Rolling
restart. Every machine trusts certs from either CA.

**Phase 2 (new leaves).** Mint new certs under the new CA for all
three machines and for bao (`fdb-bao.chibifire.com`). Replace each
machine's cert/key secrets. Rolling restart.

**Phase 3 (drop old CA).** Set `FDB_TLS_CA_B64` to the new CA only.
Rolling restart. Store the new CA key in bao and in 1Password.

The cluster file does not change (addresses keep `:tls`), so no
coordinator reset is needed.

The rotation tool is an Elixir TUI in weft-warp-burrito, packaged
via Burrito. It walks the phases, gates each on cluster health, and
stores the CA key on completion. The procedure is in DETAILS.md.

## Problem

The CA private key from RFD 2134 is not recoverable, so no new leaf
can be issued. bao needs a client cert, and the machine certs expire
in two years. RFD 2134's reset path wipes data, which was acceptable
at initial setup and is not acceptable now.

## Related

RFD 2134 (initial TLS), RFD 2140 (OpenBao on FDB).
