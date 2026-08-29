# Details

## Context

The stack needs a relational database reachable by the Elixir gateway and
the Phoenix zone backend. It must support schema migrations (DDL)
separately from application queries (DML) to limit blast radius if
application credentials are compromised.

## Consequences

- `--advertise-addr` must be `localhost`. A flycast address routes the
  internal gRPC loopback through Fly's NAT, breaking the admin UI.
- `prepare: :unnamed` is required in Postgrex to avoid statement-cache
  OOM on single-node deployments.
- Port 26257 is never publicly exposed. Access is via Fly's private
  network (6PN) using `socket_options: [:inet6]` in Ecto, because
  `.internal` DNS returns only AAAA records.
- The `root` cert is provisioned on the CRDB machine only.
  `gateway_admin` is the highest-privilege cert available to the
  application.
