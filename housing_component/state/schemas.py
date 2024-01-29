from uuid import UUID
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from enum import Enum


class DesiredStateEnum(str, Enum):
    Active = "Active"
    Inactive = "Inactive"


class ActualStateEnum(str, Enum):
    Created = "Created"
    Activating = "Activating"
    Activated = "Activated"
    Deactivating = "Deactivating"
    Deactivated = "Deactivated"


class StatusEnum(str, Enum):
    OK = "OK"
    Reconciling = "Reconciling"
    Error = "Error"


class StateSchemaResponse(BaseModel):
    id: UUID  # noqa: A003
    desired: DesiredStateEnum
    actual: ActualStateEnum
    status: StatusEnum
    error: Optional[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class StateSchema(BaseModel):
    id: UUID  # noqa: A003
    desired: DesiredStateEnum
    actual: ActualStateEnum
    status: StatusEnum

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class SuccessDeleteResponse(BaseModel):
    name: str
    message: str


class KiwiUser(BaseModel):
    user_id: int
    username: str
    email: str
    name: Optional[str]
    lastname: Optional[str]
    language: Optional[str]
    country: Optional[str]
    email_verified: Optional[datetime]
    is_managed: bool
    custom_fields: Optional[dict]
    segment_id: Optional[str]
    customer_number: str
    organization_id: Optional[int]
    deleted: Optional[bool]
    created: datetime
    created_by: Optional[int]
    last_created_session: Optional[datetime]

    class Config:
        from_attributes = True


class Permission(BaseModel):
    id: int  # noqa: A003
    granted: str
    begins: datetime
    ends: Optional[datetime]
    timeofday_begins: Optional[datetime]
    timeofday_ends: Optional[datetime]
    weekdays: List[str]
    users: List[KiwiUser]
    can_modify: bool
    timing_state: str
    deleted: Optional[datetime]
