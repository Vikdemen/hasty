import logging


def set_logging(debug: bool = False) -> None:
    """
    :param debug: If the logging level should be debug or warning
    """
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(level=level)
    logger = logging.getLogger(__name__)
    logger.debug(f'Logging is set up with level {logging.getLevelName(level)}')
