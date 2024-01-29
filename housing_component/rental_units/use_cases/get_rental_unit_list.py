from injector import Inject
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.rental_units.schemas import (
    RentalUnitSchemaListResponse,
)
from housing_component.rental_units.services.rental_unit_repository import (
    RentalUnitRepository,
)
from typing import List


class GetRentalUnitList(UseCase):
    organization_id: int
    include_access_points: bool

    class Handler(
        UseCaseHandler["GetRentalUnitList", List[RentalUnitSchemaListResponse]]
    ):
        def __init__(
            self,
            rental_unit_repository: Inject[RentalUnitRepository],
        ) -> None:
            self.rental_unit_repository = rental_unit_repository

        async def execute(
            self, use_case: "GetRentalUnitList"
        ) -> List[RentalUnitSchemaListResponse]:
            rental_units = await self.rental_unit_repository.get_list(
                organization_id=use_case.organization_id,
                include_access_points=use_case.include_access_points,
            )

            return rental_units
