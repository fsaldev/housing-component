from typing import Protocol, runtime_checkable, List

from housing_component.rental_agreements.models import RentalAgreement
from housing_component.rental_agreements.schemas import RentalAgreementSchemaResponse


@runtime_checkable
class RentalAgreementRepository(Protocol):
    async def get_by_id(
        self,
        rental_agreement_id: str,
        organization_id: int,
    ) -> RentalAgreementSchemaResponse | None:
        ...

    async def validate_rental_unit_by_id(
        self,
        rental_agreement_id: str,
        organization_id: int,
    ) -> RentalAgreement | None:
        ...

    async def get_list(
        self, organization_id: int
    ) -> List[RentalAgreementSchemaResponse]:
        ...

    async def create(
        self,
        rental_agreement: RentalAgreement,
    ) -> None:
        ...

    async def save(self, rental_agreement: RentalAgreement) -> None:
        ...

    async def delete_by_id(
        self, rental_agreement_id: str, organization_id: int
    ) -> None:
        ...
