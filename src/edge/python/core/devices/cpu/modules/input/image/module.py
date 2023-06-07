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
@Desc    :   Module for CPU image input.
"""

import cv2
import numpy as np
from abstract_input import AbstractInput
from common.exceptions import InvalidInputPathException


class Input(AbstractInput):

    """CPU image input class."""

    def __init__(self, **kwargs):
        """Initialize CPU image input class."""
        self.image_path = ""
        self.frame_size = [None, None]
        super().__init__(**kwargs)
        self._frame = None

    def run(self):
        """Run CPU image input.

        Raises:
            InvalidInputPathException: If image path cannot be found.
        """
        try:
            img = cv2.imread(self.image_path)
        except Exception as exc:
            raise InvalidInputPathException(exc) from exc
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self._frame = np.array(img)
        self.frame_size = self._frame.shape

        self.stop()

    def load_data(self, assets):
        """Load input data.

        Args:
            assets: Dictionary of assets.
        """
        assets["frame_id"] = self.image_path
        assets["orig_frame"] = self._frame
        assets["orig_shape"] = assets["orig_frame"].shape
        assets["input_frame"] = assets["orig_frame"].copy()

    def stop(self):
        """Stop CPU image input."""
        self.stopped = True
