# ADR 0001: Use Python ports-and-adapters boundaries

**Status:** Accepted

DBAForge uses API, Application, Domain, Infrastructure, and Worker Python packages. This keeps dbatools and PowerShell implementation details replaceable and prevents UI/API concerns from entering workflow business rules.

The control plane uses Python to simplify local and container deployment. PowerShell 7 and dbatools remain the execution engine behind a dedicated Worker boundary.
