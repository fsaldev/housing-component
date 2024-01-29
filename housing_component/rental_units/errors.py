from housing_component.core.exceptions import RequestException


class RentalUnitErrors:
    RENTAL_UNIT_NOT_FOUND = RequestException(
        "RENTAL_UNIT_NOT_FOUND",
        "The requested rental unit was not found",
        404,
    )
    RENTAL_UNIT_ALREADY_EXISTS = RequestException(
        "RENTAL_UNIT_ALREADY_EXISTS",
        "This rental unit is already registered with this or another Organization",
        400,
    )
    RENTAL_UNIT_UPDATE_ERROR = RequestException(
        "RENTAL_UNIT_UPDATE_ERROR",
        "An error occurred during rental unit update",
        400,
    )

    @staticmethod
    def dynamic_error(
        code: str, message: str, status_code: int = 400
    ) -> RequestException:
        """
        Create a dynamic RequestException with the given code, message, and status code.
        :param code: The error code.
        :param message: The error message.
        :param status_code: The HTTP status code (default is 400).
        :return: A new instance of RequestException.
        """
        return RequestException(code, message, status_code)


class AddressError:
    ADDRESS_NOT_FOUND = RequestException(
        "ADDRESS_NOT_FOUND",
        "The requested address was not found",
        404,
    )

    ADDRESS_INVALID_ERROR = RequestException(
        "ADDRESS_INVALID_ERROR",
        "The address provided is invalid",
        400,
    )
