from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.application.instances.service import InstanceNotFoundError, InstanceService
from app.application.jobs.service import JobService
from app.contracts.instances import CreateInstanceRequest, InstanceResponse
from app.contracts.jobs import JobResponse

router = APIRouter(prefix="/api/v1/instances", tags=["instances"])


def get_instance_service(request: Request) -> InstanceService:
    return request.app.state.instance_service


def get_job_service(request: Request) -> JobService:
    return request.app.state.job_service


InstanceServiceDependency = Annotated[InstanceService, Depends(get_instance_service)]
JobServiceDependency = Annotated[JobService, Depends(get_job_service)]


@router.post("", response_model=InstanceResponse, status_code=status.HTTP_201_CREATED)
async def create_instance(
    request: CreateInstanceRequest, service: InstanceServiceDependency
) -> InstanceResponse:
    instance = await service.create(**request.model_dump())
    return InstanceResponse.from_domain(instance)


@router.get("", response_model=list[InstanceResponse])
async def list_instances(service: InstanceServiceDependency) -> Sequence[InstanceResponse]:
    instances = await service.list()
    return [InstanceResponse.from_domain(instance) for instance in instances]


@router.get("/{instance_id}", response_model=InstanceResponse)
async def get_instance(instance_id: UUID, service: InstanceServiceDependency) -> InstanceResponse:
    try:
        instance = await service.get(instance_id)
    except InstanceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Instance not found."
        ) from error
    return InstanceResponse.from_domain(instance)


@router.post(
    "/{instance_id}/test", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED
)
async def test_instance_connection(
    instance_id: UUID,
    service: InstanceServiceDependency,
    jobs: JobServiceDependency,
) -> JobResponse:
    try:
        await service.get(instance_id)
    except InstanceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Instance not found."
        ) from error

    return JobResponse.from_domain(await jobs.enqueue_connection_test(instance_id))
