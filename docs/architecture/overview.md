# Architecture overview

DBAForge is a workflow and safety platform for SQL Server DBA operations. It delegates database-specific execution to adapters such as dbatools rather than recreating their capabilities.

## Runtime flow

```text
React UI -> FastAPI -> PostgreSQL job queue -> Python Worker -> PowerShell 7 -> dbatools -> SQL Server
```

The API owns workflow state and exposes REST endpoints plus future realtime progress. Workers own long-running execution. PostgreSQL persists platform state, audit records, jobs, and logs; it is not a SQL Server dependency.

## Boundaries

- **API** validates HTTP requests and enqueues work; it never starts PowerShell.
- **Application** orchestrates use cases and depends on domain ports.
- **Domain** contains technology-independent entities, value objects, policies, and ports.
- **Infrastructure** implements PostgreSQL, PowerShell, and dbatools adapters.
- **Worker** claims durable jobs and hosts controlled execution.

PowerShell/dbatools remain outside the domain. Scripts return structured JSON, which adapters map to application results.
