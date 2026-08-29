# RFD 1088 details: every setup option, headset access, and troubleshooting

## Option 1: mkcert, the easiest path

1. Install `mkcert`: `choco install mkcert` on Windows, or download
   from its GitHub releases; `brew install mkcert` on macOS; see
   `mkcert`'s own installation guide on Linux.
2. Install the local CA: `mkcert -install`.
3. Generate certificates: `mkcert localhost 127.0.0.1 ::1 10.0.0.32`
   (that last address is an example LAN IP), producing
   `localhost+3.pem` and `localhost+3-key.pem`.
4. Move the certificates into the certs directory:

   ```bash
   mkdir certs
   mv localhost+3.pem certs/localhost.pem
   mv localhost+3-key.pem certs/localhost-key.pem
   ```

5. Restart the dev server: `npm run dev`.
6. Access over HTTPS: `https://localhost:3000`, or
   `https://10.0.0.32:3000` for a Galaxy XR device.

## Option 2: OpenSSL, one command

```bash
npm run setup-https
```

Generates certificates directly into `certs/`.

## Option 3: manual certificate generation

```bash
mkdir certs
openssl req -x509 -newkey rsa:4096 -keyout certs/localhost-key.pem -out certs/localhost.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

Restart the dev server; Vite picks up the certificates
automatically.

## The browser security warning

A self-signed certificate always triggers a warning. Click
"Advanced" or "Show Details", then "Proceed to localhost (unsafe)"
or "Accept the Risk and Continue". Safe for local development.

## Network access, for a Galaxy XR device

1. Put both devices on the same network.
2. Find the computer's own IP address (for example, `10.0.0.32`).
3. Add that IP to the certificate (see step 3 under mkcert, above).
4. Access `https://10.0.0.32:3000` on the Galaxy XR device.

## Troubleshooting

- Certificate errors: confirm the certificates sit in `certs/`, with the exact expected names.
- Connection refused: check firewall settings, and confirm port 3000 is open.
- WebXR still not working: confirm HTTPS, not HTTP, and confirm the certificate warning was accepted.
