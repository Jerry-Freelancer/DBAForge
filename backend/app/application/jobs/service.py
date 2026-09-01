from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from app.application.jobs.ports import JobRepository
from app.domain.jobs.models import Job, JobStatus


class JobNotFoundError(Exception):
    """Raised when a job cannot be found."""


class JobService:
    def __init__(self, repository: JobRepository) -> None:
        self._repository = repository

    async def enqueue_connection_test(self, instance_id: UUID) -> Job:
        now = datetime.now(UTC)
        return await self._repository.enqueue(
            Job(
                id=uuid4(),
                job_type="instance_connection_test",
                status=JobStatus.QUEUED,
                payload={"instance_id": str(instance_id)},
                result=None,
                created_at=now,
                started_at=None,
                completed_at=None,
            )
        )

    async def get(self, job_id: UUID) -> Job:
        job = await self._repository.get(job_id)
        if job is None:
            raise JobNotFoundError(job_id)
        return job

    async def claim_next(self) -> Job | None:
        return await self._repository.claim_next()

    async def complete(self, job: Job, *, status: JobStatus, result: dict[str, Any]) -> Job:
        completed = Job(
            id=job.id,
            job_type=job.job_type,
            status=status,
            payload=job.payload,
            result=result,
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=datetime.now(UTC),
        )
        return await self._repository.complete(completed)
