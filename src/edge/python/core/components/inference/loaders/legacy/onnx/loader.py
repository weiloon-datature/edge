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
@Desc    :   ONNX Loader class.
"""

from abstract_loader import AbstractLoader
from onnxruntime import InferenceSession


class Loader(AbstractLoader):

    """ONNX Loader class."""

    def _load(self):
        """Load ONNX model."""
        self.model = InferenceSession(self.model_path,
                                      providers=["CPUExecutionProvider"])
