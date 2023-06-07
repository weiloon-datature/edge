#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   config.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Configuration exceptions.
"""


class ConfigException(Exception):

    """Base class for configuration exceptions."""


class InvalidConfigPathException(ConfigException):

    """Exception raised for invalid configuration path."""


class InvalidConfigException(ConfigException):

    """Exception raised for invalid configuration file."""
