---
title: "RFD 2111: Convert the deployment words to the hexagon vocabulary"
rfd: "2111"
state: published
scope: architecture vocabulary across all repositories
---

## Problem

This stack names one component twice. RFD 2028 names its structure; a second set names its
deployment — plane, edge plane, domain — with no RFD, defined in `lib/weft.ex`, copied into
ten or more READMEs, and giving domain, edge, and port two meanings each where ASD-STE100 permits one.

## Decision

Retire plane, edge plane, and domain; the Netflix formulation supplies each replacement.

| retired     | replacement     | the meaning that carries over             |
| ----------- | --------------- | ----------------------------------------- |
| plane       | interactor      | a process that holds entities and actions |
| edge plane  | transport layer | the input that triggers an interactor     |
| domain      | service         | the set that shares a ring, and a machine |
| store plane | data source     | the implementation behind a repository    |

The rules do not change with the words. An interactor opens no listening socket. A
transport layer holds no authority, runs no simulation, and keeps no durable state. A
service is the set of interactors that share a ring, because a ring is shared memory and forces
co-location. "Control plane" and "data plane" stay: they name a class of traffic rather than a
process. A git repository name states its type first and drops the `fabric-` prefix the
organisation already carries, so `fabric-authority-plane` becomes `interactor-authority`.
Thirty are renamed, five carrying no retired word.

## References

- [Netflix on hexagonal architecture](https://netflixtechblog.com/ready-for-changes-with-hexagonal-architecture-b315ec967749), and [Cockburn](https://alistair.cockburn.us/hexagonal-architecture)
- RFD 2028, amended by this RFD; RFD 2121 amends this one against the tree. The term table, the collisions, and the rename list are in `DETAILS.md`

## Detail

{{< include DETAILS.md >}}
