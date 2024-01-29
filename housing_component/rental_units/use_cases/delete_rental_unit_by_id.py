from injector import Inject

from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.rental_units.errors import RentalUnitErrors
from housing_component.rental_units.services.rental_unit_repository import (
    RentalUnitRepository,
)


class DeleteRentalUnitById(UseCase):
    rental_unit_id: str
    organization_id: int

    class Handler(UseCaseHandler["DeleteRentalUnitById", None]):
        def __init__(
            self, rental_unit_repository: Inject[RentalUnitRepository]
        ) -> None:
            self.rental_unit_repository = rental_unit_repository

        async def execute(self, use_case: "DeleteRentalUnitById") -> None:
            rental_unit = await self.rental_unit_repository.get_by_id(
                use_case.rental_unit_id,
                organization_id=use_case.organization_id,
            )
            if not rental_unit:
                raise RentalUnitErrors.RENTAL_UNIT_NOT_FOUND

            await self.rental_unit_repository.delete_by_id(
                use_case.rental_unit_id,
                organization_id=use_case.organization_id,
            )
