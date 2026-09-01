import asyncio
import logging
import signal
from pathlib import Path
from uuid import UUID

from app.application.instances.service import InstanceService
from app.application.jobs.service import JobService
from app.config import get_settings
from app.domain.jobs.models import Job, JobStatus
from app.infrastructure.dbatools import DbatoolsInstanceConnectionTester
from app.infrastructure.persistence import (
    Database,
    SqlAlchemyInstanceRepository,
    SqlAlchemyJobRepository,
)
from app.infrastructure.powershell import SubprocessPowerShellExecutor

logger = logging.getLogger(__name__)


async def run_worker() -> None:
    """Claim durable jobs and run dbatools only from the worker process."""
    settings = get_settings()
    database = Database(settings.database_url)
    await database.create_schema()
    instances = InstanceService(SqlAlchemyInstanceRepository(database.sessions))
    jobs = JobService(SqlAlchemyJobRepository(database.sessions))
    script = Path(__file__).resolve().parents[3] / "powershell/DBAForge/Test-DBAForgeConnection.ps1"
    tester = DbatoolsInstanceConnectionTester(SubprocessPowerShellExecutor(), script)
    stop_requested = asyncio.Event()
    loop = asyncio.get_running_loop()

    for stop_signal in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(stop_signal, stop_requested.set)
        except NotImplementedError:
            break

    logger.info("DBAForge worker started")
    try:
        while not stop_requested.is_set():
            job = await jobs.claim_next()
            if job is None:
                await asyncio.sleep(1)
                continue
            await _process_job(job, jobs, instances, tester)
    finally:
        await database.dispose()
        logger.info("DBAForge worker stopped")


async def _process_job(
    job: Job,
    jobs: JobService,
    instances: InstanceService,
    tester: DbatoolsInstanceConnectionTester,
) -> None:
    if job.job_type != "instance_connection_test":
        await jobs.complete(
            job, status=JobStatus.FAILED, result={"message": "Unsupported job type."}
        )
        return

    try:
        instance = await instances.get(UUID(job.payload["instance_id"]))
        result = await tester.test_connection(instance)
        status = JobStatus.SUCCEEDED if result.status == "success" else JobStatus.FAILED
        await jobs.complete(
            job,
            status=status,
            result={
                "status": result.status,
                "version": result.version,
                "edition": result.edition,
                "message": result.message,
            },
        )
    except Exception:
        logger.exception("Connection-test job failed. job_id=%s", job.id)
        await jobs.complete(
            job,
            status=JobStatus.FAILED,
            result={"status": "failed", "message": "Connection test failed."},
        )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        logger.info("DBAForge worker stopped")


if __name__ == "__main__":
    main()
