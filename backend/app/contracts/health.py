from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Public response for the liveness endpoint."""

    status: str
