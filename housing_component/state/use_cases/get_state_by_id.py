from injector import Inject
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.state.errors import StateErrors
from housing_component.rental_agreements.errors import RentalAgreementErrors
from housing_component.state.schemas import (
    StateSchemaResponse,
)
from housing_component.rental_agreements.services.rental_agreement_repository import (
    RentalAgreementRepository,
)


class GetStateById(UseCase):
    rental_agreement_id: str
    organization_id: int

    class Handler(UseCaseHandler["GetStateById", StateSchemaResponse]):
        def __init__(
            self,
            agreement_repository: Inject[RentalAgreementRepository],
        ) -> None:
            self.agreements_repo = agreement_repository

        async def execute(self, use_case: "GetStateById") -> StateSchemaResponse:
            agreement = await self.agreements_repo.get_by_id(
                use_case.rental_agreement_id, use_case.organization_id
            )
            if not agreement:
                raise RentalAgreementErrors.RENTAL_AGREEMENT_NOT_FOUND
            if not agreement.state:
                raise StateErrors.STATE_NOT_FOUND

            # Prepare and return StateSchemaResponse
            return StateSchemaResponse.model_validate(agreement.state)
