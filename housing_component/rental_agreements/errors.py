from housing_component.core.exceptions import RequestException


class RentalAgreementErrors:
    RENTAL_AGREEMENT_NOT_FOUND = RequestException(
        "RENTAL_AGREEMENT_NOT_FOUND",
        "The requested rental agreement in was not found",
        404,
    )
    RENTAL_AGREEMENT_ALREADY_EXISTS = RequestException(
        "RENTAL_AGREEMENT_ALREADY_EXISTS",
        "This rental agreement in is already registered.",
        400,
    )
    RENTAL_AGREEMENT_UPDATE_ERROR = RequestException(
        "RENTAL_AGREEMENT_UPDATE_ERROR",
        "An error occurred during rental agreement in update",
        400,
    )
    RENTAL_AGREEMENT_CREATE_ERROR = RequestException(
        "RENTAL_AGREEMENT_CREATE_ERROR",
        "An error occurred during the creation of rental agreement",
        400,
    )
    INVALID_START_OR_END_DATE = RequestException(
        "INVALID_START_OR_END_DATE",
        "End date must be greater than or equal to start date.",
        400,
    )
