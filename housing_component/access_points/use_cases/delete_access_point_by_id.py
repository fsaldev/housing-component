from injector import Inject

from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.access_points.errors import AccessPointErrors
from housing_component.access_points.services.access_point_repository import (
    AccessPointRepository,
)


class DeleteAccessPointById(UseCase):
    access_point_id: int

    class Handler(UseCaseHandler["DeleteAccessPointById", None]):
        def __init__(
            self, access_point_repository: Inject[AccessPointRepository]
        ) -> None:
            self.access_point_repository = access_point_repository

        async def execute(self, use_case: "DeleteAccessPointById") -> None:
            access_point = await self.access_point_repository.get_by_id(
                access_point_id=use_case.access_point_id
            )
            if not access_point:
                raise AccessPointErrors.ACCESS_POINT_NOT_FOUND

            await self.access_point_repository.delete_by_id(
                access_point_id=use_case.access_point_id
            )
