from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class AuthenticationType(StrEnum):
    WINDOWS = "windows"
    SQL = "sql"


@dataclass(frozen=True, slots=True)
class Instance:
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
