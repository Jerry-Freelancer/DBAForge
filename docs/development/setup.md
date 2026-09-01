# Development setup

Install Python 3.12+ and [uv](https://docs.astral.sh/uv/). Install PowerShell 7 and the `dbatools` module to run actual SQL Server connection checks. PostgreSQL is required for API instance persistence outside automated tests.

## Run checks without PostgreSQL or SQL Server

```bash
cd backend
uv sync --dev
uv run ruff check .
uv run pytest
```

The test suite uses a temporary SQLite database and a mocked PowerShell executor. It verifies API behavior, PostgreSQL-compatible persistence mapping, and the structured, non-secret dbatools payload without connecting to a real server.

## Run PostgreSQL, API, Worker, and dbatools with Docker

```bash
cp deploy/.env.example deploy/.env
# Set a local-only POSTGRES_PASSWORD in deploy/.env.
docker compose --env-file deploy/.env -f deploy/docker-compose.yml up --build
```

The Worker image installs PowerShell 7 and dbatools. After the API is available, register a Windows-authenticated SQL Server instance and run its connection test:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/instances \
  -H "Content-Type: application/json" \
  -d '{"name":"SQL01","host":"sql01.example.test","port":1433,"authentication_type":"windows"}'

curl -X POST http://127.0.0.1:8000/api/v1/instances/<instance-id>/test
```

The current dbatools script intentionally supports only Windows authentication. SQL credential resolution will be added through a credential-provider boundary; passwords must never be submitted to the API or the PowerShell script.
