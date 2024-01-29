from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from housing_component.rental_units.models import RentalUnit
from housing_component.rental_units.schemas import (
    RentalUnitSchema,
    RentalUnitSchemaListResponse,
)


@runtime_checkable
class RentalUnitRepository(Protocol):
    async def get_by_id(
        self,
        rental_unit_id: str,
        organization_id: int,
        include_access_points: bool = False,
    ) -> RentalUnitSchemaListResponse | None:
        ...

    async def get_list(
        self, organization_id: int, include_access_points: bool = False
    ) -> Sequence[RentalUnitSchema]:
        ...

    async def create(
        self,
        rental_unit: RentalUnit,
    ) -> None:
        ...

    async def save(
        self,
        rental_unit: RentalUnit,
    ) -> None:
        ...

    async def delete(
        self,
        rental_unit_id: str,
        organization_id: int,
    ) -> None:
        ...

    async def validate_rental_unit_by_id(
        self,
        rental_unit_id: str,
        organization_id: int,
    ) -> RentalUnit:
        ...
