# Architecture overview

DBAForge is a workflow and safety platform for SQL Server DBA operations. It delegates database-specific execution to adapters such as dbatools rather than recreating their capabilities.

## Runtime flow

```text
React UI -> ASP.NET Core API -> persisted job -> Worker -> PowerShell 7 -> dbatools -> SQL Server
```

The API owns workflow state and exposes REST endpoints plus SignalR progress. Workers own long-running execution. PostgreSQL persists platform state, audit records, jobs, and logs; it is not a SQL Server dependency.

## Layering

- **Domain** contains technology-independent entities, value objects, and interfaces.
- **Application** orchestrates use cases and depends only on Domain and Contracts.
- **Infrastructure** implements persistence and execution adapters.
- **Api** provides HTTP/SignalR composition and authentication boundaries.
- **Worker** hosts queued background processing.

The first delivered API contract is `GET /health`. Domain and application projects deliberately contain no dbatools references.
