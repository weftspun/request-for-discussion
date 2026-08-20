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

## Retraction: it was never DNS

The section above is wrong about the cause, and it is kept because the
road it went down is worth knowing.

FoundationDB substitutes a service *name* when a blobstore URL carries
no port. `fdbclient/S3BlobStore.actor.cpp`:

    service = b->knobs.secure_connection ? "https" : "http";

That string reaches `getaddrinfo`, which resolves it through
`/etc/services`. `flow/Net2.actor.cpp` then collapses every resolver
error to one code:

    if (ec) { promise.sendError(lookup_failed()); return; }

So `EAI_SERVICE` is reported as `lookup_failed` (1041), whose text is
"DNS lookup failed".

**`debian:bookworm-slim` does not ship `/etc/services`.** It comes from
`netbase`, which is not among the base image's 74 packages, and none of
`curl ca-certificates dnsutils procps openssl` pulls it in.

That single fact explains every observation at once:

| observation | why |
| --- | --- |
| every hostname fails, `s3.amazonaws.com` too | the name is never the problem |
| `/etc/hosts` does not help | the name is never looked up |
| a second nameserver does not help | the same |
| `getent` and `curl` work | neither reads `/etc/services` |
| an IP with `:443` gets past it | the port, not the IP, is the fix |

The last row is the one that reads as a contradiction and is not. The
IP test carried an explicit `:443`, so it supplied the port the URL was
missing. It confirms the diagnosis rather than the addressing theory it
was run to test.

## The fix

Two changes, either sufficient, both applied:

1. `netbase` in `Containerfile.fdb`. About 30 kB, and it repairs every
   other tool in the image at the same time.
2. An explicit port in the blobstore URL, which is what every working
   example on the FoundationDB forums writes:

       blobstore://<key>@<host>:443/<name>?bucket=<bucket>&region=auto&sc=1

The blob credentials key stays `<key>@<host>` with no port. It is
host-only, so adding `:443` to the URL does not change it.

## Not a reported bug

No issue, pull request or forum thread describes this. The
error-flattening in `resolveTCPEndpoint_impl` is a real usability
defect worth reporting upstream: `EAI_SERVICE`, `EAI_NONAME`,
`EAI_AGAIN` and `EAI_FAIL` all arrive as "DNS lookup failed".

**Untested.** The cluster was torn down before either fix could run.
Neither is confirmed, and the check is two commands on a rebuilt image:

    ls -l /etc/services
    getent services https

## Correction: the multi-anchor segfault did not reproduce

The section "A defect found on the way" above records `fdbbackup`
crashing with exit 139 on a CA file holding our root plus the public
roots, and treats it as a FoundationDB defect blocking the two-bundle
design. It did not reproduce.

Measured with 7.3.76 on Ubuntu, one run for each bundle:

| CA file | anchors | exit |
| --- | --- | --- |
| public bundle only | 146 | 124 |
| our root + public bundle | 147 | 124 |
| our root only | 1 | 124 |

All three behave the same and none crashes. 124 is the harness timeout,
not a result from FoundationDB.

Two reasons this is not a refutation, only a failure to reproduce:

* The environment differs. The crash was seen in the Fly container; this
  ran on Ubuntu under WSL.
* The host was `example.invalid`, so no handshake was attempted. A crash
  in certificate *verification* rather than certificate *loading* would
  not be reached by this test.

So the two-bundle design is not known to be blocked, and it is not known
to work either. The test that settles it is the same bundle against a
real endpoint that completes a handshake.

## The connection failure: FoundationDB prefers IPv6 and does not fall back

Supplying the port removed `lookup_failed` and left
`connection_failed`. That is a second, independent fault, and it is the
one that kept every backup from starting.

FoundationDB resolves the endpoint, receives an A record and a AAAA
record, and connects to exactly one of them.
`flow/include/flow/IConnection.h`:

    if (ipV4Addresses.size() > 0 && FLOW_KNOBS->RESOLVE_PREFER_IPV4_ADDR)
        return ipV4...
    if (ipV6Addresses.size() > 0)
        return ipV6Addresses[random];

`flow/Knobs.cpp` initialises `RESOLVE_PREFER_IPV4_ADDR` to false, so
IPv6 wins whenever a AAAA exists. There is no second attempt with the
other family. A unit test asserts IPv6 is always chosen when present,
so this is deterministic: every retry picks the same unreachable
address and fails the same way.

On a host without working IPv6 egress `connect()` returns
`ENETUNREACH`, which arrives as `connection_failed`. The name describes
the symptom and says nothing about the family that was chosen.

### Why the cluster never noticed

A cluster file carries literal addresses. Nothing is resolved, so
`pickOneAddress` is never on that path.

That is the tell, and it was visible for hours before it was read: peer
traffic stayed healthy across machine kills, quorum loss and recovery
while every backup failed. Two paths through one binary, one of which
resolves names and one of which does not.

### Measured

| condition | result |
| --- | --- |
| no knob, plaintext port 80 | `connection_failed` |
| no knob, TLS port 443 | `connection_failed` |
| `curl` and raw TCP, same host and ports | HTTP 200 in 12 ms, TCP ok |
| `--knob_resolve_prefer_ipv4_addr=1` | `backup_auth_missing` |

The last row is the fix. `backup_auth_missing` is the connection
succeeding and deliberately bogus credentials being rejected after it.

Plaintext and TLS failing identically is what eliminated TLS, the CA
bundle, the two-anchor design and SNI in one step. The `curl` row is
the control: without it, "the network is broken" reads the same way.

### The fix

`knob_resolve_prefer_ipv4_addr = true` in the `[backup_agent]` section
of `foundationdb.conf`. `true` and `1` are both accepted; a value the
binary rejects logs `Invalid`.

**Confirmed on Ubuntu under WSL2, which has no IPv6 default route.**
On Fly it is inference: both IPv4 and IPv6 egress answered there, so a
missing route cannot be the explanation, and outbound IPv6 varies per
machine. The cluster was torn down before the probe ran. Do not record
Fly as fixed.

### Expect an auth error next, not a regression

`guessRegionFromDomain` does not recognise `fly.storage.tigris.dev`, so
`region=` stays explicit in the URL, and
`--knob_http_request_aws_v4_header` defaults true in 7.3. The next
failure should be auth or region shaped. That is progress.

### Not documented anywhere

No issue or forum thread names this root cause, and none tracks the
missing IPv4 fallback. One thread reports the same shape with a
different symptom -- a routing blackhole timing out rather than an
immediate `ENETUNREACH` -- and was closed by enabling IPv6 in Docker.
Nobody named the knob.

Both faults in this RFD are ours to write down. That is the reason this
file is long.
