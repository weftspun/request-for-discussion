# Details: what moves, what redirects, what stays

## The move-cost inventory

| Piece | From | To | Note |
| --- | --- | --- | --- |
| repo | `weftspun/spot-broker` + `v-sekai/uro` | `<org>/interactor-shuttle` | spot-broker keeps a redirect; uro's fate is on that org's roadmap |
| Elixir modules | `SpotBroker.*` + `Uro.*` | `Shuttle.*` | mechanical rename; the accounting module keeps the schema, only the namespace changes |
| Fly app | `spot-broker`, `uro` | `shuttle` | two → one, blue/green cutover |
| GitHub OAuth app | `spot-broker` + `taskweft/interactor-taskweft` shared client | `shuttle` (new) | fresh credentials per the operator's earlier "different credentials" ruling; `SH_GH_CLIENT_ID`, `SH_GH_CLIENT_SECRET`, `SH_TOKEN_SECRET`, `SH_AUTH_WHITELIST` |
| Fly secrets | `SB_GH_*`, `BROKER_TOKEN`, `VAST_API_KEY`, `FDB_CLUSTER`, `FDB_TLS_*`, uro's `SECRET_KEY_BASE` and DB config | union of both, on the shuttle app | `BROKER_TOKEN` stays as the machine-caller fallback |
| DNS / hostname | `spot-broker.fly.dev`, whatever uro used | `shuttle.fly.dev` (or the operator's chosen domain) | old hostnames redirect for one week, then 410 Gone |
| manifest placement | `7-service/spot-broker` | `3-interactor/interactor-shuttle` | placement rule: repo placed when it appears in the live manifest |

## What does not move

Serials do not move: RFDs 2133-2137 keep their numbers and their
OID URNs, and the register still shows those slugs under the 1.2 arc.
The RFDs' prose is not backfilled to say "shuttle" where it says
"spot-broker": the workspace rule is that a retraction stays next to
what it retracts, and a note here plus a mention in each affected
RFD's future logbook entry does the job. `check_anti_entropy.py` will
not object because the slug matches the directory name, not the body.

The FoundationDB cluster stays `weftspun-fdb`; the shuttle is a
client of it exactly as spot-broker was. The Tigris backup bucket
stays `weftspun-fdb-blob`. The mutual-TLS certificate profile from
RFD 2134 issues one new client cert `fdb-shuttle.chibifire.com`
alongside the existing `fdb-spot-broker.chibifire.com`; the spot-
broker cert is revoked after the cutover week.

## Cutover, in place

spot-broker has less than an hour of production time and no external
callers pinned to its hostname, so the one-week 410 Gone overlap the
prior draft named is retracted here: nothing outside would ever see
those 410s. The cutover is:

1. New repo `<org>/interactor-shuttle`, first commit is the two source
   trees merged with the `Shuttle.*` rename applied.
2. Manifest updated to place the repo at `3-interactor/interactor-shuttle`.
3. Fly app `shuttle` created; secrets set; deploy runs; landing answers.
4. Uro data migration runs against the shuttle Fly app's database.
5. Fly apps `spot-broker` and `uro` destroyed; their OAuth apps deleted;
   spot-broker's FDB client cert revoked. `weftspun/spot-broker` becomes
   a GitHub-native repo redirect.

## Why interactor rather than service

An interactor is user-facing; a service is infrastructure. The merged
thing has a landing page a stranger visits, a sign-in flow, a
downloadable file, and an operator surface. The keeper's spend policy
runs inside it, but the merge is worth doing because the user flow
crosses those halves. Placing it at side 7 would hide the user-facing
role behind an infrastructure prefix and make the manifest read wrong.
