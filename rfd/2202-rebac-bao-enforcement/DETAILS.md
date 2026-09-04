# ReBAC via Bao identity groups — mapping, reconciler, and the non-enforcement scope

## Role → group → policy mapping

One group per role in RFD 2200's vocabulary. Group names are
`agents-<role>` for greppability. Policies are what each role's
capabilities require.

| role                  | Bao group                    | policies attached      |
|-----------------------|------------------------------|------------------------|
| `coordinator`         | `agents-coordinator`         | `mps-admin`            |
| `gpu-experimenter`    | `agents-gpu-experimenter`    | `agents-rw`            |
| `edge-qat-specialist` | `agents-edge-qat-specialist` | `agents-rw`            |
| `assist`              | `agents-assist`              | `agents-rw`            |

Today `gpu-experimenter`, `edge-qat-specialist`, and `assist` all
carry the same `agents-rw` policy. The role distinction is
semantic — carried by the tuple, consumed by the coordinator's
task-picking, and visible in the store's `role` field on the
agent's row. When the workspace grows a policy shape that scopes to
a specific role (say, `gpu-experimenter` needs `pki/sign/experiment-*`
grants the others do not), extending this table is the change; the
reconciler picks it up on the next run.

## Reconciler contract

`scripts/sync_rebac_groups.py` reconciles:

1. Reads every `relationships/<agent>--role--<role>` tuple.
2. Resolves each `<agent>` to its Bao entity id by scanning
   `identity/entity/id/*` for an alias whose name is
   `<agent>.agents.weftspun`.
3. Groups entities by role, compares to current
   `identity/group/name/agents-<role>` membership, computes diff.
4. Reports drift; with `--apply`, writes the new membership +
   policies via `bao write identity/group/name/agents-<role>
   policies=... member_entity_ids=...`.

Idempotent — re-running with no tuple changes produces `no change`
on every group.

The script carries:

- A `ROLE_POLICIES` table mirroring the mapping above. Adding a role
  means adding a row here and running with `--apply`.
- A self-test with three tuple-parse controls and four
  role-mapping controls, both directions.
- Explicit `UNKNOWN ROLES` and `UNRESOLVED AGENTS` surfaces when a
  tuple points at a role not in the table or an agent whose entity
  cannot be found.

Usage:

    python scripts/sync_rebac_groups.py            # dry-run, exit 1 on drift
    python scripts/sync_rebac_groups.py --apply    # write the changes
    python scripts/sync_rebac_groups.py --self-test

## What Bao enforces after this RFD lands

Any capability grant expressible as a Bao policy is enforced through
group membership. That covers:

- KV read/write on `agents/`, `certs/`, `relationships/`
- PKI operations (sign, issue, revoke)
- Cert-auth entry management
- Policy management (mps-admin only)

Templated policies like `agents-rw`
(`{{identity.entity.aliases.<accessor>.name}}` scoping writes to own
row) continue to work; adding an entity to a group does not change
the entity's alias set, so the template resolution is unchanged.

## What Bao does not enforce

**Hardware `may-use--<device>` tuples are documentation.** Bao's API
surface has no relationship to GPU or NPU compute — those live in
CUDA drivers, Metal, HailoRT, whatever. A `hailo-552dfa--may-use--cpu`
tuple describes the workspace's expectation of HAILO's behaviour; it
does not stop HAILO's Python process from importing `torch` and
grabbing a CUDA device.

Two options for future enforcement of the hardware constraint, both
out of scope for this RFD:

1. **Compute-lease broker.** A service that hands out time-bounded
   GPU / NPU access grants; consults the tuples; refuses HAILO if
   it asks for a 3090 lease. Requires the broker be the only path
   to compute (no bare `torch.cuda.set_device()`).
2. **Convention + review.** Peer coordination messages flag when a
   role tries to use compute outside its `may-use` set. Cheap; only
   as strong as agent cooperation.

Convention + review is what the workspace does today. RFD 2200's
non-enforcement stance covers this.

## Membership provisioning + revocation lifecycle

**Provisioning** (adding a new agent):

1. Operator authorises identity per RFD 2195 rule zero.
2. MPS mints cert, publishes bundle to `certs/<cn>`, adds
   `runs-on` + `role` tuples to `relationships/`.
3. Reconciler picks up the new `role` tuple on next run, adds the
   new entity to the appropriate group, entity's next token
   inherits the group's policies.

**Revocation** (removing an agent):

1. MPS revokes cert per RFD 2195 Revocation section (CN narrowing
   or cert-auth entry delete).
2. MPS deletes `relationships/<agent>--role--*` tuples so the
   reconciler removes the entity from its group on the next run.
3. MPS deletes `agents/<agent>.agents.weftspun` and
   `certs/<agent>.agents.weftspun` KV rows.
4. Optionally delete the stale entity via
   `bao delete identity/entity/id/<eid>` if it will not be
   re-provisioned (2026-09-04: mps-dataset-68764 entity deleted
   this way).

## Bootstrap that landed with this RFD

Three groups created 2026-09-04, one member each:

    agents-coordinator      -> entity 714065ee (mps-45994b)
    agents-gpu-experimenter -> entity 17b34a2f (cuda-a63415)
    agents-assist           -> entity f92af0c7 (hailo-552dfa)

`agents-edge-qat-specialist` group is not created; no live agent
holds that role after HAILO's 2026-09-04 reassignment. It exists
in `ROLE_POLICIES` so a future role restoration is one tuple write
away.

The stale `entity_policies=[agents-rw]` on HAILO's entity from the
earlier debug session was left in place; the group grant covers it
redundantly. Not blocking; can be cleaned up by future reconciler
mode that strips redundant entity-level policies where a group
grant covers them. Not scoped here.

## Idempotency and the reconciler as anti-entropy

Running the reconciler with no changes prints
`ok  <group>: N member(s), no change` per group. Any drift between
tuples and group memberships surfaces as `DRIFT` with the specific
`+` / `-` entity ids. Running with `--apply` fixes the drift.

Suitable for periodic invocation from the coordinate-agents skill
(RFD 2201) as a step-8 addition — reconcile before closing the
pass. Not adding to that skill in this RFD; the skill's seven-step
scope lands separately when this is proven idempotent over a few
cycles.

## Reference invocation

    export BAO_ADDR=https://weftspun-bao.stonecat-ratio.ts.net:8200
    export BAO_CACERT=~/.bao-creds/ca-chain.pem
    export BAO_CLIENT_CERT=~/.bao-creds/mps-admin/cert-fullchain.pem
    export BAO_CLIENT_KEY=~/.bao-creds/mps-admin/key.pem
    export BAO_TOKEN=$(cat ~/.bao-creds/cert-session-token)
    python scripts/sync_rebac_groups.py
