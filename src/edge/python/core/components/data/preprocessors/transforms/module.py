#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   module.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Image transforms preprocessor.
"""

import cv2
from abstract_preprocessor import AbstractPreprocessor
from common.exceptions import (  # noqa
    InvalidPreprocessorException, PreprocessingException,
)


class Preprocessor(AbstractPreprocessor):

    """Image transforms preprocessor."""

    def __init__(self, **kwargs):
        """Initialize image transforms preprocessor."""
        self.tools = []
        super().__init__(**kwargs)

    def run(self, assets):
        """Run image transforms preprocessor.

        Args:
            assets: Dictionary of assets.
        """
        if not self.tools:
            raise InvalidPreprocessorException("Preprocessor tools not set!")
        for transform in self.tools:
            func = getattr(self, list(transform.keys())[-1])
            params = list(transform.values())[-1]
            assets["input_frame"] = func(assets["input_frame"], **params)

    def resize(self, frame, **kwargs):
        """Resize frame to specific height and width.

        Args:
            frame: Frame to resize.

        Returns:
            Resized frame.
        """
        try:
            return cv2.resize(frame, tuple(kwargs["shape"]))
        except Exception as exc:
            raise PreprocessingException(exc) from exc
