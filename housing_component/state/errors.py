from housing_component.core.exceptions import RequestException


class StateErrors:
    STATE_NOT_FOUND = RequestException(
        "STATE_NOT_FOUND",
        "The requested state was not found",
        404,
    )
    STATE_ALREADY_EXISTS = RequestException(
        "STATE_ALREADY_EXISTS",
        "This state is already registered.",
        400,
    )
    STATE_UPDATE_ERROR = RequestException(
        "STATE_UPDATE_ERROR",
        "An error occurred during state update",
        400,
    )
    INVALID_TRANSITION_ERROR = RequestException(
        "STATE_UPDATE_ERROR",
        "An INVALID_TRANSITION error occurred during state update",
        400,
    )
