#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   predictor.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   PyTorch Object Detection Predictor class.
"""

from abstract_predictor import AbstractPredictor


class Predictor(AbstractPredictor):

    """PyTorch Object Detection Predictor class."""

    def __init__(self, model, category_index, color_map, **kwargs):
        """Initialize PyTorch Predictor."""
        super().__init__(model, category_index, color_map, **kwargs)
        raise NotImplementedError(
            f"Predictor not implemented for {self.model_architecture}")
