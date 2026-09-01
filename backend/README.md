# DBAForge backend

The Python backend contains the API control plane and a separate worker process. PowerShell and dbatools execution will be implemented behind infrastructure ports; API handlers never run PowerShell directly.
