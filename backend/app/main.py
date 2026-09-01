import logging

from fastapi import FastAPI

from app.api.v1.health import router as health_router


def create_app() -> FastAPI:
    """Create the HTTP control plane without starting background execution."""
    app = FastAPI(
        title="DBAForge API",
        version="0.1.0",
        description="SQL Server DBA automation workflow control plane.",
    )
    app.include_router(health_router)
    return app


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
app = create_app()
