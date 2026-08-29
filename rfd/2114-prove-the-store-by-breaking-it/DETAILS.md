## Trap one: a backup URL that is not restorable, and does not say so

`fdbbackup start -d file:///backup/` does not write the backup to that
path. It makes a container under it, `backup-<timestamp>/`, and writes
there.

Point `describe` at the path you gave, and it answers:

```
URL: file:///backup/
Restorable: false
SnapshotBytes: 0
```

It does not fail. It reports a backup that cannot be restored, with a zero
exit status. A runbook that records the `-d` path looks like it holds
backups. It finds out at recovery time that it does not.

A named subfolder does not correct this. It was measured. A backup sent to
`named-by-procedure/` made `named-by-procedure/backup-<timestamp>/` inside
it, and `describe` on the named folder still answered `Restorable: false`
and `SnapshotBytes: 0`. The behaviour is unconditional, so no name is
restorable by itself. A subfolder per run is still useful, because it lets
one run expire without touching another. It is not a correction.

Two rules follow:

1. Find the container. Do not assume it. `fdbbackup list -b <base>` gives
   it, and it works for `blobstore://` as well, which `ls` does not.
2. Check `Restorable: true` before you trust a backup.

The same procedure holds for S3. Only the URL changes, from `file://` to
`blobstore://<key>:<secret>@<host>/<name>?bucket=<bucket>`.

## Trap two: a key count that reads as total data loss

`fdbcli` opens a quoted key with a backtick, not an apostrophe:

```
`weft/qa/k0001' is `v1'
```

A counter that matches a leading apostrophe counts zero keys. Zero keys
after a restore reads exactly like total data loss. On a new platform this
sends you to look for a durability defect in the storage layer that does
not exist.

## The negative control

`single` redundancy holds one copy of every key. A zone that stops must
lose data. The negative control runs the same test under `single`
redundancy, and it must fail.

It found a real weakness. The first version wrote one key, and the test
passed under `single` redundancy: the stopped zone did not hold that key.
The test measured placement luck. With 200 keys, a zone that stops always
holds some of them, and the control fails as it must.

`SKIP_CLAIM=1` takes the control past the status line check, so that the
stop, and not the reported number, is the thing under test.

## A transaction that is too large for a new cluster

200 `set` commands in one `fdbcli` call return
`commit_unknown_result (1021)` on a cluster that has just been configured.
Data distribution is still settling and the whole batch is one commit.

Write in batches of 50, and retry. Error 1021 means what it says: the
commit may have succeeded. A repeated `set` of the same value is safe.

## What one machine cannot test

These tests stop a process. They do not stop a machine, and they do not
cut a network. A process that stops exercises the consensus path and the
recovery path. It does not make a network partition, and it does not make
two halves that both believe they hold the data.

GitHub Actions runners cannot supply that. It needs two hosts.
