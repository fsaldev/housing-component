from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Body, Depends
from fastapi_injector import Injected
from housing_component.core.auth import require_organization_access_token
from housing_component.organizations import check_organization_existence
from housing_component.core.use_cases import UseCase
from housing_component.state.schemas import (
    StateSchemaResponse,
    DesiredStateEnum,
)
from housing_component.state.use_cases import GetStateById, ModifyState, ReconcileState

router = APIRouter(
    prefix="/organizations/{organization_id}/rental-agreements/{rental_agreement_id}",
    tags=["Rental agreement"],
    dependencies=[
        Depends(require_organization_access_token),
        Depends(check_organization_existence),
    ],
)


@router.get("/state", description="Get a state by id")
async def get_state_by_id(
    use_case: Annotated[GetStateById, Depends()],
    handler: Annotated[GetStateById.Handler, Injected(GetStateById.Handler)],
) -> StateSchemaResponse:
    return await handler.execute(use_case)


@router.post("/reconcile", description="reconcile a state")
async def reconcile_state(
    use_case: Annotated[ReconcileState, Depends()],
    handler: Annotated[ReconcileState.Handler, Injected(ReconcileState.Handler)],
) -> StateSchemaResponse:
    return await handler.execute(use_case)


class AnnotatedUpdateState(UseCase):
    desired: Annotated[DesiredStateEnum, Body()]


@router.put("/state", description="Modify a state by id")
async def modify_state(
    state_id: UUID,
    use_case: Annotated[AnnotatedUpdateState, Body()],
    handler: Annotated[ModifyState.Handler, Injected(ModifyState.Handler)],
) -> StateSchemaResponse:
    use_case_dict = dict(use_case)
    return await handler.execute(ModifyState(state_id=state_id, **use_case_dict))
