from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel

from app.domain.jobs.models import Job


class JobResponse(BaseModel):
    id: UUID
    job_type: str
    status: str
    payload: dict[str, Any]
    result: dict[str, Any] | None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None

    @classmethod
    def from_domain(cls, job: Job) -> "JobResponse":
        return cls(
            id=job.id,
            job_type=job.job_type,
            status=job.status.value,
            payload=job.payload,
            result=job.result,
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at,
        )
