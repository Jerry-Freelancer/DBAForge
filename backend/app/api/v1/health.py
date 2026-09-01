from fastapi import APIRouter

from app.contracts.health import HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse, summary="Get service health")
async def get_health() -> HealthResponse:
    """Return the liveness status without touching external dependencies."""
    return HealthResponse(status="healthy")
