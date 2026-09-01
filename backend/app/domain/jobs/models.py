from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class Job:
    id: UUID
    job_type: str
    status: JobStatus
    payload: dict[str, Any]
    result: dict[str, Any] | None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
