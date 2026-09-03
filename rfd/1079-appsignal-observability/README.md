# RFD 1079: AppSignal observability, and versitygw's removal

**State:** published
**Scope:** `apps/weftspun_studio/`

## Decision

`Appsignal.Plug`, not raw OpenTelemetry, per the user's own
direction. `use Appsignal.Plug` in `router.ex`, before `:match`, so
it wraps every request. Config is entirely env-var driven
(`APPSIGNAL_ACTIVE`, `APPSIGNAL_APP_NAME`, `APPSIGNAL_APP_ENV`,
`APPSIGNAL_OTP_APP`), matching this project's existing pattern, no
`config.exs` entry needed. `APPSIGNAL_PUSH_API_KEY` is a secret, in
two places: the `APPSIGNAL_PUSH_API_KEY` GitHub Actions secret (the
source of record), and a Fly secret the deploy workflow now
`flyctl secrets set --stage`s from that GitHub secret on every run,
not only the one time this session set it by hand.

`versitygw` is removed outright, not deferred: no more build stage
in `Dockerfile.fly`, no more process in
`deploy/docker-entrypoint-fly.sh`, `VGW_ACCESS_KEY`/`VGW_SECRET_KEY`
unset as Fly secrets. It cost nothing extra to run, colocated inside
the already-billed machine, so removing it changes no bill, only
dead code and a credential surface nothing reads anymore.

## Problem

`weftspun_studio` ran with no request tracing or error reporting at
all. A failing deploy, or a slow request, left no trail beyond
`flyctl logs`. Separately, RFD 1073's `versitygw` (RFD 1058's
S3-API gateway) sat unused: RFD 1073 (weftspun/request-for-discussion)
and RFD 1077 already decided Tigris replaces it, and RFD 1076 split
`apps/usd_viewer_app/` onto its own Fly machine, which cannot reach
`versitygw`'s loopback-only bind at all.

## Related

RFD 1073 and RFD 1077 (both weftspun/request-for-discussion) decide
Tigris over `versitygw`. RFD 1076 gives the `apps/` split that made
`versitygw` unreachable from `usd_viewer_app` in the first place.
