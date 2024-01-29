from collections.abc import Sequence
from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Body, Depends
from fastapi_injector import Injected
from housing_component.core.use_cases import UseCase
from housing_component.core.auth import require_organization_access_token
from housing_component.organizations import check_organization_existence
from housing_component.rental_agreements.errors import RentalAgreementErrors
from housing_component.rental_agreements.schemas import (
    SuccessDeleteResponse,
    RentalAgreementSchemaResponse,
)
from housing_component.rental_agreements.use_cases import (
    CreateRentalAgreement,
    GetRentalAgreementById,
    GetRentalAgreementList,
    ModifyRentalAgreement,
    DeleteRentalAgreementById,
)

router = APIRouter(
    prefix="/organizations/{organization_id}/rental_agreements",
    tags=["Rental agreement"],
    dependencies=[
        Depends(require_organization_access_token),
        Depends(check_organization_existence),
    ],
)


@router.get("", description="Get a list of rental agreements")
async def get_rental_agreement_list(
    use_case: Annotated[GetRentalAgreementList, Depends()],
    handler: Annotated[
        GetRentalAgreementList.Handler, Injected(GetRentalAgreementList.Handler)
    ],
) -> Sequence[RentalAgreementSchemaResponse]:
    return await handler.execute(use_case)


@router.get("/{rental_agreement_id}", description="Get a rental agreement by id")
async def get_rental_agreement_by_id(
    use_case: Annotated[GetRentalAgreementById, Depends()],
    handler: Annotated[
        GetRentalAgreementById.Handler, Injected(GetRentalAgreementById.Handler)
    ],
) -> RentalAgreementSchemaResponse:
    return await handler.execute(use_case)


class AnnotatedCreateRentalAgreement(UseCase):
    rental_agreement_id: Annotated[
        str,
        Body(
            regex="^[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?$",
            max_length=63,
            description="Alphanumeric string with dashes, not at the beginning or end, max length 63",
        ),
    ]
    external_id: Annotated[str, Body()]
    tenant_id: Annotated[str, Body()]
    rental_unit_id: Annotated[str, Body()]
    start_at: Annotated[datetime, Body()]
    end_at: Annotated[datetime, Body()]


@router.post("", description="Create a rental agreement")
async def create_rental_agreement(
    organization_id: int,
    use_case: Annotated[AnnotatedCreateRentalAgreement, Body()],
    handler: Annotated[
        CreateRentalAgreement.Handler, Injected(CreateRentalAgreement.Handler)
    ],
) -> RentalAgreementSchemaResponse:
    if use_case.end_at < use_case.start_at:
        raise RentalAgreementErrors.INVALID_START_OR_END_DATE
    use_case_dict = dict(use_case)
    return await handler.execute(
        CreateRentalAgreement(organization_id=organization_id, **use_case_dict)
    )


class AnnotatedUpdateRentalAgreement(UseCase):
    start_at: Annotated[datetime, Body()]
    end_at: Annotated[datetime, Body()]


@router.put("/{rental_agreement_id}", description="Modify a rental agreement by id")
async def modify_rental_agreement(
    rental_agreement_id: str,
    organization_id: int,
    use_case: Annotated[AnnotatedUpdateRentalAgreement, Body()],
    handler: Annotated[
        ModifyRentalAgreement.Handler, Injected(ModifyRentalAgreement.Handler)
    ],
) -> RentalAgreementSchemaResponse:
    if use_case.end_at < use_case.start_at:
        raise RentalAgreementErrors.INVALID_START_OR_END_DATE
    use_case_dict = dict(use_case)

    return await handler.execute(
        ModifyRentalAgreement(
            organization_id=organization_id,
            rental_agreement_id=rental_agreement_id,
            **use_case_dict
        )
    )


@router.delete("/{rental_agreement_id}", description="Delete rental agreement by Id")
async def delete_rental_agreement_by_id(
    use_case: Annotated[DeleteRentalAgreementById, Depends()],
    handler: Annotated[
        DeleteRentalAgreementById.Handler, Injected(DeleteRentalAgreementById.Handler)
    ],
) -> SuccessDeleteResponse:
    return await handler.execute(use_case)
