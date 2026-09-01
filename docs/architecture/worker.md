# Worker architecture

The Worker consumes durable jobs created by the API. It executes controlled PowerShell 7 processes and records stdout, stderr, exit code, timeout, cancellation, and parsed JSON result as structured job events.

PowerShell scripts must emit JSON, with secrets supplied through a credential-provider boundary rather than command-line arguments or logs. The dbatools adapter belongs in Infrastructure and implements application-facing interfaces such as `IDatabaseMigrationEngine`.
