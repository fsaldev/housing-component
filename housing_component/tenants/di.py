from injector import Binder, Module

from housing_component.tenants import interfaces
from housing_component.tenants.services.tenant_repository import (
    TenantRepository,
)


class TenantModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interfaces.TenantRepository, TenantRepository)  # type: ignore[type-abstract]
