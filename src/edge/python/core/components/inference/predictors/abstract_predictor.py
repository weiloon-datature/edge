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
@Desc    :   Abstract class for all predictors.
"""

from abc import ABC, abstractmethod


class AbstractPredictor(ABC):

    """Abstract class for all predictors."""

    def __init__(self, model, category_index, color_map, **kwargs):
        """Initialize Abstract Predictor."""
        self.detection_type = ""
        self.model_format = ""
        self.model_architecture = ""
        self.threshold = 0.0
        self._model = model
        self._category_index = category_index
        self._color_map = color_map
        self.__dict__.update(kwargs)

    @abstractmethod
    def predict(self, img):
        """Predict on a single image."""
        raise NotImplementedError

    # @abstractmethod
    # def batch_predict(self, img_batch):
    #     """Predict on a batch of images."""
    #     raise NotImplementedError

    @abstractmethod
    def _preprocess(self, img):
        """Preprocess model input before prediction."""
        raise NotImplementedError

    @abstractmethod
    def _postprocess(self):
        """Postprocess raw model output after prediction."""
        raise NotImplementedError

    @property
    def model(self):
        """Get model."""
        return self._model

    @property
    def category_index(self):
        """Get category index."""
        return self._category_index

    @property
    def color_map(self):
        """Get color map."""
        return self._color_map
