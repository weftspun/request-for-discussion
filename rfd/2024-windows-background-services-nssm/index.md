---
title: "RFD 2024: Running background services on Windows with nssm"
rfd: "2024"
state: published
scope: Windows workstation service supervision
---

## Problem

Several workstation processes must survive shells, log-offs, and
reboots, and restart on crash. Examples include sccache servers, Godot
dedicated servers, a CockroachDB node, and zone servers. Running them by
hand, or through a Scheduled Task, fails to give this. Neither method
gives boot start with true Service Control Manager (SCM) restart
semantics, because the target programs are plain executables, not
SCM-aware services.

## Decision

Several workstation processes (sccache servers, Godot dedicated
servers, a CockroachDB node, zone servers) must survive shells,
log-offs, and reboots, and restart on crash. Running them by hand or
via a Scheduled Task fails: neither gives boot start with true Service
Control Manager (SCM) restart semantics, and the target programs are
plain executables, not SCM-aware services. The project wraps each
target with nssm (the Non-Sucking Service Manager), one Windows
service per instance. Each instance runs in the foreground under an
absolute-path launcher script that reads secrets at runtime from their
existing secured location, an elevated installer script registers it
with auto-start and restart-on-exit, and instances stay isolated by
port (and, for sccache, by S3 key prefix).

## References

- Full context, decision drivers, considered options, the worked
  sccache example, consequences, and confirmation steps: `DETAILS.md`
- Original record:
  `decisions/20260606-windows-background-services-nssm.md`
- [nssm](https://nssm.cc/), [sccache](https://github.com/mozilla/sccache)

## Related

- `rfd/2016-checking-sccache`
- `rfd/2017-compiling-godot-engine`

## Detail

{{< include DETAILS.md >}}
