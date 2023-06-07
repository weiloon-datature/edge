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
@Desc    :   Debug utility functions.
"""

import os
import shutil

from common.constants import EXECUTION_TIME


def clear_logs(file: str) -> None:
    """Clear logs and archive the previous log file"""
    os.makedirs(os.path.join(os.path.dirname(file), EXECUTION_TIME),
                exist_ok=True)
    if os.stat(file).st_size != 0:
        archive_file = os.path.join(
            os.path.dirname(file),
            EXECUTION_TIME,
            os.path.basename(file),
        )
        _ = shutil.copyfile(file, archive_file)
    with open(file, "w", encoding="utf-8") as new_file:
        new_file.write("")
