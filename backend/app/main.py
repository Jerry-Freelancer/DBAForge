import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.instances import router as instances_router
from app.api.v1.jobs import router as jobs_router
from app.application.instances.service import InstanceService
from app.application.jobs.service import JobService
from app.config import get_settings
from app.infrastructure.persistence import (
    Database,
    SqlAlchemyInstanceRepository,
    SqlAlchemyJobRepository,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    if not hasattr(app.state, "instance_service"):
        database = Database(get_settings().database_url)
        await database.create_schema()
        app.state.database = database
        app.state.instance_service = InstanceService(
            SqlAlchemyInstanceRepository(database.sessions)
        )
        app.state.job_service = JobService(SqlAlchemyJobRepository(database.sessions))
    yield
    database = getattr(app.state, "database", None)
    if database is not None:
        await database.dispose()


def create_app(
    *, instance_service: InstanceService | None = None, job_service: JobService | None = None
) -> FastAPI:
    """Create the HTTP control plane without starting background execution in request handlers."""
    app = FastAPI(
        title="DBAForge API",
        version="0.2.0",
        description="SQL Server DBA automation workflow control plane.",
        lifespan=lifespan,
    )
    if instance_service is not None:
        app.state.instance_service = instance_service
    if job_service is not None:
        app.state.job_service = job_service
    app.include_router(health_router)
    app.include_router(instances_router)
    app.include_router(jobs_router)
    return app


app = create_app()
