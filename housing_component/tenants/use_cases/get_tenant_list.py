from injector import Inject
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.tenants.schemas import (
    TenantSchema,
)
from housing_component.tenants.services.tenant_repository import (
    TenantRepository,
)
from typing import List


class GetTenantList(UseCase):
    organization_id: int

    class Handler(UseCaseHandler["GetTenantList", List[TenantSchema]]):
        def __init__(
            self,
            tenant_repository: Inject[TenantRepository],
        ) -> None:
            self.tenant_repository = tenant_repository

        async def execute(self, use_case: "GetTenantList") -> List[TenantSchema]:
            tenants = await self.tenant_repository.get_list(
                organization_id=use_case.organization_id,
            )

            result = []
            for tenant in tenants:
                tenant_response = TenantSchema(
                    id=tenant.id,
                    external_id=tenant.external_id,
                    organization_id=tenant.organization_id,
                    email_address=tenant.email_address,
                    first_name=tenant.first_name,
                    last_name=tenant.last_name,
                )
                result.append(tenant_response)

            return result
