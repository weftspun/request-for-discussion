---
rfd: 2135
title: "RFD 2135: Checks run where the credentials already are"
state: "discussion"
feature: "where operational monitoring lives, and what it may not live in"
scope: "weftspun-fdb machine checks; any later production check"
---

A production check runs on the machine being checked: that is the one
place the credentials already are, so nothing new is granted to CI
(which has no production access) and no monitoring pattern accretes in
an admin-authority service like the spot-broker keeper. The check
publishes a health file over a local httpd and a Fly machine check
turns it into a pass or fail in `fly status`. Two reference cases ship
with the rule: `backup_fresh`, which reads the backup layer's own
metadata and caught two backups that had silently self-completed
(`fdbbackup start` defaults to stop-when-done; continuous is `-z`),
and `cluster_health`, the operator-style roll gate that holds a
rolling deploy until re-replication finishes. Every check refuses to
arm unless its self-test controls fire in both directions, and an
unreadable signal always reads as failure.
