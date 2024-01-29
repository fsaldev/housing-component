from typing import Optional
import uuid
from housing_component.addresses.models import Address
from housing_component.addresses.services.address_repository import AddressRepository
from housing_component.core.utils import REQUIRED_ADDRESS_FIELDS
from injector import Inject
from sqlalchemy.exc import IntegrityError

from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.rental_units.models import RentalUnit
from housing_component.rental_units.schemas import (
    AddressDict,
    RentalUnitSchema,
)
from housing_component.rental_units.services.rental_unit_repository import (
    RentalUnitRepository,
)
from housing_component.rental_units.errors import AddressError, RentalUnitErrors


class CreateRentalUnit(UseCase):
    organization_id: int
    rental_unit_id: Optional[str]
    external_id: Optional[str]
    name: Optional[str]
    address: Optional[AddressDict]

    class Handler(UseCaseHandler["CreateRentalUnit", RentalUnitSchema]):
        def __init__(
            self,
            rental_unit_repository: Inject[RentalUnitRepository],
            address_repository: Inject[AddressRepository],
        ) -> None:
            self._rental_unit_repository = rental_unit_repository
            self.address_repository = address_repository

        async def execute(self, use_case: "CreateRentalUnit") -> RentalUnitSchema:
            organization_id = use_case.organization_id

            if use_case.rental_unit_id:
                if await self._rental_unit_exists(
                    use_case.rental_unit_id, organization_id
                ):
                    raise RentalUnitErrors.RENTAL_UNIT_ALREADY_EXISTS

            address_id = (
                await self.process_address(use_case.address)
                if use_case.address
                else None
            )

            rental_unit_id = use_case.rental_unit_id or str(uuid.uuid4())

            rental_unit = RentalUnit(
                id=rental_unit_id,
                external_id=use_case.external_id,
                organization_id=organization_id,
                name=use_case.name,
                address=address_id,
            )
            await self.create_rental_unit(rental_unit)
            return await self.prepare_rental_unit_response(
                rental_unit_id, organization_id
            )

        async def _rental_unit_exists(
            self, rental_unit_id: str, organization_id: int
        ) -> bool:
            return (
                await self._rental_unit_repository.get_by_id(
                    rental_unit_id, organization_id
                )
                is not None
            )

        async def process_address(
            self, address: Optional[AddressDict]
        ) -> Optional[str]:
            # Check if the address is None or any required field is missing or empty
            if not address or not all(
                address.get(field) for field in REQUIRED_ADDRESS_FIELDS
            ):
                return None  # Address is considered invalid if any field is missing

            try:
                address_obj = Address(**address)
                sha1_hash = await self.address_repository.sha1_hash_address(address_obj)

                existing_address = await self.address_repository.get_address_by_sha1(
                    sha1_hash
                )
                if existing_address:
                    return (
                        existing_address.id
                    )  # Return existing address ID if it exists

                # Create a new address if it's valid and doesn't already exist
                new_address = Address(id=sha1_hash, **address)
                await self.address_repository.create(new_address)
                return new_address.id  # Return new address ID after creation

            except Exception:
                raise AddressError.ADDRESS_INVALID_ERROR

        async def create_rental_unit(self, rental_unit: RentalUnit) -> None:
            try:
                await self._rental_unit_repository.create(rental_unit)
            except IntegrityError:
                raise RentalUnitErrors.RENTAL_UNIT_ALREADY_EXISTS

        async def prepare_rental_unit_response(
            self, rental_unit_id: str, organization_id: int
        ) -> RentalUnitSchema:
            rental_unit = await self._rental_unit_repository.get_by_id(
                rental_unit_id, organization_id
            )
            if not rental_unit:
                raise RentalUnitErrors.RENTAL_UNIT_NOT_FOUND
            return rental_unit
