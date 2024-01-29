from injector import Inject
from sqlalchemy.exc import IntegrityError
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.rental_agreements.errors import RentalAgreementErrors
from housing_component.rental_units.errors import RentalUnitErrors
from housing_component.state.schemas import DesiredStateEnum, ActualStateEnum
from housing_component.state.schemas import (
    StateSchemaResponse,
)
from housing_component.rental_units.services.rental_unit_repository import (
    RentalUnitRepository,
)
from housing_component.rental_agreements.services.rental_agreement_repository import (
    RentalAgreementRepository,
)
from housing_component.tenants.errors import TenantErrors
from housing_component.tenants.services.tenant_repository import (
    TenantRepository,
)
from housing_component.state.services.state_repository import (
    StateRepository,
)
from housing_component.state.errors import StateErrors
from housing_component.state.state_machine_service.agreement_reconciliation import (
    AgreementReconciliation,
)


class ReconcileState(UseCase):
    rental_agreement_id: str
    organization_id: int

    class Handler(UseCaseHandler["ReconcileState", StateSchemaResponse]):
        def __init__(
            self,
            state_repository: Inject[StateRepository],
            agreement_repository: Inject[RentalAgreementRepository],
            tenants_repository: Inject[TenantRepository],
            units_repository: Inject[RentalUnitRepository],
        ) -> None:
            self._state_repository = state_repository
            self.agreements_repo = agreement_repository
            self.tenants_repo = tenants_repository
            self.units_repo = units_repository

        async def execute(self, use_case: "ReconcileState") -> StateSchemaResponse:
            agreement = await self.agreements_repo.get_by_id(
                use_case.rental_agreement_id, use_case.organization_id
            )
            if not agreement:
                raise RentalAgreementErrors.RENTAL_AGREEMENT_NOT_FOUND
            tenant = await self.tenants_repo.get_by_id(
                agreement.tenant_id, use_case.organization_id
            )
            if not tenant:
                raise TenantErrors.TENANT_NOT_FOUND
            unit = await self.units_repo.get_by_id(
                agreement.rental_unit_id, use_case.organization_id
            )
            if not unit:
                raise RentalUnitErrors.RENTAL_UNIT_NOT_FOUND

            try:
                reconcile = AgreementReconciliation(self._state_repository)

                if (
                    agreement.state
                    and agreement.state.desired == DesiredStateEnum.Active
                    and agreement.state.actual
                    in [ActualStateEnum.Created, ActualStateEnum.Deactivated]
                ):
                    await reconcile.perform_active_transitions(
                        tenant=tenant,
                        agreement=agreement,
                        unit=unit,
                    )
                elif (
                    agreement.state
                    and agreement.state.desired == DesiredStateEnum.Inactive
                    and agreement.state.actual == ActualStateEnum.Activated
                ):
                    await reconcile.perform_inactive_transitions(
                        tenant=tenant,
                        agreement=agreement,
                        unit=unit,
                    )

            except IntegrityError as e:
                raise StateErrors.STATE_UPDATE_ERROR from e

            agreement = await self.agreements_repo.get_by_id(
                use_case.rental_agreement_id, use_case.organization_id
            )
            if not agreement:
                raise RentalAgreementErrors.RENTAL_AGREEMENT_NOT_FOUND

            return StateSchemaResponse.model_validate(agreement.state)
