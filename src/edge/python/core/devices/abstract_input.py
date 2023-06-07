#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   abstract_input.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Abstract input module.
"""

from abc import ABC, abstractmethod


class AbstractInput(ABC):

    """Abstract input class."""

    def __init__(self, **kwargs):
        """Initialize abstract input class."""
        self._stopped = False
        self.__dict__.update(kwargs)

    @abstractmethod
    def run(self):
        """Run input module.

        Raises:
            NotImplementedError: Abstract method.
        """
        raise NotImplementedError

    @abstractmethod
    def load_data(self, assets):
        """Load input data.

        Args:
            assets: Dictionary of assets.

        Raises:
            NotImplementedError: Abstract method.
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Stop input module.

        Raises:
            NotImplementedError: Abstract method.
        """
        raise NotImplementedError

    @property
    def stopped(self):
        """Get stopped status."""
        return self._stopped

    @stopped.setter
    def stopped(self, stopped):
        """Set stopped status."""
        self._stopped = stopped
