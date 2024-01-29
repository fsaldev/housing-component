from typing import Optional
from housing_component.tenants.schemas import (
    TenantSchema,
)
from injector import Inject
from sqlalchemy.exc import IntegrityError
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.tenants.services.tenant_repository import (
    TenantRepository,
)
from housing_component.tenants.errors import TenantErrors


class ModifyTenant(UseCase):
    organization_id: int
    tenant_id: str
    external_id: Optional[str] = None
    email_address: str
    first_name: str
    last_name: str

    class Handler(UseCaseHandler["ModifyTenant", TenantSchema]):
        def __init__(
            self,
            tenant_repository: Inject[TenantRepository],
        ) -> None:
            self._tenant_repository = tenant_repository

        async def execute(
            self,
            use_case: "ModifyTenant",
        ) -> TenantSchema:
            # Retrieve the existing tenant
            tenant = await self._tenant_repository.get_by_id(
                use_case.tenant_id,
                organization_id=use_case.organization_id,
            )

            if tenant is None:
                raise TenantErrors.TENANT_NOT_FOUND

            # Update other fields of the tenant
            if use_case.external_id is not None:
                tenant.external_id = use_case.external_id
            if use_case.email_address is not None:
                tenant.email_address = use_case.email_address
            if use_case.first_name is not None:
                tenant.first_name = use_case.first_name
            if use_case.last_name is not None:
                tenant.last_name = use_case.last_name

            # Save the updated tenant
            try:
                await self._tenant_repository.save(tenant)
            except IntegrityError:
                raise TenantErrors.TENANT_UPDATE_ERROR

            # Fetch the updated tenant
            updated_tenant = await self._tenant_repository.get_by_id(
                use_case.tenant_id, organization_id=use_case.organization_id
            )
            if not updated_tenant:
                raise TenantErrors.TENANT_NOT_FOUND

            # Prepare and return TenantSchema
            return TenantSchema(
                id=updated_tenant.id,
                external_id=updated_tenant.external_id,
                organization_id=updated_tenant.organization_id,
                email_address=updated_tenant.email_address,
                first_name=updated_tenant.first_name,
                last_name=updated_tenant.last_name,
            )
