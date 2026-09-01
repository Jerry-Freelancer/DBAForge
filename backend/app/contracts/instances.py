from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.instances.models import AuthenticationType, Instance


class CreateInstanceRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    host: str = Field(min_length=1, max_length=255)
    port: int | None = Field(default=None, ge=1, le=65535)
    instance_name: str | None = Field(default=None, max_length=128)
    authentication_type: AuthenticationType
    credential_id: UUID | None = None


class InstanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    host: str
    port: int | None
    instance_name: str | None
    authentication_type: AuthenticationType
    credential_id: UUID | None
    is_enabled: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, instance: Instance) -> "InstanceResponse":
        return cls.model_validate(instance)
