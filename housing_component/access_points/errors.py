from housing_component.core.exceptions import RequestException


class AccessPointErrors:
    ACCESS_POINT_NOT_FOUND = RequestException(
        "ACCESS_POINT_NOT_FOUND",
        "The requested access point was not found",
        404,
    )
    ACCESS_POINT_ALREADY_EXISTS = RequestException(
        "ACCESS_POINT_ALREADY_EXISTS",
        "This access point is already registered",
        400,
    )
    ACCESS_POINT_UPDATE_ERROR = RequestException(
        "ACCESS_POINT_UPDATE_ERROR",
        "An error occurred during access point update",
        400,
    )
