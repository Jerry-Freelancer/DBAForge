import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from app.domain.instances.models import AuthenticationType, Instance
from app.infrastructure.dbatools import DbatoolsInstanceConnectionTester
from app.infrastructure.powershell.executor import PowerShellResult


class FakePowerShellExecutor:
    def __init__(self) -> None:
        self.payload: dict[str, object] | None = None

    async def execute_json(self, script: Path, payload: dict[str, object]) -> PowerShellResult:
        self.payload = payload
        return PowerShellResult(
            exit_code=0,
            stdout=json.dumps(
                {
                    "status": "success",
                    "version": "16.0",
                    "edition": "Enterprise Edition",
                    "message": "Connected",
                }
            ),
            stderr="",
        )


@pytest.mark.anyio
async def test_dbatools_tester_exchanges_only_non_secret_json() -> None:
    executor = FakePowerShellExecutor()
    tester = DbatoolsInstanceConnectionTester(executor, Path("Test-DBAForgeConnection.ps1"))
    now = datetime.now(UTC)
    instance = Instance(
        id=uuid4(),
        name="SQL01",
        host="sql01.example.test",
        port=1433,
        instance_name=None,
        authentication_type=AuthenticationType.WINDOWS,
        credential_id=uuid4(),
        is_enabled=True,
        created_at=now,
        updated_at=now,
    )

    result = await tester.test_connection(instance)

    assert result.status == "success"
    assert executor.payload == {
        "host": "sql01.example.test",
        "port": 1433,
        "instanceName": None,
        "authenticationType": "windows",
        "credentialId": str(instance.credential_id),
    }
