# Backend architecture

FastAPI is the REST command/query boundary. It validates input, creates durable jobs, and returns state; it must not execute PowerShell processes in request handlers.

Future migration workflows use this sequence:

1. Discover source and destination metadata.
2. Validate compatibility and safety conditions.
3. Generate a read-only migration plan and PowerShell preview.
4. Require explicit confirmation.
5. Enqueue execution for the Worker.
6. Persist structured events and broadcast progress.

Long-running I/O must use async APIs. API logs must be structured and never contain credentials, passwords, or secret-reference values.
