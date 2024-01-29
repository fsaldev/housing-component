from injector import Inject

from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.organizations import OrganizationRepository


class DeleteOrganization(UseCase):
    organization_id: int

    class Handler(UseCaseHandler["DeleteOrganization", None]):
        def __init__(
            self,
            organization_repository: Inject[OrganizationRepository],
        ) -> None:
            self._organization_repository = organization_repository

        async def execute(self, use_case: "DeleteOrganization") -> None:
            await self._organization_repository.delete(use_case.organization_id)
