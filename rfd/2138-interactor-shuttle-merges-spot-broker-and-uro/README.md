# RFD 2138: interactor-shuttle merges spot-broker and uro

**State:** abandoned
**Feature:** the single interactor a user signs into for spend, users, and content
**Scope:** spot-broker (weftspun) and uro (v-sekai) become one service under the sides convention

## Problem

uro held V-Sekai users and served content; spot-broker held the vast.ai key and posted
double-entry entries for spend. Both needed GitHub sign-in, both wanted the same
TigerBeetle-shaped ledger, and neither could hand a stranger a downloadable VRM without
the other: two GitHub OAuth apps, two Fly apps, two deploy pipelines, one user story.

## Decision

They merge as **interactor-shuttle** at `3-interactor/interactor-shuttle`. Interactor
because the primary role is user-facing (GitHub sign-in, landing page, roll button, VRM
download); spot-broker's keeper policy, the TigerBeetle accounting on ecto_sqlite3, and
the FoundationDB event ledger become internal modules rather than peers. `shuttle` fits
the weaving vocabulary the workspace already uses (weftspun, sinew, taskweft).
spot-broker's Fly URL and repo become redirects; RFDs 2133-2137 stay as written, naming
the predecessor service, per the retractions-stay-in-place rule.

Migrating unchanged: one holder of the vast.ai key (the shuttle process); keeper
singleton-with-hysteresis (RFD 2133); mutual-TLS FoundationDB cluster plus Tigris
backup (RFDs 2134-2135); TigerBeetle-shaped Account and Transfer tables, sum-to-zero by
construction; GitHub OAuth via oauth_mcp_bridge with a **new** SH_GH_* credential set,
so spot-broker's SB_GH_* credentials rotate out with the rename.

## Operator questions and verification

Org: recommend `v-sekai-fabric` since the V-Sekai user record is the load-bearing state,
though uro lives at `v-sekai/uro` and spot-broker at `weftspun/spot-broker`. Cutover:
land the code merge with both old services running, then keep spot-broker's Fly app
alive one week so pinned callers see 410 Gone rather than timeouts. Done when one Fly
app serves both the landing and the GPU spend API, one GitHub OAuth app authenticates
both, one deploy pipeline builds one release image, and the predecessor RFDs are not
backfilled. Move-cost inventory in DETAILS.md.
