---
name: livebook-notebook-in-the-browser
description: Evaluate a Livebook notebook in a headed browser on the desk display, and report each cell by state. Use when somebody asks to test a loop notebook interactively, and whenever a notebook is said to work because it imports without warnings.
---

# Running a loop notebook in the browser

The result is a per-cell state, not an impression. If the procedure ends
with a screenshot of the top of the notebook, it was not this procedure.

## Order

1. **Start the server in the prod environment.** `MIX_ENV=prod mix run
   --no-halt -e 'IO.puts ServiceLivebook.start()'` from
   `7-service/service-livebook`. The dev environment does not boot. Read
   the token URL out of the log.
2. **Ask the health endpoint, not the log.** `/public/health` returns 200
   when the server serves. A log line says only that a start was
   attempted.
3. **Put a headed Chromium on the display.** Launch with Playwright,
   `headless: false`, and `--remote-debugging-port=9222`. Visit the token
   URL once. That visit authenticates the session.
4. **Attach to the same window for each later step.**
   `chromium.connectOverCDP` finds the open page. A second launch opens a
   second window and loses the session.
5. **Open the notebook by path.** Go to `/open?path=<absolute path>`.
   Build the path from parts and join them, because a backslash inside a
   string is an escape and a lost backslash gives a silent redirect back
   to the open dialog.
6. **Evaluate with Livebook's own keys.** Press Escape for navigation
   mode, then `e`, then `a`. The run then takes the path a person's
   keystrokes take.
7. **Read every cell, and name the state of each.** Query
   `[data-el-cell]` and read the text. `Evaluated` with a traceback is a
   failure. `Evaluate` alone means the cell never ran.

## Traps

A queued cell that never ran is NOT_RUN. It is never a pass.

Do not close a browser that Playwright reached over CDP. The close
command ends the window the person is watching.

A notebook that imports with zero warnings has not run. The import reads
the file. Only evaluation runs a cell.

The setup cell states the Python packages for the notebook process. A
cell that imports a package outside that list fails, whatever the pixi
environments hold.

Point `PHOTO` at a real photograph before you read a score. Never point
it at `coco_person_commercial_val2017`, which is the blinded holdout.
