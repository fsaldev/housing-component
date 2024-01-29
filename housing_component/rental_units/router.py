from collections.abc import Sequence
from typing import Annotated, Optional
from fastapi import APIRouter, Body, Depends
from fastapi_injector import Injected
from housing_component.core.use_cases import UseCase
from housing_component.core.auth import require_organization_access_token
from housing_component.organizations import check_organization_existence
from housing_component.rental_units.schemas import (
    RentalUnitSchema,
    AddressDict,
    RentalUnitSchemaListResponse,
)
from housing_component.rental_units.use_cases import (
    GetRentalUnitList,
    GetRentalUnitById,
    CreateRentalUnit,
    ModifyRentalUnit,
    DeleteRentalUnitById,
)

router = APIRouter(
    prefix="/organizations/{organization_id}/rental_units",
    tags=["Rental units"],
    dependencies=[
        Depends(require_organization_access_token),
        Depends(check_organization_existence),
    ],
)


@router.get("", description="Get a list of rental units")
async def get_rental_unit_list(
    use_case: Annotated[GetRentalUnitList, Depends()],
    handler: Annotated[GetRentalUnitList.Handler, Injected(GetRentalUnitList.Handler)],
) -> Sequence[RentalUnitSchemaListResponse]:
    return await handler.execute(use_case)


@router.get("/{rental_unit_id}", description="Get a rental unit by id")
async def get_rental_unit_by_id(
    use_case: Annotated[GetRentalUnitById, Depends()],
    handler: Annotated[GetRentalUnitById.Handler, Injected(GetRentalUnitById.Handler)],
) -> RentalUnitSchema:
    return await handler.execute(use_case)


class AnnotatedCreateRentalUnit(UseCase):
    rental_unit_id: Annotated[Optional[str], Body()]
    external_id: Annotated[str, Body()]
    name: Annotated[str, Body()]
    address: Annotated[Optional[AddressDict], Body()]


@router.post("", description="Create a rental unit")
async def create_rental_unit(
    organization_id: int,
    use_case: Annotated[AnnotatedCreateRentalUnit, Body()],
    handler: Annotated[CreateRentalUnit.Handler, Injected(CreateRentalUnit.Handler)],
) -> RentalUnitSchema:
    use_case_dict = dict(use_case)
    return await handler.execute(
        CreateRentalUnit(organization_id=organization_id, **use_case_dict)
    )


class AnnotatedUpdateRentalUnit(UseCase):
    external_id: Annotated[str, Body()]
    name: Annotated[str, Body()]
    address: Annotated[Optional[AddressDict], Body()]


@router.put("/{rental_unit_id}", description="Modify a rental unit by id")
async def modify_rental_unit(
    organization_id: int,
    rental_unit_id: str,
    use_case: Annotated[AnnotatedUpdateRentalUnit, Body()],
    handler: Annotated[ModifyRentalUnit.Handler, Injected(ModifyRentalUnit.Handler)],
) -> RentalUnitSchema:
    use_case_dict = dict(use_case)  # Convert use_case to a dictionary
    return await handler.execute(
        ModifyRentalUnit(
            organization_id=organization_id,
            rental_unit_id=rental_unit_id,
            **use_case_dict
        )
    )


@router.delete("/{rental_unit_id}", description="Delete Rental by Id", status_code=200)
async def delete_rental_unit_by_id(
    use_case: Annotated[DeleteRentalUnitById, Depends()],
    handler: Annotated[
        DeleteRentalUnitById.Handler, Injected(DeleteRentalUnitById.Handler)
    ],
) -> None:
    await handler.execute(use_case)
