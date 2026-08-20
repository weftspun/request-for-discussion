# RFD 0124 details

This file holds the measurements. The README holds the decision.

The work happened first. This document came after it. So the numbers
below are what occurred, not what we expected.

## The CA refuses a wildcard

The role is `allowed_domains="fdb-*.chibifire.com"`. It also sets
`allow_wildcard_certificates=false` and `allow_bare_domains=false`.

| request | result |
| --- | --- |
| `fdb-3678.chibifire.com` | issued |
| `fdb-zzzz.chibifire.com` | issued |
| `www.chibifire.com` | refused |
| `chibifire.com` | refused |
| `*.chibifire.com` | refused |

The first role permitted any subdomain. It would have issued
`www.chibifire.com`. The cluster rejects that name, so the policy held
in one of the two places that need it. A negative control found this.
Without the control we would have called the CA correct.

We revoked the earlier `*.chibifire.com` certificate. Its serial is
`054631565CEC358B51D513EE16F8A8BC63CF`.

## A NIC is not an identity

We first named each machine from the last four characters of its NIC.
That gave `fdb-3678`, `fdb-fbc7` and `fdb-a751`. One
`fly machine update` later, the same three machines reported `ee13`,
`30cb` and a third value. All three refused to start:

    a CA was given but no certificate for this machine's NIC (ee13)

That refusal is correct. The other choice lets a machine take another
machine's identity, and then peer verification means nothing. But the
cluster went down, and it would go down again after each update.

Two facts about these strings, because both ends mislead:

- Every Fly NIC starts with `de:ad`. That is the OUI. A prefix of a NIC
  identifies nothing.
- Machine IDs made at the same time share a leading prefix.

So the front of either string is useless. We now use the whole machine
ID. We measured its stability across about six `fly machine update`
calls. The machine IDs never changed. The NICs changed under them.

## The verify_peers grammar has no wildcard

This cost more time than the identity question.

The rule was `Check.Valid=1,S.CN=fdb-*`. Before that it was
`Check.Valid=1,S.CN=*.chibifire.com`. Both are the same error.

`flow/TLSConfig.actor.cpp` holds three matchers and no more:

- `EXACT` compares two strings of equal length with `memcmp`.
- `PREFIX` compares at the start.
- `SUFFIX` compares at the end.

`*` is not a metacharacter. It is a literal asterisk. The rule asked for
a peer whose Common Name is the six characters `fdb-*`. No certificate
has that name, so the cluster refused every peer.

`>=` selects the prefix match. `<=` selects the suffix match. This is
the shape in FoundationDB's own example, `S.OU>=FDB,S.OU<=Team`.

## One message, three different causes

A rule that refuses every peer looks the same as a cluster that cannot
find its coordinators. `fdbcli` reported this:

    Could not communicate with a quorum of coordination servers

That sentence sounds like a network fault. It sent two rounds of work at
coordinator lists and `:tls` suffixes. At the same time
`TLSPolicyFailure` was 0 and no severity-40 error appeared. We read that
as proof that the certificates were correct. The certificates *were*
correct. The handshake completed. The refusal came after it, on a field
match, and the trace counted it as nothing.

Three unrelated causes give this same message:

1. A cluster that moved from plaintext to TLS in place.
2. A verification rule that matches no peer.
3. A client that holds no certificate.

Read the message as "this connection did not open". Do not read it as
"the network is broken". Check the client's own credentials first,
because that check is the cheapest of the three.

## The diagnostic failed in the same direction as the fault

FoundationDB TLS is mutual. `fdbcli` needs its own
`FDB_TLS_CERTIFICATE_FILE`, `FDB_TLS_KEY_FILE`, `FDB_TLS_CA_FILE` and
`FDB_TLS_VERIFY_PEERS`. The entrypoint exports these. An
`fly ssh console` session does not inherit them.

So each manual status check ran as a client with no credentials. It
reported that it could not reach a quorum. That is the same sentence the
real fault produced. For most of a day, one answer stood for two
different questions.

The fdb-kubernetes-operator states the same rule from the other side. It
sets those four variables on itself, not only on the servers. Its manual
says the verification rules must permit the cluster's certificates, the
operator's certificate, and each client's certificate. A client is a
peer.

## The negative control for rollover

