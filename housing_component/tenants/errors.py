from housing_component.core.exceptions import RequestException


class TenantErrors:
    TENANT_NOT_FOUND = RequestException(
        "TENANT_NOT_FOUND",
        "The requested tenant was not found",
        404,
    )
    TENANT_ALREADY_EXISTS = RequestException(
        "TENANT_ALREADY_EXISTS",
        "This tenant is already registered with this or another Organization",
        400,
    )
    TENANT_UPDATE_ERROR = RequestException(
        "TENANT_UPDATE_ERROR",
        "An error occurred during tenant update",
        400,
    )
