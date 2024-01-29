from typing import Optional
from housing_component.addresses.models import Address
from housing_component.addresses.services.address_repository import AddressRepository
from housing_component.core.utils import (
    REQUIRED_ADDRESS_FIELDS,
    parse_integrity_error_message,
)
from housing_component.rental_units.models import RentalUnit
from housing_component.rental_units.schemas import (
    AddressDict,
    AddressSchema,
    RentalUnitSchema,
)
from injector import Inject
from sqlalchemy.exc import IntegrityError
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.rental_units.services.rental_unit_repository import (
    RentalUnitRepository,
)
from housing_component.rental_units.errors import AddressError, RentalUnitErrors


class ModifyRentalUnit(UseCase):
    external_id: Optional[str] = None
    name: Optional[str] = None
    address: Optional[AddressDict] = None
    organization_id: int
    rental_unit_id: str

    class Handler(UseCaseHandler["ModifyRentalUnit", RentalUnitSchema]):
        def __init__(
            self,
            rental_unit_repository: Inject[RentalUnitRepository],
            address_repository: Inject[AddressRepository],
        ) -> None:
            self._rental_unit_repository = rental_unit_repository
            self.address_repository = address_repository

        async def execute(self, use_case: "ModifyRentalUnit") -> RentalUnitSchema:
            rental_unit = await self._fetch_and_validate_rental_unit(
                use_case.rental_unit_id, use_case.organization_id
            )
            address_id = (
                await self._process_address(use_case.address)
                if use_case.address
                else None
            )
            self._update_rental_unit(rental_unit, use_case, address_id)
            await self._save_rental_unit(rental_unit)

            address_data = await self._fetch_address_data(rental_unit.address)
            return self._prepare_response(rental_unit, address_data)

        async def _fetch_and_validate_rental_unit(
            self, rental_unit_id: str, organization_id: int
        ) -> RentalUnit:
            rental_unit = await self._rental_unit_repository.validate_rental_unit_by_id(
                rental_unit_id, organization_id
            )
            if rental_unit is None:
                raise RentalUnitErrors.RENTAL_UNIT_NOT_FOUND
            return rental_unit

        async def _process_address(
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

        def _update_rental_unit(
            self,
            rental_unit: RentalUnit,
            use_case: "ModifyRentalUnit",
            address_id: Optional[str],
        ) -> None:
            if use_case.external_id is not None:
                rental_unit.external_id = use_case.external_id
            if use_case.name is not None:
                rental_unit.name = use_case.name
            if address_id:
                rental_unit.address = address_id
            else:
                rental_unit.address = None

        async def _save_rental_unit(self, rental_unit: RentalUnit) -> None:
            try:
                await self._rental_unit_repository.save(rental_unit)
            except IntegrityError as e:
                error_info = str(e)
                error_code = "INTEGRITY_VIOLATION_ERROR"
                keys, values = parse_integrity_error_message(error_info)
                if keys and values:
                    friendly_message = f"Duplicate entry for unique keys {keys} with values {values}. Please provide a unique value."
                else:
                    friendly_message = "An unknown database integrity issue occurred."
                raise RentalUnitErrors.dynamic_error(error_code, friendly_message)

        async def _fetch_address_data(
            self, address_id: Optional[str]
        ) -> Optional[AddressSchema]:
            if not address_id:
                return None
            address = await self.address_repository.get_address_by_sha1(address_id)
            return AddressSchema.model_validate(address) if address else None

        def _prepare_response(
            self, rental_unit: RentalUnit, address_data: Optional[AddressSchema]
        ) -> RentalUnitSchema:
            return RentalUnitSchema(
                id=rental_unit.id,
                external_id=rental_unit.external_id,
                organization_id=rental_unit.organization_id,
                name=rental_unit.name,
                address=address_data,
            )