The property: the cluster refuses a certificate that our CA did not
sign, whatever that certificate is named. A rollover that uses material
the cluster would accept anyway proves nothing.

We made a second CA inside the container. We signed
`CN=fdb-rogue.chibifire.com` with it. That name satisfies the
verification rule exactly. Only the signature is wrong.

| # | client certificate | CA file | result |
| --- | --- | --- | --- |
| A | rogue chain | real + rogue | segfault, exit 139 |
| B | rogue chain | rogue only | refused |
| C | real certificate | real + rogue | refused |
| D | real certificate | real only | available |
| E | rogue leaf, no anchor | real + rogue | segfault, exit 139 |

D is the positive control. A, B and E are the negative control. The
rogue identity never got access. The property holds.

Two defects came out of the same run.

**`fdbcli` stops with a segfault instead of a refusal.** Runs A and E
end with `SIGNAL: Segmentation fault (11)` in 7.3.76. A crash and a
refusal both deny access, but they are not the same result. A crash
carries no diagnosis. A script that reads exit codes sees 139, not a TLS
error. This is an upstream defect. We do not work around it here.

**An extra anchor in the CA file breaks a client that works.** Run C
holds a valid certificate and trusts the real root. It still fails. The
only difference from run D is one unrelated CA added to `ca.pem`. So the
CA file is not additive. "Add our root to the existing bundle" is not a
safe instruction. `fdb-entrypoint.sh` counts self-signed anchors for
this reason.

## The rotation half of rollover

We issued four new certificates from the same CA. Then we updated the
three machines one at a time. A poller on a machine that was not under
update asked for `status minimal` every 2 seconds.

| window | machine under update | samples | unavailable |
| --- | --- | --- | --- |
| 1 | `871e61c0354168` | 13 | 0 |
| 2 | `839743a7613568` | 13 | 1 |
| 3 | `0804290c964d28` | 8 | 0 |

Four more samples reported "available, but has issues". That is the
recovery state, not an outage.

So one sample in 34 saw an unavailable cluster. The poll interval is
2 seconds, so this measurement cannot see a gap shorter than that, and
it cannot place the gap inside the interval. The correct statement is
"one interval of at most 2 seconds", not "2 seconds of downtime".

All three machines now hold the new serial:

    871e61c0354168   207A221A064C4330CDAB1F70ADA89B264320B24B
    839743a7613568   294F56AC08237E0A2B72EC932260BAEE53CE4C4A
    0804290c964d28   1176DBB2FD908E0B1C52B0567CEA8B59FC84E12A

The cluster kept 6 processes, 3 zones, 3 machines and fault tolerance 1
through the whole sequence.

**The role caps the lifetime at 90 days.** We asked for `ttl=8760h`,
which is one year. The certificates expire on 18 November 2026, which is
90 days. The role's `max_ttl` silently reduced the request. So this
rotation must run every 90 days, not every year. A request that is
quietly cut down looks the same as a request that was met.

**A boot race, recorded because it looked like a failure.** A check of
the new certificate ran one second before the entrypoint wrote it. It
printed `Unable to load certificate`. The machine was correct and the
check was early. Read the machine's own log before you trust a probe
that runs during a restart.

## Costs to record

**There is no in-place move from a plaintext cluster to a TLS cluster.**
A coordinator's address is its identity. The `:tls` suffix is part of
that address. The coordinated state on disk holds the old address. The
processes start, report health, speak TLS to each other, and never reach
a quorum. `WEFT_FDB_RESET=1` exists for this. Choose TLS before the
cluster holds data that matters.

**Memory is below the recommendation.** Each machine is a
`shared-cpu-2x` with 2 GB. That gives 0.9 GB for each process.
FoundationDB recommends 4.0 GB. Any benchmark must state this
configuration, or the numbers cannot be quoted.

## Verification command

Run this from a cluster machine. It must print `The database is
available`.

    FDB_TLS_CERTIFICATE_FILE=/etc/foundationdb/tls/cert.pem \
    FDB_TLS_KEY_FILE=/etc/foundationdb/tls/key.pem \
    FDB_TLS_CA_FILE=/etc/foundationdb/tls/ca.pem \
    FDB_TLS_VERIFY_PEERS="Check.Valid=1,S.CN>=fdb-,S.CN<=.chibifire.com" \
      fdbcli --exec 'status minimal'
