# Details: the certificate profile, the proof, and the procedure

## The failure this profile exists for

With certificates from a bare `openssl req -x509` CA and extension-less
`openssl x509 -req` leaves, every fdbserver logged, on each handshake:

    Type="TLSPolicyFailure" Reason="preverification failed"
    VerifyError="invalid CA certificate"

and `status` reported the cluster's coordinators unreachable, the same
line a network fault produces. Read the trace event, not the status
line.

## The profile

The 10-year CA and 2-year leaf numbers below were retracted by
RFD 2145 on 2026-09-01. The current guidance is 25-year `notAfter` on
the offline root with 5-year policy rotation, 3-year intermediates, and
90-day service leaves; see RFD 2145 and its `references/` for the CFF
citations. The lines are kept in place so a reader working from an
older linked reference can see what the values used to say and what
they moved to.

CA (`fdb-ca.chibifire.com`, 4096-bit RSA, 10 years):

    basicConstraints = critical, CA:true
    keyUsage         = critical, keyCertSign, cRLSign
    subjectKeyIdentifier = hash

Leaf (2048-bit RSA, 2 years), one per machine and one per client
service:

    basicConstraints = CA:false
    keyUsage         = critical, digitalSignature, keyEncipherment
    extendedKeyUsage = serverAuth, clientAuth
    subjectKeyIdentifier   = hash
    authorityKeyIdentifier = keyid, issuer

Subjects: `fdb-<fly machine id>.chibifire.com` for cluster machines,
`fdb-<service>.chibifire.com` for clients
(`fdb-spot-broker.chibifire.com`). The machine ID survives
`fly machine update`, which the entrypoint records a NIC-named scheme
failing. All pass the one verify rule:
`Check.Valid=1,S.CN>=fdb-,S.CN<=.chibifire.com`.

## The proof, run before the push

One `foundationdb/foundationdb:7.3.63` container, one fdbserver on
`127.0.0.1:4500:tls`, the cluster's verify rule on both ends:

| certificates | result |
| --- | --- |
| v3 profile above | handshake clean, `configure new single memory` creates the database, 0 TLSPolicyFailure |
| extension-less (what production had) | `The database is unavailable`: the production symptom, reproduced |

The negative control is the point: the same server, rule, and commands
separate the two cert sets, so the diagnosis is the extensions and not
the rule, the addresses, or Fly.

## The procedure on a live plaintext cluster

1. Certificates as above; base64 each PEM (`base64 -w0`).
2. `fly secrets set` on weftspun-fdb: `FDB_TLS_CA_B64`, and per machine
   `FDB_TLS_CERT_<machine id>_B64` / `FDB_TLS_KEY_<machine id>_B64`.
   The entrypoint takes the pair addressed to the machine and refuses
   to borrow another's.
3. The cluster will NOT form: coordinated state on disk names the
   plaintext addresses. This is the entrypoint's documented wall.
   `fly secrets set WEFT_FDB_RESET=1` wipes the data directories on
   restart; the lowest address reconfigures the database.
4. Verify with a TLS-armed fdbcli (`--tls_certificate_file`,
   `--tls_key_file`, `--tls_ca_file`, `--tls_verify_peers`), then
   `fly secrets unset WEFT_FDB_RESET` and verify again; the second
   check proves a restart no longer wipes.
5. Each client service: its own leaf via `FDB_TLS_CERT_B64` /
   `FDB_TLS_KEY_B64` / `FDB_TLS_CA_B64` secrets, materialised to files
   at start and handed to libfdb_c through `FDB_TLS_CERTIFICATE_FILE`,
   `FDB_TLS_KEY_FILE`, `FDB_TLS_CA_FILE`, `FDB_TLS_VERIFY_PEERS`; the
   cluster string gains `:tls` on every coordinator.

## What the prod verification measured

spot-broker's `POST /target/zero` wrote a ledger event through the
iceoryx2 bus into the TLS cluster. The broker machine was then fully
replaced by a deploy (no volume exists on that app), and `GET /status`
on the new machine returned the same event. That is the durability the
architecture claims, measured: the machine held nothing, and the data
came back from the cluster.

## The backup, measured locally and blocked on SNI in prod

With the CA present the trust bundle forms (151 anchors) and OpenSSL
verifies Tigris against it, yet `fdbbackup` times out. The trace names
it: `N2_ConnectHandshakeError ErrorMsg="stream truncated"` against both
the A and the AAAA record. FoundationDB's blobstore client sends no SNI,
and Tigris's edge requires it; curl succeeds from the same machine
because curl sends it. The knob `resolve_prefer_ipv4_addr` changes which
address dies, not whether.

The controlled counterpart ran in local Docker against
[versitygw](https://github.com/versity/versitygw) (Apache-2.0), a
server that presents its one certificate without SNI. Same fdbbackup,
same CA profile, same verify-rule shape:

1. the TLS handshake completes — so the client's TLS is fine and SNI is
   the whole difference;
2. `--knob_http_request_aws_v4_header=true` is required — versitygw
   refuses FoundationDB's default SigV2 (Tigris also speaks v4);
3. the bucket must pre-exist — FoundationDB's create-bucket body is
   refused as MalformedXML; created through the S3 API, the backup
   submits and runs: `The backup on tag 'default' is in progress`.

The production hop that landed is stunnel, not the versitygw sidecar
first named here: the job needed only SNI added to a TCP stream, and a
second S3 implementation in the path was more moving parts than eleven
lines of stunnel config. One more wall surfaced live — Tigris routes
buckets from the Host header, so the endpoint's name has to survive the
hop (/etc/hosts points it at loopback after the IP is resolved for
stunnel's literal dial). datasource-store PRs #4 and #5 carry the
change; `logbook-rfd2134-backup-through-the-sni-hop.md` carries the
measurements, ending with kvrange objects listed in the bucket.
