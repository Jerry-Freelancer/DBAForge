# Backend architecture

The ASP.NET Core API is the command and query boundary. It must validate input, create durable jobs, and return state; it must not start PowerShell processes in request handlers.

Future workflow endpoints use the sequence:

1. Discover source and destination metadata.
2. Validate compatibility and safety conditions.
3. Generate a read-only migration plan and PowerShell preview.
4. Require explicit confirmation.
5. Enqueue execution for the Worker.
6. Persist structured events and broadcast progress over SignalR.

Every long-running API and application operation accepts a `CancellationToken`. API logs must use structured logging and must never contain a credential, secret reference value, or generated connection password.
