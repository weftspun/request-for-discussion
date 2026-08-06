# RFD 0116: Tasks panel, Clear unloads the model, done stays separate

**State:** committed
**Scope:** Tasks panel toolbar, the completed-task list

## Problem

The Tasks panel carries two controls a rewrite kept conflating: a
collapse toggle on the completed-task list, and a Clear action.
Clear must unload the viewport model, matching the Worlds panel's
own Clear. A rewrite twice narrowed Clear back down to clearing the
task list alone, and once dropped the completed-list collapse
control outright.

## Decision

The completed-task list collapses through `expand-icon-button` and
`task-completed-expand-btn`, the same pattern the Bone Structure
panel uses. Clear calls `clearModel()` whenever `currentModel` is
set, unloading the viewport, then calls `clearCompletedTasks()`,
which removes only the completed rows from the list. Task history
outside the completed rows survives a viewport Clear.

`bash scripts/verify_tasks_panel_ui.sh` runs before a merge touching
this toolbar.

## Related

RFD 0003 gives the task lifecycle this panel displays. RFD 0112
lists `tasks-panel-ui-protected.mdc`, the rule this RFD replaces.
