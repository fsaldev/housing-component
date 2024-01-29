from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from housing_component.tenants.models import Tenant


@runtime_checkable
class TenantRepository(Protocol):
    async def get_by_id(
        self,
        tenant_id: str,
        organization_id: int,
    ) -> Tenant | None:
        ...

    async def get_list(
        self,
        organization_id: int,
    ) -> Sequence[Tenant]:
        ...

    async def create(
        self,
        tenant: Tenant,
    ) -> None:
        ...

    async def save(self, tenant: Tenant) -> None:
        ...

    async def delete_by_id(self, tenant_id: str, organization_id: int) -> None:
        ...
