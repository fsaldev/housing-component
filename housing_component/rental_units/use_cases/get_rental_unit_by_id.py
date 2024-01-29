from housing_component.addresses.services.address_repository import AddressRepository
from housing_component.rental_units.errors import RentalUnitErrors
from injector import Inject
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.rental_units.schemas import (
    RentalUnitSchema,
)
from housing_component.rental_units.services.rental_unit_repository import (
    RentalUnitRepository,
)


class GetRentalUnitById(UseCase):
    organization_id: int
    rental_unit_id: str

    class Handler(UseCaseHandler["GetRentalUnitById", RentalUnitSchema]):
        def __init__(
            self,
            rental_unit_repository: Inject[RentalUnitRepository],
            address_repository: Inject[AddressRepository],
        ) -> None:
            self.rental_unit_repository = rental_unit_repository
            self.address_repository = address_repository

        async def execute(self, use_case: "GetRentalUnitById") -> RentalUnitSchema:
            rental_unit = await self.rental_unit_repository.get_by_id(
                use_case.rental_unit_id,
                organization_id=use_case.organization_id,
            )
            if not rental_unit:
                raise RentalUnitErrors.RENTAL_UNIT_NOT_FOUND

            return rental_unit
