#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   abstract_preprocessor.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Abstract preprocessor class.
"""

from abc import ABC, abstractmethod


class AbstractPreprocessor(ABC):

    """Abstract preprocessor class."""

    def __init__(self, **kwargs):
        """Initialize abstract preprocessor class."""
        self.__dict__.update(kwargs)

    @abstractmethod
    def run(self, assets):
        """Run preprocessor.

        Args:
            assets: Dictionary of assets.

        Raises:
            NotImplementedError: Abstract method.
        """
        raise NotImplementedError
