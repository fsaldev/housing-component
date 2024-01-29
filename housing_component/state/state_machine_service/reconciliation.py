from typing import List
from housing_component.rental_agreements.schemas import RentalAgreementSchemaResponse
from housing_component.rental_units.schemas import RentalUnitSchemaListResponse
from housing_component.state.state_machine_service.kiwi_crud import KiwiCrud
from housing_component.tenants.models import Tenant


# create_user(first_name="testing1", last_name="testing1", email_address="testing11@gmail.com")
# print(get_user_by_username(username="testing11@gmail.com"))


# Reconciliation function for transitioning to any desired state
#
# The reconciliation funciton only takes a rental agreement ID
# as argument and needs to fetch all the necessary data itself
# from the repositories.
# The function is meant to be run asynchronously with a
# fire-and-forget approach, so it also doesn't return an error
# but stores any errors on the agreement object instead.


class Reconcile:
    def __init__(self) -> None:
        self.kiwi_crud = KiwiCrud()

    def reconcile_active(
        self,
        tenant: Tenant,
        unit: RentalUnitSchemaListResponse,
        agreement: RentalAgreementSchemaResponse,
    ) -> None:
        user = self.kiwi_crud.get_user_by_username(username=tenant.email_address)
        if user is None:
            try:
                self.kiwi_crud.create_user(
                    first_name=tenant.first_name,
                    last_name=tenant.last_name,
                    email_address=tenant.email_address,
                )
            except Exception:
                pass
                # return userInteractionNeeded, "could not create user: " + e.message()

        # // when we reach this part of the code,
        # // we know the user has accepted the invitation,
        # // so we can now assign him the permissions
        if unit.access_points:
            sensors: List[int] = [sensor.id for sensor in unit.access_points]
            self.kiwi_crud.grant_sensor_permission_to_the_user(
                sensors=sensors, username=tenant.email_address
            )

    def reconcile_inactive(
        self,
        tenant: Tenant,
        unit: RentalUnitSchemaListResponse,
        agreement: RentalAgreementSchemaResponse,
    ) -> None:
        user = self.kiwi_crud.get_user_by_username(tenant.email_address)
        if unit.access_points and user:
            for sensor in unit.access_points:
                permissions = self.kiwi_crud.get_sensor_permissions(sensor_id=sensor.id)
                for permission in permissions:
                    if permission.users[0].user_id == user.user_id:
                        self.kiwi_crud.remove_permission(permission.id)
        # analogous to the active case, but "backwards"
