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
