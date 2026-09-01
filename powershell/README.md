# DBAForge PowerShell scripts

Scripts in this directory are invoked only by the dedicated Worker through standard input/output JSON. They must never accept, emit, or log a password, secret, or connection string.

`DBAForge/Test-DBAForgeConnection.ps1` uses `Connect-DbaInstance` to test a Windows-authenticated SQL Server connection and emits one JSON result. SQL-authentication credentials are intentionally not implemented until a secure credential-provider boundary is available.
