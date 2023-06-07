#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   output.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Output module exceptions.
"""


class OutputException(Exception):

    """Base class for exceptions in the output module."""


class InvalidOutputModuleException(OutputException):

    """Exception raised for invalid output module."""


class InvalidOutputDeviceException(OutputException):

    """Exception raised for invalid output device."""


class InvalidOutputTypeException(OutputException):

    """Exception raised for invalid output type."""


class InvalidOutputPathException(OutputException):

    """Exception raised for invalid output path."""


class MalformedOutputException(OutputException):

    """Exception raised for malformed output."""
