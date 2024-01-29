from injector import Binder, Module

from housing_component.rental_agreements import interfaces
from housing_component.rental_agreements.services.rental_agreement_repository import (
    RentalAgreementRepository,
)


class RentalAgreementModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interfaces.RentalAgreementRepository, RentalAgreementRepository)  # type: ignore[type-abstract]
