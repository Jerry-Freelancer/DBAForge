# ADR 0001: Use Clean Architecture boundaries

**Status:** Accepted

DBAForge uses separate Domain, Application, Infrastructure, API, Worker, and Contracts projects. This keeps SQL Server and dbatools implementation details replaceable and prevents UI/API concerns from entering workflow business rules.
