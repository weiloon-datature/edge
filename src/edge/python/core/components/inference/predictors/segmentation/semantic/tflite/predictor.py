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
@Desc    :   TFLite Semantic Segmentation Predictor class.
"""

import numpy as np
from abstract_predictor import AbstractPredictor
from common.exceptions import (
    InvalidModelInputException,
    InvalidModelOutputException,
    PredictionException,
)
from common.utils import get_binary_mask


class Predictor(AbstractPredictor):

    """TFLite Semantic Segmentation Predictor class."""

    def __init__(self, model, category_index, color_map, **kwargs):
        """Initialize TFLite Predictor.

        Args:
            model: TFLite Interpreter.
            category_index: Class labels map.
            color_map: Color map for bounding boxes.
        """
        super().__init__(model, category_index, color_map, **kwargs)
        # TODO: Get input shape from model
        # self.input_shape =
        self._detections_output = {}

    def predict(self, img):
        """Predict on image.

        Args:
            img: Image to predict on.

        Returns:
            Dictionary of predictions containing a mask.

        Raises:
            PredictionException: If prediction fails.
        """
        try:
            model_input = self._preprocess(img)
            self._detections_output = self._model(inputs=model_input)
            return self._postprocess()
        except Exception as exc:
            raise PredictionException(exc) from exc

    def _preprocess(self, img):
        """Preprocess image to be compatible with the model.

        Args:
            img: Image to preprocess.

        Returns:
            Preprocessed image as a list.

        Raises:
            InvalidModelInputException: If input is not a numpy array.
        """
        try:
            input_image = np.expand_dims(img.astype(np.float32), 0)
        except Exception as exc:
            raise InvalidModelInputException(exc) from exc
        return input_image

    def _postprocess(self):
        """Postprocess raw model output into interpretable predictions.

        Returns:
            Dictionary of predictions containing a mask.

        Raises:
            InvalidModelOutputException: If output cannot be parsed.
        """
        try:
            ## Filter detections
            self._detections_output = self._detections_output["output"][0]
            output_mask = get_binary_mask(self._detections_output)

            if output_mask is not None:
                output_mask = np.expand_dims(output_mask, -1)
                output_mask = np.tile(output_mask, 3)
                output_mask *= 127
                output_mask = np.clip(output_mask, 0, 255).astype(np.uint8)
        except Exception as exc:
            raise InvalidModelOutputException(exc) from exc

        predictions_output = {
            "mask": output_mask,
        }
        return predictions_output
