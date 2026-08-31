# Logbook: the backup reaches Tigris through the SNI hop

Question: RFD 2134 left the cluster backup blocked on Tigris requiring
SNI that FoundationDB's blobstore client never sends, and named a
versitygw sidecar as the path. What actually shipped, and is data in
the bucket?

RETRACTED FROM THE RFD'S OPEN SECTION, MINE: the versitygw sidecar.
versitygw was the right lab bench and the wrong production hop — the
job needed only SNI added to a TCP stream, which stunnel does in
eleven config lines with no second S3 implementation in the path.

## The apparatus

weftspun-fdb on Fly (3 machines, double, mutual TLS per RFD 2134),
datasource-store PRs #4 and #5, foundationdb-clients 7.3.76, stunnel4
from bookworm, Tigris bucket `weftspun-fdb-blob` provisioned by
`fly storage create` (which sets the AWS_* secrets the entrypoint
reads). Local rehearsals in Docker: `foundationdb/foundationdb:7.3.63`
against `versity/versitygw` under a private CA.

## The three walls, each measured before its fix

**No SNI.** `N2_ConnectHandshakeError "stream truncated"` against the
A and the AAAA record; the openssl matrix from the same machine shows
SNI required on TLS 1.2 and 1.3 both. Against versitygw locally — a
server that answers without SNI — the same client handshakes clean.
Fix: an stunnel client on 127.0.0.1:8443 supplies the SNI and verifies
the public chain; FoundationDB speaks plaintext one syscall away.

**SigV2.** versitygw refused the default signing outright, which is
how this was found before Tigris could fail the same way silently.
Fix: `knob_http_request_aws_v4_header = true`, in the agent conf and
in the printed fdbbackup command.

**The Host header names the bucket.** With the URL pointing at
127.0.0.1, Tigris answered `<BucketName>127.0.0.1</BucketName>` and
read the path as a key — it routes buckets virtual-host style. Fix
(PR #5): the URL and credentials keep the real endpoint name, the IP
is resolved first, stunnel dials the literal, and /etc/hosts then
points the name at loopback. The signature and the Host header agree
end to end. The IP pin lasts one machine start; a rotation fails
closed on stunnel's checkHost.

## The measurement

`curl --aws-sigv4` through the hop returns the bucket's
ListBucketResult. `fdbbackup start` submits; status reports the
initial snapshot running under the entrypoint's agents. The bucket
lists `backups/weft` and `data/weft/kvranges/snapshot.*/range,*,1048576`
objects with ETags — kvrange payloads, about the size of a floppy
disk each, streaming continuously. Snapshot interval 864000 seconds.

## What is still open

`fdbbackup status` is a hand check. A gate that asserts the newest
snapshot object is younger than the snapshot interval — run from CI or
a keeper — is the difference between a backup and a backup that was
running last month.
