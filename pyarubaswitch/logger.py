# logger.py

import logging


class LoggerError(Exception):
    """
    Error parsing logger.
    """


def parse_log_level(log_level: str):
    """
    Parse string level to logging.level

    Args:
        log_level(str): logging level in string format, not case sensitive.
                        Valid: DEBUG, INFO, WARNING, ERROR, CRITICAL
    Returns:
        logging.level
    """
    if log_level.upper() == 'DEBUG':
        return logging.DEBUG
    elif log_level.upper() == 'INFO':
        return logging.INFO
    elif log_level.upper() == 'WARNING':
        return logging.WARNING
    elif log_level.upper() == 'ERROR':
        return logging.ERROR
    elif log_level.upper() == 'CRITICAL':
        return logging.CRITICAL
    else:
        raise LoggerError('Invalid log_level set: %s ', log_level)


def get_logger(log_level: str) -> logging.Logger:
    """
    Set up and return a logger with the specified log level.

    Args:
        log_level(str): String representation of logging level, not case sensitive.
                        Valid: DEBUG, INFO, WARNING, ERROR, CRITICAL

    Returns:
        logging.Logger object.
    """
    # parse log_level from string to level
    logging_level = parse_log_level(log_level=log_level)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging_level)

    # Create a console handler with a higher log level than the logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    # Don't add additional handlers, will result in duplicate output.
    # https://alexandra-zaharia.github.io/posts/fix-python-logger-printing-same-entry-multiple-times/
    if not logger.hasHandlers:
        logger.addHandler(console_handler)

    return logger
