# Development setup

Install the .NET 8 SDK, Node.js 20+, PowerShell 7, and PostgreSQL before running the full platform. The initial backend can be validated with:

```bash
dotnet test
```

The production worker additionally requires PowerShell 7 and the dbatools module. No SQL Server credentials should be committed to local configuration or test fixtures.
