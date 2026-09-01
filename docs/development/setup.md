# Development setup

Install Python 3.12+ and [uv](https://docs.astral.sh/uv/). PowerShell 7, dbatools, and PostgreSQL are required when building the execution worker.

From the repository root:

```bash
cd backend
uv sync --dev
uv run ruff check .
uv run pytest
uv run uvicorn app.main:app --reload
```

No SQL Server credentials, connection strings, or production backup locations may be committed to local configuration or test fixtures.
