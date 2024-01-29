from collections.abc import Sequence
from typing import Annotated, List
from fastapi import APIRouter, Body, Depends
from fastapi_injector import Injected
from housing_component.access_points.use_cases.get_sensors_list import GetSensorList
from housing_component.core.auth import require_organization_access_token
from housing_component.organizations import check_organization_existence
from housing_component.access_points.schemas import (
    AccessPointSchema,
    PermissionEnum,
    SensorData,
)
from housing_component.access_points.use_cases import (
    GetAccessPointList,
    CreateAccessPoint,
    DeleteAccessPointById,
    CreateListAccessPoint,
    CreateAccessPointBulk,
)
from housing_component.core.use_cases import UseCase

router = APIRouter(
    prefix="/organizations/{organization_id}/rental_units/{rental_unit_id}/access-points",
    tags=["Rental units"],
    dependencies=[
        Depends(require_organization_access_token),
        Depends(check_organization_existence),
    ],
)

sensor_router = APIRouter(
    prefix="/organizations/{organization_id}/access-points",
    tags=["Rental units"],
    dependencies=[
        Depends(require_organization_access_token),
        Depends(check_organization_existence),
    ],
)


@sensor_router.get("/search", description="Get a list of sensors")
async def get_sensor_list(
    use_case: Annotated[GetSensorList, Depends()],
    handler: Annotated[GetSensorList.Handler, Injected(GetSensorList.Handler)],
) -> SensorData:
    return await handler.execute(use_case)


@router.get("", description="Get a list of access points")
async def get_access_points_list(
    use_case: Annotated[GetAccessPointList, Depends()],
    handler: Annotated[
        GetAccessPointList.Handler, Injected(GetAccessPointList.Handler)
    ],
) -> Sequence[AccessPointSchema]:
    return await handler.execute(use_case)


class AnnotatedCreateAccessPoint(UseCase):
    id: Annotated[int, Body()]  # noqa: A003
    name: Annotated[str, Body()]
    permission: Annotated[PermissionEnum, Body(default=PermissionEnum.IS_HOST)]


@router.post("", description="Create a access point")
async def create_access_point(
    organization_id: int,
    rental_unit_id: str,
    use_case: Annotated[AnnotatedCreateAccessPoint, Body()],
    handler: Annotated[CreateAccessPoint.Handler, Injected(CreateAccessPoint.Handler)],
) -> AccessPointSchema:
    use_case_dict = dict(use_case)
    return await handler.execute(
        CreateAccessPoint(
            rental_unit_id=rental_unit_id,
            organization_id=organization_id,
            **use_case_dict
        )
    )


class AnnotatedCreateAccessPointBulk(CreateAccessPointBulk):
    id: Annotated[int, Body()]  # noqa: A003
    name: Annotated[str, Body()]
    permission: Annotated[PermissionEnum, Body(default=PermissionEnum.IS_HOST)]


class AnnotatedCreateListAccessPoint(UseCase):
    access_points: List[AnnotatedCreateAccessPointBulk]


@router.post("/bulk", description="Create multiple access points")
async def create_bulk_access_points(
    organization_id: int,
    rental_unit_id: str,
    use_cases: Annotated[AnnotatedCreateListAccessPoint, Body()],
    handler: Annotated[
        CreateListAccessPoint.Handler, Injected(CreateListAccessPoint.Handler)
    ],
) -> List[AccessPointSchema]:
    use_cases_dict = dict(use_cases)

    return await handler.execute_bulk(
        CreateListAccessPoint(
            rental_unit_id=rental_unit_id,
            organization_id=organization_id,
            **use_cases_dict
        )
    )


@router.delete("/{access_point_id}", description="Delete access_point by Id")
async def delete_access_point_by_id(
    use_case: Annotated[DeleteAccessPointById, Depends()],
    handler: Annotated[
        DeleteAccessPointById.Handler, Injected(DeleteAccessPointById.Handler)
    ],
) -> None:
    return await handler.execute(use_case)
