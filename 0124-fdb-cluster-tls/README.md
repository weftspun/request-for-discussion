# RFD 0124: TLS for the FoundationDB cluster on Fly

**State:** published
**Feature:** mutual TLS between FoundationDB processes, from a private CA
**Scope:** `6-datasource/store/fly`, `6-datasource/foundationdb`

## Problem

The cluster sent every byte in the clear. A public certificate does not
solve this. FoundationDB needs a path to a self-signed trust anchor.
Let's Encrypt ends its chain at a cross-signed root, so every handshake
failed with `TLSPolicyFailure Reason="preverification"`.

A wildcard certificate is also refused. One name must not speak for the
whole domain.

## Decision

**1. Run a private CA.** OpenBao holds the PKI engine with a self-signed
root. The seal uses one key. 1Password holds the unseal key and the root
token. A private root is an anchor by construction.

**2. Name each machine by its full `FLY_MACHINE_ID`.** A NIC is not
stable. Fly gives a machine a new MAC address after an update, and the
certificate then names something that no longer exists. Fourteen hex
characters are unique, so no fleet size breaks the scheme.

**3. Pin the subject with prefix and suffix matches.** The rule is
`Check.Valid=1,S.CN>=fdb-,S.CN<=.chibifire.com`. FoundationDB has no
wildcard in this grammar. An earlier rule used `*` and matched no peer
at all. `DETAILS.md` records the code that shows why.

**4. Give every client its own certificate.** FoundationDB TLS is
mutual. A client without a certificate is refused like any other peer.

## Result

The cluster serves over TLS. It runs 6 processes on 3 machines in 3
zones, in double redundancy, with fault tolerance 1.

## Rollover

The test is complete. The negative control passes: a certificate from a
different CA never gets access. The rotation also passes. We replaced
all three certificates one machine at a time. One poll sample in 34 saw
an unavailable cluster, at a 2 second poll interval.

The role caps the lifetime at 90 days, not the one year we asked for. So
this rotation must run four times each year.

## Not done

The rotation is still manual. Option 2 in `DETAILS.md`, where each
machine asks the CA for its own certificate at boot, removes the manual
step. `DETAILS.md` also lists two defects the negative control found.

## Related

`DETAILS.md` holds the measurements, the truth tables, and the costs.
