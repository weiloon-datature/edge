#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   abstract_postprocessor.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Abstract postprocessor class.
"""

from abc import ABC, abstractmethod


class AbstractPostprocessor(ABC):

    """Abstract postprocessor class."""

    def __init__(self, **kwargs):
        """Initialize abstract postprocessor class."""
        self.__dict__.update(kwargs)

    @abstractmethod
    def run(self, assets):
        """Run postprocessor.

        Args:
            assets: Dictionary of assets.

        Raises:
            NotImplementedError: Abstract method.
        """
        raise NotImplementedError
