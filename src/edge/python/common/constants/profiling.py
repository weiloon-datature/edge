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
@Desc    :   Profiling constants.
"""

import os
from enum import Enum

from common.config import CONFIG

if CONFIG["profiling"]["active"]:
    PROFILING_LOG_FILE = os.path.join(CONFIG["profiling"]["log_folder"],
                                      "profile.log")
else:
    PROFILING_LOG_FILE = None


class Timers(Enum):

    """Enum for timer types."""

    @classmethod
    def __str__(cls) -> str:
        """Return the string representation of the enum value."""
        return str(cls.value)

    PERF_COUNTER = "PERF_COUNTER"
    PROCESS_TIMER = "PROCESS_TIMER"
    THREAD_TIMER = "THREAD_TIMER"
