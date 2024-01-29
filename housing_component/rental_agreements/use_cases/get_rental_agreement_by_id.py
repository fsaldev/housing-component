from typing import Any

from injector import Inject
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.rental_agreements.errors import RentalAgreementErrors
from housing_component.rental_agreements.schemas import (
    RentalAgreementSchemaResponse,
)
from housing_component.rental_agreements.services.rental_agreement_repository import (
    RentalAgreementRepository,
)


class GetRentalAgreementById(UseCase):
    rental_agreement_id: str
    organization_id: int

    class Handler(
        UseCaseHandler["GetRentalAgreementById", RentalAgreementSchemaResponse]
    ):
        def __init__(
            self,
            rental_agreement_repository: Inject[RentalAgreementRepository],
        ) -> None:
            self.rental_agreement_repository = rental_agreement_repository

        async def execute(
            self, use_case: "GetRentalAgreementById", *args: Any, **kwargs: Any
        ) -> RentalAgreementSchemaResponse:
            rental_agreement = await self.rental_agreement_repository.get_by_id(
                use_case.rental_agreement_id, organization_id=use_case.organization_id
            )
            if not rental_agreement:
                raise RentalAgreementErrors.RENTAL_AGREEMENT_NOT_FOUND

            return rental_agreement
