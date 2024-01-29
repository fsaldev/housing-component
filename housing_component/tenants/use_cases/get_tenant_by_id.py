from injector import Inject
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.tenants.errors import TenantErrors
from housing_component.tenants.schemas import (
    TenantSchema,
)
from housing_component.tenants.services.tenant_repository import (
    TenantRepository,
)


class GetTenantById(UseCase):
    organization_id: int
    tenant_id: str

    class Handler(UseCaseHandler["GetTenantById", TenantSchema]):
        def __init__(
            self,
            tenant_repository: Inject[TenantRepository],
        ) -> None:
            self.tenant_repository = tenant_repository

        async def execute(self, use_case: "GetTenantById") -> TenantSchema:
            tenant = await self.tenant_repository.get_by_id(
                use_case.tenant_id,
                organization_id=use_case.organization_id,
            )
            if not tenant:
                raise TenantErrors.TENANT_NOT_FOUND

            # Prepare and return TenantSchema
            return TenantSchema(
                id=tenant.id,
                external_id=tenant.external_id,
                organization_id=tenant.organization_id,
                email_address=tenant.email_address,
                first_name=tenant.first_name,
                last_name=tenant.last_name,
            )
