from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.application.instances.ports import InstanceRepository
from app.domain.instances.models import AuthenticationType, Instance


class InstanceNotFoundError(Exception):
    """Raised when an instance cannot be found."""


class InstanceService:
    def __init__(self, repository: InstanceRepository) -> None:
        self._repository = repository

    async def create(
        self,
        *,
        name: str,
        host: str,
        port: int | None,
        instance_name: str | None,
        authentication_type: AuthenticationType,
        credential_id: UUID | None,
    ) -> Instance:
        now = datetime.now(UTC)
        instance = Instance(
            id=uuid4(),
            name=name,
            host=host,
            port=port,
            instance_name=instance_name,
            authentication_type=authentication_type,
            credential_id=credential_id,
            is_enabled=True,
            created_at=now,
            updated_at=now,
        )
        return await self._repository.create(instance)

    async def get(self, instance_id: UUID) -> Instance:
        instance = await self._repository.get(instance_id)
        if instance is None:
            raise InstanceNotFoundError(instance_id)
        return instance

    async def list(self) -> list[Instance]:
        return list(await self._repository.list())
