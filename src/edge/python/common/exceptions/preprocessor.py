#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   preprocessor.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Preprocessor module exceptions.
"""


class PreprocessorException(Exception):

    """Base class for exceptions in the preprocessor module."""


class InvalidPreprocessorException(PreprocessorException):

    """Exception raised for invalid preprocessor."""


class PreprocessingException(PreprocessorException):

    """Exception raised for preprocessing errors."""
