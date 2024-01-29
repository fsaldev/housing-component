from sqlalchemy import Select, select, delete
from typing import Tuple, List
from injector import Inject
from sqlalchemy.orm import joinedload
from housing_component.rental_agreements import interfaces
from housing_component.rental_agreements.models import RentalAgreement
from housing_component.core.unit_of_work import UnitOfWork
from housing_component.rental_agreements.schemas import RentalAgreementSchemaResponse
from housing_component.state.schemas import StateSchemaResponse
from housing_component.tenants.schemas import TenantSchema


class RentalAgreementRepository(interfaces.RentalAgreementRepository):
    def __init__(self, unit_of_work: Inject[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work

    async def get_by_id(
        self,
        rental_agreement_id: str,
        organization_id: int,
    ) -> RentalAgreementSchemaResponse | None:
        query = self._get_base_query().where(RentalAgreement.id == rental_agreement_id)
        if organization_id:
            query = query.where(RentalAgreement.organization_id == organization_id)
        query = query.options(joinedload(RentalAgreement.tenant_rel))
        query = query.options(joinedload(RentalAgreement.state_rel))
        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        rental_agreement = result.scalars().one_or_none()
        if rental_agreement:
            tenant_data = None
            if rental_agreement.tenant_rel:
                tenant_data = TenantSchema.model_validate(rental_agreement.tenant_rel)
            state_data = None
            if rental_agreement.state_rel:
                state_data = StateSchemaResponse.model_validate(
                    rental_agreement.state_rel
                )
            return RentalAgreementSchemaResponse(
                id=rental_agreement.id,
                external_id=rental_agreement.external_id,
                organization_id=rental_agreement.organization_id,
                tenant_id=rental_agreement.tenant_id,
                tenant=tenant_data,
                rental_unit_id=rental_agreement.rental_unit_id,
                start_at=rental_agreement.start_at,
                end_at=rental_agreement.end_at,
                state=state_data,
            )
        return None

    async def validate_rental_unit_by_id(
        self,
        rental_agreement_id: str,
        organization_id: int,
    ) -> RentalAgreement | None:
        query = self._get_base_query().where(RentalAgreement.id == rental_agreement_id)
        if organization_id:
            query = query.where(RentalAgreement.organization_id == organization_id)
        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        return result.scalars().one_or_none()

    async def get_list(
        self, organization_id: int
    ) -> List[RentalAgreementSchemaResponse]:
        query = self._get_base_query()
        if organization_id:
            query = query.where(RentalAgreement.organization_id == organization_id)
        query = query.options(joinedload(RentalAgreement.tenant_rel))
        query = query.options(joinedload(RentalAgreement.state_rel))
        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        rental_agreements = result.scalars().fetchall()

        response_list = []
        for ra in rental_agreements:
            tenant_data = None
            if ra.tenant_rel:
                tenant_data = TenantSchema.model_validate(ra.tenant_rel)
            state_data = None
            if ra.state_rel:
                state_data = StateSchemaResponse.model_validate(ra.state_rel)

            response_list.append(
                RentalAgreementSchemaResponse(
                    id=ra.id,
                    external_id=ra.external_id,
                    organization_id=ra.organization_id,
                    tenant_id=ra.tenant_id,
                    tenant=tenant_data,
                    rental_unit_id=ra.rental_unit_id,
                    start_at=ra.start_at,
                    end_at=ra.end_at,
                    state=state_data,
                )
            )

        return response_list

    async def create(self, rental_agreement: RentalAgreement) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(rental_agreement)
        await session.flush([rental_agreement])

    async def save(self, rental_agreement: RentalAgreement) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(rental_agreement)
        await session.flush([rental_agreement])

    async def delete_by_id(
        self, rental_agreement_id: str, organization_id: int
    ) -> None:
        session = await self._unit_of_work.get_db_session()
        delete_query = delete(RentalAgreement).where(
            RentalAgreement.id == rental_agreement_id
            and RentalAgreement.organization_id == organization_id
        )
        await session.execute(delete_query)
        await session.commit()

    def _get_base_query(
        self,
    ) -> Select[Tuple[RentalAgreement]]:
        return select(RentalAgreement)
