from injector import Binder, Module

from housing_component.access_points import interfaces
from housing_component.access_points.services.access_point_repository import (
    AccessPointRepository,
)


class AccessPointModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interfaces.AccessPointRepository, AccessPointRepository)  # type: ignore[type-abstract]
