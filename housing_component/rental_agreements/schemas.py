from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from housing_component.state.schemas import StateSchemaResponse
from housing_component.tenants.schemas import TenantSchema


class RentalAgreementSchema(BaseModel):
    id: str  # noqa: A003
    external_id: str
    organization_id: int
    tenant_id: str
    rental_unit_id: str
    start_at: datetime
    end_at: datetime

    class Config:
        from_attributes = True


class RentalAgreementSchemaResponse(RentalAgreementSchema):
    tenant: Optional[TenantSchema]
    state: Optional[StateSchemaResponse]

    class Config:
        from_attributes = True


class SuccessDeleteResponse(BaseModel):
    name: str
    message: str
