#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   debug.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Debug logger.
"""

import logging
import os

from common.config import CONFIG
from common.constants import CONFIG_LOG_FILE, DEBUG_FORMAT, DEBUG_LOG_FILE
from common.utils import clear_logs
from yaml import dump as yaml_dump


def add_debug_logger(logger, warnings_logger):
    """Add debug logger to main logger.

    Args:
        logger: Main logger.
        warnings_logger: Warnings logger.

    Raises:
        FileNotFoundError: If config or debug log file path is not set.
    """
    if not CONFIG_LOG_FILE:
        raise FileNotFoundError("Config log file path is not set!")
    if not DEBUG_LOG_FILE:
        raise FileNotFoundError("Debug log file path is not set!")
    if not os.path.exists(DEBUG_LOG_FILE) or not os.path.exists(
            CONFIG_LOG_FILE):
        os.makedirs(os.path.dirname(DEBUG_LOG_FILE), exist_ok=True)

    clear_logs(DEBUG_LOG_FILE)
    clear_logs(CONFIG_LOG_FILE)
    with open(CONFIG_LOG_FILE, "w", encoding="utf-8") as config_log:
        yaml_dump(CONFIG, config_log, default_flow_style=False)

    debug_formatter = logging.Formatter(fmt=DEBUG_FORMAT)
    debug_handler = logging.FileHandler(DEBUG_LOG_FILE)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(debug_formatter)

    logger.addHandler(debug_handler)
    warnings_logger.addHandler(debug_handler)
