from typing import Any

from injector import Inject

from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.rental_agreements.errors import RentalAgreementErrors
from housing_component.rental_agreements.schemas import SuccessDeleteResponse
from housing_component.rental_agreements.services.rental_agreement_repository import (
    RentalAgreementRepository,
)


class DeleteRentalAgreementById(UseCase):
    organization_id: int
    rental_agreement_id: str

    class Handler(UseCaseHandler["DeleteRentalAgreementById", SuccessDeleteResponse]):
        def __init__(
            self, rental_agreement_repository: Inject[RentalAgreementRepository]
        ) -> None:
            self.rental_agreement_repository = rental_agreement_repository

        async def execute(
            self, use_case: "DeleteRentalAgreementById", *args: Any, **kwargs: Any
        ) -> SuccessDeleteResponse:
            rental_agreement = await self.rental_agreement_repository.get_by_id(
                use_case.rental_agreement_id, organization_id=use_case.organization_id
            )
            if not rental_agreement:
                raise RentalAgreementErrors.RENTAL_AGREEMENT_NOT_FOUND

            await self.rental_agreement_repository.delete_by_id(
                use_case.rental_agreement_id, organization_id=use_case.organization_id
            )

            return SuccessDeleteResponse(
                name="RENTAL AGREEMENT_DELETED_SUCCESSFULLY",
                message="rental agreement successfully deleted",
            )
