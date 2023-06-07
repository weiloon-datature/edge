#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   loader.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Model loader exceptions.
"""


class LoaderException(Exception):

    """Base class for exceptions in the loader module."""


class UnsupportedModelFormatException(LoaderException):

    """Exception raised for invalid model format."""


class InvalidModelConfigException(LoaderException):

    """Exception raised for invalid model config."""


class InvalidModelPathException(LoaderException):

    """Exception raised for invalid model path."""


class InvalidModelException(LoaderException):

    """Exception raised for invalid model."""


class InvalidLabelMapPathException(LoaderException):

    """Exception raised for invalid label map path."""


class InvalidLabelMapException(LoaderException):

    """Exception raised for invalid label map."""


class InvalidColorMapException(LoaderException):

    """Exception raised for invalid color map."""
