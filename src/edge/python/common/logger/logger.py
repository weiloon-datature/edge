#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   logger.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Common logger.
"""

import logging

from common.config import CONFIG
from common.constants import COLORED_FORMAT

from .debug import add_debug_logger
from .profiling import add_profile_logger

logging.captureWarnings(True)
Logger = logging.getLogger(__name__)
Logger.setLevel(logging.DEBUG)

WarningsLogger = logging.getLogger("py.warnings")

ProfileLogger = logging.getLogger("profile")
ProfileLogger.setLevel(logging.DEBUG)


class ColoredFormatter(logging.Formatter):

    """Logging colored formatter"""

    def __init__(self):
        """Initialize logging colored formatter."""
        super().__init__()

    def format(self, record):
        """Format the log message."""
        log_fmt = COLORED_FORMAT.get(record.levelno)
        date_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt=log_fmt, datefmt=date_fmt)
        return formatter.format(record)


stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(ColoredFormatter())

if CONFIG["debug"]["active"]:
    add_debug_logger(Logger, WarningsLogger)
    stdout_handler.setLevel(logging.DEBUG)

    if CONFIG["profiling"]["active"]:
        add_profile_logger(ProfileLogger)
else:
    stdout_handler.setLevel(logging.INFO)

Logger.addHandler(stdout_handler)
WarningsLogger.addHandler(stdout_handler)
