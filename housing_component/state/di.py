from injector import Binder, Module

from housing_component.state import interfaces
from housing_component.state.services.state_repository import (
    StateRepository,
)


class StateModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interfaces.StateRepository, StateRepository)  # type: ignore[type-abstract]
