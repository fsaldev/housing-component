from sqlalchemy import Select, select, delete
from typing import Sequence, Tuple
from injector import Inject

from housing_component.access_points import interfaces
from housing_component.access_points.models import AccessPoint
from housing_component.core.unit_of_work import UnitOfWork


class AccessPointRepository(interfaces.AccessPointRepository):
    def __init__(self, unit_of_work: Inject[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work

    async def get_by_id(self, access_point_id: int) -> AccessPoint | None:
        query = self._get_base_query().where(AccessPoint.id == access_point_id)

        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        return result.scalars().one_or_none()

    async def get_list(
        self, rental_unit_id: str, organization_id: int
    ) -> Sequence[AccessPoint]:
        query = self._get_base_query()

        query = query.where(
            AccessPoint.rental_unit_id == rental_unit_id
            and AccessPoint.organization_id == organization_id
        )

        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        return result.scalars().fetchall()

    async def create(self, access_point: AccessPoint) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(access_point)
        await session.flush([access_point])

    async def save(self, access_point: AccessPoint) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(access_point)
        await session.flush([access_point])

    async def delete_by_id(self, access_point_id: int) -> None:
        session = await self._unit_of_work.get_db_session()
        delete_query = delete(AccessPoint).where(AccessPoint.id == access_point_id)
        await session.execute(delete_query)
        await session.commit()

    def _get_base_query(self) -> Select[Tuple[AccessPoint]]:
        return select(AccessPoint)
