import logging

import kiwi_logging_config

from housing_component.settings import (
    LOGGING_LEVEL,
    LOGGING_JSON,
    LOGGING_PREFIX,
    LOGGING_PATH,
)


def setup_logging() -> None:
    kiwi_logging_config.setup_logging(
        level=LOGGING_LEVEL,
        json=LOGGING_JSON,
        prefix=LOGGING_PREFIX,
        file_path=LOGGING_PATH,
    )

    # Make uvicorn use configured root logger
    logging.getLogger("uvicorn").handlers.clear()
    logging.getLogger("uvicorn").propagate = True
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.access").propagate = True

    # Suppress excessive logging of libraries
    logging.getLogger("aio_pika").setLevel(logging.WARNING)
    logging.getLogger("aiormq").setLevel(logging.WARNING)
    logging.getLogger("watchfiles.main").setLevel(logging.WARNING)
