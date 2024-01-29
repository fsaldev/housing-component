from enum import Enum
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel


class PermissionEnum(str, Enum):
    CAN_SEE_GATEWAYS = "CAN_SEE_GATEWAYS"
    IS_ADMIN = "IS_ADMIN"
    IS_MANAGER = "IS_MANAGER"
    IS_GUEST = "IS_GUEST"
    IS_HOST = "IS_HOST"
    IS_SUPPORT = "IS_SUPPORT"
    IS_REPORTING = "IS_REPORTING"
    IS_OPERATIONS = "IS_OPERATIONS"
    IS_SUPERUSER = "IS_SUPERUSER"


class AccessPointSchema(BaseModel):
    id: int  # noqa: A003
    name: str
    permission: PermissionEnum = PermissionEnum.IS_HOST
    rental_unit_id: str
    organization_id: int

    class Config:
        from_attributes = True


class Address(BaseModel):
    id: Optional[int]  # noqa: A003
    street: Optional[str]
    postal_code: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    specifier: Optional[str]
    floor: Optional[str]
    door_number: Optional[str]


class Admin(BaseModel):
    org: Optional[str]
    name: Optional[str]
    email: Optional[str]
    org_id: Optional[int]
    user_id: Optional[int]
    lastname: Optional[str]
    username: Optional[str]
    customer_number: Optional[str]


class Settings(BaseModel):
    last_updated: Optional[datetime]
    handover_enabled: Optional[bool]


class Status(BaseModel):
    status: Optional[str]
    timestamp: Optional[datetime]


class Sensor(BaseModel):
    sensor_id: Optional[int]
    sensor_name: Optional[str]
    name: Optional[str]
    customer_name: Optional[str]
    can_invite: Optional[bool]
    address: Address
    hardware_type: Optional[str]
    hardware_variant: Optional[str]
    highest_permission: Optional[str]
    installation_date: Optional[datetime]
    settings: Settings
    battery_level: Optional[int]
    battery_level_since: Optional[datetime]
    battery_step: Optional[int]
    battery_status: Optional[str]
    door_type: Optional[str]
    is_favorite: Optional[bool]
    max_kis: Optional[int]
    custom_attributes: Optional[Dict[str, str]]
    admins: Optional[List[Admin]]
    is_transferable: Optional[bool]
    is_transferred: Optional[bool]
    owner: Optional[Admin]
    is_owner: Optional[bool]
    firmware: Optional[str]
    hardware: Optional[str]
    crystal: Optional[str]
    manufacture_date: Optional[datetime]
    sensor_uuid: Optional[str]
    protocol: Optional[str]
    sticky: Optional[str]
    features: Optional[List[str]]
    status: Status
    usage: Optional[str]
    service_provider_access: Optional[bool]
    link_868: Optional[str]
    lifecycle_state: Optional[str]
    registration_type: Optional[str]
    installation_location: Optional[str]


class SensorData(BaseModel):
    sensors: List[Sensor]
    total_results: Optional[int]
    page_size: Optional[int]
    page_number: Optional[int]
    order_by: Optional[str]
    sort_by: Optional[List[str]]
    custom_attributes: Optional[List[Dict[str, str]]]


class SearchParameters(BaseModel):
    session_key: str
    page_number: int = 1
    page_size: int = 20
    lat: Optional[float]
    lng: Optional[float]
    max_distance: Optional[int]
    specifier: Optional[str]
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    search: Optional[str]
