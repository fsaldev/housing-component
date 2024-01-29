from uuid import UUID
from housing_component.rental_agreements.schemas import RentalAgreementSchemaResponse
from housing_component.rental_units.schemas import RentalUnitSchemaListResponse
from housing_component.state.schemas import (
    DesiredStateEnum,
    ActualStateEnum,
    StatusEnum,
)
from housing_component.tenants.models import Tenant
from housing_component.state.state_machine_service.reconciliation import Reconcile
from housing_component.state.models import State
from housing_component.state.services.state_repository import (
    StateRepository,
)


def calculate_status(
    desired_state: DesiredStateEnum, actual_state: ActualStateEnum, error_state: bool
) -> StatusEnum:
    """
    Calculate the status based on the desired state, actual state, and error state.

    Parameters:
    - desired_state: An instance of DesiredStateEnum.
    - actual_state: An instance of ActualStateEnum.
    - error_state: A boolean indicating whether there is an error.

    Returns:
    - An instance of StatusEnum representing the calculated status.
    """
    if error_state:
        return StatusEnum.Error

    inactive_states = (ActualStateEnum.Created, ActualStateEnum.Deactivated)
    reconciling_states = (
        ActualStateEnum.Activating,
        ActualStateEnum.Activated,
        ActualStateEnum.Deactivating,
    )

    if desired_state == DesiredStateEnum.Inactive and actual_state in inactive_states:
        return StatusEnum.OK
    elif (
        desired_state == DesiredStateEnum.Inactive
        and actual_state in reconciling_states
    ):
        return StatusEnum.Reconciling
    elif desired_state == DesiredStateEnum.Active and actual_state in (
        ActualStateEnum.Created,
        ActualStateEnum.Activating,
        ActualStateEnum.Deactivating,
        ActualStateEnum.Deactivated,
    ):
        return StatusEnum.Reconciling
    elif (
        desired_state == DesiredStateEnum.Active
        and actual_state == ActualStateEnum.Activated
    ):
        return StatusEnum.OK

    return StatusEnum.Error  # Default to Error status if no condition is met


class AgreementReconciliation:
    def __init__(self, state_repository_instance: StateRepository) -> None:
        self._state_repository = state_repository_instance
        self._reconcile = Reconcile()

    async def perform_active_transitions(
        self,
        tenant: Tenant,
        unit: RentalUnitSchemaListResponse,
        agreement: RentalAgreementSchemaResponse,
    ) -> None:
        if agreement.state:
            state_id = agreement.state.id
            try:
                await self._update_state(
                    state_id=state_id,
                    desired_state=DesiredStateEnum.Active,
                    actual_state=ActualStateEnum.Activating,
                )

                self._reconcile.reconcile_active(tenant, unit, agreement)

                await self._update_state(
                    state_id=state_id,
                    desired_state=DesiredStateEnum.Active,
                    actual_state=ActualStateEnum.Activated,
                )

            except ValueError as err:
                await self._handle_error(err, state_id=state_id)

    async def perform_inactive_transitions(
        self,
        tenant: Tenant,
        unit: RentalUnitSchemaListResponse,
        agreement: RentalAgreementSchemaResponse,
    ) -> None:
        if agreement.state:
            state_id = agreement.state.id
            try:
                await self._update_state(
                    state_id=state_id,
                    desired_state=DesiredStateEnum.Inactive,
                    actual_state=ActualStateEnum.Deactivating,
                )

                self._reconcile.reconcile_inactive(tenant, unit, agreement)

                await self._update_state(
                    state_id=state_id,
                    desired_state=DesiredStateEnum.Inactive,
                    actual_state=ActualStateEnum.Deactivated,
                )

            except ValueError as err:
                await self._handle_error(err, state_id=state_id)

    async def _update_state(
        self,
        state_id: UUID,
        desired_state: DesiredStateEnum,
        actual_state: ActualStateEnum,
    ) -> None:
        state = await self._load_state(state_id=state_id)
        if state:
            state.desired = desired_state
            state.actual = actual_state
            state.status = calculate_status(desired_state, state.actual, False)
            state.error = ""

            await self._state_repository.save(state)

    async def _load_state(self, state_id: UUID) -> State | None:
        return await self._state_repository.get_by_id(state_id)

    async def _handle_error(self, err: ValueError, state_id: UUID) -> None:
        state = await self._load_state(state_id=state_id)
        if state:
            state.status = StatusEnum.Error
            state.error = str(err)
            await self._state_repository.save(state)
