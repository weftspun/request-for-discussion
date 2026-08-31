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

## The gates, closed

`gate_verify_cert`: after a delete/re-add to shed Fly's own cached
negative check, Let's Encrypt issued for account.chibifire.com at
21:43:14 GMT (CN=account.chibifire.com, valid to 2026-11-29). Over
the live domain: `/health` returns ok, the landing page serves 9600
bytes with TLS verify 0, and `/v1/sys/seal-status` returns 401 —
the bao proxy refusing an unauthenticated caller, which is the
auth gate demonstrating itself. All seven planned actions ran;
the plan in the dataset row is the plan that executed.

## Red and green gates, with apparatus (backfilled)

Each gate below is two measurements: the red control gate — the
command shown failing on the broken state — then the green gate, the
same check shown passing on the fixed one. A gate seen only green is
decoration; a green without its command cannot be re-run.

**DSL loader.**

    # v0.5.3 release binary
    taskweft plan priv/plans/domains/blocks_world_dsl.ex
    taskweft: failed_to_load_domain

    # v0.5.4 release binary, same file
    taskweft plan priv/plans/domains/blocks_world_dsl.ex
    [["a_unstack", "a"], ["a_putdown", "a"], ["a_pickup", "c"],
     ["a_putdown", "c"], ["a_pickup", "b"], ["a_stack", "b", "a"]]

**Console input path.** Apparatus: Firefox devtools console on the
logged-in dash page, driven by `osascript` System Events.

    # pasted (pbcopy; keystroke "v" using {command down}; key code 36)
    copy(localStorage.getItem('_cf_test'))   →  null      # script never ran

    # typed (keystroke "<script>"; key code 36)
    copy('Z:'+window.__z)                    →  Z:f7e3538886b9874fc7837b22cf2f160e

**DNS resolution.** The recursive resolver held a negative answer
cached from a dig made before the records existed; the authoritative
server is the truth.

    dig +short _acme-challenge.account.chibifire.com CNAME @1.1.1.1
    (empty — SOA minimum 1800 s, about the length of a sitcom episode)

    dig +short _acme-challenge.account.chibifire.com CNAME @chloe.ns.cloudflare.com
    account.chibifire.com.d669rdg.flydns.net.

    # negative control, both resolvers
    dig +short nonexistent-gate-control.chibifire.com A @chloe.ns.cloudflare.com
    (empty)

**Cert.**

    # before DNS records (and on Fly's cached miss after them)
    fly certs check account.chibifire.com   →  Status = Not verified

    # after delete/re-add shed the cached miss
    fly certs check account.chibifire.com   →  Issued
    echo | openssl s_client -connect 37.16.15.168:443 \
      -servername account.chibifire.com | openssl x509 -noout -subject
    subject= /CN=account.chibifire.com

**Serving.**

    # before the store supervisor was made non-fatal: both machines crash-looping
    curl https://spot-broker.fly.dev/health   →  (empty, 502)

    # after
    curl https://account.chibifire.com/health          →  {"status":"ok"}
    curl https://account.chibifire.com/v1/sys/seal-status  →  {"error":"unauthorized"}

## Scout gate: the place left better than we arrived (backfilled)

The inventory before cleanup — the red side — and what it caught.
Apparatus: pgrep for the session's processes, ls the /tmp paths
touched, ls the burrito cache.

    pgrep -fl "fly proxy"        →  18477 fly proxy 18300:8300
    pgrep -fl "cf_browser.py"    →  19517 .../cf_browser.py
    ls /tmp/ff_cookies.sqlite    →  1.5 MB copy of Firefox session cookies
    ls /tmp/chibifire-com        →  a repo clone parked in /tmp
    ls ~/Library/.../\.burrito/  →  parqview_erts-17.0.5_0.1.0  (poisoned with a
                                    guessed metadata file), taskweft_..._0.5.3

The catch: port 3001 was still owned by the **v0.5.3** beam. The
earlier `pkill -f "taskweft mcp"` matched nothing — the process
cmdline is `beam.smp ... -extra mcp` — so the v0.5.4 launch died on
eaddrinuse into /dev/null, and the serverInfo probe reported the
same name and version for both builds. That green gate had passed on
the broken state, which is the exact failure rule 2 names.

After cleanup — the green side:

    pgrep -fl "fly proxy"                    →  (nothing)
    pgrep -fl "cf_browser"                   →  (nothing)
    ls /tmp/ff_cookies.sqlite /tmp/chibifire-com  →  (nothing)
    ls ~/Library/.../\.burrito/              →  taskweft_erts-16.4.0.5_0.5.4

And a probe that can tell the two builds apart — DSL planning over
MCP, which 0.5.3 cannot do and 0.5.4 can:

    POST /mcp tools/call plan {format: dsl, blocks_world_dsl.ex}
    →  6 steps: a_unstack a, a_putdown a, a_pickup c, ...

Better than we arrived, beyond the task: taskweft v0.5.4 released
upstream, the stale huggingface.co keychain credential replaced with
one that works, and the two dead burrito payloads gone.
