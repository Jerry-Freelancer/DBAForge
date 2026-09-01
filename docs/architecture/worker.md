# Worker architecture

The Worker is an independent Python process that consumes durable jobs created by the API. It will execute controlled PowerShell 7 processes and record stdout, stderr, exit code, timeout, cancellation, and parsed JSON result as structured job events.

PowerShell scripts must emit JSON. Secrets must enter through a credential-provider boundary rather than command-line arguments or logs. The dbatools adapter belongs in Infrastructure and implements application-facing ports such as `DatabaseMigrationEngine`.
