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
@Desc    :   Debug constants.
"""

import os

from common.config import CONFIG

if CONFIG["debug"]["active"]:
    CONFIG_LOG_FILE = os.path.join(CONFIG["debug"]["log_folder"], "config.log")
    DEBUG_LOG_FILE = os.path.join(CONFIG["debug"]["log_folder"], "debug.log")
else:
    CONFIG_LOG_FILE = None
    DEBUG_LOG_FILE = None

DEBUG_FORMAT = (
    "[%(asctime)s,%(msecs)010.6f %(levelname)s %(filename)s:%(lineno)d"
    " %(funcName)s] %(message)s")
