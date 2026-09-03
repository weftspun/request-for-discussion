# Expose weftspun-bao privately via Tailscale (no public IP)

## 0. Prereqs on your Tailscale admin console

- Create a **tag** for Fly machines: **Access controls → Tags** → add `tag:fly-bao`, owned by your user.
- **Machines → Auth keys → Generate auth key**
  - Reusable: **yes**
  - Ephemeral: **yes** (machine deregisters on shutdown)
  - Pre-approved: **yes**
  - Tags: `tag:fly-bao`
  - Copy the `tskey-auth-…` string.

## 1. Set the auth key as a Fly secret

```sh
flyctl secrets set TS_AUTHKEY=tskey-auth-XXXXXXXXXXXX --app weftspun-bao
```

## 2. Extend the OpenBao container

Add to `Dockerfile.fdb` (append to whatever's there now):

```dockerfile
# Tailscale
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl gnupg iptables && \
    curl -fsSL https://pkgs.tailscale.com/stable/debian/bookworm.noarmor.gpg \
      -o /usr/share/keyrings/tailscale-archive-keyring.gpg && \
    curl -fsSL https://pkgs.tailscale.com/stable/debian/bookworm.tailscale-keyring.list \
      -o /etc/apt/sources.list.d/tailscale.list && \
    apt-get update && apt-get install -y --no-install-recommends tailscale && \
    rm -rf /var/lib/apt/lists/*

# Replace whatever CMD/ENTRYPOINT you have with:
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

## 3. `entrypoint.sh`

```sh
#!/bin/sh
set -eu

# Start tailscaled in userspace-networking mode (no TUN needed on Fly VMs)
mkdir -p /var/lib/tailscale
/usr/sbin/tailscaled \
    --state=/var/lib/tailscale/tailscaled.state \
    --socket=/var/run/tailscale/tailscaled.sock \
    --tun=userspace-networking &

# Wait for it, then join the tailnet with the auth key
sleep 2
tailscale up \
    --authkey="${TS_AUTHKEY}" \
    --hostname=weftspun-bao \
    --advertise-tags=tag:fly-bao \
    --accept-dns=false

# Now run OpenBao (the original CMD)
exec dumb-init bao server -config=/bao/config/config.hcl
```

Notes:
- `--tun=userspace-networking` — Fly machines don't get `/dev/net/tun`; userspace tun works fine, just slightly slower.
- `--hostname=weftspun-bao` gives you the stable MagicDNS name `weftspun-bao.<your-tailnet>.ts.net`.
- Openbao still listens on `[::]:8200` inside the machine; Tailscale routes to it because it's in the same netns.

## 4. Deploy

```sh
flyctl deploy --app weftspun-bao
```

## 5. From any Tailscale peer

```sh
export BAO_ADDR=https://weftspun-bao.<tailnet>.ts.net:8200
export BAO_CACERT=~/.bao/ca-chain.pem
export BAO_CLIENT_CERT=~/.bao/cert.pem   # signed by that CA
export BAO_CLIENT_KEY=~/.bao/key.pem
bao status
```

The mTLS requirement in your listener config is unchanged — Tailscale is just the transport. Peers still need a client cert signed by `/bao/data/tls/ca-chain.pem`.

## 6. Client cert distribution (the remaining piece)

Two options:
- **Simple, small trust surface**: `flyctl ssh sftp shell -a weftspun-bao`, `get /bao/data/tls/cert.pem` + `key.pem` + `ca-chain.pem`, `chmod 600` on the laptop.  That cert is the machine's own cert — fine for a bootstrap admin, don't share it as an agent identity.
- **Proper**: enable bao's PKI secrets engine, issue per-agent client certs signed by the same CA (or a sub-CA). Then each Claude Code session mints its own cert on first run.

## 7. mTLS + Tailscale ACL — belt and suspenders

With mTLS enforced you can also lock down Tailscale ACLs so only your user's devices can reach `weftspun-bao:8200`. In the Tailscale admin console → **Access controls**:

```json
"acls": [
  { "action": "accept",
    "src": ["group:you"],
    "dst": ["tag:fly-bao:8200"] }
]
```

Now a rogue Tailscale device can't even open TCP to 8200, let alone attempt mTLS.

## 8. Multi-machine (later)

Your config already sets `min_machines_running: 3` (currently 1). When you scale (`flyctl scale count 3 -a weftspun-bao`), each machine joins Tailscale with its own `weftspun-XXXX` hostname. Point clients at any one, or use `weftspun-bao.internal:8200` (the Fly 6PN LB name) if the client is on Fly, or add all three as `--advertise-tags` peers behind a Tailscale Serve.

## Cheaper "dev" alternative that reuses zero Fly changes

Skip everything above and use `flyctl proxy 8200:8200 -a weftspun-bao` while you develop. It forwards localhost:8200 through Fly's WireGuard mesh — no public exposure, no container change. Only good for interactive use; a daemon that depends on it dies when you close the laptop.

## Gotchas that cost the setup an hour each

Six backlog items from the first two agents running against this. Each is a
one-line footgun that reads as an unrelated problem until you know it.

### Client cert must include the intermediate

Bao's listener trusts only the Root CA. A client that presents only its
leaf cert is rejected with `unknown certificate authority`, even though the
leaf is validly signed. Bao expects the client to include the intermediate
in its own chain.

    cat leaf.pem intermediate.pem > client-fullchain.pem
    export BAO_CLIENT_CERT=client-fullchain.pem

The same shape bites the listener the other way: full-chain the server cert
too, or clients see the same error against your Bao.

### Cert-auth alias name is the full CN; KV keys mirror it

The templated policy at `auth/cert/certs/agents-weftspun` uses
`{{identity.entity.aliases.<accessor>.name}}`, and that resolves to the
alias's Name field, which cert-auth populates with the CN. Bao does not
strip a trailing suffix. Two conventions have to line up:

- CN in the CSR is the full `<short>.agents.weftspun` form.
- KV keys under `agents/` use the same full-CN form (`agents/mps-45994b.agents.weftspun`), not the short form.

Mixing shapes makes the templated write silently no-op — the policy
resolves to `agents/mps-45994b.agents.weftspun` and your session's write
to `agents/mps-45994b` gets 403.

### Named grant `agents/data/+ read` for peer visibility

Templated per-agent write isolates *writes* to your own row, but it also
prevents you seeing peers' rows. Add a separate grant to the same policy:

    path "agents/data/+" { capabilities = ["read"] }
    path "agents/metadata" { capabilities = ["list"] }

Now every agent can see the coordination store; only its own row is
writable.

### `flyctl ssh console -C "cat file" | head` truncates on SIGPIPE

`flyctl ssh console -C "cat /some/big/file" | tee copy | head -3` returns
truncated stdout because the SSH stream races the pipe. The fix is
write-then-read:

    flyctl ssh console -C "cat /some/big/file" > local.copy
    head -3 local.copy

Same for any long stdout through `flyctl ssh console -C`.

### `openssl req -subj "/CN=..."` mangles on Git-Bash

MSYS silently rewrites `/CN=weftspun-bao` to a filesystem path when the
argument starts with a single slash. The resulting cert has `CN=
C:\...\CN=weftspun-bao` or similar. Escape with a double slash:

    openssl req -new -key key.pem -subj "//CN=weftspun-bao.internal" ...

Same for every `-subj` on Git-Bash. Native shells (zsh, POSIX sh under
WSL) do not need this.

### Rule zero: every live session gets an identity

Formalised in `weftspun/dot-claude` PR #15's `agent-sync.md` skill body.
The rule: every session that appears in `ListAgents` gets a Bao client
cert and a `agents/<cn>.agents.weftspun` KV row, minted by whichever
session holds the admin policy (currently `mps-45994b` via
`auth/cert/certs/mps-45994b`). Read-only policy is fine as a first grant;
write is deferred until the operator or the session itself asks for it.
The provisioning bundle lands in 1Password (`agent-cert <cn>` item) and
the receiving session's first action is `bao login` against it.

## Revocation

The Bao cert-auth method does not consult CRLs by default. `pki/revoke
serial_number=<X>` records the revocation in the PKI store but does not
gate access — a revoked cert still authenticates until you take one of
these steps:

1. **Narrow the cert-auth entry's `allowed_common_names`** to exclude the
   revoked CN. Immediate effect, no reload needed. Best for revoking one
   CN from a shared wildcard entry (e.g. change `*.agents.weftspun` to
   `cuda-a63415.agents.weftspun` when revoking mps-dataset).
2. **Delete the cert-auth entry** entirely (`bao delete
   auth/cert/certs/<name>`). Immediate effect. Best when revoking every
   identity that authed through that entry.
3. **Enable CRL consultation** via `auth/cert/crls/<name>` and reload the
   CRL after every revoke. Correct but higher operational load and the
   default intermediate here reports `error building CRLs: x509: issuer
   certificate doesn't contain a subject key identifier` — a re-issue of
   the intermediate is needed before this path works.

Options 1 and 2 are what we use. The KV row also gets deleted (`bao kv
metadata delete agents/<cn>.agents.weftspun`) so peers don't see a stale
identity. The 1Password item is annotated REVOKED with the reason and the
cert body kept for audit.
