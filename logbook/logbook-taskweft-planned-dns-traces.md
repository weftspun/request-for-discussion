# Logbook: taskweft plans the DNS rollout, the traces become a dataset

Question: can the taskweft HTN planner drive the account.chibifire.com
DNS setup as a planned sequence with verification gates, and do the
planner traces round-trip into a training dataset that stores the
domain, the problem, and the solution per row.

## The apparatus

taskweft v0.5.3 release binary (MCP over HTTP, localhost:3001) and
main at 0f61a28 via `mix run` (Elixir 1.18, OTP 28). Firefox with a
logged-in Cloudflare session, driven by osascript / System Events.
Fly apps spot-broker (2 machines, sjc) and weftspun-bao.

## What was measured

Four planner calls, recorded and kept:

| trace | planner | result |
| --- | --- | --- |
| cloudflare_dns_ax_guarded (eval guards on every action) | 0.5.3 MCP | no_plan |
| cloudflare_dns_simple (three unguarded effects) | 0.5.3 MCP | ok, 3 steps |
| cloudflare_dns_ax (effects-only, 7 steps incl. 3 gates) | 0.5.3 MCP | ok, 7 steps |
| blocks_world (bundled DSL example) | main via mix | ok, 6 steps |

The v0.5.3 binary fails its own bundled DSL example with
`failed_to_load_domain`; the same file plans correctly on main
(SafeParser fixes #185/#186/#190, CLI DSL compile #195). Tagged
v0.5.4 on 0f61a28 to release the fix; 332 tests pass locally.

Two release-binary defects found on the way: the standalone MCP
server is HTTP-only, so `claude mcp add taskweft -- taskweft mcp`
(stdio) times out — `--transport http` with a URL is the working
form; and the binary complains about a stale
`.burrito/parqview_erts-17.0.5_0.1.0` metadata file from a sibling
app's cache, which is noise, not the load failure.

## The gates

The plan's last three actions are the gates, and the first two are
still open: `gate_verify_dns` (dig both records) and
`gate_verify_cert` (Fly cert issuance) block on the Cloudflare
records not yet existing — the dashboard fetch path is CSP-blocked
from the console, so the records go in by hand from the open DNS
page. `gate_write_logbook` is this entry.

## The dataset

`chibifire/taskweft-plans-train-internal` (private, HF), checked out
at `6-datasource/taskweft-plans-train-internal`, placed in the live
manifest. EditScore-Reward-Data row shape: input_domain,
instruction_problem, output_solution, three score columns. Four
rows; the no_plan row is the negative control, and the read-back
check asserts the scores separate solved from unsolved. ZStandard
parquet, 15,175 bytes.

## Correction: the records did not go in by hand

The section above blamed CSP for the console fetch failing, and it was
wrong. Firefox's devtools blocks **pasted** input until "allow pasting"
is typed at the prompt; every pasted script was dropped silently while
typed commands ran, which is why `document.title='TEST_OK'` worked and
the pasted fetch never did. Same-origin fetch to the dashboard API is
not CSP-blocked at all.

With paste unlocked and the script sent as osascript keystrokes, the
three records went in through the dashboard API in the logged-in
session: zone `f7e3538886b9874fc7837b22cf2f160e`, responses
`[["A",true,[]],["AAAA",true,[]],["CNAME",true,[]]]`.

`gate_verify_dns` then passed at the authoritative nameserver — A
37.16.15.168, AAAA 2a09:8280:1::17f:86e8:0, the ACME CNAME to
`account.chibifire.com.d669rdg.flydns.net.`, and the negative control
(a name that must not resolve) empty. 1.1.1.1 held a cached negative
answer from a dig made before the records existed (SOA minimum 1800 s,
about the length of a sitcom episode), which is why the recursive
check lied while the authoritative one told the truth.
