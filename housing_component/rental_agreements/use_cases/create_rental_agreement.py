import uuid
from datetime import datetime
from injector import Inject
from sqlalchemy.exc import IntegrityError

from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.rental_agreements.models import RentalAgreement
from housing_component.rental_agreements.schemas import RentalAgreementSchemaResponse
from housing_component.rental_agreements.services.rental_agreement_repository import (
    RentalAgreementRepository,
)
from housing_component.rental_agreements.errors import RentalAgreementErrors
from housing_component.state.services.state_repository import (
    StateRepository,
)
from housing_component.state.models import State
from housing_component.state.schemas import DesiredStateEnum, ActualStateEnum
from housing_component.state.state_machine_service.agreement_reconciliation import (
    calculate_status,
)


class CreateRentalAgreement(UseCase):
    organization_id: int
    rental_agreement_id: str
    external_id: str
    tenant_id: str
    rental_unit_id: str
    start_at: datetime
    end_at: datetime

    class Handler(UseCaseHandler["RentalAgreement", RentalAgreementSchemaResponse]):
        def __init__(
            self,
            rental_agreement_repository: Inject[RentalAgreementRepository],
            state_repository: Inject[StateRepository],
        ) -> None:
            self._rental_agreement_repository = rental_agreement_repository
            self._state_repository = state_repository

        async def execute(
            self, use_case: "CreateRentalAgreement"
        ) -> RentalAgreementSchemaResponse:
            if use_case.rental_agreement_id:
                existing_rental_agreement = (
                    await self._rental_agreement_repository.get_by_id(
                        use_case.rental_agreement_id,
                        organization_id=use_case.organization_id,
                    )
                )
                if existing_rental_agreement:
                    raise RentalAgreementErrors.RENTAL_AGREEMENT_ALREADY_EXISTS

            state = State(
                id=uuid.uuid4(),
                desired=DesiredStateEnum.Inactive.value,
                actual=ActualStateEnum.Created.value,
                error="",
                status=calculate_status(
                    DesiredStateEnum.Inactive, ActualStateEnum.Created, False
                ),
            )

            await self._state_repository.create(state)

            rental_agreement = RentalAgreement(
                id=use_case.rental_agreement_id,
                external_id=use_case.external_id,
                organization_id=use_case.organization_id,
                tenant_id=use_case.tenant_id,
                rental_unit_id=use_case.rental_unit_id,
                start_at=use_case.start_at,
                end_at=use_case.end_at,
                state=state.id,
            )

            try:
                await self._rental_agreement_repository.create(rental_agreement)
            except IntegrityError:
                raise RentalAgreementErrors.RENTAL_AGREEMENT_CREATE_ERROR

            fetched_rental_agreement = (
                await self._rental_agreement_repository.get_by_id(
                    use_case.rental_agreement_id,
                    organization_id=use_case.organization_id,
                )
            )
            if fetched_rental_agreement is None:
                raise RentalAgreementErrors.RENTAL_AGREEMENT_NOT_FOUND
            return fetched_rental_agreement
