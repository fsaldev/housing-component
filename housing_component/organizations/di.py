from injector import Binder, Module

from housing_component.organizations import interfaces
from housing_component.organizations.services.organization_repository import (
    OrganizationRepository,
)


class OrganizationModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interfaces.OrganizationRepository, OrganizationRepository)  # type: ignore[type-abstract]
