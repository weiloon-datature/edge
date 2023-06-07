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
@Desc    :   Tensorflow Loader class.
"""

import tensorflow as tf
from abstract_loader import AbstractLoader


class Loader(AbstractLoader):

    """TF Loader class."""

    def _load(self):
        """Load TF model."""
        loaded = tf.saved_model.load(self.model_path)
        self.model = loaded.signatures["serving_default"]
