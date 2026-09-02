---
name: pr-150-serial-collision
description: "PR weftspun/request-for-discussion#150 auto-merge blocked on 5-serial collision S2143-S2147"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6af7ce67-cc66-41b2-8c13-0bc4c0cb6fde
  modified: 2026-09-02T03:24:18.272Z
---

PR `weftspun/request-for-discussion#150` (RFDs 2152-2156 landing on
branch `rfd-2143-2151-grafcet-fbd-chain`) is auto-merge queued but
blocked. Real conflict is not text — it is a **semantic collision on
the "serials never reuse" rule** stated at line 23 of
`SERIALS-vsekai-fabric.usda`.

Both workstreams grabbed S2143-S2147 independently:

    serial   our branch (grafcet/FBD)                         main (already landed)
    S2143    grafcet-as-taskwefts-authoring-surface           fdb-backup-fans-out-to-r2
    S2144    grafcet-static-analysis-in-lean4                 fdb-dr-runbook-first-run
    S2145    rectgtn-on-openplc4-over-coap-oscore             certificate-lifetimes
    S2146    coap-oscore-nif-for-taskweft                     bao-is-the-secret-store
    S2147    or-divergence-plcopen-emit                       bao-is-critical-infrastructure

S2148-S2156 on our branch (fbd-to-nodegraph -> vn-avatar-cleanroom)
do not collide. Sensible fix per the register's monotonic rule:
shift our whole chain to start after main's last, mapping S2143 ->
S2148 up through S2156 -> S2161. Fourteen RFDs to renumber.

**RESOLVED 2026-09-02:** merged as PR #150 (RFDs at S2148-S2161),
PR #151 (bullets -> numbered lists to pass trope-density), PR #152
(check_tropes.py `em_dash_join` regex tightened to literal-spaces so
markdown bullets do not false-flag), and PR #153 (strip PR #152's
inline comment so `scripts/check_tropes.py` is back on its 4% rung).
All four landed on main.

The original fix procedure below is kept for the archaeology:

1. `git rebase weftspun/main` on `rfd-2143-2151-grafcet-fbd-chain`;
   accept ours on non-SERIALS conflicts; hand-edit the SERIALS block
   to append S2148 through S2161 with our slugs.
2. Rename `rfd/2143-*` through `rfd/2156-*` directories in-tree to
   match the new numbers (2148-* through 2161-*).
3. Grep for cross-references (`RFD 2143` etc, `S2143` etc) in
   RFD bodies + manifest + memory files, update all mentions.
   Notable: `3-interactor/editscore-lora-qwen3vl-4b/README.md` and
   `pixi.toml` mention "RFD 2156" and "rfd/2156-*" paths — those
   become "RFD 2161" and `rfd/2161-*`.
4. Update memory files that reference old numbers:
   [[hardware-pivot-2026-09-01]], [[editscore-qwen3vl-mlx-works]],
   [[rfd-2156-retraction-trail]] (rename this to
   `rfd-2161-retraction-trail.md`), [[weights-live-on-huggingface]].
5. Force-push the branch; auto-merge fires when mergeable.

**Repo merge-method configs (from `gh api repos/... --jq ...`):**

    weftspun/request-for-discussion:  auto_merge=true  merge=true   squash=NO   rebase=NO
    weftspun/weftspun-keypoint:       auto_merge=NO    merge=true   squash=yes  rebase=yes

Auto-merge on request-for-discussion accepts only MERGE method. On
weftspun-keypoint auto-merge is disabled; use immediate `gh pr merge
--squash` there. That is why PR #75 merged immediately with squash
and PR #150 queued a merge-commit that never fires.
