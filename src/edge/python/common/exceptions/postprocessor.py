#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   postprocessor.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Postprocessor module exceptions.
"""


class PostprocessorException(Exception):

    """Base class for exceptions in the postprocessor module."""


class InvalidPostprocessorException(PostprocessorException):

    """Exception raised for invalid postprocessor."""


class PostprocessingException(PostprocessorException):

    """Exception raised for postprocessing errors."""
