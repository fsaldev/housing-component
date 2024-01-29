from typing import Optional

import requests
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.access_points.schemas import (
    SensorData,
    Sensor,
    Address,
    Admin,
    Settings,
    Status,
    SearchParameters,
)
from housing_component.settings import SENSOR_URL


class GetSensorList(UseCase):
    session_key: str
    page_number: int = 1
    page_size: int = 20
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    max_distance: Optional[int] = None
    specifier: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    search: Optional[str] = None

    class Handler(UseCaseHandler["GetSensorList", SensorData]):
        async def execute(self, use_case: "GetSensorList") -> SensorData:
            param = SearchParameters(
                session_key=use_case.session_key,
                page_number=use_case.page_number,
                page_size=use_case.page_size,
                lat=use_case.latitude,
                lng=use_case.longitude,
                max_distance=use_case.max_distance,
                specifier=use_case.specifier,
                street=use_case.street,
                city=use_case.city,
                state=use_case.state,
                search=use_case.search,
            )

            resp = requests.get(url=SENSOR_URL, params=param.dict())
            resp_json = resp.json().get("result", {})
            sensors = resp_json.get("sensors", [])
            results = []
            for sensor in sensors:
                admins = []
                for admin in sensor.get("admins", []):
                    if admin:
                        admins.append(
                            Admin(
                                org=admin.get("org"),
                                name=admin.get("name"),
                                email=admin.get("email"),
                                org_id=admin.get("org_id"),
                                user_id=admin.get("user_id"),
                                lastname=admin.get("lastname"),
                                username=admin.get("username"),
                                customer_number=admin.get("customer_number"),
                            )
                        )
                address = sensor.get("address", {})
                owner = sensor.get("owner", {})
                results.append(
                    Sensor(
                        sensor_id=sensor.get("sensor_id"),
                        sensor_name=sensor.get("sensor_name"),
                        name=sensor.get("name"),
                        customer_name=sensor.get("customer_name"),
                        can_invite=sensor.get("can_invite"),
                        address=Address(
                            id=address.get("id"),
                            street=address.get("street"),
                            postal_code=address.get("postal_code"),
                            city=address.get("city"),
                            state=address.get("state"),
                            country=address.get("country"),
                            lat=address.get("lat"),
                            lng=address.get("lng"),
                            specifier=address.get("specifier"),
                            floor=address.get("floor"),
                            door_number=address.get("door_number"),
                        ),
                        hardware_type=sensor.get("hardware_type"),
                        hardware_variant=sensor.get("hardware_variant"),
                        highest_permission=sensor.get("highest_permission"),
                        installation_date=sensor.get("installation_date"),
                        settings=Settings(
                            last_updated=sensor.get("settings", {}).get("last_updated"),
                            handover_enabled=sensor.get("settings", {}).get(
                                "handover_enabled"
                            ),
                        ),
                        battery_level=sensor.get("battery_level"),
                        battery_level_since=sensor.get("battery_level_since"),
                        battery_step=sensor.get("battery_step"),
                        battery_status=sensor.get("battery_status"),
                        door_type=sensor.get("door_type"),
                        is_favorite=sensor.get("is_favorite"),
                        max_kis=sensor.get("max_kis"),
                        custom_attributes=sensor.get("custom_attributes"),
                        admins=admins,
                        is_transferable=sensor.get("is_transferable"),
                        is_transferred=sensor.get("is_transferred"),
                        owner=Admin(
                            org=owner.get("org"),
                            name=owner.get("name"),
                            org_id=owner.get("org_id"),
                            user_id=owner.get("user_id"),
                            lastname=owner.get("lastname"),
                            username=owner.get("username"),
                            email=owner.get("email"),
                            customer_number=owner.get("customer_number"),
                        ),
                        is_owner=sensor.get("is_owner"),
                        firmware=sensor.get("firmware"),
                        hardware=sensor.get("hardware"),
                        crystal=sensor.get("crystal"),
                        manufacture_date=sensor.get("manufacture_date"),
                        sensor_uuid=sensor.get("sensor_uuid"),
                        protocol=sensor.get("protocol"),
                        sticky=sensor.get("sticky"),
                        features=sensor.get("features"),
                        status=Status(
                            status=sensor.get("status", {}).get("status"),
                            timestamp=sensor.get("status", {}).get("timestamp"),
                        ),
                        usage=sensor.get("usage"),
                        service_provider_access=sensor.get("service_provider_access"),
                        link_868=sensor.get("link_868"),
                        lifecycle_state=sensor.get("lifecycle_state"),
                        registration_type=sensor.get("registration_type"),
                        installation_location=sensor.get("installation_location"),
                    )
                )
            return SensorData(
                sensors=results,
                total_results=resp_json.get("total_results"),
                page_size=resp_json.get("page_size"),
                page_number=resp_json.get("page_number"),
                order_by=resp_json.get("order_by"),
                sort_by=resp_json.get("sort_by"),
                custom_attributes=resp_json.get("custom_attributes"),
            )
