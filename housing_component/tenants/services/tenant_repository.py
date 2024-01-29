from sqlalchemy import Select, select, delete
from typing import Sequence, Tuple
from injector import Inject

from housing_component.tenants import interfaces
from housing_component.tenants.models import Tenant
from housing_component.core.unit_of_work import UnitOfWork


class TenantRepository(interfaces.TenantRepository):
    def __init__(self, unit_of_work: Inject[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work

    async def get_by_id(
        self,
        tenant_id: str,
        organization_id: int,
    ) -> Tenant | None:
        query = self._get_base_query().where(Tenant.id == tenant_id)
        if organization_id:
            query = query.where(Tenant.organization_id == organization_id)

        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        return result.scalars().one_or_none()

    async def get_list(
        self,
        organization_id: int,
    ) -> Sequence[Tenant]:
        query = self._get_base_query()
        if organization_id:
            query = query.where(Tenant.organization_id == organization_id)

        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        return result.scalars().fetchall()

    async def create(self, tenant: Tenant) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(tenant)
        await session.flush([tenant])

    async def save(self, tenant: Tenant) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(tenant)
        await session.flush([tenant])

    async def delete_by_id(self, tenant_id: str, organization_id: int) -> None:
        session = await self._unit_of_work.get_db_session()
        delete_query = delete(Tenant).where(
            Tenant.id == tenant_id and Tenant.organization_id == organization_id
        )
        await session.execute(delete_query)
        await session.commit()

    def _get_base_query(self) -> Select[Tuple[Tenant]]:
        return select(Tenant)
