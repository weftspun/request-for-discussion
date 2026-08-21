# RFD 106f details: the endpoint groups the removed reference held

`GET /health` and other system checks; optional token-based user
management, off by default (`user_auth_enabled`); a file upload
system returning file IDs, with a 24-hour cleanup; mesh generation,
by task type; mesh segmentation; auto-rigging; splat generation;
mesh editing, by text or image; mesh retopology; UV unwrapping;
worked workflow examples per task type; a named error-code table;
the spatial-fabric publish path (RP1/OMB); model preference
settings; and the file formats each endpoint group accepts.

Every response follows one shape: a job envelope
(`job_id`/`status`/`message`) on success, an error envelope
(`error`/`message`/`detail`) on failure.

A client developer who needs the exact request and response schema
for one of these groups reads `3DAIGC-API`'s own `/docs` (Swagger UI)
or `/redoc`, generated from the live server, not this page.
