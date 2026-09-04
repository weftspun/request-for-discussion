# ReBAC agent roles — tuples, roles, and what enforcement would look like

## The tuple shape

Each tuple is one KV row under `relationships/`. Key format is
`<subject>--<verb>--<object>` (double-hyphen separator, all segments
lowercase-kebab). Data is the parsed fields plus a timestamp:

    subject: mps-45994b
    verb: authors
    object: weftspun-agreements
    created_at: <unix>

Verbs currently used:

| verb | meaning |
|---|---|
| `authors` | the subject drafts and owns retractions for the object (docs, experiments, RFDs) |
| `admin` | the subject holds administrative capability over the object (Bao PKI, cert-auth, mount config) |
| `owns` | the subject holds and operates the object as hardware (a GPU card, an NPU) |
| `runs-on` | the subject's Claude Code process is hosted on the object machine |
| `hosts` | inverse of `runs-on`, from the host side; makes queries "who is on host X" cheap |

Verb vocabulary is small on purpose. A new verb costs an RFD amendment;
overloading existing verbs is fine when the mapping is obvious.

## The three roles

**Coordinator** — MPS. Bao admin (`mps-admin` policy). Authors
`weftspun-agreements` (CLAUDE.md, RFDs, doctrine, retraction pointers).
Provisions agent identities on operator instruction. Drafts logbook
entries **only** when relaying a peer's measurement, with the peer
credited as the measuring session. Does not own ML hypotheses; does not
run GPU experiments; does not touch peer hardware.

**GPU-experimenter** — CUDA. Owns 3090 + 4090. Authors
`gpu-experiments` — Lumina2 distillation, LLaDA-o step sweeps, OmniGen2
comparisons, EditScore ladder runs. Publishes measurements as logbook
PRs on its own branches; drafts + files its own retractions when a
result doesn't survive scale-up. `agents-rw` policy; no admin ops
(no mint, no revoke, no policy edit).

**Edge-QAT-specialist** — HAILO. Owns USB-Hailo NPU. Authors
`edge-qat-experiments` — RFD 2199 direction, HailoRT + DFC compiler
work, HEF deployment. Same PR-driven measurement discipline as
gpu-experimenter. `agents-rw` policy; does not touch CUDA's cards, and
CUDA does not touch the Hailo NPU, even though both agents `runs-on`
the same `windows-desktop`.

## What the tuples buy that RBAC doesn't

**Composability.** "CUDA touches the 3090" is not a permission written
into a policy; it is `cuda-a63415 owns desktop-3090` and a general rule
"an agent's `owns` relations bound the hardware it can drive." Adding
a fourth agent that inherits GPU access means adding `<new>--owns--
<card>`, not editing a policy.

**Cross-cutting constraints from graph traversal.** The shared-$HOME
risk that killed CUDA's key earlier today is graph-reachable:

    ?x runs-on ?h  AND  ?y runs-on ?h  AND  ?x != ?y

resolves to `(cuda-a63415, hailo-552dfa, windows-desktop)`. A future
onboarding flow can check "does this new agent share a host with an
existing agent?" mechanically from the tuples, and if so require the
per-agent-suffixed cred dir before enrolment. RBAC has no way to
express that.

**Retraction responsibility.** When an RFD is retracted, the doctrine
in CLAUDE.md says the pointer names the logbook entry that carries the
measurement. `authored-by` tuples on the RFD and the logbook entry
resolve to the same agent, so the pointer's target is not a lookup;
it is the second tuple that shares a subject with the first.

## What the tuples do not do today

No policy consults them. `agents-rw` still writes based on identity
templating, not tuple membership. This RFD lands the **schema and the
tuples**, not enforcement.

Enforcement would need one of:

1. **Client-side check in the agent-sync skill.** Read
   `relationships/*` on startup, memoise, refuse local operations
   that would violate a tuple relation. Cheap; only as strong as
   agent cooperation.
2. **Bao Sentinel or a custom auth method** that consults
   `relationships/` before granting a write. Requires either Bao
   Enterprise or a shim.
3. **A separate ReBAC engine** (OpenFGA, SpiceDB, Zanzibar-alike) as
   the source of truth; Bao KV becomes cache. Correct long-term shape
   at the cost of a second service.

None of the three ships in this RFD. The tuples come first because
storing the relationships is the small commitment that any of the
three build on. Enforcement is a separate call and a separate RFD.

## The extend flow

Adding a new agent:

1. Operator authorises identity (per RFD 2195 rule zero).
2. Admin (MPS) mints cert, publishes bundle to `certs/<cn>`.
3. **Admin writes the new agent's tuples to `relationships/`** in
   the same session — at minimum a `runs-on` tuple, plus the
   `owns` and `authors` tuples that scope the new agent's role.
4. If a `runs-on` shares a host with an existing agent, admin
   confirms the new agent will use a per-agent-suffixed cred dir
   before completing onboarding.
5. Agent writes its first KV row to `agents/<cn>.agents.weftspun`.

Removing an agent (revocation):

1. Admin revokes cert per RFD 2195's Revocation section.
2. Admin deletes tuples where the revoked agent is `subject` (its
   claims stop being active) but preserves tuples where the revoked
   agent is `object` (so `windows-desktop hosts cuda-a63415`
   survives if we're just revoking CUDA, and the tuple gets deleted
   on the same step as CUDA's other row cleanups).

## Enumerating current relationships

Cheap `bao kv list relationships/` followed by per-tuple read:

    for k in $(bao kv list -format=json relationships/ | jq -r '.[]'); do
      bao kv get -field=subject relationships/$k
      bao kv get -field=verb    relationships/$k
      bao kv get -field=object  relationships/$k
    done

A `list_agent_roles.py` helper would do this more efficiently
against the API; not written today.
