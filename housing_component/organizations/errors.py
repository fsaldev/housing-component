from housing_component.core.exceptions import RequestException


class OrganizationErrors:
    ORGANIZATION_NOT_FOUND = RequestException(
        "ORGANIZATION_NOT_FOUND",
        "The requested organization was not found",
        404,
    )
