from collections.abc import Sequence
from typing import Annotated
from fastapi import APIRouter, Body, Depends
from fastapi_injector import Injected
from pydantic import EmailStr
from housing_component.core.auth import require_organization_access_token
from housing_component.organizations import check_organization_existence
from housing_component.core.use_cases import UseCase
from housing_component.tenants.schemas import (
    TenantSchema,
)
from housing_component.tenants.use_cases import (
    GetTenantList,
    GetTenantById,
    CreateTenant,
    ModifyTenant,
    DeleteTenantById,
)

router = APIRouter(
    prefix="/organizations/{organization_id}/tenants",
    tags=["tenants"],
    dependencies=[
        Depends(require_organization_access_token),
        Depends(check_organization_existence),
    ],
)


@router.get("", description="Get a list of tenants")
async def get_tenant_list(
    use_case: Annotated[GetTenantList, Depends()],
    handler: Annotated[GetTenantList.Handler, Injected(GetTenantList.Handler)],
) -> Sequence[TenantSchema]:
    return await handler.execute(use_case)


@router.get("/{tenant_id}", description="Get a tenant by id")
async def get_tenant_by_id(
    use_case: Annotated[GetTenantById, Depends()],
    handler: Annotated[GetTenantById.Handler, Injected(GetTenantById.Handler)],
) -> TenantSchema:
    return await handler.execute(use_case)


class AnnotatedCreateTenant(UseCase):
    tenant_id: Annotated[
        str,
        Body(
            regex="^[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?$",
            max_length=63,
            description="Alphanumeric string with dashes, not at the beginning or end, max length 63",
        ),
    ]
    external_id: Annotated[str, Body()]
    email_address: Annotated[EmailStr, Body()]
    first_name: Annotated[str, Body()]
    last_name: Annotated[str, Body()]


@router.post("", description="Create a tenant")
async def create_tenant(
    organization_id: int,
    use_case: Annotated[AnnotatedCreateTenant, Body()],
    handler: Annotated[CreateTenant.Handler, Injected(CreateTenant.Handler)],
) -> TenantSchema:
    use_case_dict = dict(use_case)
    return await handler.execute(
        CreateTenant(organization_id=organization_id, **use_case_dict)
    )


class AnnotatedUpdateTenant(UseCase):
    external_id: Annotated[str, Body()]
    email_address: Annotated[EmailStr, Body()]
    first_name: Annotated[str, Body()]
    last_name: Annotated[str, Body()]


@router.put("/{tenant_id}", description="Modify a tenant by id")
async def modify_tenant(
    organization_id: int,
    tenant_id: str,
    use_case: Annotated[AnnotatedUpdateTenant, Body()],
    handler: Annotated[ModifyTenant.Handler, Injected(ModifyTenant.Handler)],
) -> TenantSchema:
    use_case_dict = dict(use_case)
    return await handler.execute(
        ModifyTenant(
            organization_id=organization_id, tenant_id=tenant_id, **use_case_dict
        )
    )


@router.delete("/{tenant_id}", description="Delete tenant by Id")
async def delete_tenant_by_id(
    use_case: Annotated[DeleteTenantById, Depends()],
    handler: Annotated[DeleteTenantById.Handler, Injected(DeleteTenantById.Handler)],
) -> None:
    return await handler.execute(use_case)
