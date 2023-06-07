#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   abstract_output.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Abstract output module.
"""

from abc import ABC, abstractmethod


class AbstractOutput(ABC):

    """Abstract output class."""

    def __init__(self, **kwargs):
        """Initialize abstract output module."""
        self.__dict__.update(kwargs)
        self._stopped = False

    @abstractmethod
    def run(self, assets):
        """Run output module.

        Args:
            assets: Dictionary of assets.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    def stop(self):
        """Stop output module."""
        self._stopped = True

    @property
    def stopped(self):
        """Get output module stopped status.

        Returns:
            True if output module is stopped, False otherwise.
        """
        return self._stopped
