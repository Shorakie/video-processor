import logging

from app.core.config import LogLevels, settings

LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


def configure_logging() -> None:
    """Configures the Python logging system based on application settings.

    Sets up basic logging configuration according to the LOG_LEVEL defined in settings.
    When in DEBUG log level, uses a more detailed format that includes:
    - Log level
    - Message
    - Source file path
    - Function name
    - Line number

    For all other log levels (INFO, WARNING, ERROR, CRITICAL), uses the default format.

    Note:
        This is currently a basic implementation marked for future enhancement.

    Example:
        >>> configure_logging()
        # Sets up logging with either debug or standard format based on settings.LOG_LEVEL

    Side Effects:
        - Configures the root logger for the entire application
        - Overrides any existing logging configuration
    """
    if settings.LOG_LEVEL == LogLevels.DEBUG:
        logging.basicConfig(level=str(settings.LOG_LEVEL), format=LOG_FORMAT_DEBUG)
    else:
        logging.basicConfig(level=str(settings.LOG_LEVEL))
