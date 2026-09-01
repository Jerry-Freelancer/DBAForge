# DBAForge

**Open-source SQL Server DBA Automation Platform powered by dbatools.**

DBAForge turns complex DBA operations into workflows that can be discovered, validated, planned, previewed, explicitly confirmed, executed, and audited. It does not attempt to reimplement dbatools; dbatools is the first execution engine behind the platform.

## Initial architecture

```text
React UI -> ASP.NET Core API -> Job Queue -> Worker -> PowerShell 7 -> dbatools -> SQL Server
                              |
                         PostgreSQL
```

The initial foundation provides a Clean Architecture backend solution, structured Serilog request logging, a health endpoint, a hosted Worker skeleton, test projects, and CI.

## Projects

| Project | Responsibility |
| --- | --- |
| `DBAForge.Domain` | Technology-independent domain model and interfaces. |
| `DBAForge.Application` | Workflow use cases and orchestration. |
| `DBAForge.Infrastructure` | Persistence, PowerShell, and dbatools adapter implementations. |
| `DBAForge.Api` | REST, SignalR, and application composition. |
| `DBAForge.Worker` | Durable background job execution host. |
| `DBAForge.Contracts` | Cross-boundary request/response contracts. |

## Run locally

Install the .NET 8 SDK, then run:

```bash
dotnet run --project src/DBAForge.Api
curl http://localhost:5000/health
```

Run the test suite with:

```bash
dotnet test
```

See [development setup](docs/development/setup.md) and the [architecture overview](docs/architecture/overview.md) for prerequisites and design decisions.

## Safety principles

- Never store plaintext passwords or write secrets to logs.
- Never execute PowerShell directly from the frontend or API request pipeline.
- Keep discovery, validation, planning, preview, confirmation, and execution distinct.
- Keep dbatools details out of the domain model.
- Require explicit confirmation before destructive operations.
