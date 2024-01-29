from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from housing_component.access_points.models import AccessPoint


@runtime_checkable
class AccessPointRepository(Protocol):
    async def get_by_id(self, access_point_id: int) -> AccessPoint | None:
        ...

    async def get_list(
        self, rental_unit_id: str, organization_id: int
    ) -> Sequence[AccessPoint]:
        ...

    async def create(
        self,
        access_point: AccessPoint,
    ) -> None:
        ...

    async def save(self, access_point: AccessPoint) -> None:
        ...

    async def delete_by_id(self, access_point_id: int) -> None:
        ...
