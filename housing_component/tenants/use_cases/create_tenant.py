from typing import Any, Optional
from injector import Inject
from sqlalchemy.exc import IntegrityError

from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.tenants.models import Tenant
from housing_component.tenants.schemas import (
    TenantSchema,
)
from housing_component.tenants.services.tenant_repository import (
    TenantRepository,
)
from housing_component.tenants.errors import TenantErrors


class CreateTenant(UseCase):
    organization_id: int
    tenant_id: str
    external_id: str
    email_address: str
    first_name: Optional[str]
    last_name: Optional[str]

    class Handler(UseCaseHandler["CreateTenant", TenantSchema]):
        def __init__(
            self,
            tenant_repository: Inject[TenantRepository],
        ) -> None:
            self._tenant_repository = tenant_repository

        async def execute(
            self, use_case: "CreateTenant", *args: Any, **kwargs: Any
        ) -> TenantSchema:
            if use_case.tenant_id:
                existing_tenant = await self._tenant_repository.get_by_id(
                    use_case.tenant_id, use_case.organization_id
                )
                if existing_tenant:
                    raise TenantErrors.TENANT_ALREADY_EXISTS

            tenant = Tenant(
                id=use_case.tenant_id,
                external_id=use_case.external_id,
                organization_id=use_case.organization_id,
                email_address=use_case.email_address,
                first_name=use_case.first_name,
                last_name=use_case.last_name,
            )

            try:
                await self._tenant_repository.create(tenant)
            except IntegrityError:
                raise TenantErrors.TENANT_ALREADY_EXISTS

            # Prepare and return TenantSchema
            return TenantSchema.model_validate(tenant)
