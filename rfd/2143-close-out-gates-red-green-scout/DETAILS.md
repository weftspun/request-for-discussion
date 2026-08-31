# RFD 2143 details: the reference case

The gates were first run — and backfilled — on the account.chibifire.com
DNS rollout. `logbook-taskweft-planned-dns-traces.md` holds the full
record; this file keeps the shape each gate takes.

## Red control gate

One command, the broken state, the observed failure:

    # taskweft v0.5.3 release binary, on its own bundled example
    taskweft plan priv/plans/domains/blocks_world_dsl.ex
    taskweft: failed_to_load_domain

## Green gate

The same command on the fixed state:

    # taskweft v0.5.4, same file
    taskweft plan priv/plans/domains/blocks_world_dsl.ex
    [["a_unstack", "a"], ["a_putdown", "a"], ...]

A green gate must tell the two states apart. The counterexample from
the reference case: an MCP `initialize` probe reported the same
serverInfo for v0.5.3 and v0.5.4, so it stayed green while a stale
v0.5.3 process held the port and the v0.5.4 launch died on
eaddrinuse into /dev/null. The qualifying probe plans a DSL domain
over MCP — an operation only the fixed build performs.

## Scout gate

Inventory before, non-empty; the same inventory after, empty; and
what improved beyond the task.

    # red side
    pgrep -fl "fly proxy"        →  18477 fly proxy 18300:8300
    ls /tmp/ff_cookies.sqlite    →  1.5 MB of session cookies in /tmp
    ls ~/Library/.../.burrito/   →  two stale payload directories

    # green side
    pgrep -fl "fly proxy"        →  (nothing)
    ls /tmp/ff_cookies.sqlite    →  (nothing)
    ls ~/Library/.../.burrito/   →  the current payload only

Beyond the task: the planner defect was fixed upstream and released
rather than worked around locally.

## What stays out of an RFD

Machine-local facts — ports, cache paths on one desk, credential
store contents, tokens — belong to the desk that produced them, not
to this record. The gate shapes above are the published part; the
values flow through a logbook entry when they are measurements, and
through nothing at all when they are secrets.
