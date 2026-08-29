---
title: "RFD 2114: Prove the store by breaking it"
rfd: "2114"
state: discussion
scope: store verification, fault tolerance test, disaster recovery procedure
---

## Problem

A FoundationDB cluster reports its own fault tolerance. A test that reads
`Fault Tolerance - 1 zones` and stops there asserts nothing. A cluster that
reports tolerance, and then loses data when a zone stops, passes that test.

`ci.yml` in the store plane already names this failure: a green step that
asserted nothing is the failure the suite exists to prevent.

A backup that nobody restores is a belief, not a backup.

## Decision

**Stop a zone. Then read the data.** The test writes 200 keys, stops one
zone with `kill -9`, and then checks that the cluster still answers and
that all 200 keys are still readable. It then restarts the zone and waits
for tolerance to return.

Use many keys, not one. One key lives on one storage team. A stop can miss
it, and placement luck then looks like redundancy. The first version of
this test passed with one key under `single` redundancy, which holds no
second copy at all.

**Stop two of three zones. Then confirm the cluster refuses to work.** With
no quorum, FoundationDB must stop answering. It must not take a write it
cannot order. In this stage a working cluster is a failure, because a
minority that answers can split-brain.

**Restore into a cluster that was wiped, and prove it was empty first.**
The disaster recovery test backs up 200 keys, deletes the data
directories, confirms the new cluster holds 0 keys, and then restores.
Without the empty check, the restore proves nothing.

**A backup is real only when `describe` says `Restorable: true`.** Record
the container, not the folder that the backup was sent to. `DETAILS.md`
gives the trap.

**Run these as `systemd` oneshot units.** The run survives the shell, the
exit status stays readable, and the output goes to the journal with times.

## References

- The two traps, and the negative control: `DETAILS.md`
- `rfd/2113-foundationdb-on-windows-built-from-source`: the store under test.

## Related

- `rfd/2109-two-tiers-with-foundationdb-as-the-store`: why the store is FoundationDB.

## Detail

{{< include DETAILS.md >}}
