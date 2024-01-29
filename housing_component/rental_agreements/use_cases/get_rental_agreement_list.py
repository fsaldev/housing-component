from injector import Inject
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.rental_agreements.schemas import (
    RentalAgreementSchemaResponse,
)
from housing_component.rental_agreements.services.rental_agreement_repository import (
    RentalAgreementRepository,
)
from typing import List


class GetRentalAgreementList(UseCase):
    organization_id: int

    class Handler(
        UseCaseHandler["GetRentalAgreementList", List[RentalAgreementSchemaResponse]]
    ):
        def __init__(
            self,
            rental_agreement_repository: Inject[RentalAgreementRepository],
        ) -> None:
            self.rental_agreement_repository = rental_agreement_repository

        async def execute(
            self, use_case: "GetRentalAgreementList"
        ) -> List[RentalAgreementSchemaResponse]:
            rental_agreements = await self.rental_agreement_repository.get_list(
                organization_id=use_case.organization_id
            )

            return rental_agreements
