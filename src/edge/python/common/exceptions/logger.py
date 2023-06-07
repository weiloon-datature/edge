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
@Desc    :   Logger exceptions.
"""


class LoggerException(Exception):

    """Base class for exceptions in the logger module."""


class InvalidDebugFilePathException(LoggerException):

    """Exception raised for invalid debug file path."""
