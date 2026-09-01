# Troubleshooting


## `IServiceCollection` or `Microsoft.Extensions` cannot be found

The Application and Infrastructure projects register services through dependency-injection extension methods. They explicitly reference the SDK-provided `Microsoft.AspNetCore.App` framework, so this requires no additional NuGet package. Pull the latest changes, then restore and run from the repository root:

```powershell
git pull
dotnet restore
dotnet run --project src/DBAForge.Api
```

## `NU1100` when starting the API

The initial scaffold targeted `net8.0`. A machine with only the .NET 10 SDK may not have the .NET 8 targeting packs installed, and an offline or restricted NuGet configuration cannot download them. DBAForge now targets `net10.0`, which uses the reference packs bundled with the .NET 10 SDK.

The repository includes `NuGet.Config` with the official `nuget.org` v3 feed so normal restores can resolve test dependencies. If the machine is intentionally offline, use a configured internal package mirror or an approved local NuGet cache before running the full test suite.

Run these commands from the repository root:

```powershell
dotnet restore
dotnet run --project src/DBAForge.Api
```

After the API reports that it is listening, query its health endpoint. In PowerShell, use `curl.exe` to invoke the actual curl binary rather than the `curl` alias:

```powershell
curl.exe http://localhost:5000/health
```
