# DBAForge Engineering Guide

## Project

DBAForge is an open-source SQL Server DBA automation platform. dbatools is the first execution engine, not the product boundary.

## Architecture

The frontend must never execute PowerShell directly:

`Frontend -> API -> Job Queue -> Worker -> PowerShell -> dbatools -> SQL Server`

- Keep dbatools- and PowerShell-specific code out of the Domain layer.
- Represent credentials only by references; never store or log a password.
- Separate discover, validate, plan, preview, confirmation, and execution stages.
- Require an explicit confirmation for destructive operations.

## Engineering rules

1. Use nullable reference types, implicit usings, asynchronous APIs, and cancellation tokens for long-running work.
2. Treat compiler warnings as errors.
3. Every endpoint requires automated coverage.
4. PowerShell integrations must return structured JSON; do not use textual console output as an API contract.
5. Every migration workflow supports a read-only plan/dry-run mode.
6. Use conventional commits.

## Commands

- Backend: `dotnet test`
- Frontend: `npm test`
- PowerShell: `Invoke-Pester`
