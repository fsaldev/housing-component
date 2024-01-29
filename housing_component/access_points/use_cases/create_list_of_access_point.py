from injector import Inject
from sqlalchemy.exc import IntegrityError
from typing import List
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.access_points.models import AccessPoint
from housing_component.access_points.schemas import AccessPointSchema, PermissionEnum
from housing_component.access_points.services.access_point_repository import (
    AccessPointRepository,
)
from housing_component.access_points.errors import AccessPointErrors


class CreateAccessPointBulk(UseCase):
    id: int  # noqa: A003
    name: str
    permission: PermissionEnum


class CreateListAccessPoint(UseCase):
    organization_id: int
    rental_unit_id: str
    access_points: List[CreateAccessPointBulk]

    class Handler(UseCaseHandler["CreateListAccessPoint", List[AccessPointSchema]]):
        def __init__(
            self,
            access_point_repository: Inject[AccessPointRepository],
        ) -> None:
            self._access_point_repository = access_point_repository

        async def execute_bulk(
            self, use_case: "CreateListAccessPoint"
        ) -> List[AccessPointSchema]:
            results = []
            for access_point_data in use_case.access_points:
                try:
                    access_point = AccessPoint(
                        id=int(access_point_data.id),
                        rental_unit_id=use_case.rental_unit_id,
                        organization_id=use_case.organization_id,
                        name=access_point_data.name,
                        permission=access_point_data.permission,
                    )
                    await self._access_point_repository.create(access_point)

                    results.append(AccessPointSchema.model_validate(access_point))
                except IntegrityError:
                    raise AccessPointErrors.ACCESS_POINT_ALREADY_EXISTS
            return results
