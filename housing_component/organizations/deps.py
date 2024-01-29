from typing import Annotated

from fastapi import Path
from fastapi_injector import Injected

from housing_component.organizations.errors import OrganizationErrors
from housing_component.organizations.services.organization_repository import (
    OrganizationRepository,
)


async def check_organization_existence(
    organization_id: Annotated[int, Path()],
    organization_repository: Annotated[
        OrganizationRepository, Injected(OrganizationRepository)
    ],
) -> None:
    organization = await organization_repository.get_by_id(organization_id)
    if organization is None:
        raise OrganizationErrors.ORGANIZATION_NOT_FOUND
