from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.instances.models import AuthenticationType, Instance
from app.infrastructure.persistence.models import InstanceRecord


class SqlAlchemyInstanceRepository:
    def __init__(self, sessions: async_sessionmaker[AsyncSession]) -> None:
        self._sessions = sessions

    async def create(self, instance: Instance) -> Instance:
        record = InstanceRecord(
            id=instance.id,
            name=instance.name,
            host=instance.host,
            port=instance.port,
            instance_name=instance.instance_name,
            authentication_type=instance.authentication_type.value,
            credential_id=instance.credential_id,
            is_enabled=instance.is_enabled,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )
        async with self._sessions() as session:
            session.add(record)
            await session.commit()
        return instance

    async def get(self, instance_id: UUID) -> Instance | None:
        async with self._sessions() as session:
            record = await session.get(InstanceRecord, instance_id)
        return self._to_domain(record) if record else None

    async def list(self) -> Sequence[Instance]:
        async with self._sessions() as session:
            result = await session.scalars(select(InstanceRecord).order_by(InstanceRecord.name))
            records = result.all()
        return [self._to_domain(record) for record in records]

    @staticmethod
    def _to_domain(record: InstanceRecord) -> Instance:
        return Instance(
            id=record.id,
            name=record.name,
            host=record.host,
            port=record.port,
            instance_name=record.instance_name,
            authentication_type=AuthenticationType(record.authentication_type),
            credential_id=record.credential_id,
            is_enabled=record.is_enabled,
            created_at=SqlAlchemyInstanceRepository._as_utc(record.created_at),
            updated_at=SqlAlchemyInstanceRepository._as_utc(record.updated_at),
        )

    @staticmethod
    def _as_utc(value: datetime) -> datetime:
        return value.replace(tzinfo=UTC) if value.tzinfo is None else value
