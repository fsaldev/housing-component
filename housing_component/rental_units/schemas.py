from typing import TypedDict, List, Optional
from pydantic import BaseModel

from housing_component.access_points.schemas import AccessPointSchema


class AddressDict(TypedDict, total=False):
    street: str
    postal_code: str
    city: str
    state: str
    country: str
    lat: float
    lng: float


class AddressSchema(BaseModel):
    id: str  # noqa: A003
    street: str
    postal_code: str
    city: str
    state: str
    country: str
    lat: float
    lng: float

    class Config:
        from_attributes = True


class RentalUnitSchema(BaseModel):
    id: str  # noqa: A003
    external_id: str
    organization_id: int
    name: str
    address: AddressSchema | None

    class Config:
        from_attributes = True


class RentalUnitSchemaListResponse(RentalUnitSchema):
    access_points: Optional[List[AccessPointSchema]]

    class Config:
        from_attributes = True


class SuccessDeleteResponse(BaseModel):
    name: str
    message: str
