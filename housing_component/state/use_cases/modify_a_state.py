from uuid import UUID

from housing_component.state.schemas import (
    StateSchemaResponse,
    DesiredStateEnum,
)
from injector import Inject
from sqlalchemy.exc import IntegrityError
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.state.services.state_repository import (
    StateRepository,
)
from housing_component.state.errors import StateErrors


class ModifyState(UseCase):
    state_id: UUID
    desired: DesiredStateEnum

    class Handler(UseCaseHandler["ModifyState", StateSchemaResponse]):
        def __init__(
            self,
            state_repository: Inject[StateRepository],
        ) -> None:
            self._state_repository = state_repository

        async def execute(
            self,
            use_case: "ModifyState",
        ) -> StateSchemaResponse:
            # Retrieve the existing state
            state = await self._state_repository.get_by_id(
                use_case.state_id,
            )

            if state is None:
                raise StateErrors.STATE_NOT_FOUND

            try:
                state.desired = use_case.desired
                await self._state_repository.save(state)
            except IntegrityError:
                raise StateErrors.STATE_UPDATE_ERROR

            # Fetch the updated state
            updated_state = await self._state_repository.get_by_id(use_case.state_id)
            if not updated_state:
                raise StateErrors.STATE_NOT_FOUND

            # Prepare and return StateSchemaResponse
            return StateSchemaResponse(
                id=updated_state.id,
                desired=updated_state.desired,
                actual=updated_state.actual,
                status=updated_state.status,
                error=updated_state.error,
            )
