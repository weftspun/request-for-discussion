# RFD 1003: Task Manager job lifecycle

**State:** published
**Feature:** task lifecycle

## Decision

Use one task lifecycle for all job types.

1. Create the task locally.
2. POST the job to the API.
3. Poll the job status until it completes or fails.
4. Store the result on the task row.

TaskManager owns HTTP and polling. TaskContext exposes the lifecycle
to React. The taskStore keeps the rows in memory.

Long jobs poll with a 3 second interval. The upload path falls back
from file id to base64 when the upload endpoint is unavailable.

## Problem

AI jobs run on a remote API. The API returns a job id and completes
later. The UI must poll, retry, and show progress.

## References

- Lifecycle: `src/library/taskManager.js`
- React hook: `src/context/TaskContext.jsx`
- Store: `src/stores/taskStore.js`
- API docs: `docs/api/api.md`

## Related

RFD 1004 catalogs the tasks that use this lifecycle.
