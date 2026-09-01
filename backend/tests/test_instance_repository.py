from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.domain.instances.models import AuthenticationType, Instance
from app.infrastructure.persistence import Database, SqlAlchemyInstanceRepository


@pytest.mark.anyio
async def test_sqlalchemy_repository_persists_instances() -> None:
    database = Database("sqlite+aiosqlite://")
    await database.create_schema()
    repository = SqlAlchemyInstanceRepository(database.sessions)
    now = datetime.now(UTC)
    instance = Instance(
        id=uuid4(),
        name="SQL01",
        host="sql01.example.test",
        port=1433,
        instance_name=None,
        authentication_type=AuthenticationType.WINDOWS,
        credential_id=None,
        is_enabled=True,
        created_at=now,
        updated_at=now,
    )

    await repository.create(instance)
    found = await repository.get(instance.id)

    assert found == instance
    await database.dispose()


@pytest.mark.anyio
async def test_sqlalchemy_job_repository_claims_and_completes_jobs() -> None:
    from app.application.jobs.service import JobService
    from app.domain.jobs.models import JobStatus
    from app.infrastructure.persistence import SqlAlchemyJobRepository

    database = Database("sqlite+aiosqlite://")
    await database.create_schema()
    jobs = JobService(SqlAlchemyJobRepository(database.sessions))

    queued = await jobs.enqueue_connection_test(uuid4())
    claimed = await jobs.claim_next()
    completed = await jobs.complete(
        claimed,
        status=JobStatus.SUCCEEDED,
        result={"status": "success", "message": "Connected"},
    )

    assert queued.status is JobStatus.QUEUED
    assert claimed is not None and claimed.status is JobStatus.RUNNING
    assert completed.status is JobStatus.SUCCEEDED
    await database.dispose()
