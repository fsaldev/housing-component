from sqlalchemy import Select, select, delete
from typing import Sequence, Tuple
from injector import Inject
from uuid import UUID

from housing_component.state import interfaces
from housing_component.state.models import State
from housing_component.core.unit_of_work import UnitOfWork


class StateRepository(interfaces.StateRepository):
    def __init__(self, unit_of_work: Inject[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work

    async def get_by_id(
        self,
        state_id: UUID,
    ) -> State | None:
        query = self._get_base_query().where(State.id == state_id)

        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        return result.scalars().one_or_none()

    async def get_list(
        self,
    ) -> Sequence[State]:
        query = self._get_base_query()

        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        return result.scalars().fetchall()

    async def create(self, state: State) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(state)
        await session.flush([state])

    async def save(self, state: State) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(state)
        await session.flush([state])

    async def delete_by_id(self, state_id: UUID) -> None:
        session = await self._unit_of_work.get_db_session()
        delete_query = delete(State).where(State.id == state_id)
        await session.execute(delete_query)
        await session.commit()

    def _get_base_query(self) -> Select[Tuple[State]]:
        return select(State)
