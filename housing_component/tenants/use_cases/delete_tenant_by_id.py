from injector import Inject

from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.tenants.errors import TenantErrors
from housing_component.tenants.services.tenant_repository import (
    TenantRepository,
)


class DeleteTenantById(UseCase):
    organization_id: int
    tenant_id: str

    class Handler(UseCaseHandler["DeleteTenantById", None]):
        def __init__(self, tenant_repository: Inject[TenantRepository]) -> None:
            self.tenant_repository = tenant_repository

        async def execute(self, use_case: "DeleteTenantById") -> None:
            tenant = await self.tenant_repository.get_by_id(
                use_case.tenant_id, organization_id=use_case.organization_id
            )
            if not tenant:
                raise TenantErrors.TENANT_NOT_FOUND

            await self.tenant_repository.delete_by_id(
                use_case.tenant_id, organization_id=use_case.organization_id
            )
