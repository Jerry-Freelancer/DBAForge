# DBAForge

**Open-source SQL Server DBA Automation Platform powered by dbatools.**

DBAForge makes complex SQL Server DBA operations discoverable, validated, planned, previewable, explicitly confirmed, executable, and auditable. It does not reimplement dbatools; dbatools is its first execution engine.

## Architecture

```text
React UI -> Python API -> PostgreSQL job queue -> Python Worker -> PowerShell 7 -> dbatools -> SQL Server
```

The Python API is the workflow control plane. The Worker is a separate process and is the only platform component that will execute controlled PowerShell jobs. This keeps REST requests short-lived and makes execution auditable and cancellable.

## Repository layout

| Path | Responsibility |
| --- | --- |
| `backend/app/api` | FastAPI REST endpoints and request/response boundaries. |
| `backend/app/application` | Workflow use cases and orchestration. |
| `backend/app/domain` | Technology-independent business rules and ports. |
| `backend/app/infrastructure` | PostgreSQL, PowerShell, and dbatools adapter implementations. |
| `backend/app/worker` | Independent durable-job worker host. |
| `backend/tests` | API and unit tests. |
| `powershell` | Structured-JSON PowerShell/dbatools scripts. |
| `deploy` | Container deployment assets. |

## Quick start

Install [uv](https://docs.astral.sh/uv/), then from the repository root run:

```bash
cd backend
uv sync --dev
uv run uvicorn app.main:app --reload
```

In a second terminal, verify the API:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"healthy"}
```

Run checks:

```bash
cd backend
uv run ruff check .
uv run pytest
```

## Containers

Start the API, Worker, and PostgreSQL development stack:

```bash
cp deploy/.env.example deploy/.env
# Edit deploy/.env and set a local-only PostgreSQL password.
docker compose --env-file deploy/.env -f deploy/docker-compose.yml up --build
```

## Test a registered SQL Server instance

The API does not run PowerShell. It stores a connection-test job in PostgreSQL, and the Worker claims that job before invoking dbatools. Register a Windows-authenticated instance:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/instances \
  -H "Content-Type: application/json" \
  -d '{"name":"SQL01","host":"sql01.example.test","port":1433,"authentication_type":"windows"}'
```

Copy the returned `id`, then queue a test and poll its job result:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/instances/<instance-id>/test
curl http://127.0.0.1:8000/api/v1/jobs/<job-id>
```

A queued job becomes `succeeded` or `failed` after the Worker runs `Connect-DbaInstance`. Current V1 connection testing intentionally supports Windows authentication only; no password is sent through the API or PowerShell script.

## Safety principles

- Never store plaintext passwords or write secrets to logs.
- Never execute PowerShell from the frontend or API request process.
- Keep discovery, validation, planning, preview, confirmation, and execution distinct.
- Keep dbatools details out of the domain model.
- Require explicit confirmation before destructive operations.
