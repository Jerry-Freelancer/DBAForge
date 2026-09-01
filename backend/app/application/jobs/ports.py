from typing import Protocol
from uuid import UUID

from app.domain.jobs.models import Job


class JobRepository(Protocol):
    async def enqueue(self, job: Job) -> Job: ...

    async def get(self, job_id: UUID) -> Job | None: ...

    async def claim_next(self) -> Job | None: ...

    async def complete(self, job: Job) -> Job: ...
