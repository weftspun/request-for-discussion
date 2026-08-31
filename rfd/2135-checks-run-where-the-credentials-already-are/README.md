# RFD 2135: Checks run where the credentials already are

**State:** discussion
**Feature:** where operational monitoring lives, and what it may not live in
**Scope:** weftspun-fdb's machine checks; any later production check

## Problem

The weftspun-fdb backup needed a staleness gate, and the two obvious
homes were both wrong. CI has no production access, and granting it
some means a new credential with a new blast radius. The spot-broker
keeper holds spend authority, and an admin service that accumulates
monitoring scripts becomes the home of every capability.

## Decision

A production check runs on the machine being checked, because that is
the one place the credentials already are: nothing new is granted
anywhere. It publishes a health file over a local httpd, and a Fly
machine check turns the file into a pass or fail in `fly status`.

Two reference cases ship, both on weftspun-fdb. `backup_fresh` reads
the backup layer's own metadata; a backup is fresh only when it is
running and its restorable point is close. `cluster_health` fails
until the data state is healthy and a zone can be lost without losing
data, so a rolling deploy waits out re-replication after each
restart, the way the Kubernetes FDB operator gates its own rolls.

Every check refuses to arm unless its self-test controls fire in both
directions, and an unreadable signal always reads as failure. The
measurements behind both checks, including the two backups that
silently self-completed and the curl signing limits that reshaped the
probe, are in DETAILS.md and the logbook.

## Verification

The roll gate's first live exercise was its own deploy: after each
machine restart the check held red (`data_healthy=no`) through
re-replication and the roll waited, then all three machines converged
to 2 of 2 checks passing.
