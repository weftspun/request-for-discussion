# RFD 2146: Bao is the secret store, cert-auth is the fence

**State:** discussion
**Scope:** the workspace's Bao instance and every consumer that
already presents a per-identity TLS leaf.

## Decision

The cert is the answer. Bao's cert auth backend accepts each
identity's per-service leaf as the login credential, mints a scoped
token bound to that identity's role's policies, and returns it. No
shared bearers, no root token in service code, no network ACL as an
identity substitute. The cert is already the fence at TLS; this RFD
extends it up the stack.

Two axes carry the design. **Policies** shape `<verb>-<scope>`:
verb in {read, write, admin, issue}; scope is a KV subtree, a PKI
mount, or `*` for sudo. **Roles** bind one identity's leaf (or a
small exact-match CN allow-list, no globs) to a set of policies
with a short-session TTL. New app: one policy, one role. New
capability: one policy against an existing scope.

The store becomes the source of truth for every secret; 1P retains
the material as an offline mirror. Role table, walkthrough, negative
controls in `DETAILS.md`.

## Problem

Every service ends up with three identity questions: what secrets
can it read, what actions can it take, and how does it prove it is
what it claims to be. Left alone, each answer accretes its own
credential: a shared bearer for reads, a root token for writes, a
network ACL as an identity substitute. Every one becomes a rotation
problem and a leak surface. When the store sits behind mTLS, the
client already presents a per-identity cert at the TLS handshake,
and the API layer above ignores it and re-asks with a token.

## Related

RFD 2140, 2142 (implemented here), 2144, 2145.
