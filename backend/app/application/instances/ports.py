from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from app.domain.instances.models import Instance


class InstanceRepository(Protocol):
    async def create(self, instance: Instance) -> Instance: ...

    async def get(self, instance_id: UUID) -> Instance | None: ...

    async def list(self) -> Sequence[Instance]: ...
