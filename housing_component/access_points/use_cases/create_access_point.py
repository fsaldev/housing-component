from injector import Inject
from sqlalchemy.exc import IntegrityError
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.access_points.models import AccessPoint
from housing_component.access_points.schemas import AccessPointSchema, PermissionEnum
from housing_component.access_points.services.access_point_repository import (
    AccessPointRepository,
)
from housing_component.access_points.errors import AccessPointErrors


class CreateAccessPoint(UseCase):
    organization_id: int
    id: int  # noqa: A003
    rental_unit_id: str
    name: str
    permission: PermissionEnum

    class Handler(UseCaseHandler["CreateAccessPoint", AccessPointSchema]):
        def __init__(
            self,
            access_point_repository: Inject[AccessPointRepository],
        ) -> None:
            self._access_point_repository = access_point_repository

        async def execute(self, use_case: "CreateAccessPoint") -> AccessPointSchema:
            try:
                # Create the AccessPoint object with the address_id as foreign key

                access_point = AccessPoint(
                    id=int(use_case.id),
                    rental_unit_id=use_case.rental_unit_id,
                    organization_id=use_case.organization_id,
                    name=use_case.name,
                    permission=use_case.permission,
                )

                # Try to create the AccessPoint
                try:
                    await self._access_point_repository.create(access_point)
                except IntegrityError:
                    raise AccessPointErrors.ACCESS_POINT_ALREADY_EXISTS

                return AccessPointSchema.model_validate(access_point)

            except IntegrityError:
                raise AccessPointErrors.ACCESS_POINT_ALREADY_EXISTS
