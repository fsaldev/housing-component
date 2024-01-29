from datetime import datetime

from housing_component.rental_agreements.schemas import RentalAgreementSchemaResponse
from injector import Inject
from sqlalchemy.exc import IntegrityError
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.rental_agreements.services.rental_agreement_repository import (
    RentalAgreementRepository,
)
from housing_component.rental_agreements.errors import RentalAgreementErrors


class ModifyRentalAgreement(UseCase):
    organization_id: int
    rental_agreement_id: str
    start_at: datetime
    end_at: datetime

    class Handler(
        UseCaseHandler["ModifyRentalAgreement", RentalAgreementSchemaResponse]
    ):
        def __init__(
            self,
            rental_agreement_repository: Inject[RentalAgreementRepository],
        ) -> None:
            self._rental_agreement_repository = rental_agreement_repository

        async def execute(
            self, use_case: "ModifyRentalAgreement"
        ) -> RentalAgreementSchemaResponse:
            rental_agreement = (
                await self._rental_agreement_repository.validate_rental_unit_by_id(
                    use_case.rental_agreement_id,
                    organization_id=use_case.organization_id,
                )
            )
            if rental_agreement is None:
                raise RentalAgreementErrors.RENTAL_AGREEMENT_NOT_FOUND

            if use_case.start_at is not None:
                rental_agreement.start_at = use_case.start_at
            if use_case.end_at is not None:
                rental_agreement.end_at = use_case.end_at

            try:
                await self._rental_agreement_repository.save(rental_agreement)
            except IntegrityError:
                raise RentalAgreementErrors.RENTAL_AGREEMENT_UPDATE_ERROR

            updated_rental_agreement = (
                await self._rental_agreement_repository.get_by_id(
                    use_case.rental_agreement_id,
                    organization_id=use_case.organization_id,
                )
            )
            if not updated_rental_agreement:
                raise RentalAgreementErrors.RENTAL_AGREEMENT_NOT_FOUND

            return updated_rental_agreement
