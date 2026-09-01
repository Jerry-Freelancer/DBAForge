import asyncio
import logging
import signal

logger = logging.getLogger(__name__)


async def run_worker() -> None:
    """Run the independent worker host until the service receives a stop signal.

    Job claiming and PowerShell execution are intentionally not implemented here yet.
    They will be added behind application and infrastructure ports so the API process
    cannot execute PowerShell directly.
    """
    stop_requested = asyncio.Event()
    loop = asyncio.get_running_loop()

    for stop_signal in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(stop_signal, stop_requested.set)
        except NotImplementedError:
            # Windows event loops do not support asyncio signal handlers.
            break

    logger.info("DBAForge worker started")
    await stop_requested.wait()
    logger.info("DBAForge worker stopped")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        logger.info("DBAForge worker stopped")


if __name__ == "__main__":
    main()
