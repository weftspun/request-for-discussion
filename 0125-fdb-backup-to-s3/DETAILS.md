# RFD 0125 details

## The procedure

This is what the entrypoint now does, and what an operator repeats.

**1. Write the blob credentials file.** From the injected environment,
at `/etc/foundationdb/blob-credentials.json`, mode 0600:

    {"accounts":{"<AWS_ACCESS_KEY_ID>@<host>":{"secret":"<secret>"}}}

The account key must equal `<key>@<host>` in the URL exactly. If it does
not, the lookup fails and the error names the account, not the file.

**2. Declare the agent in `foundationdb.conf`.**

    [backup_agent]
    command = /usr/lib/foundationdb/backup_agent/backup_agent
    logdir = /var/log/foundationdb
    blob_credentials = /etc/foundationdb/blob-credentials.json
    tls_certificate_file = /etc/foundationdb/tls/cert.pem
    tls_key_file = /etc/foundationdb/tls/key.pem
    tls_ca_file = /etc/foundationdb/tls/ca-blobstore.pem
    tls_verify_peers = <cluster rule>|Check.Valid=1,S.CN=<host>

    [backup_agent.1]

**3. Start the backup once.** It continues without further commands.

    fdbbackup start -d "blobstore://<key>@<host>/<name>?bucket=<bucket>&region=auto&sc=1"

**4. Check it.** `fdbbackup status`. To restore, `fdbrestore start`
with the same URL and a target version.

## Two trust bundles, not one

FoundationDB uses the same `tls_ca_file` and `tls_verify_peers` for
cluster peers and for the HTTPS connection to the object store. There is
no separate policy.

Our `ca.pem` holds one anchor: our own root. The object store presents a
certificate from a public CA. So the agent needs the public roots too.

The `fdbserver` processes do not get them. A cluster that trusts every
public CA has the membership rule "anyone who can buy a certificate".

The verification rule is two alternatives joined by `|`, which
FoundationDB reads as "match any". The first alternative is the cluster
rule. The second is an exact match on the endpoint host, built from the
endpoint variable rather than written down, so it admits one host and
not a suffix of neighbours.

## What actually blocks this: DNS

The failure looked like TLS for three rounds. It is not TLS.

`fdbbackup start` reports:

    ERROR: Could not create backup container: Operation timed out

That sentence names a timeout, so it reads as a network fault. The trace
log names the real error:

    Type="S3BlobStoreEndpointRequestFailedRetryable"
    Error="lookup_failed" ErrorDescription="DNS lookup failed"
    ErrorCode="1041" RemoteHost="fly.storage.tigris.dev"
    Verb="HEAD" Resource="/weftspun-fdb-backup" ThisTry="1"

Eight of these for each attempt, then the timeout.

The container's network is not the problem. Measured from the same
machine:

| check | result |
| --- | --- |
| `getent ahosts fly.storage.tigris.dev` | 149.248.213.147 and an IPv6 address |
| `curl https://fly.storage.tigris.dev/` | HTTP 307 in 0.08 s |
| `curl https://example.com` | HTTP 200 |
| path-style bucket GET | HTTP 403 in milliseconds |
| virtual-host-style bucket GET | HTTP 403 in milliseconds |

So DNS and egress both work for glibc. FoundationDB's resolver fails on
the same name.

`/etc/resolv.conf` in a Fly container holds one nameserver, `fdaa::3`,
which is IPv6 only. `getent` and `curl` go through glibc and succeed.
FoundationDB does not use glibc's path here.

**An `/etc/hosts` entry does not help.** We added
`149.248.213.147 fly.storage.tigris.dev` and retried. Eight more
`lookup_failed`. So FoundationDB queries the nameserver directly and
never reads the hosts file.

## Hypotheses this replaced, each wrong

Recorded because each was plausible and each cost a round.

**TLS trust.** The theory: the agent trusts only our private root, so
the public certificate fails and the handshake never completes. Correct
about the configuration, wrong as the cause. The connection never
reaches a handshake.

**Redirects or bucket addressing.** The theory: Tigris answers 307 and
FoundationDB does not follow it. Measured: both path style and
virtual-host style answer 403 immediately, with no redirect.

**Plaintext to isolate TLS.** We ran with `sc=0`. It also timed out,
which looked like confirmation that TLS was innocent. It proves nothing:
`sc=0` uses port 80, and the endpoint does not serve port 80. An
inconclusive test that looks conclusive is worse than no test.

## A defect found on the way

`fdbbackup` **segfaults** when `tls_ca_file` holds our root plus the 150
public roots, exit 139, with the same trace addresses as the `fdbcli`
crashes in RFD 0124. So that RFD's finding is a real FoundationDB defect
and not an artefact of the rogue CA it was found with.

This matters for the decision above: the two-bundle design is written
and deployed, but the wide bundle cannot be proven to work until both
the resolver defect and this crash are settled.

## Next step

Find how FoundationDB resolves names and why it fails against an
IPv6-only nameserver. If it cannot be fixed by configuration, the
options are:

1. Put the IP address in the URL host and set the `Host` header through
   the URL's `header` parameter. FoundationDB parses `header` as
   `FieldName:FieldValue`. This removes DNS. It needs the TLS name check
   to still pass, which is untested.
2. Run a resolver in the container that answers over IPv4 on localhost.
3. Back up through a machine that is not on Fly.

None is tested. Do not record any of them as the answer.
