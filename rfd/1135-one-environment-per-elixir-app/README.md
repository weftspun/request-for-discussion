# RFD 1135: One Python environment per Elixir app

**State:** discussion
**Feature:** how an Elixir app reaches Python
**Scope:** `7-service/service-livebook`

## Decision

An Elixir app reaches Python through pythonx and through nothing else.
`priv/python/check_pixi_free.py` fails the build on a call to the other
environment manager, and it reads prose without complaining, so the rule
stays writable.

An embedded interpreter starts once, with one dependency set. So a second
dependency set is a second app: its own mix project, its own setup cell,
its own runtime. The gate holds that too. It reads the `pyproject.toml`
cell of every notebook in an app and fails when two of them differ.

This is what the corpus repository's environments were for. OmniGen2 pins
torch 2.6.0+cu124 and EditScore pins cu128, and no interpreter holds
both. That separation stays, as apps beside each other rather than
environments inside one app. The corpus repository keeps its own
environments, and what is forbidden is this app calling into them.

## Problem

`service-livebook` embeds a Python interpreter with `pythonx`. Its setup
cell names the packages and the pins travel in the notebook file. Beside
that, a helper shelled into five environments in another repository. The
notebook described three packages while the loop depended on five
environments it never names, so it ran on one desk and nowhere else.

The failure was not theoretical. Loop 1 stopped with `No module named
'drjit'`, because it called the `anny` environment for a renderer that
only the default environment carries. The notebook cannot show that.

## Related

RFD 1134 tests these notebooks in the browser, which is how the missing
renderer was found.
