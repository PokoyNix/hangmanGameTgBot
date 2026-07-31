'''
Application logging configuration.

This module configures the global logging system for the application.
It should be initialized exactly once during application startup.
'''

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import settings

LOG_FORMAT = (
        '%(asctime)s | '
        '%(levelname)-8s | '
        '%(name)s | '
        '%(message)s'
)

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def configure_logging() -> None:
    '''
    Configure application logging.

    Creates the log directory if necessary and configures console and
    file handlers.

    This function must be called exactly once during application startup.
    '''

    settings.LOG_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    root_logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=DATE_FORMAT,
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    app_handler = RotatingFileHandler(
            settings.LOG_DIR / 'app.log',
            maxBytes=1_000_000,
            backupCount=5,
            encoding='utf-8',
    )
    app_handler.setFormatter(formatter)

    error_handler = RotatingFileHandler(
            settings.LOG_DIR / 'error.log',
            maxBytes=1_000_000,
            backupCount=5,
            encoding='utf-8',
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)

