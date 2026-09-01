[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

try {
    $request = [Console]::In.ReadToEnd() | ConvertFrom-Json
    if ($request.authenticationType -ne 'windows') {
        throw 'SQL authentication requires the credential provider and is not yet enabled.'
    }

    $sqlInstance = $request.host

    if ($request.instanceName) {
        $sqlInstance = "$sqlInstance\$($request.instanceName)"
    }

    if ($request.port) {
        $sqlInstance = "$sqlInstance,$($request.port)"
    }

    # Credentials are resolved by the Worker credential provider in a later milestone.
    # This script never accepts a password, credential value, or connection string from stdin.
    $server = Connect-DbaInstance -SqlInstance $sqlInstance

    [pscustomobject]@{
        status  = 'success'
        version = $server.VersionString
        edition = $server.Edition
        message = "Connected to $sqlInstance"
    } | ConvertTo-Json -Compress
}
catch {
    [pscustomobject]@{
        status  = 'failed'
        version = $null
        edition = $null
        message = 'dbatools connection test failed.'
    } | ConvertTo-Json -Compress
    exit 1
}
