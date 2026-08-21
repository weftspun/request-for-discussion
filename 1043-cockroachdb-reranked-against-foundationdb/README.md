# RFD 1043: CockroachDB, reranked against FoundationDB

**State:** abandoned
**Scope:** `weftspun_studio/`, `character_taxonomy/`

## Problem

RFD 1014 picked CockroachDB before sibling `weftspun` repositories
built and benchmarked FoundationDB, its Relational Layer, and
mvsqlite. One of them, `h2o-bench-tpcc`, picked FoundationDB over
CockroachDB, and called the CockroachDB fork this project pins "a
dead engine." Does that verdict carry over here.

## Decision, as published and now retracted

This RFD published "keep CockroachDB, RFD 1014 stands." That decision
no longer holds. `weftspun/cockroach-local` is archived and out of
`default.xml`, and `datasource-foundationdb` and `datasource-store`
are forked in on side 6.

The retraction is narrow. Two of its three reasons were answered by
events rather than found wrong, and the third never argued for
moving. The dead-fork risk this RFD called open work is the part that
aged badly. Today arrived.

Abandoned here means the decision was in force and has been reversed.
It does not mean nobody acted on it.

See `DETAILS.md` for the three reasons in full, what answered each,
the two questions this leaves open, and the evidence from each
sibling repository.

## Related

RFD 1014 picks CockroachDB. RFD 103a and RFD 103b state the
zero-trust, one-command build. RFD 1041's taxonomy runs on
CockroachDB in `character_taxonomy/`. RFD 1039 gets the dead-fork
risk as a new open-work item.
