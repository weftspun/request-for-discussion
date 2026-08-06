# RFD 0088: HTTPS for local WebXR development

**State:** published
**Scope:** the Vite dev server, `certs/`

## Problem

WebXR needs HTTPS. A plain `npm run dev` over HTTP cannot open an
AR or VR session at all, on a desktop browser or on a Galaxy XR
headset over the LAN.

## Decision

Generate a local certificate into `certs/`, and let Vite pick it up
automatically. `mkcert` is the recommended path: install it, run
`mkcert -install` once for the local CA, then `mkcert localhost
127.0.0.1 ::1 <LAN-IP>` for a certificate that also covers the
headset's LAN address. An OpenSSL path (`npm run setup-https`, or a
manual `openssl req`) covers a host without `mkcert`. A self-signed
certificate still shows a browser warning; accepting it is safe for
local development.

See `DETAILS.md` for every option's exact commands, the headset
network-access steps, and troubleshooting.

## Related

**Unresolved duplicate:** weftspun-3d-studio's own
`thirdparty/m3/docs/HTTPS_SETUP.md` covers the same topic, with real
content differences. Neither version is authoritative; that
reconciliation is still open. RFD 0086 gives the Surface/DGX/headset
topology this certificate serves.
