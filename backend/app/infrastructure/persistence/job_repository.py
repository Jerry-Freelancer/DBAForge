from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.jobs.models import Job, JobStatus
from app.infrastructure.persistence.models import JobRecord


class SqlAlchemyJobRepository:
    def __init__(self, sessions: async_sessionmaker[AsyncSession]) -> None:
        self._sessions = sessions

    async def enqueue(self, job: Job) -> Job:
        async with self._sessions() as session:
            session.add(self._to_record(job))
            await session.commit()
        return job

    async def get(self, job_id: UUID) -> Job | None:
        async with self._sessions() as session:
            record = await session.get(JobRecord, job_id)
        return self._to_domain(record) if record else None

    async def claim_next(self) -> Job | None:
        async with self._sessions() as session:
            statement = (
                select(JobRecord)
                .where(JobRecord.status == JobStatus.QUEUED.value)
                .order_by(JobRecord.created_at)
                .with_for_update(skip_locked=True)
                .limit(1)
            )
            record = (await session.scalars(statement)).first()
            if record is None:
                return None
            record.status = JobStatus.RUNNING.value
            record.started_at = datetime.now(UTC)
            await session.commit()
            await session.refresh(record)
        return self._to_domain(record)

    async def complete(self, job: Job) -> Job:
        async with self._sessions() as session:
            record = await session.get(JobRecord, job.id, with_for_update=True)
            if record is None:
                raise RuntimeError("Cannot complete a missing job.")
            record.status = job.status.value
            record.result = job.result
            record.completed_at = job.completed_at
            await session.commit()
        return job

    @staticmethod
    def _to_record(job: Job) -> JobRecord:
        return JobRecord(
            id=job.id,
            job_type=job.job_type,
            status=job.status.value,
            payload=job.payload,
            result=job.result,
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at,
        )

    @staticmethod
    def _to_domain(record: JobRecord) -> Job:
        def utc_or_none(value: datetime | None) -> datetime | None:
            return (
                value.replace(tzinfo=UTC) if value is not None and value.tzinfo is None else value
            )

        return Job(
            id=record.id,
            job_type=record.job_type,
            status=JobStatus(record.status),
            payload=record.payload,
            result=record.result,
            created_at=utc_or_none(record.created_at),
            started_at=utc_or_none(record.started_at),
            completed_at=utc_or_none(record.completed_at),
        )
