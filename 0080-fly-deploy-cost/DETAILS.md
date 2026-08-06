# RFD 0080 details: the numbers, and where they came from

## Source prices

From `fly.io/docs/about/pricing/`, the published rates this
breakdown uses directly:

| Resource | Per-second | Per-month |
| --- | --- | --- |
| `shared-cpu-1x`, 256MB | $0.00000078 | $2.02 |
| `shared-cpu-1x`, 512MB | $0.00000128 | $3.32 |
| Volume storage | — | $0.15/GB |

Hourly = per-second × 3600. Yearly = per-month × 12, the number Fly
itself bills against, not hourly × 8760 (the two differ slightly
because a month is not exactly 730 hours; the per-month figure is
the one Fly actually charges).

## This deployment's real sizes, checked live

`flyctl machine list` and `flyctl volumes list`, run against all
three apps, the same session these prices apply to:

| App | Machine(s) | Volume |
| --- | --- | --- |
| `weftspun-studio` | 1× `shared-cpu-1x`, 512MB | 3GB |
| `weftspun-character-taxonomy` | 1× `shared-cpu-1x`, 512MB | 1GB |
| `weftspun-usd-viewer` | 1× `shared-cpu-1x`, 256MB | none |

`weftspun-usd-viewer` started as Fly's default 2-machine HA pair
(zero-downtime deploys); scaled to one (`min_machines_running = 0`
in its own `fly.toml`, then `flyctl scale count 1`) per the user's
own choice of cost over restart-window downtime.

No dedicated IPv4 anywhere (checked with `flyctl ips list` against
all three apps): only shared IPv4 and free dedicated IPv6, so no
extra per-app IP charge applies.

## The breakdown, hourly / monthly / yearly

| App | Hourly | Monthly | Yearly |
| --- | --- | --- | --- |
| `weftspun-studio` (machine) | $0.004608 | $3.32 | $39.84 |
| `weftspun-studio` (3GB volume) | $0.000616 | $0.45 | $5.40 |
| `weftspun-character-taxonomy` (machine) | $0.004608 | $3.32 | $39.84 |
| `weftspun-character-taxonomy` (1GB volume) | $0.000205 | $0.15 | $1.80 |
| `weftspun-usd-viewer` (machine) | $0.002808 | $2.02 | $24.24 |
| **Total** | **$0.012845** | **$9.26** | **$111.12** |

Volume hourly figures divide the monthly rate by 730 (Fly's own
average hours-per-month), since Fly bills Volumes monthly, not
per-second; machine hourly figures are the real per-second billing
rate × 3600, both shown for a like-for-like row.

## What this excludes

- **Outbound bandwidth.** Usage-based, not a fixed size like a
  Machine or a Volume. Fly's free tier covers a baseline before
  per-GB egress billing starts; this deployment's actual traffic
  was not measured this session.
- **Tigris.** RFD 0073's still-open fetch-path work (`apps/usd_viewer_app/`
  fetching gallery assets from Tigris instead of baking them into
  its own image) would add real, usage-based storage and bandwidth
  cost once built. Not yet built, so not yet billed, so not in this
  total.
- **`taskweft-mcp`**, a fourth already-deployed Fly app in the same
  org, unrelated to the three this RFD scopes (`weftspun-studio`,
  `weftspun-character-taxonomy`, `weftspun-usd-viewer`). Its own
  cost is real but out of this RFD's scope.
