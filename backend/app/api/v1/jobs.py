from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.application.jobs.service import JobNotFoundError, JobService
from app.contracts.jobs import JobResponse

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])


def get_job_service(request: Request) -> JobService:
    return request.app.state.job_service


JobServiceDependency = Annotated[JobService, Depends(get_job_service)]


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: UUID, service: JobServiceDependency) -> JobResponse:
    try:
        job = await service.get(job_id)
    except JobNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found."
        ) from error
    return JobResponse.from_domain(job)
