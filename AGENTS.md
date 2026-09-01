# DBAForge Engineering Guide

## Project

DBAForge is an open-source SQL Server DBA automation platform. dbatools is the first execution engine, not the product boundary.

## Architecture

The frontend must never execute PowerShell directly:

`Frontend -> Python API -> Job Queue -> Worker -> PowerShell -> dbatools -> SQL Server`

- Keep dbatools- and PowerShell-specific code out of the Domain layer.
- Represent credentials only by references; never store or log a password.
- Separate discover, validate, plan, preview, confirmation, and execution stages.
- Require an explicit confirmation for destructive operations.

## Engineering rules

1. Use Python 3.12+, type hints, asynchronous APIs, and cancellation-aware long-running jobs.
2. Use ruff and pytest; CI must fail on lint or test failures.
3. Every API endpoint requires automated coverage.
4. PowerShell integrations must return structured JSON; do not use textual console output as an API contract.
5. Every migration workflow supports a read-only plan/dry-run mode.
6. Use conventional commits.

## Commands

- Backend setup: `cd backend && uv sync --dev`
- Backend test: `cd backend && uv run pytest`
- Backend lint: `cd backend && uv run ruff check .`
- PowerShell: `Invoke-Pester`
