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
@Desc    :   TFLite Loader class.
"""

from abstract_loader import AbstractLoader

try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    from tensorflow import lite
    Interpreter = lite.Interpreter


class Loader(AbstractLoader):

    """TFLite Loader class."""

    def _load(self):
        """Load TFLite model and allocate tensors."""
        interpreter = Interpreter(self.model_path)
        self.model = interpreter.get_signature_runner()
