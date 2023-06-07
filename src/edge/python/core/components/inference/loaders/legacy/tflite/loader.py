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
@Desc    :   TFLite Loader class (legacy).
"""

import tensorflow as tf
from abstract_loader import AbstractLoader


class Loader(AbstractLoader):

    """TFLite Loader class."""

    def _load(self):
        """Load TFLite model and allocate tensors."""
        self.model = tf.lite.Interpreter(self.model_path)
        self.model.allocate_tensors()
