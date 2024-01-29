from injector import Inject

from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.organizations.models import Organization
from housing_component.organizations.schemas import OrganizationSchema
from housing_component.organizations import OrganizationRepository


class CreateOrganization(UseCase):
    organization_id: int

    class Handler(UseCaseHandler["CreateOrganization", OrganizationSchema]):
        def __init__(
            self,
            organization_repository: Inject[OrganizationRepository],
        ) -> None:
            self._organization_repository = organization_repository

        async def execute(self, use_case: "CreateOrganization") -> OrganizationSchema:
            organization = Organization(id=use_case.organization_id)
            await self._organization_repository.create(organization)

            return OrganizationSchema.from_orm(organization)
