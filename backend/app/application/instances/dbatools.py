from dataclasses import dataclass
from typing import Protocol

from app.domain.instances.models import Instance


@dataclass(frozen=True, slots=True)
class ConnectionTestResult:
    status: str
    version: str | None
    edition: str | None
    message: str


class InstanceConnectionTester(Protocol):
    async def test_connection(self, instance: Instance) -> ConnectionTestResult: ...
