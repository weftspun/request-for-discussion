---
title: "RFD 2006: CockroachDB with mTLS and role-separated access"
rfd: "2006"
state: published
scope: gateway/db
---

## Problem

The Elixir gateway and the Phoenix zone backend needed a shared
database. No RFD fixed how they would connect securely, or with what
access level. A single, undifferentiated database credential would let
any leaked credential alter the schema. The project needed a
deployment and certificate plan before either service could connect.

## Decision

The stack runs a single-node CockroachDB on Fly.io. The Elixir gateway and
the Phoenix zone backend both connect to it. All connections use mTLS.
The database defines three application roles: `gateway_admin` for schema
migrations, `gateway_writer` for normal queries, and `gateway_reader` for
read-only access. This role split limits the damage if one credential
leaks; a leaked writer credential cannot alter the schema.

Certificates come from `gen_crdb_certs.sh` and are valid for 100 years.
They are stored as Fly secrets. The node certificate carries both
`serverAuth` and `clientAuth`, because CockroachDB reuses the node
certificate for its own internal gRPC calls.

`DETAILS.md` records the deployment consequences: the required
`--advertise-addr` setting, the Postgrex `prepare: :unnamed` requirement,
the private-network access rule, and the certificate-provisioning
boundary.

## References

- Full consequences and deployment notes: `DETAILS.md`
- Original record: `decisions/20260501-cockroachdb-with-mtls-role-separation.md`

## Detail

{{< include DETAILS.md >}}
