from housing_component.access_points.schemas import AccessPointSchema
from housing_component.rental_units.errors import RentalUnitErrors
from housing_component.rental_units.schemas import (
    AddressSchema,
    RentalUnitSchemaListResponse,
)
from sqlalchemy import Select, select, delete
from sqlalchemy.orm import joinedload
from typing import List, Tuple
from injector import Inject
from housing_component.rental_units import interfaces
from housing_component.rental_units.models import RentalUnit
from housing_component.core.unit_of_work import UnitOfWork


class RentalUnitRepository(interfaces.RentalUnitRepository):
    def __init__(self, unit_of_work: Inject[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work

    async def get_by_id(
        self,
        rental_unit_id: str,
        organization_id: int,
        include_access_points: bool = False,
    ) -> RentalUnitSchemaListResponse | None:
        query = self._get_base_query()
        query = query.where(RentalUnit.id == rental_unit_id)
        if organization_id:
            query = query.where(RentalUnit.organization_id == organization_id)
        query = query.options(joinedload(RentalUnit.address_rel))

        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        rental_unit = result.scalars().one_or_none()
        if rental_unit:
            address_data = None
            if rental_unit.address_rel:
                address_data = AddressSchema.model_validate(rental_unit.address_rel)
            if include_access_points:
                access_point_data = [
                    AccessPointSchema.model_validate(access_point)
                    for access_point in rental_unit.access_point_rel
                ]
            else:
                access_point_data = []
            return RentalUnitSchemaListResponse(
                id=rental_unit.id,
                external_id=rental_unit.external_id,
                organization_id=rental_unit.organization_id,
                name=rental_unit.name,
                address=address_data,
                access_points=access_point_data,
            )
        return None

    async def validate_rental_unit_by_id(
        self, rental_unit_id: str, organization_id: int
    ) -> RentalUnit:
        query = self._get_base_query().where(RentalUnit.id == rental_unit_id)
        if organization_id:
            query = query.where(RentalUnit.organization_id == organization_id)
        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        rental_unit = result.scalars().one_or_none()
        if not rental_unit:
            raise RentalUnitErrors.RENTAL_UNIT_NOT_FOUND
        return rental_unit

    async def get_list(
        self, organization_id: int, include_access_points: bool = False
    ) -> List[RentalUnitSchemaListResponse]:
        query = self._get_base_query()
        if organization_id:
            query = query.where(RentalUnit.organization_id == organization_id)

        query = query.options(
            joinedload(RentalUnit.address_rel)  # This adds a join to fetch addresses
        )

        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)

        rental_units = result.scalars().fetchall()

        response_list = []
        for ru in rental_units:
            address_data = None
            if ru.address_rel:
                address_data = AddressSchema.model_validate(ru.address_rel)

            if include_access_points:
                access_point_data = [
                    AccessPointSchema.model_validate(access_point)
                    for access_point in ru.access_point_rel
                ]
            else:
                access_point_data = []

            response_list.append(
                RentalUnitSchemaListResponse(
                    id=ru.id,
                    external_id=ru.external_id,
                    organization_id=ru.organization_id,
                    name=ru.name,
                    address=address_data,
                    access_points=access_point_data,
                )
            )

        return response_list

    async def create(self, rental_unit: RentalUnit) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(rental_unit)
        await session.flush([rental_unit])

    async def save(self, rental_unit: RentalUnit) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(rental_unit)
        await session.flush([rental_unit])

    async def delete_by_id(self, rental_unit_id: str, organization_id: int) -> None:
        session = await self._unit_of_work.get_db_session()
        delete_query = (
            delete(RentalUnit)
            .where(RentalUnit.id == rental_unit_id)
            .where(RentalUnit.organization_id == organization_id)
        )
        await session.execute(delete_query)
        await session.commit()

    def _get_base_query(self) -> Select[Tuple[RentalUnit]]:
        return select(RentalUnit)
