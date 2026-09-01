from collections.abc import Sequence
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from app.application.instances.service import InstanceService
from app.application.jobs.service import JobService
from app.domain.instances.models import Instance
from app.domain.jobs.models import Job, JobStatus
from app.main import create_app


class InMemoryInstanceRepository:
    def __init__(self) -> None:
        self.instances: dict[UUID, Instance] = {}

    async def create(self, instance: Instance) -> Instance:
        self.instances[instance.id] = instance
        return instance

    async def get(self, instance_id: UUID) -> Instance | None:
        return self.instances.get(instance_id)

    async def list(self) -> Sequence[Instance]:
        return sorted(self.instances.values(), key=lambda instance: instance.name)


class InMemoryJobRepository:
    def __init__(self) -> None:
        self.jobs: dict[UUID, Job] = {}

    async def enqueue(self, job: Job) -> Job:
        self.jobs[job.id] = job
        return job

    async def get(self, job_id: UUID) -> Job | None:
        return self.jobs.get(job_id)

    async def claim_next(self) -> Job | None:
        for job in self.jobs.values():
            if job.status is JobStatus.QUEUED:
                return job
        return None

    async def complete(self, job: Job) -> Job:
        self.jobs[job.id] = job
        return job


@pytest.fixture
def client() -> AsyncClient:
    app = create_app(
        instance_service=InstanceService(InMemoryInstanceRepository()),
        job_service=JobService(InMemoryJobRepository()),
    )
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver")


@pytest.mark.anyio
async def test_create_list_get_and_queue_connection_test(client: AsyncClient) -> None:
    async with client:
        create_response = await client.post(
            "/api/v1/instances",
            json={
                "name": "SQL01",
                "host": "sql01.example.test",
                "port": 1433,
                "authentication_type": "windows",
            },
        )
        created = create_response.json()

        list_response = await client.get("/api/v1/instances")
        get_response = await client.get(f"/api/v1/instances/{created['id']}")
        queue_response = await client.post(f"/api/v1/instances/{created['id']}/test")
        job_response = await client.get(f"/api/v1/jobs/{queue_response.json()['id']}")

    assert create_response.status_code == 201
    assert list_response.json()[0]["name"] == "SQL01"
    assert get_response.json()["host"] == "sql01.example.test"
    assert queue_response.status_code == 202
    assert job_response.json()["status"] == "queued"
    assert job_response.json()["payload"] == {"instance_id": created["id"]}


@pytest.mark.anyio
async def test_get_unknown_instance_returns_not_found(client: AsyncClient) -> None:
    async with client:
        response = await client.get("/api/v1/instances/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
