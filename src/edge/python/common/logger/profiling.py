#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   profiling.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Profile logger.
"""

import logging
import os

from common.constants import DEBUG_FORMAT, PROFILING_LOG_FILE
from common.utils import clear_logs


def add_profile_logger(logger):
    """Set up profile logger.

    Args:
        logger: Profile logger.

    Raises:
        FileNotFoundError: If profile log file path is not set.
    """
    if not PROFILING_LOG_FILE:
        raise FileNotFoundError("Profile log file path is not set!")
    if not os.path.exists(PROFILING_LOG_FILE):
        os.makedirs(os.path.dirname(PROFILING_LOG_FILE), exist_ok=True)

    clear_logs(PROFILING_LOG_FILE)

    profile_formatter = logging.Formatter(fmt=DEBUG_FORMAT)
    profile_handler = logging.FileHandler(PROFILING_LOG_FILE)
    profile_handler.setLevel(logging.DEBUG)
    profile_handler.setFormatter(profile_formatter)

    logger.addHandler(profile_handler)
