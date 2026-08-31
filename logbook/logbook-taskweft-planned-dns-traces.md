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
