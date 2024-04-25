# logger.py

import inspect
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


def get_logger(log_level: str, name: str = None) -> logging.Logger:
    """
    Set up and return a logger with the specified log level.

    Args:
        log_level (str): String representation of logging level, not case sensitive.
                         Valid: DEBUG, INFO, WARNING, ERROR, CRITICAL
        name (str): Name of the logger. If None, uses the name of the calling module or package.

    Returns:
        logging.Logger object.
    """
    # Parse log_level from string to level
    logging_level = parse_log_level(log_level=log_level)

    # If name is not provided, use the name of the calling module or package
    if name is None:
        # Get the name of the calling module or package
        name = inspect.getmodule(inspect.stack()[1][0]).__name__

    logger = logging.getLogger(name)
    logger.setLevel(logging_level)

    # Create a console handler with a higher log level than the logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)

    # Create a formatter including the logger name and add it to the handler
    formatter = logging.Formatter(
        '%(asctime)s [%(name)s] [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)'
    )

    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    # Don't add additional handlers, will result in duplicate output.
    # https://alexandra-zaharia.github.io/posts/fix-python-logger-printing-same-entry-multiple-times/
    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger


def set_logger_level(logger: logging.Logger, log_level: str):
    """
    Change the logging level of a pre-existing logger object.

    Args:
        logger (logging.Logger): The logger object.
        log_level (str): String representation of logging level, not case sensitive.
                         Valid: DEBUG, INFO, WARNING, ERROR, CRITICAL

    Raises:
        LoggerError: If an invalid log level is provided.
    """
    # Parse log_level from string to level
    logging_level = parse_log_level(log_level=log_level)

    # Set the logging level of the logger
    logger.setLevel(logging_level)

    # Also set the logging level of all existing handlers attached to the logger
    for handler in logger.handlers:
        handler.setLevel(logging_level)
