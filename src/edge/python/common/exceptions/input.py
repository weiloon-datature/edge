#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   input.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Input module exceptions.
"""


class InputException(Exception):

    """Base class for exceptions in the input module."""


class InvalidInputException(InputException):

    """Exception raised for invalid input."""


class InvalidInputPathException(InputException):

    """Exception raised for invalid input path."""


class InvalidInputDeviceException(InputException):

    """Exception raised for invalid input device."""


class EmptyFrameBufferException(InputException):

    """Exception raised for empty frame buffer."""
