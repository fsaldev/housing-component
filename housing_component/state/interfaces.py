from collections.abc import Sequence
from typing import Protocol, runtime_checkable
from uuid import UUID
from housing_component.state.models import State


@runtime_checkable
class StateRepository(Protocol):
    async def get_by_id(
        self,
        state_id: UUID,
    ) -> State | None:
        ...

    async def get_list(
        self,
    ) -> Sequence[State]:
        ...

    async def create(
        self,
        state: State,
    ) -> None:
        ...

    async def save(self, state: State) -> None:
        ...

    async def delete_by_id(self, state_id: UUID) -> None:
        ...
