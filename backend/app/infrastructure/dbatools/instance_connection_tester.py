import json
from pathlib import Path

from app.application.instances.dbatools import ConnectionTestResult
from app.domain.instances.models import Instance
from app.infrastructure.powershell.executor import PowerShellExecutor


class DbatoolsInstanceConnectionTester:
    """Tests registered SQL Server instances through the dbatools PowerShell module."""

    def __init__(self, executor: PowerShellExecutor, script_path: Path) -> None:
        self._executor = executor
        self._script_path = script_path

    async def test_connection(self, instance: Instance) -> ConnectionTestResult:
        result = await self._executor.execute_json(
            self._script_path,
            {
                "host": instance.host,
                "port": instance.port,
                "instanceName": instance.instance_name,
                "authenticationType": instance.authentication_type.value,
                "credentialId": str(instance.credential_id) if instance.credential_id else None,
            },
        )
        if result.exit_code != 0:
            return ConnectionTestResult(
                status="failed",
                version=None,
                edition=None,
                message="PowerShell/dbatools connection test failed.",
            )

        payload = json.loads(result.stdout)
        return ConnectionTestResult(
            status=payload["status"],
            version=payload.get("version"),
            edition=payload.get("edition"),
            message=payload["message"],
        )
