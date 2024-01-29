from injector import Inject
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.access_points.schemas import (
    AccessPointSchema,
)
from housing_component.access_points.services.access_point_repository import (
    AccessPointRepository,
)
from typing import List


class GetAccessPointList(UseCase):
    organization_id: int
    rental_unit_id: str

    class Handler(UseCaseHandler["GetAccessPointList", List[AccessPointSchema]]):
        def __init__(
            self,
            access_point_repository: Inject[AccessPointRepository],
        ) -> None:
            self.access_point_repository = access_point_repository

        async def execute(
            self, use_case: "GetAccessPointList"
        ) -> List[AccessPointSchema]:
            access_points = await self.access_point_repository.get_list(
                rental_unit_id=use_case.rental_unit_id,
                organization_id=use_case.organization_id,
            )
            results = []
            for access_point in access_points:
                results.append(
                    AccessPointSchema(
                        id=access_point.id,
                        name=access_point.name,
                        rental_unit_id=access_point.rental_unit_id,
                        organization_id=access_point.organization_id,
                        permission=access_point.permission,
                    )
                )

            return results
