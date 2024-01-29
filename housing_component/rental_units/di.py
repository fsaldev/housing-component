from injector import Binder, Module

from housing_component.rental_units import interfaces
from housing_component.rental_units.services.rental_unit_repository import (
    RentalUnitRepository,
)


class RentalUnitsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interfaces.RentalUnitRepository, RentalUnitRepository)  # type: ignore[type-abstract]
