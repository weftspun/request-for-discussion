# RFD 1134: A loop notebook is tested in the browser

**State:** discussion
**Feature:** interactive test of the loop notebooks
**Scope:** `7-service/service-livebook`

## Problem

The four loop notebooks carried one check. `Livebook.LiveMarkdown.Import`
read each file and reported zero warnings. That check reads the file. It
never evaluates a cell.

A run in the browser found the difference. Evaluate all on loop 1 stops
at the fit cell, and Python reports `ModuleNotFoundError: No module named
'torch'`. The setup cell declares pillow, numpy and matplotlib only. The
four cells after it stayed queued and never ran.

A queued cell and a passing cell look the same in a screenshot. A silent
skip reads exactly like a pass.

## Decision

Test a notebook by evaluating it in the browser that serves it.
`SKILL.md` gives the order.

A headed Chromium runs on the desk display. Playwright attaches to that
window over a debug port. One window stays open across the steps, so a
person watches each cell and takes the keyboard at any point.

Report every cell by name and by state. Name each cell that never ran.
Do not average over the cells that did run.

The same run corrected the start command. `mix run --no-halt` in the dev
environment does not boot. `MIX_ENV=prod` is the command that serves.

See `DETAILS.md` for the apparatus and the defect in loop 1.

## Related

RFD 1122 states the wholebody gap that loop 1 serves.
